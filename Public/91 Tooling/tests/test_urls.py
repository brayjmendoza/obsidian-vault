"""validate_urls: judging fetches, fetching for real against a local server, and the CLI."""

import json
import socket
from pathlib import Path
from typing import Final

import pytest

from tests.conftest import CopyFixture, LoadVault, keys, run_module
from vault_tools.cli import ExitCode
from vault_tools.issues import IssueCode, Severity
from vault_tools.markup import urls
from vault_tools.validate_urls import (
    FetchFailure,
    FetchResult,
    UrlFetcher,
    UrlUse,
    check,
    url_issue,
    url_uses,
)
from vault_tools.vault import Note

E: Final = Severity.ERROR
W: Final = Severity.WARNING


def free_port() -> int:
    """Find a local port nothing listens on."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port: int = sock.getsockname()[1]
    return port


NOTE: Final = Note(path=Path("/vault/50 References/A.md"), rel="50 References/A.md")


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        (FetchResult(status=200), None),
        (FetchResult(status=404), (E, IssueCode.URL_BROKEN)),
        (FetchResult(status=410), (E, IssueCode.URL_BROKEN)),
        (FetchResult(status=403), (W, IssueCode.URL_UNVERIFIED)),
        (FetchResult(status=503), (W, IssueCode.URL_UNVERIFIED)),
        (FetchResult(failure=FetchFailure.DNS), (E, IssueCode.URL_BROKEN)),
        (FetchResult(failure=FetchFailure.REFUSED), (E, IssueCode.URL_BROKEN)),
        (FetchResult(failure=FetchFailure.TLS), (E, IssueCode.URL_BROKEN)),
        (FetchResult(failure=FetchFailure.TIMEOUT), (W, IssueCode.URL_UNVERIFIED)),
        (FetchResult(failure=FetchFailure.OTHER), (W, IssueCode.URL_UNVERIFIED)),
    ],
)
def test_url_issue(result: FetchResult, expected: tuple[Severity, IssueCode] | None) -> None:
    """Gone pages and unreachable hosts are errors; anything possibly temporary warns."""
    issue = url_issue(NOTE, "https://example.com", result)
    assert (None if issue is None else (issue.severity, issue.code)) == expected


BODY: Final = """Read [the guide](https://docs.example.com/guide) or https://docs.example.com/gone.

Run `curl https://code.example.com/inline`, or:

```bash
curl https://code.example.com/block
```
"""


def test_url_uses() -> None:
    """A note uses its `url` and each body URL outside code, and a template's body is skipped."""
    note = Note(
        path=Path("/vault/50 References/Docs.md"),
        rel="50 References/Docs.md",
        properties={"type": "reference", "url": "https://docs.example.com"},
        body=BODY,
        body_line=7,
    )
    assert url_uses(note) == [
        UrlUse(note=note, url="https://docs.example.com"),
        UrlUse(note=note, url="https://docs.example.com/guide", line=7),
        UrlUse(note=note, url="https://docs.example.com/gone", line=7),
    ]
    template = note.model_copy(update={"properties": {"type": "template"}})
    assert url_uses(template) == []


def test_sentence_punctuation_is_not_part_of_a_url() -> None:
    """A bare URL that ends a sentence leaves the period out."""
    assert [
        found.text for found in urls("See https://example.com/docs. Or https://a.example.com, too!")
    ] == [
        "https://example.com/docs",
        "https://a.example.com",
    ]


def test_body_urls_are_fetched(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """Body URLs are fetched like `url`, and a broken one is reported with its line."""
    root = copy_fixture("valid")
    frontmatter = (
        "---\ntype: reference\ncreated: 2026-11-11\nupdated: 2026-11-11\ntopic: tools\n---\n"
    )
    (root / "50 References/Docs.md").write_text(frontmatter + BODY, encoding="utf-8")
    fetched: list[str] = []

    def fake(url: str) -> FetchResult:
        fetched.append(url)
        return FetchResult(status=404 if url.endswith("/gone") else 200)

    issues = check(load_vault(root), fetch=fake)
    assert "https://docs.example.com/guide" in fetched
    assert not [url for url in fetched if "code.example.com" in url]
    assert keys(issues) == {(E, "url-broken", "50 References/Docs.md", None)}
    assert issues[0].message == "line 7: https://docs.example.com/gone is gone (HTTP 404)"


def test_sessions_are_reused_per_thread(server: str) -> None:
    """One thread fetching many URLs uses one session, and closing releases it."""
    with UrlFetcher() as fetcher:
        for path in ("/ok", "/gone", "/moved"):
            fetcher.fetch(server + path)
        assert fetcher.open_sessions == 1
    assert fetcher.open_sessions == 0


def test_each_url_fetched_once(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """Every distinct URL is fetched once, and its result applies to every note using it."""
    root = copy_fixture("valid")
    mathcha = root / "50 References/Mathcha.md"
    twin = root / "50 References/Mathcha Twin.md"
    twin.write_text(mathcha.read_text(encoding="utf-8"), encoding="utf-8")
    fetched: list[str] = []

    def fake(url: str) -> FetchResult:
        fetched.append(url)
        return FetchResult(status=404 if "mathcha" in url else 200)

    issues = check(load_vault(root), fetch=fake)
    assert sorted(fetched) == ["https://www.desmos.com", "https://www.mathcha.io"]
    assert keys(issues) == {
        (E, "url-broken", "50 References/Mathcha.md", "url"),
        (E, "url-broken", "50 References/Mathcha Twin.md", "url"),
    }


@pytest.mark.parametrize(
    ("path", "status"),
    [("/ok", 200), ("/moved", 200), ("/no-head", 200), ("/gone", 410), ("/error", 500)],
)
def test_fetch(server: str, path: str, status: int) -> None:
    """Redirects are followed and GET stands in when HEAD is refused."""
    with UrlFetcher() as fetcher:
        assert fetcher.fetch(server + path).status == status


def test_fetch_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """A port nothing listens on is a refused connection."""
    monkeypatch.setenv("NO_PROXY", "127.0.0.1")
    monkeypatch.setenv("no_proxy", "127.0.0.1")
    with UrlFetcher() as fetcher:
        result = fetcher.fetch(f"http://127.0.0.1:{free_port()}/")
    assert result.failure == FetchFailure.REFUSED, result


def test_vault_validate_always_fetches_urls(served_copy: CopyFixture, server: str) -> None:
    """vault-validate fetches every `url` on every run, and a gone page fails it."""
    root = served_copy("valid")
    desmos = root / "50 References/Bookmarks/Desmos.md"
    text = desmos.read_text(encoding="utf-8")
    desmos.write_text(text.replace(f"{server}/ok", f"{server}/gone"), encoding="utf-8")

    result = run_module("validate", str(root), "--json")
    assert result.returncode == ExitCode.ERRORS, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert [(i["code"], i["path"]) for i in data["issues"]] == [
        ("url-broken", "50 References/Bookmarks/Desmos.md")
    ]

"""validate_urls: judging fetches, fetching for real against a local server, and the CLI."""

import json
import socket
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Final

import pytest

from tests.conftest import CopyFixture, LoadVault, keys, run_module
from vault_tools.cli import ExitCode
from vault_tools.issues import IssueCode, Severity
from vault_tools.validate_urls import FetchFailure, FetchResult, check, fetch_url, url_issue
from vault_tools.vault import Note

E: Final = Severity.ERROR
W: Final = Severity.WARNING
ROUTES: Final = {"/ok": 200, "/moved": 301, "/gone": 410, "/forbidden": 403, "/error": 500}


class Handler(BaseHTTPRequestHandler):
    """Answers each route with its status; `/no-head` refuses HEAD but serves GET."""

    def do_HEAD(self) -> None:
        """Answer a HEAD request."""
        self._respond(405 if self.path == "/no-head" else ROUTES.get(self.path, 404))

    def do_GET(self) -> None:
        """Answer a GET request."""
        self._respond(200 if self.path == "/no-head" else ROUTES.get(self.path, 404))

    def _respond(self, status: int) -> None:
        """Send an empty response with a status; redirects go to /ok."""
        self.send_response(status)
        if status == 301:
            self.send_header("Location", "/ok")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        """Keep test output quiet."""


@pytest.fixture
def server(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    """Serve ROUTES on localhost, bypassing any proxy, and yield the base URL."""
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


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
def test_fetch_url(server: str, path: str, status: int) -> None:
    """Redirects are followed and GET stands in when HEAD is refused."""
    assert fetch_url(server + path).status == status


def test_fetch_refused() -> None:
    """A port nothing listens on is a refused connection."""
    result = fetch_url(f"http://127.0.0.1:{free_port()}/")
    assert result.failure == FetchFailure.REFUSED, result


def test_cli_checks_urls_only_when_asked(server: str, copy_fixture: CopyFixture) -> None:
    """vault-validate fetches URLs only with --check-urls, and says when it didn't."""
    root = copy_fixture("valid")
    for name, path in (("Mathcha.md", "/ok"), ("Bookmarks/Desmos.md", "/gone")):
        note = root / "50 References" / name
        text = note.read_text(encoding="utf-8")
        start = text.index("url: ")
        end = text.index("\n", start)
        note.write_text(text[:start] + f"url: {server}{path}" + text[end:], encoding="utf-8")

    offline = json.loads(run_module("validate", str(root), "--json").stdout)
    assert offline["summary"]["ok"] is True
    assert any("--check-urls" in reason for reason in offline["skipped"])

    result = run_module("validate", str(root), "--json", "--check-urls")
    assert result.returncode == ExitCode.ERRORS, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert [(i["code"], i["path"]) for i in data["issues"]] == [
        ("url-broken", "50 References/Bookmarks/Desmos.md")
    ]
    assert not any("--check-urls" in reason for reason in data["skipped"])

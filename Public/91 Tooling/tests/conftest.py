"""Shared pytest setup: loads fixture vaults and runs the validators as programs.

Each folder in tests/.fixtures/ is a small Public/ folder. Every vault is judged
by the real schemas in 91 Tooling/schemas/, so a broken schema fails the tests
before CI judges the real vault.
"""

import re
import shutil
import subprocess
import sys
import threading
from collections.abc import Iterable, Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Final, Protocol

import pytest

from vault_tools.issues import CheckName, Issue, IssueCode, Severity
from vault_tools.markup import is_web_url
from vault_tools.vault import DEFAULT_SCHEMA_DIR, TOOLING_DIR, Vault

FIXTURES_DIR: Final = TOOLING_DIR / "tests" / ".fixtures"
# A stand-in Private/ folder: only its file names matter, as in CI.
PRIVATE_SAMPLE_DIR: Final = TOOLING_DIR / "tests" / "private_sample"

URL_LINE_RE: Final = re.compile(r"^url: (.+)$", re.MULTILINE)

type IssueKey = tuple[Severity, IssueCode, str, str | None]


class LoadVault(Protocol):
    """Loads a fixture vault by name, or any vault by path."""

    def __call__(
        self,
        name: str | Path,
        schema_dir: Path = DEFAULT_SCHEMA_DIR,
        private_dir: Path | None = None,
    ) -> Vault:
        """Load a vault with the given schemas and, optionally, a Private/ folder."""
        ...


class CopyFixture(Protocol):
    """Copies a fixture vault somewhere a test may change it."""

    def __call__(self, name: str) -> Path:
        """Copy the fixture and return the copy's path."""
        ...


def keys(issues: Iterable[Issue], check: CheckName | None = None) -> set[IssueKey]:
    """Reduce issues to comparable (severity, code, path, property) tuples."""
    return {
        (issue.severity, issue.code, issue.path, issue.property)
        for issue in issues
        if check is None or issue.check == check
    }


def run_module(
    module: str, *args: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run `python -m vault_tools.<module>` with arguments and capture its output."""
    return subprocess.run(
        [sys.executable, "-m", f"vault_tools.{module}", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        check=False,
    )


@pytest.fixture
def load_vault() -> LoadVault:
    """Load a fixture vault by folder name (or any path) with the real schemas."""

    def load(
        name: str | Path, schema_dir: Path = DEFAULT_SCHEMA_DIR, private_dir: Path | None = None
    ) -> Vault:
        path = Path(name)
        return Vault(path if path.is_absolute() else FIXTURES_DIR / path, schema_dir, private_dir)

    return load


@pytest.fixture
def copy_fixture(tmp_path: Path) -> CopyFixture:
    """Copy a fixture vault into tmp_path so a test can change it."""

    def copy(name: str) -> Path:
        dest = tmp_path / name
        shutil.copytree(FIXTURES_DIR / name, dest)
        return dest

    return copy


@pytest.fixture
def schema_copy(tmp_path: Path) -> Path:
    """Copy the real schemas into tmp_path so a test can break them."""
    dest = tmp_path / "schemas"
    shutil.copytree(DEFAULT_SCHEMA_DIR, dest)
    return dest


# -- a local web server, so no test touches the internet ------------------------

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
    thread = threading.Thread(target=httpd.serve_forever, args=(0.01,), daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


@pytest.fixture
def served_copy(copy_fixture: CopyFixture, server: str) -> CopyFixture:
    """Copy a fixture vault with every well-formed `url` pointed at the local server's /ok.

    vault-validate fetches every `url`, so tests that run it use these copies
    instead of the fixtures themselves.
    """

    def copy(name: str) -> Path:
        root = copy_fixture(name)
        for note in root.rglob("*.md"):
            text = note.read_text(encoding="utf-8")
            served = URL_LINE_RE.sub(
                lambda match: f"url: {server}/ok" if is_web_url(match.group(1)) else match.group(0),
                text,
            )
            if served != text:
                note.write_text(served, encoding="utf-8")
        return root

    return copy

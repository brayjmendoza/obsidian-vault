"""Check that every `url` property loads, over the network.

Every distinct URL is fetched once, many at a time, with `requests`: each
worker thread keeps one session, so repeat hosts reuse their connections. A
fetch tries HEAD first and falls back to GET (without downloading the body)
for servers that mishandle HEAD. Pages that are gone (HTTP 404 or 410) and
hosts that don't exist, refuse connections, or fail TLS are errors. Anything
that might be temporary or a bot block (other 4xx, 5xx, timeouts, proxy
failures) is a warning, since only opening the page by hand can tell.

Slow and dependent on the network, so `vault-validate` runs it only with
`--check-urls`.

    vault-validate-urls [PUBLIC_DIR] [--json]
    python -m vault_tools.validate_urls
"""

import socket
import ssl
import sys
import threading
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor
from enum import StrEnum
from types import TracebackType
from typing import Final, Self

import requests
from pydantic import BaseModel, ConfigDict
from urllib3.exceptions import NameResolutionError

from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue, warning_issue
from vault_tools.markup import is_web_url
from vault_tools.validate_links import URL_PROPERTY
from vault_tools.vault import Note, Vault

DESCRIPTION: Final = "Check that every `url` property loads."
CHECK: Final = CheckName.URLS
# (connect, read) seconds: an unreachable host fails fast, a slow page gets longer.
TIMEOUT: Final = (5.0, 15.0)
MAX_WORKERS: Final = 16
GONE_STATUSES: Final = frozenset({404, 410})
FIRST_ERROR_STATUS: Final = 400
# Some sites turn away the default `python-requests` user agent.
USER_AGENT: Final = "Mozilla/5.0 (compatible; vault-tools link checker)"


class FetchFailure(StrEnum):
    """Why a URL couldn't be fetched at all."""

    DNS = "no such host"
    REFUSED = "connection refused"
    TLS = "TLS failed"
    TIMEOUT = "timed out"
    OTHER = "request failed"


class FetchResult(BaseModel):
    """What fetching a URL produced: an HTTP status, or a failure.

    Attributes:
        status: The final HTTP status, after redirects.
        failure: Why there is no status.
        detail: The underlying error, for messages.
    """

    model_config = ConfigDict(frozen=True)

    status: int | None = None
    failure: FetchFailure | None = None
    detail: str = ""

    @property
    def loaded(self) -> bool:
        """Whether the URL answered with a success or redirect status."""
        return self.status is not None and self.status < FIRST_ERROR_STATUS


type Fetcher = Callable[[str], FetchResult]

# Failures a GET retry can't fix.
FINAL_FAILURES: Final = frozenset(
    {FetchFailure.DNS, FetchFailure.REFUSED, FetchFailure.TLS, FetchFailure.TIMEOUT}
)
DEFINITE_FAILURES: Final = frozenset({FetchFailure.DNS, FetchFailure.REFUSED, FetchFailure.TLS})


def _causes(exc: BaseException) -> Iterator[BaseException]:
    """Walk an exception and everything that caused it.

    `requests` wraps urllib3, which wraps the socket error that says what
    really happened, through `__cause__`, `__context__`, `args`, and `reason`.

    Args:
        exc: The exception `requests` raised.

    Yields:
        The exception, then each exception inside it, once each.
    """
    seen: set[int] = set()
    stack: list[BaseException] = [exc]
    while stack:
        current = stack.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        inner: list[object] = [current.__cause__, current.__context__, *current.args]
        inner.append(getattr(current, "reason", None))
        stack += [item for item in inner if isinstance(item, BaseException)]


def _connection_failure(exc: requests.ConnectionError) -> FetchResult:
    """Classify a failed connection by the socket error underneath it.

    Args:
        exc: The connection error `requests` raised.

    Returns:
        The failure, with the innermost error's message as detail.
    """
    for cause in _causes(exc):
        match cause:
            case NameResolutionError() | socket.gaierror():
                return FetchResult(failure=FetchFailure.DNS, detail=str(cause))
            case ConnectionRefusedError():
                return FetchResult(failure=FetchFailure.REFUSED, detail=str(cause))
            case ssl.SSLError():
                return FetchResult(failure=FetchFailure.TLS, detail=str(cause))
            case _:
                continue
    return FetchResult(failure=FetchFailure.OTHER, detail=str(exc))


class UrlFetcher:
    """Fetches URLs with one pooled `requests` session per worker thread.

    Use it as a context manager so every session is closed afterwards.
    """

    def __init__(self) -> None:
        """Start with no sessions; each thread makes its own on first use."""
        self._local = threading.local()
        self._sessions: list[requests.Session] = []
        self._lock = threading.Lock()

    def __enter__(self) -> Self:
        """Return the fetcher.

        Returns:
            This fetcher.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close every session.

        Args:
            exc_type: The exception's type, if the block raised.
            exc: The exception, if the block raised.
            traceback: Its traceback, if the block raised.
        """
        self.close()

    @property
    def open_sessions(self) -> int:
        """How many sessions are open: one per thread that has fetched."""
        with self._lock:
            return len(self._sessions)

    def close(self) -> None:
        """Close every session this fetcher opened."""
        with self._lock:
            for session in self._sessions:
                session.close()
            self._sessions.clear()

    def _session(self) -> requests.Session:
        """Get this thread's session, making it on first use.

        Returns:
            The session.
        """
        session: requests.Session | None = getattr(self._local, "session", None)
        if session is None:
            session = requests.Session()
            session.headers["User-Agent"] = USER_AGENT
            self._local.session = session
            with self._lock:
                self._sessions.append(session)
        return session

    def _request(self, url: str, method: str) -> FetchResult:
        """Make one request, following redirects, and record its outcome.

        Args:
            url: The URL.
            method: `HEAD` or `GET`. A GET's body is never downloaded.

        Returns:
            The status, or why there is none.
        """
        try:
            response = self._session().request(
                method, url, timeout=TIMEOUT, allow_redirects=True, stream=True
            )
        except requests.Timeout as exc:  # before ConnectionError: ConnectTimeout is both
            return FetchResult(failure=FetchFailure.TIMEOUT, detail=str(exc))
        except requests.exceptions.SSLError as exc:
            return FetchResult(failure=FetchFailure.TLS, detail=str(exc))
        except requests.exceptions.ProxyError as exc:
            return FetchResult(failure=FetchFailure.OTHER, detail=str(exc))
        except requests.ConnectionError as exc:
            return _connection_failure(exc)
        except requests.RequestException as exc:
            return FetchResult(failure=FetchFailure.OTHER, detail=str(exc))
        with response:
            return FetchResult(status=response.status_code)

    def fetch(self, url: str) -> FetchResult:
        """Fetch a URL with HEAD, falling back to GET when HEAD doesn't load it.

        Args:
            url: A well-formed http or https URL.

        Returns:
            The outcome.
        """
        head = self._request(url, "HEAD")
        if head.loaded or head.failure in FINAL_FAILURES:
            return head
        return self._request(url, "GET")


def url_issue(note: Note, url: str, result: FetchResult) -> Issue | None:
    """Judge one fetch: fine, broken (an error), or unverified (a warning).

    Args:
        note: The note whose `url` it is.
        url: The URL.
        result: What fetching it produced.

    Returns:
        The issue, or None when the URL loaded.
    """
    if result.loaded:
        return None
    if result.status is not None:
        if result.status in GONE_STATUSES:
            message = f"{url} is gone (HTTP {result.status})"
            return error_issue(CHECK, IssueCode.URL_BROKEN, note.rel, message, prop=URL_PROPERTY)
        message = f"{url} answered HTTP {result.status}; open it by hand to confirm it works"
        return warning_issue(CHECK, IssueCode.URL_UNVERIFIED, note.rel, message, prop=URL_PROPERTY)
    failure = result.failure or FetchFailure.OTHER
    if failure in DEFINITE_FAILURES:
        message = f"{url} can't be reached: {failure} ({result.detail})"
        return error_issue(CHECK, IssueCode.URL_BROKEN, note.rel, message, prop=URL_PROPERTY)
    message = f"{url} couldn't be checked: {failure} ({result.detail})"
    return warning_issue(CHECK, IssueCode.URL_UNVERIFIED, note.rel, message, prop=URL_PROPERTY)


def check(vault: Vault, *, fetch: Fetcher | None = None) -> list[Issue]:
    """Fetch every note's `url` and report the ones that don't load.

    Malformed URLs are skipped: validate_links reports them.

    Args:
        vault: The vault to check.
        fetch: How to fetch a URL; tests pass a fake. A `UrlFetcher` when None.

    Returns:
        Every issue found.
    """
    pairs = [
        (note, value)
        for note in vault.notes
        if not note.load_issues
        and isinstance(value := (note.properties or {}).get(URL_PROPERTY), str)
        and is_web_url(value)
    ]
    unique = sorted({url for _, url in pairs})
    with UrlFetcher() as fetcher, ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = dict(zip(unique, pool.map(fetch or fetcher.fetch, unique), strict=True))
    issues = (url_issue(note, url, results[url]) for note, url in pairs)
    return [issue for issue in issues if issue is not None]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the URL check from the command line.

    Args:
        argv: The arguments, without the program name; `sys.argv[1:]` when None.

    Returns:
        The exit code.
    """
    return run_cli(DESCRIPTION, check, argv)


if __name__ == "__main__":
    sys.exit(main())

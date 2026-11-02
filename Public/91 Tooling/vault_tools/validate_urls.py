"""Check that every `url` property loads, over the network.

Every distinct URL is fetched once (HEAD, then GET when HEAD fails), a few at
a time. Pages that are gone (HTTP 404 or 410) and hosts that don't exist,
refuse connections, or fail TLS are errors. Anything that might be temporary
or a bot block (other 4xx, 5xx, timeouts, proxy failures) is a warning, since
only opening the page by hand can tell.

Slow and dependent on the network, so `vault-validate` runs it only with
`--check-urls`.

    vault-validate-urls [PUBLIC_DIR] [--json]
    python -m vault_tools.validate_urls
"""

import http.client
import socket
import ssl
import sys
import urllib.error
import urllib.request
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from enum import StrEnum
from typing import Final

from pydantic import BaseModel, ConfigDict

from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue, warning_issue
from vault_tools.markup import is_web_url
from vault_tools.validate_links import URL_PROPERTY
from vault_tools.vault import Note, Vault

DESCRIPTION: Final = "Check that every `url` property loads."
CHECK: Final = CheckName.URLS
TIMEOUT_SECONDS: Final = 10.0
MAX_WORKERS: Final = 8
GONE_STATUSES: Final = frozenset({404, 410})
FIRST_ERROR_STATUS: Final = 400
# Some sites turn away Python's default user agent.
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


type Fetcher = Callable[[str], FetchResult]

DEFINITE_FAILURES: Final = frozenset({FetchFailure.DNS, FetchFailure.REFUSED, FetchFailure.TLS})


def _failure_kind(reason: object) -> FetchFailure:
    """Classify the reason inside a `URLError`.

    Args:
        reason: `URLError.reason`, an exception or text.

    Returns:
        The kind of failure.
    """
    match reason:
        case socket.gaierror():
            return FetchFailure.DNS
        case ConnectionRefusedError():
            return FetchFailure.REFUSED
        case ssl.SSLError():
            return FetchFailure.TLS
        case TimeoutError():
            return FetchFailure.TIMEOUT
        case _:
            return FetchFailure.OTHER


def _request(url: str, method: str) -> FetchResult:
    """Make one request and record its outcome.

    Args:
        url: The URL.
        method: `HEAD` or `GET`. A GET's body is never read.

    Returns:
        The status, or why there is none.
    """
    request = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            status: int = response.status
            return FetchResult(status=status)
    except urllib.error.HTTPError as exc:  # before URLError, its parent
        exc.close()
        return FetchResult(status=exc.code)
    except urllib.error.URLError as exc:
        return FetchResult(failure=_failure_kind(exc.reason), detail=str(exc.reason))
    except TimeoutError as exc:
        return FetchResult(failure=FetchFailure.TIMEOUT, detail=str(exc) or "timed out")
    except (http.client.HTTPException, OSError, ValueError) as exc:
        return FetchResult(failure=FetchFailure.OTHER, detail=str(exc))


def fetch_url(url: str) -> FetchResult:
    """Fetch a URL with HEAD, falling back to GET for servers that mishandle HEAD.

    Args:
        url: A well-formed http or https URL.

    Returns:
        The outcome.
    """
    head = _request(url, "HEAD")
    loaded = head.status is not None and head.status < FIRST_ERROR_STATUS
    if loaded or head.failure in DEFINITE_FAILURES or head.failure == FetchFailure.TIMEOUT:
        return head
    return _request(url, "GET")


def url_issue(note: Note, url: str, result: FetchResult) -> Issue | None:
    """Judge one fetch: fine, broken (an error), or unverified (a warning).

    Args:
        note: The note whose `url` it is.
        url: The URL.
        result: What fetching it produced.

    Returns:
        The issue, or None when the URL loaded.
    """
    if result.status is not None:
        if result.status < FIRST_ERROR_STATUS:
            return None
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


def check(vault: Vault, *, fetch: Fetcher = fetch_url) -> list[Issue]:
    """Fetch every note's `url` and report the ones that don't load.

    Malformed URLs are skipped: validate_links reports them.

    Args:
        vault: The vault to check.
        fetch: How to fetch a URL; tests pass a fake.

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
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = dict(zip(unique, pool.map(fetch, unique), strict=True))
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

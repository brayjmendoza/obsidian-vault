"""Enforce the vault's link rules, without touching the network.

Checks, per note: no link into Private/ (wikilinks, embeds, and Markdown links,
in the body and in any property); URLs appear only in the `url` property; and
every `url` is a single well-formed http or https URL. Code blocks and inline
code are ignored. Whether each URL actually loads is validate_urls's job.

    vault-validate-links [PUBLIC_DIR] [--private DIR] [--json]
    python -m vault_tools.validate_links
"""

import sys
from collections.abc import Iterator, Sequence
from typing import Final

from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue
from vault_tools.markup import (
    blank_code,
    is_web_url,
    markdown_link_targets,
    markdown_links,
    urls,
    wikilinks,
)
from vault_tools.vault import Note, PrivateMatch, Vault, YamlValue

DESCRIPTION: Final = "Enforce the link rules: nothing links into Private/, URLs only in `url`."
CHECK: Final = CheckName.LINKS
URL_PROPERTY: Final = "url"


def text_values(value: YamlValue) -> Iterator[str]:
    """Yield every piece of text inside a property value, however nested.

    Args:
        value: A property value.

    Yields:
        Each text value.
    """
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from text_values(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from text_values(item)


def private_message(link: str, *, ambiguous: bool) -> str:
    """Explain why a link breaks the Private/ boundary.

    The message names only the link as written in the Public note, never a
    file in Private/, since reports reach Claude.

    Args:
        link: The link as it should be shown (e.g., `[[Salary]]`).
        ambiguous: Whether the target is a name both Public/ and Private/ have.

    Returns:
        The message.
    """
    if ambiguous:
        return (
            f"{link} matches a note in Public/ and a file in Private/; rename one or link by path"
        )
    return f"{link} links into Private/; Public notes never link to Private notes"


class LinkChecker:
    """Checks one vault's notes against the link rules."""

    def __init__(self, vault: Vault) -> None:
        """Hold the vault whose links to resolve.

        Args:
            vault: The vault to check.
        """
        self.vault = vault

    def check(self, note: Note) -> list[Issue]:
        """Check one note's properties and body.

        Args:
            note: The note. Notes that failed to load are skipped; the
                properties validator reports them.

        Returns:
            Every issue found.
        """
        if note.load_issues:
            return []
        return [*self._property_issues(note), *self._body_issues(note)]

    def _property_issues(self, note: Note) -> Iterator[Issue]:
        """Check every property: URL placement, the `url` format, and private links.

        Args:
            note: The note.

        Yields:
            Each issue found.
        """
        for prop, value in (note.properties or {}).items():
            texts = list(text_values(value))
            if prop == URL_PROPERTY:
                if isinstance(value, str) and not is_web_url(value):
                    message = f"{value!r} must be a single http or https URL"
                    yield self._error(note, IssueCode.URL_INVALID, message, prop=prop)
            elif any(urls(text) for text in texts):
                message = f"URLs belong in the `{URL_PROPERTY}` property, not `{prop}`"
                yield self._error(note, IssueCode.URL_MISPLACED, message, prop=prop)
            for text in texts:
                for link in wikilinks(text):
                    yield from self._private_issue(note, f"[[{link.text}]]", [link.text], prop)

    def _body_issues(self, note: Note) -> Iterator[Issue]:
        """Check the body, outside code: private links and URLs.

        Args:
            note: The note.

        Yields:
            Each issue found, its message starting with the line number.
        """
        text = blank_code(note.body)
        for link in wikilinks(text):
            where = f"line {note.body_line + link.line - 1}: [[{link.text}]]"
            yield from self._private_issue(note, where, [link.text], None)
        for link in markdown_links(text):
            where = f"line {note.body_line + link.line - 1}: ({link.text})"
            targets = markdown_link_targets(note.rel, link.text)
            yield from self._private_issue(note, where, targets, None)
        for url in urls(text):
            line = note.body_line + url.line - 1
            message = (
                f"line {line}: URLs belong in the `{URL_PROPERTY}` property, "
                f"not the note body ({url.text})"
            )
            yield self._error(note, IssueCode.URL_MISPLACED, message)

    def _private_issue(
        self, note: Note, shown: str, targets: list[str], prop: str | None
    ) -> Iterator[Issue]:
        """Report a link whose target (under any reading) points into Private/.

        Args:
            note: The note holding the link.
            shown: The link as messages show it, with its line for body links.
            targets: Every reading of the link's target.
            prop: The property holding the link, or None for the body.

        Yields:
            At most one issue: a definite private link wins over an ambiguous one.
        """
        matches = {self.vault.private_match(target) for target in targets}
        if PrivateMatch.PRIVATE in matches:
            message = private_message(shown, ambiguous=False)
        elif PrivateMatch.AMBIGUOUS in matches:
            message = private_message(shown, ambiguous=True)
        else:
            return
        yield self._error(note, IssueCode.PRIVATE_LINK, message, prop=prop)

    @staticmethod
    def _error(note: Note, code: IssueCode, message: str, *, prop: str | None = None) -> Issue:
        """Build a links error against a note.

        Args:
            note: The note.
            code: What kind of problem it is.
            message: What's wrong.
            prop: The property at fault, or None for the body.

        Returns:
            The issue.
        """
        return error_issue(CHECK, code, note.rel, message, prop=prop)


def check(vault: Vault) -> list[Issue]:
    """Check every note against the link rules.

    Args:
        vault: The vault to check.

    Returns:
        Every issue found.
    """
    checker = LinkChecker(vault)
    return [issue for note in vault.notes for issue in checker.check(note)]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the links check from the command line.

    Args:
        argv: The arguments, without the program name; `sys.argv[1:]` when None.

    Returns:
        The exit code.
    """
    return run_cli(DESCRIPTION, check, argv, checks_private_links=True)


if __name__ == "__main__":
    sys.exit(main())

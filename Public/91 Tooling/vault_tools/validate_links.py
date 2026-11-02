"""Enforce the vault's link rules, without touching the network.

Checks, per note: no link into Private/ (wikilinks, embeds, and Markdown links,
in the body and in any property); every link, in the body or a property,
reaches a note or file in Public/ and, when it names one, a heading or block
in that note (warnings otherwise); URLs appear only in the `url` property; and
every `url` is a single well-formed http or https URL. Code blocks and inline
code are ignored. Whether each URL actually loads is validate_urls's job.

    vault-validate-links [PUBLIC_DIR] [--private DIR] [--json]
    python -m vault_tools.validate_links
"""

import sys
from collections.abc import Iterator, Sequence
from typing import Final

from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue, warning_issue
from vault_tools.markup import (
    Link,
    blank_code,
    has_heading_chain,
    is_web_url,
    markdown_link_targets,
    markdown_links,
    urls,
    wikilinks,
)
from vault_tools.vault import TEMPLATE_TYPE, Note, PrivateMatch, Vault, YamlValue

DESCRIPTION: Final = (
    "Enforce the link rules: no broken links or links into Private/, URLs only in `url`."
)
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
                    yield from self._link_issues(note, link, [link.target], prop)

    def _body_issues(self, note: Note) -> Iterator[Issue]:
        """Check the body, outside code: every link, and that it holds no URLs.

        Args:
            note: The note.

        Yields:
            Each issue found, its message starting with the line number.
        """
        text = blank_code(note.body)
        for link in wikilinks(text):
            yield from self._link_issues(note, self._on_line(note, link), [link.target], None)
        for link in markdown_links(text):
            targets = markdown_link_targets(note.rel, link.target) if link.target else [""]
            yield from self._link_issues(note, self._on_line(note, link), targets, None)
        for url in urls(text):
            message = (
                f"line {note.file_line(url.line)}: URLs belong in the `{URL_PROPERTY}` property, "
                f"not the note body ({url.text})"
            )
            yield self._error(note, IssueCode.URL_MISPLACED, message)

    @staticmethod
    def _on_line(note: Note, link: Link) -> Link:
        """Prefix a body link's shown text with its line in the file.

        Args:
            note: The note holding the link.
            link: The link, its line counted within the body.

        Returns:
            The link, shown as e.g. `line 12: [[Note]]`.
        """
        shown = f"line {note.file_line(link.line)}: {link.shown}"
        return link.model_copy(update={"shown": shown})

    def _link_issues(
        self, note: Note, link: Link, targets: list[str], prop: str | None
    ) -> Iterator[Issue]:
        """Check that one link resolves: not into Private/, to a note or file, and to its anchor.

        Unresolved links and anchors are only warnings: the note or heading
        may not be written yet (CONVENTIONS.md section 1). Templates hold
        placeholder links, so theirs aren't resolved.

        Args:
            note: The note holding the link.
            link: The link.
            targets: Every reading of its target; any one resolving is enough.
                `[""]` means the same note.
            prop: The property holding the link, or None for the body.

        Yields:
            At most one issue.
        """
        if not any(targets):
            yield from self._anchor_issues(note, link, [note], prop)
            return
        private = self._private_issue(note, link.shown, targets, prop)
        if private is not None:
            yield private
            return
        if note.note_type == TEMPLATE_TYPE:
            return
        resolved = [match for target in targets for match in self.vault.resolve(target).notes]
        if resolved:
            yield from self._anchor_issues(note, link, resolved, prop)
        elif not any(self.vault.link_exists(target) for target in targets):
            message = f"{link.shown} matches no note or file (broken, or not written yet)"
            yield warning_issue(CHECK, IssueCode.LINK_UNRESOLVED, note.rel, message, prop=prop)
        # A link to another kind of file (e.g., `doc.pdf#page=2`) has no anchors to check.

    def _anchor_issues(
        self, note: Note, link: Link, targets: list[Note], prop: str | None
    ) -> Iterator[Issue]:
        """Check that a link's heading chain or block exists in the note it reaches.

        Args:
            note: The note holding the link.
            link: The link.
            targets: The notes its target resolved to; one having the anchor is enough.
            prop: The property holding the link, or None for the body.

        Yields:
            At most one issue.
        """
        anchor = link.anchor
        if not anchor.headings and anchor.block is None:
            return
        found = [self.vault.anchors(target) for target in targets]
        has_headings = not anchor.headings or any(
            has_heading_chain(anchors.headings, anchor.headings) for anchors in found
        )
        has_block = anchor.block is None or any(
            anchor.block.casefold() in anchors.blocks for anchors in found
        )
        if has_headings and has_block:
            return
        where = "this note" if targets == [note] else targets[0].stem
        if not has_headings:
            missing = "heading " + "#".join(anchor.headings)
        else:
            missing = f"block ^{anchor.block}"
        message = f"{link.shown}: {where} has no {missing}"
        yield warning_issue(CHECK, IssueCode.ANCHOR_UNRESOLVED, note.rel, message, prop=prop)

    def _private_issue(
        self, note: Note, shown: str, targets: list[str], prop: str | None
    ) -> Issue | None:
        """Report a link whose target (under any reading) points into Private/.

        Args:
            note: The note holding the link.
            shown: The link as messages show it, with its line for body links.
            targets: Every reading of the link's target.
            prop: The property holding the link, or None for the body.

        Returns:
            The issue, or None. A definite private link wins over an ambiguous one.
        """
        matches = {self.vault.private_match(target) for target in targets}
        if PrivateMatch.PRIVATE in matches:
            message = private_message(shown, ambiguous=False)
        elif PrivateMatch.AMBIGUOUS in matches:
            message = private_message(shown, ambiguous=True)
        else:
            return None
        return self._error(note, IssueCode.PRIVATE_LINK, message, prop=prop)

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

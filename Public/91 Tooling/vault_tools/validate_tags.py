"""Enforce the allowed tags on every inline `#tag` in note bodies.

The `tags` property is already held to the same list by properties-schema.yaml
(the `tag` vocabulary). This check covers what a schema can't see: tags
written in a note's body. Code blocks and inline code are ignored, and nested
tags (e.g., `#idea/music`) count as tags of their own, so they're not allowed.

    vault-validate-tags [PUBLIC_DIR] [--json]
    python -m vault_tools.validate_tags
"""

import sys
from collections.abc import Sequence
from typing import Final

from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue
from vault_tools.markup import blank_code, tags
from vault_tools.schemas import TAG_VOCAB
from vault_tools.vault import Note, Vault

DESCRIPTION: Final = "Enforce the allowed tags on every inline #tag in note bodies."
CHECK: Final = CheckName.TAGS


def tag_problem(tag: str, allowed: Sequence[str]) -> str | None:
    """Explain why a tag isn't allowed, with a hint for near misses.

    Args:
        tag: The tag, without its `#`.
        allowed: The allowed tags.

    Returns:
        What's wrong, or None when the tag is allowed.
    """
    if tag in allowed:
        return None
    listed = ", ".join(f"#{name}" for name in allowed)
    if tag.lower() in allowed:
        return f"#{tag} must be lowercase: #{tag.lower()}"
    if tag.split("/", 1)[0] in allowed:
        return f"#{tag} is a nested tag; only {listed} are allowed (link the subject instead)"
    return f"#{tag} is not an allowed tag ({listed})"


def note_issues(note: Note, allowed: Sequence[str]) -> list[Issue]:
    """Check every inline tag in one note's body.

    Args:
        note: The note. Notes that failed to load are skipped; the
            properties validator reports them.
        allowed: The allowed tags.

    Returns:
        One issue per tag that isn't allowed, its message starting with the line.
    """
    if note.load_issues:
        return []
    issues = []
    for tag in tags(blank_code(note.body)):
        problem = tag_problem(tag.text, allowed)
        if problem is not None:
            message = f"line {note.file_line(tag.line)}: {problem}"
            issues.append(error_issue(CHECK, IssueCode.UNKNOWN_TAG, note.rel, message))
    return issues


def check(vault: Vault) -> list[Issue]:
    """Check every note's inline tags against the `tag` vocabulary.

    Args:
        vault: The vault to check.

    Returns:
        Every issue found.
    """
    allowed = vault.properties_schema.vocabularies[TAG_VOCAB]
    return [issue for note in vault.notes for issue in note_issues(note, allowed)]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the tags check from the command line.

    Args:
        argv: The arguments, without the program name; `sys.argv[1:]` when None.

    Returns:
        The exit code.
    """
    return run_cli(DESCRIPTION, check, argv)


if __name__ == "__main__":
    sys.exit(main())

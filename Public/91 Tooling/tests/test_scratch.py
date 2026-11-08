"""Scratch notes: skipped by every validator except the Private/ boundary."""

from pathlib import Path
from typing import Final

from tests.conftest import PRIVATE_SAMPLE_DIR, CopyFixture, LoadVault, keys, run_module
from vault_tools import (
    validate_links,
    validate_properties,
    validate_structure,
    validate_tags,
)
from vault_tools.cli import ExitCode
from vault_tools.issues import IssueCode, Severity

E: Final = Severity.ERROR

# Breaks nearly every rule a checked note could: wrong folder for a typed note,
# unknown and wrong-type properties, a bad tag, a malformed and unreachable
# `url`, a broken link and anchor, and URLs in a property and the body.
MESSY: Final = """---
type: scratch
created: yesterday
colour: red
status: whatever
tags: [todo]
topic: https://example.com/in-a-property
url: https://unreachable.invalid/page
---
# Working

Half an idea: [[Nowhere]], [[Piano#No Such Heading]], see https://example.com.
#todo #Idea/music
"""

# Each scratch note, by path, in a folder or under a name a checked note couldn't use.
SCRATCH_NOTES: Final = {
    "10 Projects/Scratch Pad.md": MESSY,
    "40 Knowledge/Loose Thoughts.md": "---\ntype: scratch\n---\nnothing but a type\n",
    "01 Logs/Daily/not a date.md": "---\ntype: scratch\ncreated: 2026-11-08\n---\n",
    "20 Hobbies/Fitness/Exercises/Maybe.md": "---\ntype: scratch\nurl: not a url\n---\n",
}


def add_scratch(root: Path, notes: dict[str, str] = SCRATCH_NOTES) -> None:
    """Write scratch notes into a vault copy."""
    for rel, text in notes.items():
        (root / rel).write_text(text, encoding="utf-8")


def test_scratch_notes_are_not_checked(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """No offline validator reports anything about scratch notes."""
    root = copy_fixture("valid")
    add_scratch(root)
    vault = load_vault(root)
    for check in (validate_structure, validate_properties, validate_links, validate_tags):
        assert check.check(vault) == [], check.__name__


def test_full_run_ignores_scratch(served_copy: CopyFixture) -> None:
    """vault-validate passes, so a scratch note's unreachable `url` is never fetched."""
    root = served_copy("valid")
    add_scratch(root)
    result = run_module("validate", str(root))
    assert result.returncode == ExitCode.OK, result.stdout + result.stderr
    assert "0 errors, 0 warnings" in result.stdout


def test_scratch_notes_are_link_targets(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """Scratch notes aren't checked, but links to them resolve, so typed links judge them."""
    root = copy_fixture("valid")
    add_scratch(root)
    piece = root / "20 Hobbies/Music/Piano/Pieces/Liszt - Sketch.md"
    piece.write_text(
        "---\ntype: piece\ncreated: 2026-11-08\nupdated: 2026-11-08\n"
        'composers: ["[[Scratch Pad]]"]\nstatus: wishlist\n---\nSee [[Loose Thoughts]].\n',
        encoding="utf-8",
    )
    vault = load_vault(root)
    scratch = {note.rel for note in vault.scratch_notes}
    assert scratch == set(SCRATCH_NOTES)
    assert not scratch & {note.rel for note in vault.notes}
    assert scratch <= {note.rel for note in vault.link_targets}
    assert validate_links.check(vault) == []  # [[Loose Thoughts]] resolves
    assert keys(validate_properties.check(vault)) == {
        (
            E,
            IssueCode.LINK_WRONG_TYPE,
            "20 Hobbies/Music/Piano/Pieces/Liszt - Sketch.md",
            "composers",
        )
    }


def test_scratch_never_links_into_private(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """The Private/ boundary holds for scratch notes, in the body and in properties."""
    root = copy_fixture("valid")
    add_scratch(
        root,
        {
            "10 Projects/By Path.md": "---\ntype: scratch\n---\n[[Private/Budget]]\n",
            "10 Projects/By Name.md": "---\ntype: scratch\naliases: ['[[Salary]]']\n---\n",
            "10 Projects/Markdown.md": "---\ntype: scratch\n---\n[r](../../Private/Budget.md)\n",
        },
    )
    path_only = {
        (E, IssueCode.PRIVATE_LINK, "10 Projects/By Path.md", None),
        (E, IssueCode.PRIVATE_LINK, "10 Projects/Markdown.md", None),
    }
    assert keys(validate_links.check(load_vault(root))) == path_only
    with_private = keys(validate_links.check(load_vault(root, private_dir=PRIVATE_SAMPLE_DIR)))
    assert with_private == path_only | {
        (E, IssueCode.PRIVATE_LINK, "10 Projects/By Name.md", "aliases")
    }


def test_scratch_cannot_take_a_hub_name(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """A domain's hub name is reserved for its hub, even for scratch work."""
    root = copy_fixture("valid")
    hub = root / "20 Hobbies/Fitness/Fitness.md"
    hub.write_text("---\ntype: scratch\n---\n", encoding="utf-8")
    assert keys(validate_structure.check(load_vault(root))) == {
        (E, IssueCode.HUB_WRONG_TYPE, "20 Hobbies/Fitness/Fitness.md", None)
    }


def test_broken_frontmatter_is_still_reported(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """A note whose frontmatter doesn't parse can't be known as scratch, so it is checked."""
    root = copy_fixture("valid")
    add_scratch(root, {"10 Projects/Broken.md": "---\ntype: scratch\nbad: [\n---\n"})
    vault = load_vault(root)
    assert "10 Projects/Broken.md" in {note.rel for note in vault.notes}
    assert keys(validate_properties.check(vault)) == {
        (E, IssueCode.FRONTMATTER_INVALID, "10 Projects/Broken.md", None)
    }

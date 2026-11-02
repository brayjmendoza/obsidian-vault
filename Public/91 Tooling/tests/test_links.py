"""validate_links against the fixture vaults and a stand-in Private/ folder."""

import shutil
from pathlib import Path
from typing import Final

import pytest

from tests.conftest import FIXTURES_DIR, PRIVATE_SAMPLE_DIR, CopyFixture, IssueKey, LoadVault, keys
from vault_tools import validate_links, validate_properties
from vault_tools.issues import IssueCode, Severity
from vault_tools.markup import (
    blank_code,
    block_ids,
    has_heading_chain,
    headings,
    markdown_link_targets,
    parse_wikilink,
    wikilinks,
)
from vault_tools.vault import PrivateMatch

E: Final = Severity.ERROR
W: Final = Severity.WARNING
REFS: Final = "50 References"

# Reported whether or not Private/ can be seen.
ALWAYS: Final[set[IssueKey]] = {
    (E, IssueCode.URL_MISPLACED, f"{REFS}/Body URL.md", None),
    (E, IssueCode.URL_MISPLACED, f"{REFS}/Markdown URL.md", None),
    (E, IssueCode.URL_MISPLACED, f"{REFS}/Topic URL.md", "topic"),
    (E, IssueCode.URL_INVALID, f"{REFS}/Bad URL.md", "url"),
    (E, IssueCode.PRIVATE_LINK, f"{REFS}/Private Path.md", None),
    (E, IssueCode.PRIVATE_LINK, f"{REFS}/Private Markdown.md", None),
}

# Broken body links: warnings, since the note may not be written yet.
BROKEN: Final[set[IssueKey]] = {
    (W, IssueCode.LINK_UNRESOLVED, f"{REFS}/Broken Links.md", None),
    (W, IssueCode.ANCHOR_UNRESOLVED, f"{REFS}/Broken Links.md", None),
}

# Reported only when Private/'s file names can be seen.
BY_NAME: Final[set[IssueKey]] = {
    (E, IssueCode.PRIVATE_LINK, f"{REFS}/Private Name.md", None),
    (E, IssueCode.PRIVATE_LINK, f"{REFS}/Private Embed.md", None),
    (E, IssueCode.PRIVATE_LINK, f"{REFS}/Ambiguous Private.md", None),
    (E, IssueCode.PRIVATE_LINK, f"{REFS}/Private Property.md", "topic"),
}


def test_valid_vault_has_no_link_issues(load_vault: LoadVault) -> None:
    """The valid fixture passes, with or without a Private/ folder."""
    assert validate_links.check(load_vault("valid")) == []
    assert validate_links.check(load_vault("valid", private_dir=PRIVATE_SAMPLE_DIR)) == []


def test_link_rules_with_private_visible(load_vault: LoadVault) -> None:
    """With Private/ visible, links to its files by name are caught too."""
    vault = load_vault("bad-link-rules", private_dir=PRIVATE_SAMPLE_DIR)
    assert keys(validate_links.check(vault)) == ALWAYS | BROKEN | BY_NAME


def test_link_rules_without_private(load_vault: LoadVault) -> None:
    """Without Private/, links to its files by name look like broken links instead."""
    vault = load_vault("bad-link-rules")
    assert vault.private_dir is None
    assert keys(validate_links.check(vault)) == ALWAYS | BROKEN | {
        (W, IssueCode.LINK_UNRESOLVED, f"{REFS}/Private Name.md", None),
        (W, IssueCode.LINK_UNRESOLVED, f"{REFS}/Private Embed.md", None),
        (W, IssueCode.LINK_UNRESOLVED, f"{REFS}/Private Property.md", "topic"),
    }


def test_messages(load_vault: LoadVault) -> None:
    """Body issues give the line; private-link messages never name a Private/ file."""
    vault = load_vault("bad-link-rules", private_dir=PRIVATE_SAMPLE_DIR)
    messages = {(i.path, i.property): i.message for i in validate_links.check(vault)}
    assert messages[(f"{REFS}/Body URL.md", None)].startswith("line 9: ")
    name = messages[(f"{REFS}/Private Name.md", None)]
    assert name == (
        "line 9: [[Salary#Raise]] links into Private/; Public notes never link to Private notes"
    )
    assert "Public/ and a file in Private/" in messages[(f"{REFS}/Ambiguous Private.md", None)]


def test_every_private_markdown_link_is_reported(load_vault: LoadVault) -> None:
    """Relative and vault-root Markdown links into Private/ are both caught."""
    issues = validate_links.check(load_vault("bad-link-rules"))
    lines = [i.message for i in issues if i.path == f"{REFS}/Private Markdown.md"]
    assert len(lines) == 2, lines


def test_broken_body_links(load_vault: LoadVault) -> None:
    """Links to missing notes, files, headings, and blocks are each reported with the line."""
    vault = load_vault("bad-link-rules", private_dir=PRIVATE_SAMPLE_DIR)
    messages = [
        i.message for i in validate_links.check(vault) if i.path.endswith("Broken Links.md")
    ]
    missing = "matches no note or file (broken, or not written yet)"
    assert messages == [
        f"line 9: [[Missing Note]] {missing}",
        f"line 9: [[missing.png]] {missing}",
        "line 10: [[Good Bookmark#No Such Heading]]: Good Bookmark has no heading No Such Heading",
        "line 10: [[#Nowhere Here]]: this note has no heading Nowhere Here",
        "line 10: [[Good Bookmark#^nope]]: Good Bookmark has no block ^nope",
        f"line 9: (Nowhere.md) {missing}",
    ]


def test_links_resolve_like_obsidian(tmp_path: Path, load_vault: LoadVault) -> None:
    """Vault-root paths, partial paths, attachments, and exempt files all resolve."""
    root = tmp_path / "Public"
    shutil.copytree(FIXTURES_DIR / "valid", root)
    (root / "00 Inbox/Links.md").write_text(
        "[[Public/10 Projects/Spring Recital]] [[Piano/Piano]] [[changelog]]\n"
        "![[2026-10-30 nocturne score.pdf]] ![[98 Attachments/2026-10-30 nocturne score.pdf]]\n"
        "[recital](../10%20Projects/Spring%20Recital.md) [[References/Mathcha]]\n",
        encoding="utf-8",
    )
    issues = validate_links.check(load_vault(root))
    # Only the last link fails: a partial path must end on a folder boundary.
    assert [i.message for i in issues] == [
        "line 3: [[References/Mathcha]] matches no note or file (broken, or not written yet)"
    ]


def test_template_links_are_not_resolved(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """Templates hold placeholder links, so they aren't reported as broken."""
    root = copy_fixture("valid")
    template = root / "90 System/Templates/Piece Template.md"
    template.write_text(
        template.read_text(encoding="utf-8") + "\nComposer: [[{{composer}}]]\n", encoding="utf-8"
    )
    assert validate_links.check(load_vault(root)) == []


def test_code_is_not_searched(load_vault: LoadVault) -> None:
    """URLs and links inside inline code or a fenced block are ignored."""
    vault = load_vault("bad-link-rules", private_dir=PRIVATE_SAMPLE_DIR)
    issues = validate_links.check(vault)
    assert not [i for i in issues if i.path == f"{REFS}/Good Bookmark.md"]


def test_typed_link_into_private_is_left_to_links_check(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """A typed property link into Private/ is a private-link error, not also a warning."""
    root = copy_fixture("valid")
    note = root / "10 Projects/Spring Recital.md"
    text = note.read_text(encoding="utf-8")
    note.write_text(text.replace("[[Piano]]", "[[Salary]]"), encoding="utf-8")
    vault = load_vault(root, private_dir=PRIVATE_SAMPLE_DIR)
    assert validate_properties.check(vault) == []
    assert keys(validate_links.check(vault)) == {
        (E, "private-link", "10 Projects/Spring Recital.md", "area")
    }


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("Private/Anything", PrivateMatch.PRIVATE),  # a path, even if it doesn't exist
        ("private/finance/salary", PrivateMatch.PRIVATE),
        ("Salary", PrivateMatch.PRIVATE),
        ("passport scan.png", PrivateMatch.PRIVATE),
        ("Budget", PrivateMatch.AMBIGUOUS),
        ("Mathcha", PrivateMatch.NONE),
        ("Finance/Salary", PrivateMatch.NONE),  # a Public/ path
    ],
)
def test_private_match(load_vault: LoadVault, target: str, expected: PrivateMatch) -> None:
    """Targets are matched against Private/ by path prefix, or by name when it is visible."""
    vault = load_vault("bad-link-rules", private_dir=PRIVATE_SAMPLE_DIR)
    assert vault.private_match(target) == expected


@pytest.mark.parametrize(
    ("inner", "target", "headings", "block"),
    [
        ("Note", "Note", [], None),
        ("Note.md#Life|the composer", "Note", ["Life"], None),
        ("Note#Part#Section", "Note", ["Part", "Section"], None),
        ("Note#^abc-1", "Note", [], "abc-1"),
        ("Note^abc", "Note", [], "abc"),
        ("#Heading", "", ["Heading"], None),
        (
            "Folder Structure#Placement Rules\\|Placement Rules",
            "Folder Structure",
            ["Placement Rules"],
            None,
        ),
    ],
)
def test_parse_wikilink(inner: str, target: str, headings: list[str], block: str | None) -> None:
    """A wikilink splits into target, heading chain, and block; escaped table pipes work."""
    link = parse_wikilink(inner)
    assert (link.target, link.anchor.headings, link.anchor.block) == (target, headings, block)


def test_heading_matching() -> None:
    """Headings match ignoring case and dropped characters; a chain must nest."""
    body = "# Top\n## Notes: Part 1\n### Deep\n## Other\n```\n## In Code\n```\n## `code.py`\n"
    found = headings(body)
    assert [heading.key for heading in found] == ["top", "notes part 1", "deep", "other", "code.py"]
    assert has_heading_chain(found, ["notes part 1"])
    assert has_heading_chain(found, ["Top", "Notes: Part 1", "Deep"])
    assert not has_heading_chain(found, ["Other", "Deep"])  # Deep isn't inside Other
    assert not has_heading_chain(found, ["In Code"])
    assert block_ids("a line ^id-1\n`^not` code\nend^nope\n^Alone") == {"id-1", "alone"}


def test_blank_code_keeps_lines() -> None:
    """Blanking code removes links inside it and keeps the line count."""
    text = "a `[[X]]` b\n```\n[[Y]]\n```\n[[Z]]"
    blanked = blank_code(text)
    assert blanked.count("\n") == text.count("\n")
    assert [(link.target, link.line) for link in wikilinks(blanked)] == [("Z", 5)]


def test_markdown_link_targets() -> None:
    """A Markdown path is read as vault-root and note-relative; climbing out reaches the repo."""
    assert markdown_link_targets("50 References/A.md", "Salary.md") == ["Salary"]
    assert markdown_link_targets("50 References/A.md", "B/C.md") == ["B/C", "50 References/B/C"]
    assert markdown_link_targets("50 References/A.md", "../../Private/F/S.md") == [
        "../../Private/F/S",
        "Private/F/S",
    ]

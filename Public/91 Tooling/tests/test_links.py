"""validate_links against the fixture vaults and a stand-in Private/ folder."""

from typing import Final

import pytest

from tests.conftest import PRIVATE_SAMPLE_DIR, CopyFixture, IssueKey, LoadVault, keys
from vault_tools import validate_links, validate_properties
from vault_tools.issues import IssueCode, Severity
from vault_tools.markup import blank_code, markdown_link_targets, wikilinks
from vault_tools.vault import PrivateMatch

E: Final = Severity.ERROR
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
    assert keys(validate_links.check(vault)) == ALWAYS | BY_NAME


def test_link_rules_without_private(load_vault: LoadVault) -> None:
    """Without Private/, only explicit Private/ paths and the URL rules are checked."""
    vault = load_vault("bad-link-rules")
    assert vault.private_dir is None
    assert keys(validate_links.check(vault)) == ALWAYS


def test_messages(load_vault: LoadVault) -> None:
    """Body issues give the line; private-link messages never name a Private/ file."""
    vault = load_vault("bad-link-rules", private_dir=PRIVATE_SAMPLE_DIR)
    messages = {(i.path, i.property): i.message for i in validate_links.check(vault)}
    assert messages[(f"{REFS}/Body URL.md", None)].startswith("line 9: ")
    name = messages[(f"{REFS}/Private Name.md", None)]
    assert name == (
        "line 9: [[Salary]] links into Private/; Public notes never link to Private notes"
    )
    assert "Public/ and a file in Private/" in messages[(f"{REFS}/Ambiguous Private.md", None)]


def test_every_private_markdown_link_is_reported(load_vault: LoadVault) -> None:
    """Relative and vault-root Markdown links into Private/ are both caught."""
    issues = validate_links.check(load_vault("bad-link-rules"))
    lines = [i.message for i in issues if i.path == f"{REFS}/Private Markdown.md"]
    assert len(lines) == 2, lines


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


def test_blank_code_keeps_lines() -> None:
    """Blanking code removes links inside it and keeps the line count."""
    text = "a `[[X]]` b\n```\n[[Y]]\n```\n[[Z]]"
    blanked = blank_code(text)
    assert blanked.count("\n") == text.count("\n")
    assert [(link.text, link.line) for link in wikilinks(blanked)] == [("Z", 5)]


def test_markdown_link_targets() -> None:
    """A Markdown path is read as vault-root and note-relative; climbing out reaches the repo."""
    assert markdown_link_targets("50 References/A.md", "Salary.md") == ["Salary"]
    assert markdown_link_targets("50 References/A.md", "../../Private/F/S.md") == [
        "../../Private/F/S",
        "Private/F/S",
    ]

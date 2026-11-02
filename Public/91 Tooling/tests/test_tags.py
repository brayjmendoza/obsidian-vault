"""validate_tags against the fixture vaults."""

from typing import Final

import pytest

from tests.conftest import CopyFixture, LoadVault, keys
from vault_tools import validate_tags
from vault_tools.issues import IssueCode, Severity
from vault_tools.markup import tags

E: Final = Severity.ERROR
ALLOWED: Final = ["inbox", "review", "idea", "question"]


def test_valid_vault_has_no_tag_issues(load_vault: LoadVault) -> None:
    """The valid fixture passes."""
    assert validate_tags.check(load_vault("valid")) == []


def test_bad_tags(load_vault: LoadVault) -> None:
    """Every disallowed tag is reported with its line; allowed tags and non-tags aren't."""
    issues = validate_tags.check(load_vault("bad-tags"))
    assert keys(issues) == {(E, IssueCode.UNKNOWN_TAG, "50 References/Bad Tags.md", None)}
    assert [issue.message for issue in issues] == [
        "line 9: #todo is not an allowed tag (#inbox, #review, #idea, #question)",
        "line 10: #Idea must be lowercase: #idea",
        "line 11: #idea/music is a nested tag; only #inbox, #review, #idea, #question are "
        "allowed (link the subject instead)",
    ]


def test_tags_in_any_folder_are_checked(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """Untyped Inbox captures are checked too."""
    root = copy_fixture("valid")
    (root / "00 Inbox/Quick.md").write_text("remember this #someday\n", encoding="utf-8")
    assert keys(validate_tags.check(load_vault(root))) == {
        (E, IssueCode.UNKNOWN_TAG, "00 Inbox/Quick.md", None)
    }


@pytest.mark.parametrize(
    ("text", "found"),
    [
        ("#idea at the start", ["idea"]),
        ("mid-sentence #review, then more", ["review"]),
        ("two #a and #b-c/d_e", ["a", "b-c/d_e"]),
        ("unicode #idée", ["idée"]),
        ("# Heading and ## Sub", []),
        ("C# F# issue #123", []),
        ("[[Note#Heading]] [[#Heading]] (#anchor) &#8212;", []),
    ],
)
def test_tag_syntax(text: str, found: list[str]) -> None:
    """Tags are recognized the way Obsidian recognizes them."""
    assert [tag.text for tag in tags(text)] == found


def test_allowed_tags_come_from_the_schema(load_vault: LoadVault) -> None:
    """The check uses the schema's `tag` vocabulary, the same list the `tags` property uses."""
    vault = load_vault("valid")
    assert vault.properties_schema.vocabularies["tag"] == ALLOWED

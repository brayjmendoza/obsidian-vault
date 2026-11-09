"""validate_properties against the fixture vaults."""

import unicodedata
from typing import Final

from tests.conftest import CopyFixture, LoadVault, keys
from vault_tools import validate_properties
from vault_tools.issues import Severity
from vault_tools.vault import parse_link

E: Final = Severity.ERROR
W: Final = Severity.WARNING


def test_valid_vault_has_no_property_issues(load_vault: LoadVault) -> None:
    """The valid fixture passes."""
    assert validate_properties.check(load_vault("valid")) == []


def test_archive_and_tests_are_skipped_but_archive_is_linkable(load_vault: LoadVault) -> None:
    """Archived notes aren't checked but still resolve as link targets; fixtures do neither."""
    vault = load_vault("valid")
    rels = {n.rel for n in vault.notes}
    assert not any(r.startswith(("99 Archive/", "91 Tooling/tests/")) for r in rels)
    assert "90 System/Claude/changelog.md" not in rels  # exempt
    # The archive holds a broken note and an invalid project; neither is reported.
    assert (vault.root / "99 Archive/Old Stuff/Broken.md").exists()
    assert validate_properties.check(vault) == []
    targets = {n.rel for n in vault.link_targets}
    assert "99 Archive/20 Hobbies/Music/Composers/Franz Liszt.md" in targets
    assert not any(r.startswith("91 Tooling/tests/") for r in targets)


def test_bad_properties(load_vault: LoadVault) -> None:
    """Each kind of frontmatter problem is reported exactly once, on its property."""
    issues = validate_properties.check(load_vault("bad-properties"))
    assert keys(issues) == {
        (E, "wrong-value-type", "01 Logs/Daily/2026-10-01.md", "energy"),
        (E, "wrong-value-type", "01 Logs/Daily/2026-10-02.md", "created"),
        (E, "wrong-value-type", "10 Projects/Bad Due Date.md", "due"),
        (E, "not-in-vocab", "10 Projects/Bad Status.md", "status"),
        (E, "not-in-vocab", "10 Projects/Bad Tag.md", "tags"),
        (E, "frontmatter-invalid", "10 Projects/Broken YAML.md", None),
        (E, "wrong-value-type", "10 Projects/Comma Tags.md", "tags"),
        (E, "empty-property", "10 Projects/Empty Status.md", "status"),
        (E, "empty-property", "10 Projects/Empty Due.md", "due"),
        (E, "unknown-property", "10 Projects/Extra Property.md", "colour"),
        (E, "missing-property", "10 Projects/Missing Created.md", "created"),
        (E, "missing-property", "10 Projects/Missing Status.md", "status"),
        (E, "missing-type", "10 Projects/No Frontmatter.md", "type"),
        (E, "frontmatter-invalid", "10 Projects/Unclosed.md", None),
        (E, "wrong-value-type", "10 Projects/Unquoted Link.md", "area"),
        (E, "not-in-vocab", "20 Hobbies/Fitness/Exercises/Rope Climb.md", "equipment"),
        (E, "not-in-vocab", "20 Hobbies/Music/Composers/Bad Style.md", "styles"),
        (E, "wrong-value-type", "20 Hobbies/Music/Composers/Comma Styles.md", "styles"),
        (E, "unknown-property", "20 Hobbies/Music/Composers/Old Eras.md", "eras"),
        (E, "pattern-mismatch", "20 Hobbies/Music/Composers/Nobody Known.md", "lived"),
        (E, "out-of-range", "20 Hobbies/Music/Piano/Pieces/Chopin - Too Hard.md", "difficulty"),
        (E, "nested-object", "20 Hobbies/Travel/Trips/2026-12 Tokyo.md", "budget"),
        (E, "missing-property", "40 Knowledge/Concepts/Wrong Field.md", "fields"),
        (E, "property-not-allowed", "40 Knowledge/Concepts/Wrong Field.md", "field"),
        (E, "unknown-type", "50 References/Pancakes.md", "type"),
        (E, "missing-property", "92 Templates/Bad Template.md", "version"),
    }


def test_messages_carry_hints(load_vault: LoadVault) -> None:
    """Common mistakes get a message saying how to fix them."""
    issues = {
        (i.path, i.property): i.message
        for i in validate_properties.check(load_vault("bad-properties"))
    }
    assert "quoted" in issues[("10 Projects/Unquoted Link.md", "area")]
    assert "comma strings" in issues[("10 Projects/Comma Tags.md", "tags")]
    assert "got datetime" in issues[("01 Logs/Daily/2026-10-02.md", "created")]
    assert "body table" in issues[("20 Hobbies/Travel/Trips/2026-12 Tokyo.md", "budget")]


def test_typed_links(load_vault: LoadVault) -> None:
    """A resolving typed link must reach one note of the right type."""
    issues = validate_properties.check(load_vault("bad-links"))
    pieces = "20 Hobbies/Music/Piano/Pieces"
    assert keys(issues) == {
        (E, "link-wrong-type", "10 Projects/Wrong Area.md", "area"),
        (E, "not-a-link", f"{pieces}/Chopin - Not A Link.md", "composers"),
        (E, "link-wrong-type", f"{pieces}/Chopin - Wrong Type.md", "composers"),
        (E, "link-ambiguous", f"{pieces}/Liszt - Ambiguous.md", "composers"),
        (E, "link-wrong-type", f"{pieces}/Someone - Untyped Target.md", "composers"),
        (E, "link-wrong-type", "20 Hobbies/Music/Piano/Practice/2026-10-30 Practice.md", "pieces"),
    }
    # Resolve by alias, heading + display text, explicit path, and an archived
    # target: none of these notes may appear above.
    flagged = {i.path for i in issues}
    for ok in ("Chopin - Nocturne.md", "Chopin - Heading Link.md", "Liszt - By Path.md"):
        assert f"{pieces}/{ok}" not in flagged
    assert "40 Knowledge/Concepts/Recurrence.md" not in flagged


def test_resolve_strips_heading_display_and_extension(load_vault: LoadVault) -> None:
    """Headings, block references, display text, and .md don't change a link's target."""
    vault = load_vault("bad-links")
    target = parse_link("[[Frédéric Chopin.md#Life^abc|the composer]]")
    assert target == "Frédéric Chopin"
    note = vault.resolve(target).unique
    assert note is not None
    assert note.rel == "20 Hobbies/Music/Composers/Frédéric Chopin.md"
    assert vault.resolve("chopin").unique is not None  # alias, case-insensitive
    assert parse_link("Chopin") is None
    assert parse_link("[[A]] and [[B]]") is None


def test_decomposed_filenames_resolve(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """macOS stores 'é' decomposed (NFD); links in YAML are usually NFC."""
    root = copy_fixture("bad-links")
    composers = root / "20 Hobbies/Music/Composers"
    nfd = unicodedata.normalize("NFD", "Frédéric Chopin.md")
    (composers / "Frédéric Chopin.md").rename(composers / nfd)
    vault = load_vault(root)
    assert vault.resolve("Frédéric Chopin").unique is not None
    issues = validate_properties.check(vault)
    assert not any(i.path.endswith("Chopin - Heading Link.md") for i in issues)


def test_untyped_notes_allowed_only_in_inbox_and_attachments(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """Only 00 Inbox/ and 98 Attachments/ may hold notes without a type."""
    root = copy_fixture("valid")
    (root / "98 Attachments/Scan notes.md").write_text("no frontmatter\n", encoding="utf-8")
    (root / "50 References/Untyped.md").write_text("---\ntopic: x\n---\n", encoding="utf-8")
    issues = validate_properties.check(load_vault(root))
    assert keys(issues) == {(E, "missing-type", "50 References/Untyped.md", "type")}


def test_typed_inbox_notes_are_still_checked(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """A typed note in the Inbox must still meet its type's rules."""
    root = copy_fixture("valid")
    (root / "00 Inbox/Half done.md").write_text(
        "---\ntype: project\ncreated: 2026-10-01\nupdated: 2026-10-01\ntags: [inbox]\n---\n",
        encoding="utf-8",
    )
    issues = validate_properties.check(load_vault(root))
    assert keys(issues) == {
        (E, "missing-property", "00 Inbox/Half done.md", "status"),
        (E, "missing-property", "00 Inbox/Half done.md", "area"),
    }


def test_empty_optional_property_is_an_error(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """An optional property with no value is left out, never left blank."""
    root = copy_fixture("valid")
    note = root / "10 Projects/Spring Recital.md"
    text = note.read_text(encoding="utf-8")
    for blank in ("due:", "due: []", 'due: ""'):
        note.write_text(text.replace("due: 2027-04-15", blank), encoding="utf-8")
        assert keys(validate_properties.check(load_vault(root))) == {
            (E, "empty-property", "10 Projects/Spring Recital.md", "due")
        }, blank
    note.write_text(text.replace("due: 2027-04-15\n", ""), encoding="utf-8")
    assert validate_properties.check(load_vault(root)) == []


def test_quoted_iso_date_is_a_date(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """Quoted text in ISO form counts as a date, but only a real calendar date."""
    root = copy_fixture("valid")
    note = root / "10 Projects/Spring Recital.md"
    text = note.read_text(encoding="utf-8")
    note.write_text(text.replace("due: 2027-04-15", 'due: "2027-04-15"'), encoding="utf-8")
    assert validate_properties.check(load_vault(root)) == []
    note.write_text(text.replace("due: 2027-04-15", 'due: "2027-02-30"'), encoding="utf-8")
    assert keys(validate_properties.check(load_vault(root))) == {
        (E, "wrong-value-type", "10 Projects/Spring Recital.md", "due")
    }

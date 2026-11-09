"""validate_structure against the fixture vaults."""

from typing import Final

from tests.conftest import CopyFixture, LoadVault, keys
from vault_tools import validate_structure
from vault_tools.issues import Severity

E: Final = Severity.ERROR


def test_valid_vault_has_no_structure_issues(load_vault: LoadVault) -> None:
    """The valid fixture passes."""
    assert validate_structure.check(load_vault("valid")) == []


def test_bad_structure(load_vault: LoadVault) -> None:
    """Each kind of layout problem is reported exactly once, where it is."""
    issues = validate_structure.check(load_vault("bad-structure"))
    assert keys(issues) == {
        (E, "type-not-allowed", "Stray Root Note.md", None),
        (E, "undeclared-folder", "15 Extras/", None),
        (E, "filename-mismatch", "01 Logs/Daily/Oct 3.md", None),
        (E, "not-flat", "10 Projects/Sub/", None),
        (E, "file-not-allowed", "10 Projects/diagram.png", None),
        (E, "type-not-allowed", "20 Hobbies/Loose.md", None),
        (E, "undeclared-folder", "20 Hobbies/Knitting/", None),
        (E, "type-not-allowed", "20 Hobbies/Music/Composers/Chopin - Nocturne Op 9.md", None),
        (E, "not-flat", "20 Hobbies/Music/Composers/Old/", None),
        (E, "missing-hub", "20 Hobbies/Music/Piano/", None),
        (E, "hub-wrong-type", "20 Hobbies/Fitness/Fitness.md", None),
        (E, "hub-misnamed", "20 Hobbies/Fitness/Overview.md", None),
        (E, "type-not-allowed", "20 Hobbies/Fitness/Notes.md", None),
        (E, "type-not-allowed", "40 Knowledge/Stray.md", None),
        (E, "too-deep", "50 References/Topic/Deeper/", None),
        (E, "file-not-allowed", "50 References/notes.txt", None),
        (E, "file-not-allowed", "91 Tooling/vault_tools/helpers/notes.txt", None),
    }
    # Skipped folders (99 Archive/, 91 Tooling/tests/) report nothing.
    assert not any(i.path.startswith(("99 Archive/", "91 Tooling/tests/")) for i in issues)


def test_ignored_names_are_skipped(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """OS and app clutter in the ignore list is never reported."""
    root = copy_fixture("valid")
    (root / ".DS_Store").write_bytes(b"\0")
    (root / "10 Projects/.DS_Store").write_bytes(b"\0")
    (root / ".obsidian/plugins").mkdir(parents=True)
    (root / ".obsidian/app.json").write_text("{}", encoding="utf-8")
    (root / ".trash").mkdir()
    (root / ".trash/Deleted.md").write_text("gone\n", encoding="utf-8")
    (root / "10 Projects/.gitkeep").write_bytes(b"")
    assert validate_structure.check(load_vault(root)) == []


def test_tool_caches_and_environments_are_ignored(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """Python caches, virtual environments, and uv.lock are ignored."""
    root = copy_fixture("valid")
    for folder in (
        "91 Tooling/vault_tools/__pycache__",
        "91 Tooling/vault_tools/helpers/__pycache__",
        "91 Tooling/__pycache__",
        "91 Tooling/.pytest_cache/v/cache",
        "91 Tooling/.mypy_cache/3.12",
        "91 Tooling/.ruff_cache/0.17.3",
        "91 Tooling/.venv/bin",
    ):
        (root / folder).mkdir(parents=True)
        (root / folder / "vault.cpython-312.pyc").write_bytes(b"\0")
    (root / "91 Tooling/uv.lock").write_text("version = 1\n", encoding="utf-8")
    assert validate_structure.check(load_vault(root)) == []


def test_ignore_entries_can_be_globs(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """A glob such as *.egg-info matches, and only what it says."""
    root = copy_fixture("valid")
    egg = root / "91 Tooling/schemas.egg-info"
    egg.mkdir()
    (egg / "PKG-INFO").write_text("Name: schemas\n", encoding="utf-8")
    assert validate_structure.check(load_vault(root)) == []
    (root / "91 Tooling/egg-info-notes").mkdir()
    (root / "91 Tooling/egg-info-notes/x.txt").write_text("x\n", encoding="utf-8")
    assert keys(validate_structure.check(load_vault(root))) == {
        (E, "undeclared-folder", "91 Tooling/egg-info-notes/", None)
    }


def test_vault_tools_folder_is_open(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """vault_tools/ may hold subpackages at any depth."""
    root = copy_fixture("valid")
    deep = root / "91 Tooling/vault_tools/helpers/more"
    deep.mkdir(parents=True)
    (deep / "util.py").write_text("X = 1\n", encoding="utf-8")
    assert validate_structure.check(load_vault(root)) == []


def test_absent_domains_need_no_hub(load_vault: LoadVault) -> None:
    """A declared domain with no folder on disk isn't reported."""
    vault = load_vault("valid")
    assert not (vault.root / "20 Hobbies/Music/Violin").exists()
    assert validate_structure.check(vault) == []


def test_empty_domain_folder_needs_a_hub(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """A domain folder that exists needs its hub, even when it holds only a .gitkeep."""
    root = copy_fixture("valid")
    (root / "30 Life Admin/Planning").mkdir()
    (root / "30 Life Admin/Planning/.gitkeep").write_bytes(b"")
    assert keys(validate_structure.check(load_vault(root))) == {
        (E, "missing-hub", "30 Life Admin/Planning/", None)
    }


def test_open_folder_inherits_files_and_depth(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """Subfolders of an open folder without max_depth inherit its rules at any depth."""
    root = copy_fixture("valid")
    deep = root / "98 Attachments/Scans/2026"
    deep.mkdir(parents=True)
    (deep / "2026-10-30 scan.png").write_bytes(b"\0")
    assert validate_structure.check(load_vault(root)) == []


def test_domain_root_allows_plan_notes_only(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """Beside the hub, a domain root holds only plan notes."""
    root = copy_fixture("valid")
    (root / "20 Hobbies/Fitness/Eating Plan.md").write_text(
        "---\ntype: plan\ncreated: 2026-10-01\nupdated: 2026-10-01\n---\n", encoding="utf-8"
    )
    (root / "20 Hobbies/Fitness/Squat Form.md").write_text(
        "---\ntype: reference\ncreated: 2026-10-01\nupdated: 2026-10-01\ntopic: x\n---\n",
        encoding="utf-8",
    )
    assert keys(validate_structure.check(load_vault(root))) == {
        (E, "type-not-allowed", "20 Hobbies/Fitness/Squat Form.md", None)
    }


_DOCUMENTATION: Final = "---\ntype: documentation\ncreated: 2026-11-08\nupdated: 2026-11-08\n---\n"
_PLAN: Final = "---\ntype: plan\ncreated: 2026-11-08\nupdated: 2026-11-08\n---\n"


def test_domain_may_have_an_about_page(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """A domain, or a subdomain, may hold one documentation note: About.md."""
    root = copy_fixture("valid")
    (root / "20 Hobbies/Fitness/About.md").write_text(_DOCUMENTATION, encoding="utf-8")
    (root / "20 Hobbies/Music/Piano/About.md").write_text(_DOCUMENTATION, encoding="utf-8")
    assert validate_structure.check(load_vault(root)) == []


def test_about_page_must_be_documentation(copy_fixture: CopyFixture, load_vault: LoadVault) -> None:
    """About.md at a domain root is reserved for documentation, even for scratch notes."""
    root = copy_fixture("valid")
    (root / "20 Hobbies/Fitness/About.md").write_text(_PLAN, encoding="utf-8")
    (root / "20 Hobbies/Music/About.md").write_text("---\ntype: scratch\n---\n", encoding="utf-8")
    assert keys(validate_structure.check(load_vault(root))) == {
        (E, "about-wrong-type", "20 Hobbies/Fitness/About.md", None),
        (E, "about-wrong-type", "20 Hobbies/Music/About.md", None),
    }


def test_domain_documentation_must_be_named_about(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """A documentation note at a domain root under any other name is misnamed."""
    root = copy_fixture("valid")
    (root / "20 Hobbies/Fitness/Fitness Tracking.md").write_text(_DOCUMENTATION, encoding="utf-8")
    (root / "20 Hobbies/Fitness/Routines/About.md").write_text(_DOCUMENTATION, encoding="utf-8")
    assert keys(validate_structure.check(load_vault(root))) == {
        (E, "about-misnamed", "20 Hobbies/Fitness/Fitness Tracking.md", None),
        (E, "type-not-allowed", "20 Hobbies/Fitness/Routines/About.md", None),
    }


_SESSION: Final = (
    "---\ntype: session\ncreated: 2026-11-06\nupdated: 2026-11-06\n"
    "date: 2026-11-06\nkind: sport\n---\n"
)


def test_session_name_is_the_date_and_one_word(
    copy_fixture: CopyFixture, load_vault: LoadVault
) -> None:
    """A session note's name is its date and any one word, e.g., 2026-11-06 Basketball."""
    root = copy_fixture("valid")
    sessions = root / "20 Hobbies/Fitness/Sessions"
    good = ("2026-11-06 Basketball", "2026-11-07 Swim", "2051-08-22 Gym", "2026-11-08 Pull-Day")
    bad = ("2026-11-09", "2026-11-09 Two Words", "Swim 2026-11-09", "2026-11-09 2")
    for name in (*good, *bad):
        (sessions / f"{name}.md").write_text(_SESSION, encoding="utf-8")
    assert keys(validate_structure.check(load_vault(root))) == {
        (E, "filename-mismatch", f"20 Hobbies/Fitness/Sessions/{name}.md", None) for name in bad
    }

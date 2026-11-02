"""The schemas themselves: the real ones are consistent; broken ones are caught."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Final

import pytest
import yaml

from tests.conftest import FIXTURES_DIR, CopyFixture, LoadVault, run_module
from vault_tools.cli import ExitCode
from vault_tools.issues import IssueCode
from vault_tools.schemas import PROPERTIES_SCHEMA, STRUCTURE_SCHEMA, SchemaError
from vault_tools.validate import version_issues
from vault_tools.vault import CONVENTIONS_PATH, Vault

type Edit = Callable[[object], None]


# -- editing raw YAML -----------------------------------------------------------


def _walk(data: object, keys: list[str]) -> object:
    """Follow mapping keys down into parsed YAML."""
    for key in keys:
        if not isinstance(data, dict):
            raise TypeError(f"{key!r}: not inside a mapping")
        data = data[key]
    return data


def set_key(path: str, value: object) -> Edit:
    """An edit that sets the dotted key `path` to `value`."""

    def edit(data: object) -> None:
        *parents, key = path.split(".")
        target = _walk(data, parents)
        assert isinstance(target, dict)
        target[key] = value

    return edit


def append_to(path: str, value: object) -> Edit:
    """An edit that appends `value` to the list at the dotted key `path`."""

    def edit(data: object) -> None:
        target = _walk(data, path.split("."))
        assert isinstance(target, list)
        target.append(value)

    return edit


def remove_from(path: str, value: object) -> Edit:
    """An edit that removes `value` from the list at the dotted key `path`."""

    def edit(data: object) -> None:
        target = _walk(data, path.split("."))
        assert isinstance(target, list)
        target.remove(value)

    return edit


def edit_yaml(path: Path, edit: Edit) -> None:
    """Apply an edit to a YAML file in place."""
    data: object = yaml.safe_load(path.read_text(encoding="utf-8"))
    edit(data)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def schema_errors(schema_dir: Path) -> list[str]:
    """Load the valid fixture with broken schemas and return the schema error messages."""
    with pytest.raises(SchemaError) as caught:
        Vault(FIXTURES_DIR / "valid", schema_dir)
    assert {issue.code for issue in caught.value.issues} == {IssueCode.SCHEMA_ERROR}
    return [issue.message for issue in caught.value.issues]


# -- the real schemas -----------------------------------------------------------


def test_real_schemas_are_consistent(load_vault: LoadVault) -> None:
    """The real schemas load and share a version with the fixture's CONVENTIONS.md."""
    assert version_issues(load_vault("valid")) == []


def test_both_schemas_share_a_version(load_vault: LoadVault) -> None:
    """Both schemas carry the same version, as text."""
    vault = load_vault("valid")
    assert vault.properties_schema.version == vault.structure_schema.version


# -- broken schemas -------------------------------------------------------------

PROPERTY_BREAKS: Final[dict[str, tuple[Edit, str]]] = {
    "undeclared property": (
        append_to("types.piece.optional", "opus"),
        "types.piece: 'opus' is not declared in property_types",
    ),
    "unknown obsidian type": (
        set_key("property_types.grade", "string"),
        "property_types.grade: Input should be 'text'",
    ),
    "missing vocabulary": (
        set_key("types.piece.constraints.status.vocab", "nope"),
        "no vocabulary named 'nope'",
    ),
    "link to unknown type": (
        set_key("types.piece.constraints.composer.link", "person"),
        "link target 'person' is not a note type",
    ),
    "type missing from note_type": (
        remove_from("vocabularies.note_type", "plan"),
        "types missing from vocabularies.note_type: plan",
    ),
    "constraint on absent property": (
        set_key("types.hub.constraints", {"status": {"vocab": "project_status"}}),
        "'status' is not a property of this type",
    ),
    "unknown constraint key": (
        set_key("types.daily.constraints.energy.vocabb", "field"),
        "types.daily.constraints.energy.vocabb: unknown key",
    ),
    "bad range": (
        set_key("types.daily.constraints.energy.range", [5, 1]),
        "range must be [min, max]",
    ),
    "bad pattern": (
        set_key("types.weekly.constraints.week.pattern", "(["),
        "does not compile",
    ),
    "unquoted version": (
        set_key("version", 0.1),
        "version: Input should be a valid string",
    ),
}


@pytest.mark.parametrize("name", PROPERTY_BREAKS)
def test_broken_properties_schema_is_caught(name: str, schema_copy: Path) -> None:
    """Each kind of mistake in the properties schema is reported with where it is."""
    edit, expected = PROPERTY_BREAKS[name]
    edit_yaml(schema_copy / PROPERTIES_SCHEMA, edit)
    errors = schema_errors(schema_copy)
    assert any(expected in error for error in errors), errors


STRUCTURE_BREAKS: Final[dict[str, tuple[Edit, str]]] = {
    "unknown folder type": (
        set_key("root.10 Projects.types", ["projekt"]),
        "root.10 Projects: 'projekt' is not a note type",
    ),
    "unknown role type": (
        set_key("root.20 Hobbies.domains.Fitness.items.Gear", ["gear"]),
        "'gear' is not a note type",
    ),
    "unknown folder key": (
        set_key("root.10 Projects.flatt", True),
        "root.10 Projects.flatt: unknown key",
    ),
    "unknown domain key": (
        set_key("root.30 Life Admin.domains.Health.records", {}),
        "root.30 Life Admin.domains.Health.records: unknown key",
    ),
    "max_depth without open": (
        set_key("root.10 Projects.max_depth", 2),
        "max_depth only applies to open folders",
    ),
    "bad filename pattern": (
        set_key("filenames.daily", "(["),
        "does not compile",
    ),
}


@pytest.mark.parametrize("name", STRUCTURE_BREAKS)
def test_broken_structure_schema_is_caught(name: str, schema_copy: Path) -> None:
    """Each kind of mistake in the structure schema is reported with where it is."""
    edit, expected = STRUCTURE_BREAKS[name]
    edit_yaml(schema_copy / STRUCTURE_SCHEMA, edit)
    errors = schema_errors(schema_copy)
    assert any(expected in error for error in errors), errors


def test_problems_in_both_schemas_are_reported_together(schema_copy: Path) -> None:
    """One run shows every schema problem, not just the first file's."""
    edit_yaml(schema_copy / PROPERTIES_SCHEMA, append_to("types.piece.optional", "opus"))
    edit_yaml(schema_copy / STRUCTURE_SCHEMA, set_key("root.10 Projects.flatt", True))
    errors = schema_errors(schema_copy)
    assert len(errors) == 2, errors


def test_broken_schema_is_reported_instead_of_note_checks(schema_copy: Path) -> None:
    """From the command line, a broken schema is the whole report and the run fails."""
    edit_yaml(schema_copy / PROPERTIES_SCHEMA, append_to("types.piece.optional", "opus"))
    vault = str(FIXTURES_DIR / "bad-properties")
    result = run_module("validate", vault, "--schemas", str(schema_copy), "--json")
    assert result.returncode == ExitCode.ERRORS
    data = json.loads(result.stdout)
    assert data["notes_checked"] == 0
    assert {issue["code"] for issue in data["issues"]} == {"schema-error"}


def test_version_mismatch(
    copy_fixture: CopyFixture, schema_copy: Path, load_vault: LoadVault
) -> None:
    """CONVENTIONS.md and both schemas must carry the same version."""
    root = copy_fixture("valid")
    version = load_vault(root, schema_copy).properties_schema.version
    (root / CONVENTIONS_PATH).write_text(
        f'---\ntype: system\ncreated: 2026-10-10\nupdated: 2026-10-10\nversion: "{version}"\n---\n',
        encoding="utf-8",
    )
    assert version_issues(load_vault(root, schema_copy)) == []

    edit_yaml(schema_copy / STRUCTURE_SCHEMA, set_key("version", "0.1"))
    issues = version_issues(load_vault(root, schema_copy))
    assert [issue.code for issue in issues] == [IssueCode.VERSION_MISMATCH]

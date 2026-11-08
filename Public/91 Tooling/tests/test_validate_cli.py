"""Validate and the validators as command-line programs."""

import json
from pathlib import Path
from typing import Final

import pytest

from tests.conftest import FIXTURES_DIR, CopyFixture, run_module
from vault_tools.cli import ExitCode

FAILING: Final = ["bad-properties", "bad-links", "bad-structure", "bad-link-rules", "bad-tags"]


def test_valid_vault_passes(served_copy: CopyFixture) -> None:
    """The valid fixture exits 0 with nothing to report."""
    result = run_module("validate", str(served_copy("valid")))
    assert result.returncode == ExitCode.OK, result.stdout + result.stderr
    assert "0 errors, 0 warnings" in result.stdout


@pytest.mark.parametrize("name", FAILING)
def test_failing_vaults_exit_1(name: str, served_copy: CopyFixture) -> None:
    """Every failing fixture exits 1."""
    result = run_module("validate", str(served_copy(name)))
    assert result.returncode == ExitCode.ERRORS, result.stdout + result.stderr


def test_every_fixture_is_covered() -> None:
    """Each fixture folder is either the valid vault or listed as failing."""
    assert sorted(p.name for p in FIXTURES_DIR.iterdir() if p.is_dir()) == sorted(
        [*FAILING, "valid"]
    )


def test_json_report() -> None:
    """The JSON report counts issues and leaves out empty fields."""
    result = run_module("validate", str(FIXTURES_DIR / "bad-links"), "--json")
    data = json.loads(result.stdout)
    assert data["summary"] == {"errors": 6, "warnings": 1, "ok": False}
    assert data["notes_checked"] == 17  # the archived book is a link target, not checked
    issue = next(i for i in data["issues"] if i["code"] == "link-unresolved")
    assert issue == {
        "severity": "warning",
        "check": "links",
        "code": "link-unresolved",
        "path": "20 Hobbies/Music/Piano/Pieces/Schumann - Missing Composer.md",
        "message": "[[Clara Schumann]] matches no note or file (broken, or not written yet)",
        "property": "composers",
    }


def test_warnings_alone_do_not_fail(served_copy: CopyFixture) -> None:
    """A run with only warnings exits 0."""
    root = served_copy("valid")
    note = root / "10 Projects/Spring Recital.md"
    note.write_text(
        note.read_text(encoding="utf-8").replace("[[Piano]]", "[[Harpsichord]]"), encoding="utf-8"
    )
    result = run_module("validate", str(root), "--json")
    assert result.returncode == ExitCode.OK
    assert json.loads(result.stdout)["summary"] == {"errors": 0, "warnings": 1, "ok": True}


def test_output_file_written_alongside_text(tmp_path: Path) -> None:
    """--output writes the JSON report and the text report still prints."""
    out = tmp_path / "report.json"
    result = run_module("validate", str(FIXTURES_DIR / "bad-structure"), "--output", str(out))
    assert result.returncode == ExitCode.ERRORS
    assert "too-deep" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["summary"]["ok"] is False


@pytest.mark.parametrize(
    ("module", "check"),
    [("validate_properties", "properties"), ("validate_structure", "structure")],
)
def test_single_validators_report_only_their_check(module: str, check: str) -> None:
    """Each single validator reports only its own check's issues."""
    result = run_module(module, str(FIXTURES_DIR / "bad-structure"), "--json")
    assert result.returncode == ExitCode.ERRORS
    assert {i["check"] for i in json.loads(result.stdout)["issues"]} == {check}


def test_missing_schema_exits_2(tmp_path: Path) -> None:
    """A schema folder without the schema files exits 2."""
    result = run_module("validate", str(FIXTURES_DIR / "valid"), "--schemas", str(tmp_path))
    assert result.returncode == ExitCode.LOAD_FAILED


def test_runs_from_another_folder(tmp_path: Path, served_copy: CopyFixture) -> None:
    """The installed package runs from outside 91 Tooling/, as from the repository root."""
    result = run_module("validate", str(served_copy("valid")), cwd=tmp_path)
    assert result.returncode == ExitCode.OK, result.stdout + result.stderr
    assert "0 errors, 0 warnings" in result.stdout

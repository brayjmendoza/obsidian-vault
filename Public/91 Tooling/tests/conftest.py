"""Shared pytest setup: loads fixture vaults and runs the validators as programs.

Each folder in tests/fixtures/ is a small Public/ folder. Every vault is judged
by the real schemas in 91 Tooling/schemas/, so a broken schema fails the tests
before CI judges the real vault.
"""

import shutil
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Final, Protocol

import pytest

from vault_tools.issues import CheckName, Issue, IssueCode, Severity
from vault_tools.vault import DEFAULT_SCHEMA_DIR, TOOLING_DIR, Vault

FIXTURES_DIR: Final = TOOLING_DIR / "tests" / "fixtures"
# A stand-in Private/ folder: only its file names matter, as in CI.
PRIVATE_SAMPLE_DIR: Final = TOOLING_DIR / "tests" / "private_sample"

type IssueKey = tuple[Severity, IssueCode, str, str | None]


class LoadVault(Protocol):
    """Loads a fixture vault by name, or any vault by path."""

    def __call__(
        self,
        name: str | Path,
        schema_dir: Path = DEFAULT_SCHEMA_DIR,
        private_dir: Path | None = None,
    ) -> Vault:
        """Load a vault with the given schemas and, optionally, a Private/ folder."""
        ...


class CopyFixture(Protocol):
    """Copies a fixture vault somewhere a test may change it."""

    def __call__(self, name: str) -> Path:
        """Copy the fixture and return the copy's path."""
        ...


def keys(issues: Iterable[Issue], check: CheckName | None = None) -> set[IssueKey]:
    """Reduce issues to comparable (severity, code, path, property) tuples."""
    return {
        (issue.severity, issue.code, issue.path, issue.property)
        for issue in issues
        if check is None or issue.check == check
    }


def run_module(
    module: str, *args: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run `python -m vault_tools.<module>` with arguments and capture its output."""
    return subprocess.run(
        [sys.executable, "-m", f"vault_tools.{module}", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        check=False,
    )


@pytest.fixture
def load_vault() -> LoadVault:
    """Load a fixture vault by folder name (or any path) with the real schemas."""

    def load(
        name: str | Path, schema_dir: Path = DEFAULT_SCHEMA_DIR, private_dir: Path | None = None
    ) -> Vault:
        path = Path(name)
        return Vault(path if path.is_absolute() else FIXTURES_DIR / path, schema_dir, private_dir)

    return load


@pytest.fixture
def copy_fixture(tmp_path: Path) -> CopyFixture:
    """Copy a fixture vault into tmp_path so a test can change it."""

    def copy(name: str) -> Path:
        dest = tmp_path / name
        shutil.copytree(FIXTURES_DIR / name, dest)
        return dest

    return copy


@pytest.fixture
def schema_copy(tmp_path: Path) -> Path:
    """Copy the real schemas into tmp_path so a test can break them."""
    dest = tmp_path / "schemas"
    shutil.copytree(DEFAULT_SCHEMA_DIR, dest)
    return dest

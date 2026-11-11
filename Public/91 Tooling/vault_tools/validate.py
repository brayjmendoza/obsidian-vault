"""Run every vault check: schema versions, structure, properties, links, tags, then URLs.

Exit code 0 when there are no errors (warnings are allowed), 1 when there are
errors, 2 when the vault or a schema file can't be read. From anywhere in the
repository, with the environment active:

    vault-validate                           # text report
    vault-validate --json                    # JSON report
    vault-validate --json --skip-urls        # without fetching any `url`, for Claude
    vault-validate Public --output report.json
    python -m vault_tools.validate
"""

import sys
from collections.abc import Sequence
from typing import Final

from vault_tools import (
    validate_links,
    validate_properties,
    validate_structure,
    validate_tags,
    validate_urls,
)
from vault_tools.cli import run_cli
from vault_tools.issues import CheckName, Issue, IssueCode, error_issue
from vault_tools.schemas import PROPERTIES_SCHEMA, STRUCTURE_SCHEMA
from vault_tools.vault import CONVENTIONS_PATH, Vault, load_note

DESCRIPTION: Final = "Run every vault check: schemas, structure, properties, links, tags, URLs."


def version_issues(vault: Vault) -> list[Issue]:
    """Check that CONVENTIONS.md and both schemas share one version number.

    Args:
        vault: The vault to check.

    Returns:
        One `version-mismatch` issue when the versions differ, otherwise none.
    """
    versions = {
        PROPERTIES_SCHEMA: vault.properties_schema.version,
        STRUCTURE_SCHEMA: vault.structure_schema.version,
    }
    conventions = vault.root / CONVENTIONS_PATH
    if conventions.is_file():
        version = (load_note(conventions, vault.root).properties or {}).get("version")
        versions[CONVENTIONS_PATH] = str(version)
    if len(set(versions.values())) <= 1:
        return []
    listed = ", ".join(f"{name} = {version!r}" for name, version in versions.items())
    message = f"CONVENTIONS.md and both schemas must share one version: {listed}"
    return [error_issue(CheckName.SCHEMA, IssueCode.VERSION_MISMATCH, PROPERTIES_SCHEMA, message)]


def check_without_urls(vault: Vault) -> list[Issue]:
    """Run every check over a vault except the network one, so no `url` is fetched.

    Args:
        vault: The vault to check.

    Returns:
        Every issue found.
    """
    return (
        version_issues(vault)
        + validate_structure.check(vault)
        + validate_properties.check(vault)
        + validate_links.check(vault)
        + validate_tags.check(vault)
    )


def check(vault: Vault) -> list[Issue]:
    """Run every check over a vault, fetching every `url` over the network.

    Args:
        vault: The vault to check.

    Returns:
        Every issue found.
    """
    return check_without_urls(vault) + validate_urls.check(vault)


def main(argv: Sequence[str] | None = None) -> int:
    """Run every check from the command line.

    Args:
        argv: The arguments, without the program name; `sys.argv[1:]` when None.

    Returns:
        The exit code.
    """
    return run_cli(
        DESCRIPTION, check, argv, checks_private_links=True, check_without_urls=check_without_urls
    )


if __name__ == "__main__":
    sys.exit(main())

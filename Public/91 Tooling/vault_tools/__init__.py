"""Tooling for the Obsidian vault: validators for its schemas.

Installed by `uv sync` in 91 Tooling/ (see README.md). From anywhere in the
repository, with the environment active:

    vault-validate                      # every check
    vault-validate-properties
    vault-validate-structure
    python -m vault_tools.validate

Modules:
    issues: the Issue model and its enums.
    schemas: both schemas as typed models, and the loader that checks them.
    vault: walks Public/, parses frontmatter, and resolves links.
    cli: the command line, report, and exit codes every validator shares.
    validate_properties, validate_structure: the two validators.
    validate: runs the version check and both validators.
"""

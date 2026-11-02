---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.10"
aliases: [GitHub Actions]
---
# CI Workflows

GitHub Actions workflows live in `.github/workflows/` at the repository root. They run the checks described in [[Schemas and Validation]] on every push. Below are the GitHub actions that are currently being used.

## `validate.yml`

Checks the schemas:

1. Check out the repository. CI gets no git-crypt key, so the contents of `Private/` stay encrypted and are never read (see [[Sync and Backup#git-crypt|git-crypt]]).
2. Set up uv (`astral-sh/setup-uv`), which installs the Python in `.python-version` and runs `uv sync --locked`. `--locked` fails the run if `uv.lock` is out of date with `pyproject.toml`.
3. Run the test fixtures, so a broken schema or script fails before the vault is judged.
4. Run `vault-validate` over `Public/` and upload the JSON report as a build artifact. The checkout puts `Private/` beside `Public/`, so links into `Private/` by name are caught too, from file names alone. URLs are fetched only when the step passes `--check-urls`.
5. On failure, mark the commit red, and optionally open or update a single "Vault validation" issue.

## `validate-links.yml`

Enforces no links from Public into Private (see [[Privacy Boundary]]):

1. Check out the repository, again without the git-crypt key. git-crypt encrypts file contents, not file names, so the list of files in `Private/` is still visible.
2. Collect every link in every note in `Public/`. These include wikilinks (e.g., `[[Note]]`, `[[Note|text]]`, `[[Note#Heading]]`), embeds (e.g., `![[file]]`), and Markdown links to local files.
3. Resolve each link the way Obsidian does: an exact path if one is given, otherwise the file with that name anywhere in the vault.
4. Fail if any link resolves to a file under `Private/`, or if a name is ambiguous between a Public and a Private file. Print each offending note and link.

## Shared Properties

- **CI reports; it doesn't block.** Phone edits reach GitHub through the Mac's auto-commit (see [[Sync and Backup]]), so there is nothing to reject. For the same reason there is no pre-commit hook: it would stop Obsidian Git's auto-commits.
- **Out of Claude's reach:** the workflows live outside `Public/`, so Claude can neither see nor change them.
- **Deployment, later:** there is nothing to deploy yet. A later workflow could regenerate templates from the body schema and commit them.

---
← [[Schemas and Validation]] · Next: [[Claude Guardrails]] →

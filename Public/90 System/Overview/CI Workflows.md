---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.10"
aliases: [GitHub Actions]
---
# CI Workflows

GitHub Actions workflows live in `.github/workflows/` at the repository root. They run the checks described in [[Schemas and Validation]] on every push. Every vault check lives in `vault-validate`, so one workflow runs them all. Below are the GitHub Actions currently in use.

## `validate.yml`

Runs on every push to main, weekly on Mondays (to catch URLs that died without a push), and on demand. Three jobs run side by side: `static-check` (mypy), `pre-commit` (the ruff hooks on every file), and `test-and-validate`, which runs the tests and then checks the vault:

1. Check out the repository. CI gets no git-crypt key, so the contents of `Private/` stay encrypted and are never read (see [[Sync and Backup#git-crypt|git-crypt]]).
2. Set up uv (`astral-sh/setup-uv`), which installs the Python in `.python-version` and runs `uv sync --locked`. `--locked` fails the run if `uv.lock` is out of date with `pyproject.toml`.
3. Run the test fixtures, so a broken schema or script fails before the vault is judged.
4. Run `vault-validate --check-urls` over `Public/`: the schemas, the link rules, the allowed tags, and a fetch of every `url`. The checkout puts `Private/` beside `Public/`. git-crypt encrypts contents, not file names, so links into `Private/` by name are caught from the names alone (see [[Privacy Boundary]]).
5. Write the text report to the job summary and upload the JSON report as a build artifact.
6. On any error, mark the commit red. Warnings (e.g., a URL that couldn't be verified) don't.

## Shared Properties

- **CI reports; it doesn't block.** Phone edits reach GitHub through the Mac's auto-commit (see [[Sync and Backup]]), so there is nothing to reject. For the same reason there is no pre-commit hook: it would stop Obsidian Git's auto-commits.
- **Outside `Public/`:** the workflows aren't in `Public/`, so Claude can see and change them only in a session where you connect `.github/` as well.
- **Deployment, later:** there is nothing to deploy yet. A later workflow could regenerate templates from the body schema and commit them.

---
← [[Schemas and Validation]] · Next: [[Claude Guardrails]] →

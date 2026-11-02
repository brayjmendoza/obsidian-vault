---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.12"
aliases: [GitHub Actions]
---
# CI Workflows

GitHub Actions workflows live in `.github/workflows/` at the repository root. `validate.yml` runs the checks described in [[Schemas and Validation]] on every push, and `pre-commit-autoupdate.yml` keeps the pre-commit hooks current. Every vault check lives in `vault-validate`, so one workflow runs them all.

## `validate.yml`

Runs on every push to main, weekly on Mondays (to catch URLs that died without a push), and on demand. Three jobs run side by side, so a failure in one doesn't hide the others:

| Job                 | Runs                                                       | Catches                                                                                                                                                                                                  |
| ------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `static-check`      | Strict mypy on `vault_tools/` and `tests/`                 | Type errors in the tooling                                                                                                                                                                               |
| `pre-commit`        | The ruff hooks from `.pre-commit-config.yaml`, on every file | Lint and format problems, even in commits that skipped the hooks (e.g., a desktop without `pre-commit install`, `--no-verify`, or a GitHub web edit). Fixes aren't committed: the job fails and prints the diff |
| `test-and-validate` | The tests, then `vault-validate --check-urls`              | A broken schema or validator, then anything in `Public/` that breaks a rule                                                                                                                              |

`test-and-validate` runs these steps:

1. Check out the repository. CI gets no git-crypt key, so the contents of `Private/` stay encrypted and are never read (see [[Sync and Backup#git-crypt|git-crypt]]).
2. Set up uv (`astral-sh/setup-uv`), which installs the Python in `.python-version` and runs `uv sync --locked`. `--locked` fails the run if `uv.lock` is out of date with `pyproject.toml`.
3. Run the test fixtures, so a broken schema or script fails before the vault is judged.
4. Run `vault-validate --check-urls` over `Public/`: the schemas, the link rules, the allowed tags, and a fetch of every `url`. The checkout puts `Private/` beside `Public/`. git-crypt encrypts contents, not file names, so links into `Private/` by name are caught from the names alone (see [[Privacy Boundary]]).
5. Write the text report to the job summary and upload the JSON report as a build artifact.
6. On any error, mark the commit red. Warnings (e.g., a URL that couldn't be verified) don't.

## `pre-commit-autoupdate.yml`

Keeps `.pre-commit-config.yaml` on the latest ruff release, so you never run `pre-commit autoupdate` by hand. Runs weekly on Mondays and on demand:

1. Check out the repository and set up uv.
2. Run `uvx pre-commit autoupdate`, which moves each hook's `rev` to its newest release.
3. If the file changed, commit it to main as `github-actions[bot]`, pull with rebase (Obsidian Git may have pushed in the meantime), and push. Otherwise, stop.

Each desktop's hooks switch to the new version after Obsidian Git pulls the commit. This is the only workflow that writes to the repository, so it's the only one with `contents: write`.

## Pre-commit Hooks

`.pre-commit-config.yaml` at the repository root runs two ruff hooks before every commit: `ruff check --fix`, then `ruff format`. Each desktop installs them once (see the tooling's [[Public/91 Tooling/README|README]]).

- **Only Python:** the hooks match `.py` files in `91 Tooling/`, fixture vaults excluded. Commits of notes alone skip them, so Obsidian Git's auto-commits go straight through.
- **Fixable problems fix themselves.** The hooks rewrite the file and fail that commit once, and the next commit includes the fix.
- **Unfixable problems block the commit.** Obsidian Git stages every change at once, so a Python file with an error ruff can't fix (e.g., an undefined name) also holds back the notes committed with it, until the code is fixed.
- **Same rules everywhere:** ruff reads its settings from `91 Tooling/pyproject.toml`, so the hooks, the `pre-commit` job, and `uv run ruff` agree.

## Shared Properties

- **CI reports; it doesn't block.** Phone edits reach GitHub through the Mac's auto-commit (see [[Sync and Backup]]), so there is nothing to reject.
- **Outside `Public/`:** the workflows and `.pre-commit-config.yaml` aren't in `Public/`, so Claude can see and change them only in a session where you connect them as well.
- **Deployment, later:** there is nothing to deploy yet. A later workflow could regenerate templates from the body schema and commit them.

---
← [[Schemas and Validation]] · Next: [[Claude Guardrails]] →

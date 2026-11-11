---
type: system
created: 2026-11-01
updated: 2026-11-07
version: "0.12"
---
# Vault Tools

`vault-tools` is the Python package that checks `Public/` against the vault's schemas. It walks every note, parses its frontmatter, resolves its links the way Obsidian does, and reports anything that breaks any of the rules defined in the schemas, the link rules, or the four allowed tags. What each schema checks, and why, is in [[Schemas and Validation]]. How GitHub runs these checks is in [[CI Workflows]].

## Folder Layout

The folder is laid out as follows:

```
91 Tooling/
├── README.md                    this file
├── pyproject.toml               package metadata, dependencies, console scripts, and ruff, mypy, and pytest settings
├── uv.lock                      exact version of every dependency (written by uv, committed)
├── .python-version              the Python version uv uses
├── schemas/
│   ├── properties-schema.yaml   every note type's properties and allowed values
│   └── structure-schema.yaml    every allowed folder, the types it holds, and filename patterns
├── vault_tools/
│   ├── issues.py                the Issue model and its severities, checks, and codes
│   ├── schemas.py               both schemas as pydantic models, loaded and cross-checked
│   ├── vault.py                 walks Public/, parses frontmatter, resolves links
│   ├── markup.py                finds links and URLs in note text, skipping code
│   ├── cli.py                   arguments, reports, and exit codes every validator shares
│   ├── validate_properties.py   enforces properties-schema.yaml
│   ├── validate_structure.py    enforces structure-schema.yaml
│   ├── validate_links.py        no links into Private/, URLs only in `url`
│   ├── validate_urls.py         fetches every `url` (network; only on request)
│   ├── validate_tags.py         every inline #tag is one of the four allowed tags
│   └── validate.py              runs every offline check: versions, structure, properties, links, and tags
└── tests/
    ├── __init__.py              makes tests/ a package, so mypy and ruff see it as tests.*
    ├── conftest.py              loads fixture vaults with the real schemas
    ├── test_*.py                one file per validator, plus the schemas and the CLI
    ├── private_sample/          a stand-in Private/ folder: only its file names matter
    └── fixtures/                small sample Public/ folders: valid, bad-links, bad-link-rules, bad-properties, bad-structure, bad-tags
```

Two files sit outside this folder: `.envrc` at the repository root (see [[#The Python Environment]]) and `.pre-commit-config.yaml`, also at the root.

## Requirements

- **uv:** installs Python 3.14, the dependencies, and the package itself
	- On MacOS, just run `brew install uv`.
- **direnv:** optional but recommended. It keeps the virtual environment out of iCloud and activates it for you 
	- On MacOs, run `brew install direnv`, then add `eval "$(direnv hook zsh)"` to `~/.zshrc`
- **PyYAML, pydantic, and requests** are the runtime dependencies. Everything else is a dev tool.

## Setup

On each new machine:

1. Clone the repository, or let iCloud sync it.
2. At the repository root, run `direnv allow` once, so direnv trusts `.envrc`.
3. In `Public/91 Tooling/`, run `uv sync`. uv downloads Python 3.14 if needed, creates the environment at `~/.venvs/vault-tools`, and installs the package and its dev tools from `uv.lock`.
4. Run `uv run pytest` to confirm everything works.
5. At the repository root, run `uv run --project "Public/91 Tooling" pre-commit install` to set up the ruff hooks.

## The Python Environment

- **Managed by uv.** `pyproject.toml` says what the package needs, `uv.lock` pins the exact versions, and `uv sync` makes the environment match. Never install into it with pip.
- **Kept out of iCloud.** A virtual environment holds thousands of machine-specific files that iCloud would sync to every device. `.envrc` sets `UV_PROJECT_ENVIRONMENT=$HOME/.venvs/vault-tools`, so uv builds it there instead of in a `.venv` folder here.
- **Activated by direnv.** Anywhere inside the repository, direnv also sets `VIRTUAL_ENV` and puts the environment's `bin/` on your `PATH`, so `python`, `pytest`, and the console scripts work without activating anything. Leaving the repository deactivates it.
- **Claude has no direnv.** Claude's runs happen on another machine, so Claude puts `UV_PROJECT_ENVIRONMENT=$HOME/.venvs/vault-tools` in front of every uv command (see [[CONVENTIONS]], section 7). Without it, uv would build a `.venv` inside this folder.

## Commands

Installing the package creates six console scripts:

| Command                     | Checks                                                                                                                                                                             |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vault-validate`            | Everything: the shared version of [[CONVENTIONS]] and all schemas, then structure, properties, links, tags, and a fetch of every `url`                                             |
| `vault-validate-structure`  | Only `structure-schema.yaml`: folders, note types per folder, filenames, hubs, and non-note files                                                                                  |
| `vault-validate-properties` | Only `properties-schema.yaml`: types, required properties, value types, vocabularies, and typed links                                                                              |
| `vault-validate-links`      | Only the link rules: no links into `Private/`, no broken links or missing headings and blocks, in bodies or properties (warnings), URLs only in `url`, and every `url` well formed |
| `vault-validate-tags`       | Only inline `#tags` in note bodies: each must be one of the four allowed tags (the `tags` property is checked with the properties)                                                 |
| `vault-validate-urls`       | Only the network check: fetches every `url` and reports pages that are gone or unreachable                                                                                         |

All of them take these options:

| Option          | Does                                                                                                                                     |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `PUBLIC_DIR`    | The `Public/` folder to check. Defaults to the one this package lives in                                                                 |
| `--schemas DIR` | The folder holding the schemas. Defaults to `91 Tooling/schemas/`                                                                        |
| `--json`        | Print a JSON report instead of text                                                                                                      |
| `--output FILE` | Also write the JSON report to `FILE`                                                                                                     |
| `--private DIR` | The `Private/` folder whose file names (never contents) links are checked against. Defaults to `Private/` beside `Public/`, if it exists |

The exit code is 0 when there are no errors (warnings are allowed), 1 when there are errors, and 2 when the vault or a schema file can't be read. A schema that reads fine but breaks its own rules counts as errors: its problems become the whole report, each naming the key at fault.

The report's `skipped` list names checks a run couldn't or didn't do: links into `Private/` by name when there's no `Private/` folder to see, and the URL check when `--skip-urls` was given.

`vault-validate` fetches every `url` by default. `--skip-urls` leaves that check out, for runs on a network that can't reach most sites (e.g., Claude's).

A URL that's gone (HTTP 404 or 410), or whose host doesn't exist, refuses connections, or fails TLS, is an error. Anything that might be temporary or a bot block (other 4xx, 5xx, timeouts, proxy refusals) is a warning: open the page by hand to confirm.

With direnv active, run them from anywhere in the repository:

```bash
vault-validate
vault-validate --json --output report.json
vault-validate --skip-urls
vault-validate-structure
```

`uv run` does the same, but first syncs the environment with `uv.lock`. That's useful right after a pull that changed dependencies. Outside this folder, point it here with `--project`:

```bash
uv run vault-validate                                   # from 91 Tooling/
uv run --project "Public/91 Tooling" vault-validate     # from the repository root
```

Each validator also runs as a module with the environment active (e.g., `python -m vault_tools.validate`).

## Development

From `91 Tooling/`:

| Task | Command |
|---|---|
| Run the tests | `uv run pytest` |
| Lint and format | `uv run ruff check --fix` and `uv run ruff format` |
| Type-check | `uv run mypy` |
| Run the pre-commit hooks | `uv run pre-commit run --all-files` (from the repository root, with `--project`) |

- **Tests use the real schemas.** Each fixture in `tests/fixtures/` is a small `Public/` folder judged by the schemas in `schemas/`, so a broken schema fails the tests before CI judges the real vault.
- **Fixtures are data, not code.** ruff and mypy skip `tests/fixtures/`, and the structure validator skips `tests/` entirely.
- **mypy is strict** on `vault_tools/` and `tests/` alike, with the pydantic plugin.
- **Code style:** every change follows [[CODE_STYLE]], and isn't done until ruff, mypy, and pytest pass.

To add a check, write a module in `vault_tools/` with a `check(vault) -> list[Issue]` function and a `main()` that calls `vault_tools.cli.run_cli`. Then call it from `validate.py`, add a console script under `[project.scripts]` in `pyproject.toml`, and add a fixture and a test that fail without it.

## Dependencies

| Task | Command |
|---|---|
| Add a runtime dependency | `uv add <pkg>` |
| Add a dev tool | `uv add --dev <pkg>` |
| Remove one | `uv remove <pkg>` |
| Upgrade everything to the latest releases | `uv lock --upgrade`, then `uv sync` |
| Change the Python version | Edit `requires-python` in `pyproject.toml`, then `uv python pin <version>` |

Commit `pyproject.toml`, `uv.lock`, and `.python-version` together. CI installs with `uv sync --locked`, which fails when `uv.lock` is out of date.

## Changing This Folder

- **Claude needs approval.** Claude never edits anything in `91 Tooling/` without your approval of the specific change (see [[CONVENTIONS]], section 7).
- **Schema changes bump the version.** [[CONVENTIONS]] and both schemas share one version number, and `vault-validate` reports an error when they differ. Bump all three and add a line to section 8 of [[CONVENTIONS]].
- **New files need the structure schema.** `91 Tooling/` allows only `.toml` files and system notes at its top level, `.yaml` in `schemas/`, and `.py` in `vault_tools/`. Anything else needs a `structure-schema.yaml` edit, or an entry in its `ignore` list.

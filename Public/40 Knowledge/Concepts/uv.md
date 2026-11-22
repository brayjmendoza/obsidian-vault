---
type: concept
created: 2026-11-11
updated: 2026-11-21
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-11
sources:
  - "[[uv Documentation]]"
---
**uv** is a Python package and project manager that installs Python itself, resolves a project's dependencies into a lockfile, and keeps the project's virtual environment identical to that lockfile.

uv is made by Astral and written in Rust. It replaces several older single-purpose tools with one command: pip and virtualenv for installing packages into environments, pip-tools and Poetry for locking, pyenv for installing Python versions, and pipx for running command-line tools. Its central idea is that a project's environment is never managed by hand. A **project** declares what it needs, uv resolves those needs into exact versions, and every command that runs code first makes the environment match.

# Project Files

A uv project is described by three files and one directory:

| File | Holds | Written by | Committed |
|---|---|---|---|
| `pyproject.toml` | What the project needs: metadata, dependencies with version constraints, and tool settings | The author, or `uv add` and `uv remove` | Yes |
| `uv.lock` | The exact version of every package, indirect dependencies included, for every platform | uv only | Yes |
| `.python-version` | The Python version the environment uses | `uv python pin` | Yes |
| `.venv/` | The installed packages | uv only | No |

The split is between intent and result. `pyproject.toml` states a constraint (e.g., `pyyaml>=6.0.3`), and `uv.lock` records which version satisfied it. The lockfile is cross-platform: one file covers macOS, Linux, and Windows, so every machine that installs from it gets the same versions. It's readable TOML, but it's never edited by hand, and it's committed so that every machine reproduces the same environment. The environment itself is machine-specific and never committed.

# Locking and Syncing

Two operations connect the files. **Locking** (`uv lock`) resolves `pyproject.toml` into `uv.lock`. **Syncing** (`uv sync`) installs what `uv.lock` lists into the environment. `uv sync` is exact: it also removes packages the lockfile doesn't list. `uv run <command>` locks and syncs before running the command, so the environment is always current and never needs activating. Unlike `uv sync`, `uv run` leaves extra packages in place unless it's given `--exact`.

Locking is conservative. uv keeps previously locked versions as long as they still satisfy `pyproject.toml`, so a new release upstream doesn't make the lockfile outdated. Upgrading is always explicit: `uv lock --upgrade` moves every package to the newest version its constraints allow, and `uv lock --upgrade-package <name>` moves one package and leaves the rest alone.

Two flags make locking strict or skip it. `--locked` makes uv fail when `uv.lock` is out of date with `pyproject.toml`, instead of quietly rewriting it. This suits continuous integration, where a stale lockfile is a mistake to report rather than repair. `--frozen` uses the lockfile as is, without checking it at all.

# Dependencies and Groups

`pyproject.toml` separates two kinds of dependency. `[project.dependencies]` lists what the package needs to run, and these are published with it. `[dependency-groups]`, standardized in PEP 735, lists local-only dependencies for development (e.g., test runners, linters, and type checkers), which are never published.

`uv add <pkg>` adds to the first, `uv add --dev <pkg>` adds to the `dev` group, and `uv add --group <name> <pkg>` adds to any other group. Each writes a lower bound at the version it resolved (e.g., `pytest>=9.2.0`) and updates the lockfile and environment in the same step. The `dev` group is synced by default, and `--no-dev` leaves it out (e.g., for a production install).

# The Python Interpreter

uv manages Python versions as well as packages. `requires-python` in `pyproject.toml` sets the range of versions a project supports, and `.python-version` picks the one its environment uses. `uv python pin 3.14` writes that file. When no matching interpreter exists on the machine, uv downloads a managed build of it, so a project needs no system Python, Homebrew Python, or conda.

# Where the Environment Lives

By default, the environment is `.venv/` inside the project folder. The `UV_PROJECT_ENVIRONMENT` environment variable moves it: an absolute path is used as is, and a relative path is resolved from the project root. Moving it matters when the project folder is synced by a cloud service, since an environment is thousands of small, machine-specific files that shouldn't travel between devices.

Because the variable is read on every command, it has to be set for every command that touches the project. An absolute path set globally in a shell is a trap: every project would share one environment, and each would overwrite the others' packages.

An environment can still be activated the usual way (i.e., `source <environment>/bin/activate`), which puts its executables on the `PATH` and sets `VIRTUAL_ENV`. Activation is optional with uv, and uv warns when `VIRTUAL_ENV` points somewhere other than the project's own environment.

# Installing the Project Itself

When `pyproject.toml` names a build system (e.g., setuptools), uv installs the project into its own environment in editable mode, so code changes take effect without reinstalling. That also makes each entry in `[project.scripts]` a command in the environment's `bin/`. Without a build system, uv installs only the dependencies, and entry points aren't available.

# Running from Another Folder

`uv run` finds its project by searching upward from the current directory for a `pyproject.toml`. Two options point it elsewhere. `--project <dir>` uses the project in `<dir>` but runs the command from the current directory, and `--directory <dir>` changes into `<dir>` first.

# Tools Outside Projects

Some command-line tools aren't part of any project. `uvx <tool>`, short for `uv tool run`, runs a tool in a temporary, isolated environment kept in uv's cache, without installing it. `uv tool install <tool>` installs it permanently, with its executables on the `PATH`. Tools are always isolated from projects, so a tool that has to import a project's code (e.g., pytest or mypy) belongs in a dependency group and runs through `uv run`.

uv also offers `uv pip`, a lower-level interface that mirrors pip's commands. It installs into an environment directly and bypasses `pyproject.toml` and the lockfile, so in a uv project it puts the environment out of step with `uv.lock` until the next sync.

# Common Commands

| Task | Command |
|---|---|
| Start a project | `uv init` |
| Create or update the environment from the lockfile | `uv sync` |
| Run a command in the environment | `uv run <command>` |
| Add or remove a runtime dependency | `uv add <pkg>`, `uv remove <pkg>` |
| Add a development dependency | `uv add --dev <pkg>` |
| Upgrade every package, or one | `uv lock --upgrade`, `uv lock --upgrade-package <pkg>` |
| Pin the Python version | `uv python pin <version>` |
| Install from the lockfile, failing if it's stale | `uv sync --locked` |
| Run a tool without installing it | `uvx <tool>` |

# Example

The vault's own tooling in `Public/91 Tooling/` is a uv project. Its `pyproject.toml` declares a build system, three runtime dependencies, a `dev` group of tools, and console scripts (abridged):

```toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"

[project]
name = "vault-tools"
requires-python = ">=3.14"
dependencies = ["pydantic>=2.14.2", "pyyaml>=6.0.3", "requests>=2.34.2"]

[project.scripts]
vault-validate = "vault_tools.validate:main"

[dependency-groups]
dev = ["mypy>=2.4.1", "pre-commit>=4.7.0", "pytest>=9.2.0", "ruff>=0.17.3"]
```

Beside it, `.python-version` holds `3.14` and `uv.lock` pins every package. The folder sits in iCloud, so the environment is moved out of it, and every command sets the same variable:

```bash
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/vault-tools"

uv sync                                              # build the environment from uv.lock
uv run pytest                                        # run the tests in it
uv run --project "Public/91 Tooling" vault-validate  # a console script, from the repository root
uv lock --upgrade && uv sync                         # move everything to the latest releases
```

`setuptools` is the build system, so `uv sync` installs `vault-tools` itself in editable mode, and `vault-validate` becomes a command in `~/.venvs/vault-tools/bin/`. In GitHub Actions, the same project installs strictly from its lockfile:

```yaml
- uses: astral-sh/setup-uv@v10.3.2
  with:
    enable-cache: true
- run: uv sync --locked
- run: uv run --locked pytest
```

# Connections
+ [ ] Make concepts out of these
- [[Virtual Environment]]: what uv creates and syncs for each project, an isolated folder of packages and its own interpreter
- [[Lockfile]]: the general idea behind `uv.lock`, recording resolved versions so installs are reproducible
- [[Dependency Resolution]]: how uv chooses versions that satisfy every constraint in `pyproject.toml` at once

# Sources

- [[uv Documentation]]

# Maps

![[Map.base#Maps]]

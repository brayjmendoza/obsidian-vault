---
type: article
created: 2026-11-11
updated: 2026-11-11
url: https://docs.astral.sh/uv/
year: 2026
status: to-read
fields:
  - computer-science
authors:
  - Astral
---
## Summary

Astral's documentation for [[uv]], a Python package and project manager written in Rust. Its guides walk through daily use, and its concept pages explain each part. These pages cover what the concept draws on:

| Page | Covers |
|---|---|
| [Working on Projects](https://docs.astral.sh/uv/guides/projects/) | A project's files, `uv run`, and adding, removing, and upgrading dependencies |
| [Managing Dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/) | Published dependencies versus dependency groups |
| [Locking and Syncing](https://docs.astral.sh/uv/concepts/projects/sync/) | Automatic locking, `--locked` and `--frozen`, exact syncing, and upgrades |
| [Configuring Projects](https://docs.astral.sh/uv/concepts/projects/config/) | Moving the environment with `UV_PROJECT_ENVIRONMENT`, build systems, and entry points |
| [Tools](https://docs.astral.sh/uv/concepts/tools/) | `uvx` and `uv tool install` |
| [Using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/) | `astral-sh/setup-uv`, caching, and `uv sync --locked` |

## Key Ideas

- [[uv]] keeps a project's environment identical to its lockfile, and `uv run` locks and syncs before every command.
- Upgrades are explicit: uv keeps locked versions until `uv lock --upgrade`, even after new releases.
- Development dependencies go in `[dependency-groups]` and are never published.
- Tools run with `uvx` are isolated from every project.

## Open Questions


## Quotes

> "uv will not consider lockfiles outdated when new versions of packages are released" (Locking and Syncing)

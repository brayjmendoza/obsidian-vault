---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.10"
---
# Schemas and Validation

Every rule a machine can check lives in a schema in `91 Tooling/`, and scripts enforce them in two places: Claude runs them after each skill run, and GitHub Actions run them on every push (see [[CI Workflows]]). [[CONVENTIONS]] keeps only the rules that need judgment, and points to the schemas instead of restating them.

The current layout of `91 Tooling/` is as follows:

```
91 Tooling/
├── README.md                    how to set up, run, and change the tooling
├── pyproject.toml               the vault-tools package: dependencies, console scripts, ruff, mypy, and pytest settings
├── uv.lock                      exact version of every dependency (written by uv, committed)
├── .python-version              the Python version uv uses (3.14)
├── schemas/
│   ├── properties-schema.yaml
│   └── structure-schema.yaml
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
│   └── validate.py              runs the version check and both validators
└── tests/fixtures/              small sample vaults that must pass or fail
```

## Python Environment

uv manages the tooling's Python, packages, and virtual environment, and `uv.lock` pins every package, so every machine and CI get the same set. The environment lives at `~/.venvs/vault-tools`, outside the vault: iCloud would otherwise sync thousands of machine-specific files. direnv points uv there through `.envrc` at the repository root and activates the environment anywhere in the repository. Setup, commands, and dependency management are in `91 Tooling/README.md`.

## The Schemas

| Schema                   | Stage                                  | What it checks                                                                                                                                                                                                               |
| ------------------------ | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `properties-schema.yaml` | Core                                   | Frontmatter: each property's one value type, vocabularies, required and optional properties per note type, value constraints                                                                                                 |
| `structure-schema.yaml`  | Core                                   | Layout: the allowed top-level folders, every domain and its role folders, which note types live in each folder, filename patterns, hubs present, flat folders, how deep open folders may go, allowed non-note files          |
| Typed links              | Core, inside the properties schema     | `link: composer` instead of `link: true`: `piece.composer` must point to a composer, `project.area` to a hub, `concept.sources` to a paper, book, course, or article. Wrong type is an error; an unresolved link is a warning |
| Link rules               | Core, a script rather than a schema    | No link into `Private/`, in bodies or properties; URLs only in `url`, each a single well-formed http(s) URL; with `--check-urls`, every URL loads. Code blocks and inline code are skipped |
| Tags                     | Core, a script reading the `tag` vocabulary | Every inline `#tag` in a note body (outside code) is one of the four allowed tags; the `tags` property is held to the same list by the properties schema |
| `body-schema.yaml`       | Planned                                | Required headings and tables per type: hub headings, concept Connections and Sources, the spending Categories table, the session sets table, and daily and weekly sections. Templates can be generated from it                   |
| `access-schema.yaml`     | Planned                                | Per folder, what Claude may do: create, edit, regenerate whole (daily and weekly notes), or read only. CI can then check that Claude's commits touched only allowed files                                                     |
| Template check           | Planned, a script rather than a schema | Each template in `90 System/Templates/` yields a note that passes every schema                                                                                                                                               |

Which of the planned schemas to build, and when, is still open: see [[Vault Open Questions]].

- **One home per rule:** the core schemas join on note type names. A type's folders and filename pattern are declared once, in the structure schema; its properties once, in the properties schema. [[Note Types and Properties]] summarizes both.
- **Approval enforces itself:** an undeclared folder fails validation, so a new hobby or area means a schema edit, which needs your approval.
- **Shared version:** `CONVENTIONS.md` and both schemas carry one version number and change together.

## Where Validation Runs

| Where | When | On failure |
| --- | --- | --- |
| Claude | End of every skill run (`vault-validate --json`), plus `--check-urls` when a run adds or changes a `url` | Fixes what it broke; reports the rest, and anything `skipped`, in the changelog |
| GitHub Actions | Every push to main, plus a weekly scheduled run | Red check and a JSON report; vault-health reads the latest result |
| Any desktop | On demand (`vault-validate`) | Prints the failures |

The private-link check is complete only where `Private/`'s file names are visible: GitHub Actions and your Mac. Claude can't see `Private/` (see [[Privacy Boundary]]), so its runs catch only links written as a `Private/…` path and list the rest under `skipped`.

---
← [[Everyday Lists]] · Next: [[CI Workflows]] →

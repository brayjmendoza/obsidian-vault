---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.12"
---
# Schemas and Validation

Every rule a machine can check lives in a schema in `91 Tooling/`, and scripts enforce them in two places: Claude runs them after each skill run, and GitHub Actions run them on every push (see [[CI Workflows]]). [[CONVENTIONS]] keeps only the rules that need judgment, and points to the schemas instead of restating them.

The current layout of `91 Tooling/` is as follows. This is a summary and excludes files that are more relevant for development. For the full layout, see the [[Public/91 Tooling/README|README]].

```
91 Tooling/
├── README.md                    how to set up, run, and change the tooling
├── schemas/
│   ├── properties-schema.yaml
│   └── structure-schema.yaml
├── vault_tools/                 data structures & validation scripts that use them
│   ├── validate_properties.py   enforces properties-schema.yaml
│   ├── validate_structure.py    enforces structure-schema.yaml
│   ├── validate_links.py        no links into Private/, URLs only in `url`
│   ├── validate_urls.py         fetches every `url` (network; only on request)
│   ├── validate_tags.py         every inline #tag is one of the four allowed tags
│   └── validate.py              runs every offline check: versions, structure, properties, links, and tags
└── tests/                       pytest tests to ensure scripts run as expected
```

## The Schemas

| Schema                   | Stage                                       | What it checks                                                                                                                                                                                                                                                                                                                                               |
| ------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `properties-schema.yaml` | Done                                        | Frontmatter: each property's one value type, vocabularies, required and optional properties per note type, value constraints                                                                                                                                                                                                                                 |
| `structure-schema.yaml`  | Done                                        | Layout: the allowed top-level folders, every domain and its role folders, which note types live in each folder, filename patterns, hubs present, flat folders, how deep open folders may go, allowed non-note files                                                                                                                                          |
| Typed links              | Done, inside the properties schema          | `link: composer` instead of `link: true`: `piece.composer` must point to a composer, `project.area` to a hub, `concept.sources` to a paper, book, course, or article. Wrong type is an error; an unresolved link is a warning                                                                                                                                |
| Link rules               | Done, a script rather than a schema         | No link into `Private/`, in bodies or properties; every link, in a body or a property, reaches a note or file in `Public/`, and any heading or block it names exists in that note (warnings otherwise, since the note may not be written yet); URLs only in `url`, each a single well-formed http(s) URL that loads. Code blocks and inline code are skipped |
| Tags                     | Done, a script reading the `tag` vocabulary | Every inline `#tag` in a note body (outside code) is one of the four allowed tags; the `tags` property is held to the same list by the properties schema                                                                                                                                                                                                     |
| `body-schema.yaml`       | Planned                                     | Required headings and tables per type: hub headings, concept Connections and Sources, the spending Categories table, the session sets table, and daily and weekly sections. Templates can be generated from it                                                                                                                                               |
| `access-schema.yaml`     | Planned                                     | Per folder, what Claude may do: create, edit, regenerate whole (daily and weekly notes), or read only. CI can then check that Claude's commits touched only allowed files                                                                                                                                                                                    |
| Template check           | Planned, a script rather than a schema      | Each template in `90 System/Templates/` yields a note that passes every schema                                                                                                                                                                                                                                                                               |

Which of the planned schemas to build, and when, is still open: see [[Vault Open Questions]].

- **One home per rule:** the core schemas join on note type names. A type's folders and filename pattern are declared once, in the structure schema; its properties once, in the properties schema. [[Note Types and Properties]] summarizes both.
- **Approval enforces itself:** an undeclared folder fails validation, so a new hobby or area means a schema edit, which needs your approval.
- **Shared version:** [[CONVENTIONS]] and all schemas carry one version number and change together. `vault-validate` reports an error when they differ.

## Where Validation Runs

| Where          | When                                             | On failure                                                                      |
| -------------- | ------------------------------------------------ | ------------------------------------------------------------------------------- |
| Claude         | End of every skill run (`vault-validate --json`) | Fixes what it broke; reports the rest, and anything `skipped`, in the changelog |
| GitHub Actions | Every push to main, plus a weekly scheduled run  | Red check and a JSON report; vault-health reads the latest result               |
| Any desktop    | On demand (`vault-validate`)                     | Prints all issues                                                               |

The private-link check is complete only where `Private/`'s file names are visible: GitHub Actions and your Mac. Claude can't see `Private/` (see [[Privacy Boundary]]), so its runs catch only links written as a `Private/…` path and list the rest under `skipped`.

---
← [[Everyday Lists]] · Next: [[CI Workflows]] →

---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.12"
aliases: [Guardrails for self-maintenance]
---
# Claude Guardrails

One hard boundary, several soft ones, and a full audit trail. The binding wording of these rules is in [[CONVENTIONS]] (sections 1 and 7); this note summarizes them.

- **Hard:** folder access. Claude is connected to `Public/` only (see [[Privacy Boundary]]).
- **Schema-valid writes:** Claude runs `vault-validate` before finishing, and every note it touched must pass all schemas (see [[Schemas and Validation]]). Claude never invents properties, types, vocabulary values, tags, folders, or domains, and never edits [[CONVENTIONS]], a schema, or anything else in `91 Tooling/` without approval of the specific change.
- **No links into Private:** Public notes never link to Private ones. `vault-validate` catches links written as a `Private/` path on every run, and links by name wherever `Private/`'s file names are visible, CI included (see [[CI Workflows]]).
- **URLs only in `url`:** a URL lives in a note's `url` property, never in a body or another property. `vault-validate` fetches every URL on every run.
- **Code style:** Python that Claude writes follows [[CODE_STYLE]] and isn't done until ruff, mypy, and pytest pass.
- **Read-only notes:** a `claude: read-only` property means read but never edit.
- **Generated notes:** daily and weekly notes are written entirely by skills (see [[Claude Skills]]), so Claude may create and rewrite them whole. Anything you write by hand goes in another note and gets linked.
- **No deletes:** Claude moves notes to `99 Archive/` instead.
- **Ask, don't guess:** ambiguous captures stay in the Inbox with a tagged question (see [[Folder Structure#Placement Rules|Placement Rules]]).
- **Audit trail:** each skill run appends one line to `90 System/Claude/changelog.md`; Git holds the diffs (see [[Sync and Backup]]).

---
← [[CI Workflows]] · Next: [[Vault Plugins]] →

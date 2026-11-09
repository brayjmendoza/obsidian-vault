---
type: documentation
created: 2026-10-25
updated: 2026-11-08
aliases:
  - Guardrails for self-maintenance
---
# Claude Guardrails

One hard boundary, several soft ones, and a full audit trail. The binding wording is in [[CONVENTIONS]] (sections 1 and 7), and this note summarizes it.

- **Hard: folder access.** Claude is connected to `Public/` only (see [[Privacy Boundary]]).
- **Valid notes only:** every note Claude touches must pass the schemas, and Claude checks before it finishes (see [[Schemas and Validation]]).
- **No new structure without approval:** Claude never invents folders, domains, properties, types, values, or tags, and never changes [[CONVENTIONS]] or the schemas without your approval of the specific change.
- **Read-only notes:** Claude never edits a note marked `claude: read-only`.
- **Generated notes:** daily and weekly notes are written entirely by skills, so anything you write by hand goes in another note (see [[Claude Skills]]).
- **No deletes:** Claude archives notes instead.
- **Your calls stay yours:** Claude never ticks off a task or changes a status or confidence unless you say so.
- **Ask, don't guess:** an unclear capture stays in the Inbox with a question (see [[Folder Structure#Placement Rules|Placement Rules]]).
- **Code style:** Python that Claude writes follows [[CODE_STYLE]] and isn't done until its checks pass.
- **Audit trail:** every run adds a line to the [[changelog]], and Git keeps the diffs (see [[Sync and Backup]]).

---
← [[CI Workflows]] · Next: [[Vault Plugins]] →

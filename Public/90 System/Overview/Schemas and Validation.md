---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Schemas and Validation

Every rule a machine can check lives in a schema, and scripts enforce them: Claude runs them at the end of every skill run, and GitHub runs them on every push (see [[CI Workflows]]). [[CONVENTIONS]] keeps only the rules that need judgment. How to set up and run the scripts is in the tooling's [[Public/91 Tooling/README|README]].

## The Schemas

- **The properties schema:** which properties each note type has, and the values each one accepts
- **The structure schema:** which folders exist, which note types each holds, and how notes are named

Scripts also check what the schemas can't: links reach a note, and the right kind of note, nothing links into `Private/`, URLs are well formed and still load, and every tag is one of the four. More checks are planned (e.g., required sections in note bodies, and which folders Claude may edit), and which to build is still open (see [[Vault Open Questions]]).

- **Approval enforces itself:** an undeclared folder, type, or property fails validation, so a new hobby or field means a schema change, which needs your approval.
- **One version:** [[CONVENTIONS]] and the schemas share a version number and change together.
- **Scratch notes are skipped** (see [[Note Types and Properties#Scratch Notes|Scratch Notes]]).

## Where Validation Runs

| Where | When | On failure |
|---|---|---|
| Claude | End of every skill run | Fixes what it broke and reports the rest |
| GitHub Actions | Every push, plus a weekly run | A red check and a report |
| Any desktop | On demand | Prints every issue |

Claude can't see `Private/` (see [[Privacy Boundary]]), so the check for links into it is complete only on your Mac and in CI.

---
← [[Everyday Lists]] · Next: [[CI Workflows]] →

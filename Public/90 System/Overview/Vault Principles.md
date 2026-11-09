---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Vault Principles

These are the ideas the rest of the vault's design follows from.

- **Predictable over clever:** a fixed folder map (see [[Folder Structure]]), a small set of note types (see [[Note Types and Properties]]), consistent properties. Claude queries structure; it guesses at chaos.
- **One contract, three files:** `90 System/Claude/CONVENTIONS.md` ([[CONVENTIONS]]) holds the rules in prose; `91 Tooling/schemas/` holds the machine-checked schemas: `properties-schema.yaml` for YAML frontmatter and `structure-schema.yaml` for folder layout. Every skill reads all three first, and validation scripts enforce the schemas on Claude's runs and in CI (see [[Schemas and Validation]]). These overview notes are background, not part of the contract.
- **Link, don't duplicate:** each fact lives in exactly one note. `Hobbies/` and `Life Admin/` link to `Projects/`, `Knowledge/`, and `References/` rather than copying them (see [[Domain Skeleton]]).
- **Privacy by access, not by instruction:** Claude only ever gets the folder it is allowed to see (see [[Privacy Boundary]]).
- **Reversible:** every Claude edit is versioned in Git (see [[Sync and Backup]]) and logged (see [[Claude Guardrails]]).
- **Schemas before automation:** use real notes for a few weeks before building skills on top of them (see [[Vault Rollout]]).

---
← [[Vault Overview]] · Next: [[Privacy Boundary]] →

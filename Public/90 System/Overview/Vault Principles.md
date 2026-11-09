---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Vault Principles

These are the ideas the rest of the vault's design follows from.

- **Predictable over clever:** a fixed folder map (see [[Folder Structure]]), a small set of note types (see [[Note Types and Properties]]), and consistent properties. Claude can query structure, but it has to guess at chaos.
- **One contract, three files:** [[CONVENTIONS]] holds the rules in prose, and two schemas hold the rules a machine can check. Every skill reads all three first, and scripts enforce the schemas (see [[Schemas and Validation]]).
- **Link, don't duplicate:** each fact lives in exactly one note. Domains link to projects, knowledge, and references rather than copying them (see [[Domain Skeleton]]).
- **Privacy by access, not by instruction:** Claude only ever gets the folder it's allowed to see (see [[Privacy Boundary]]).
- **Reversible:** every Claude edit is versioned in Git (see [[Sync and Backup]]) and logged (see [[Claude Guardrails]]).
- **Schemas before automation:** use real notes for a few weeks before building skills on top of them (see [[Vault Rollout]]).

---
← [[Vault Overview]] · Next: [[Privacy Boundary]] →

---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.6"
aliases:
  - Overview
---
# Vault Overview

This is the entry point to the documentation for how the vault is structured and maintained: the folder layout, note types, schemas and CI, sync, and the skills that keep it tidy. The rules themselves live in [[CONVENTIONS]] and the note schemas in `91 Tooling/schemas/`. These notes explain the rules and how they fit together. They are background for people. Skills don't need to read them on every run.

## The Contract

Three files make up the contract between you and every Claude skill. These overview notes are not part of it.

| File                                        | Holds                                                                                                        |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `90 System/Claude/CONVENTIONS.md`           | Rules that need judgment: placement, linking, note bodies, what Claude may and may not do                    |
| `91 Tooling/schemas/properties-schema.yaml` | Defines every note type's properties, value types, and allowed values (i.e., constraints on YAML frontmatter) |
| `91 Tooling/schemas/structure-schema.yaml`  | Defines every allowed folder, the note types each holds, the domain skeleton, filename patterns              |

See [[Vault Principles]] for why it's split this way, and [[Schemas and Validation]] for how the schemas are enforced.

## Contents

Read in this order the first time; each note links to the next.

**Design**
1. [[Vault Principles]]: the ideas everything else follows from
2. [[Privacy Boundary]]: the Public/Private split and why Claude can't see `Private/`

**Structure**
3. [[Folder Structure]]: the numbered top-level layout, the bands, and the placement rules
4. [[Domain Skeleton]]: the shape shared by every `Hobbies/` and `Life Admin/` domain
5. [[Knowledge Structure]]: how sources, concepts, and maps organize `Knowledge/` by links
6. [[Note Types and Properties]]: every note type, where it lives, and its properties
7. [[Note Properties]]: what each property means and the values it accepts
8. [[Tags]]: the four reserved tags and why everything else is a property
9. [[Everyday Lists]]: Schedule, Wishlist, and To-dos

**Enforcement**
10. [[Schemas and Validation]]: what the schemas check and where validation runs
11. [[CI Workflows]]: GitHub Actions used for maintenance
12. [[Claude Guardrails]]: hard and soft limits on what Claude may do

**Tools and Sync**
13. [[Vault Plugins]]: a list of Obsidian plugins used in this vault
14. [[Sync and Backup]]: iCloud, Git, and git-crypt across devices
15. [[Claude Skills]]: the AI skills that maintain the vault and help you get the most out of it

**Roadmap**
16. [[Vault Rollout]]: the five build phases
17. [[Vault Open Questions]]: decisions still to make
18. [[Vault TODOs]]: action items to improve or extend the vault

---
Start: [[Vault Principles]] →

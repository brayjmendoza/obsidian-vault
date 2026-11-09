---
type: documentation
created: 2026-10-25
updated: 2026-11-08
aliases:
  - Overview
---
# Vault Overview

This is the entry point to the vault's documentation: how it's laid out, what kinds of notes it holds, how it stays valid, and the skills that maintain it. The rules themselves live in [[CONVENTIONS]] and the schemas in `91 Tooling/schemas/`. These notes are background for people, so skills don't read them on every run.

## The Contract

Three files make up the contract between you and every Claude skill:

- **[[CONVENTIONS]]:** the rules that need judgment, like where notes go, how they link, and what Claude may do
- **The properties schema:** which properties each note type has
- **The structure schema:** which folders exist and which note types each one holds

Two style guides sit beside it: [[STYLE]] for writing notes and [[CODE_STYLE]] for the vault's Python. See [[Vault Principles]] for why it's split this way.

## Contents

Read in this order the first time. Each note links to the next.

**Design**
1. [[Vault Principles]]: the ideas everything else follows from
2. [[Privacy Boundary]]: the Public/Private split and why Claude can't see `Private/`

**Structure**
3. [[Folder Structure]]: the numbered top-level layout, the bands, and the placement rules
4. [[Domain Skeleton]]: the shape shared by every Hobbies and Life Admin domain
5. [[Knowledge Structure]]: how sources, concepts, and maps organize Knowledge by links
6. [[Note Types and Properties]]: every note type and where it lives
7. [[Note Properties]]: what each property means
8. [[Tags]]: the four reserved tags and why everything else is a property
9. [[Everyday Lists]]: Schedule, Wishlist, and To-dos

**Enforcement**
10. [[Schemas and Validation]]: what the schemas check and where validation runs
11. [[CI Workflows]]: the checks GitHub runs on every push
12. [[Claude Guardrails]]: what Claude may and may not do

**Tools and Sync**
13. [[Vault Plugins]]: the Obsidian plugins the vault uses
14. [[Vault Templates]]: templates for new notes and automations for existing ones
15. [[Sync and Backup]]: iCloud, Git, and encryption across devices
16. [[Claude Skills]]: the skills that maintain the vault and help you use it

**Roadmap**
17. [[Vault Rollout]]: the five build phases
18. [[Vault Open Questions]]: decisions still to make
19. [[Vault TODOs]]: action items to improve or extend the vault

---
Start: [[Vault Principles]] →

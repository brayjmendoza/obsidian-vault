---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.6"
---
# Vault Rollout

Five phases. The schema test in phase 2 matters most, because schemas change once real notes hit them (see [[Vault Principles|schemas before automation]]).

1. **Skeleton:** create the vault in iCloud Drive with the Public/Private split (see [[Privacy Boundary]]) and the domain folders (see [[Domain Skeleton]]); finalize `CONVENTIONS.md` and the properties and structure schemas; write the validation scripts, their tests, and both GitHub Actions (see [[Schemas and Validation]], [[CI Workflows]]); write templates for all note types. Set up Git: private remote, git-crypt for `Private/`, `.gitignore`, Git directory out of iCloud, Obsidian Git on every desktop (see [[Sync and Backup]]).
2. **Real content:** migrate repertoire, current routine, a few papers, and a past trip. Adjust schemas.
3. **First skills:** daily-note and inbox-triage; use them for two weeks (see [[Claude Skills]]).
4. **Core skills:** recall, weekly-review, ingest-source.
5. **Automation:** hobby planners, spending-import, quiz-me, vault-health on a schedule.

---
← [[Claude Skills]] · Next: [[Vault Open Questions]] →

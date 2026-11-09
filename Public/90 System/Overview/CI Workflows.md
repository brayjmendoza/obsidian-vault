---
type: documentation
created: 2026-10-25
updated: 2026-11-08
aliases: [GitHub Actions]
---
# CI Workflows

GitHub Actions check the vault on every push, so a broken rule shows up even when the edit came from your phone. How the workflows are set up is in the tooling's [[Public/91 Tooling/README|README]].

- **Validation:** on every push, weekly (to catch web pages that have disappeared), and on demand, CI tests the tooling and then runs every vault check (see [[Schemas and Validation]]). Errors mark the commit red, and warnings don't.
- **Lint hooks:** on each desktop, Python changes are linted and formatted before every commit, and a weekly workflow keeps those hooks on their latest release. Commits of notes alone skip them, so Obsidian Git's auto-commits go straight through.
- **Private stays encrypted:** CI never gets the key, so it can check links into `Private/` by file name without reading any of its notes (see [[Sync and Backup#git-crypt|git-crypt]]).
- **CI reports, it doesn't block.** Phone edits reach GitHub through the Mac's auto-commit (see [[Sync and Backup]]), so there's nothing to reject.
- **Outside `Public/`:** the workflows live at the repository root, so Claude can change them only in a session where you connect them too.

---
← [[Schemas and Validation]] · Next: [[Claude Guardrails]] →

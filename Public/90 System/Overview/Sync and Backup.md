---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.6"
---
# Sync and Backup

iCloud syncs the Apple devices, Git syncs the desktops, and the Mac connects the two. Obsidian Git (see [[Vault Plugins]]) works poorly on mobile, so phones and tablets rely on iCloud alone.

```
iPhone / iPad ── iCloud ──▶ Mac ◀── Git remote ──▶ Windows / Linux desktops
```

| Device                  | Syncs through  | Obsidian Git                                  |
| ----------------------- | -------------- | --------------------------------------------- |
| iPhone, iPad            | iCloud         | Off                                           |
| Mac                     | iCloud and Git | On: auto-commit, pull, and push on an interval |
| Windows, Linux desktops | Git            | On: auto-commit, pull, and push on an interval |

## Setup

- **Vault location:** the vault lives in iCloud Drive's Obsidian folder so Obsidian on iOS can open it. On the Mac, set that folder to "Keep Downloaded" so iCloud never offloads files Git or Claude need.
- **The Mac is the bridge:** phone edits reach the other desktops only after the Mac commits and pushes them. Keep Obsidian Git's auto-commit and auto-pull on there. This is also why CI reports instead of blocking (see [[CI Workflows#Shared Properties|Shared Properties]]).
- **Keep `.git` out of iCloud:** iCloud can corrupt Git's many small object files and would copy them to the phone. Either keep the Git directory outside the vault (`git init --separate-git-dir`) or rename it `.git.nosync` (iCloud skips `.nosync`) and point a `.git` file at it.
- **`.gitignore`:** `.obsidian/workspace*.json`, `.trash/`, `.DS_Store`. These change constantly and cause needless conflicts.
- **Remote:** a private GitHub repository holding the whole vault, `Private/` included.

## git-crypt

`.gitattributes` marks `Private/**` for encryption (see [[Privacy Boundary]]). Every desktop needs git-crypt installed and the repository unlocked; a locked clone shows `Private/` as unreadable binary files. Keep the key in your password manager, never in the vault.

## Conflicts and Backup

- **Conflicts:** avoid editing the same note on the phone and a non-Apple desktop between Mac syncs. Git flags conflicts; iCloud quietly makes duplicate copies (`Note 2.md`), which vault-health reports (see [[Claude Skills]]).
- **Backup:** Git history is the real backup. iCloud is sync, not backup: a deletion syncs everywhere.

---
← [[Vault Plugins]] · Next: [[Claude Skills]] →

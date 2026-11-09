---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Sync and Backup

iCloud syncs the Apple devices, Git syncs the desktops, and the Mac connects the two. Obsidian Git works poorly on mobile, so phones and tablets rely on iCloud alone (see [[Vault Plugins]]).

```
iPhone / iPad ── iCloud ──▶ Mac ◀── Git remote ──▶ Windows / Linux desktops
```

## Setup

- **Vault location:** the vault lives in iCloud Drive so Obsidian on iOS can open it. On the Mac, keep it downloaded so iCloud never offloads files Git or Claude need.
- **The Mac is the bridge:** phone edits reach the other desktops only after the Mac commits and pushes them, so keep its auto-commit and auto-pull on. This is also why CI reports instead of blocking (see [[CI Workflows]]).
- **Keep Git out of iCloud:** iCloud can corrupt Git's many small files, and would copy them to the phone.
- **Remote:** a private GitHub repository holds the whole vault, `Private/` included.
- **Tooling:** a desktop that runs the validators needs a one-time setup (see the tooling's [[Public/91 Tooling/README|README]]).

## git-crypt

`Private/` is encrypted on GitHub with git-crypt (see [[Privacy Boundary]]). Every desktop needs the key to read it, and the key lives in your password manager, never in the vault.

## Conflicts and Backup

- **Conflicts:** avoid editing the same note on the phone and a non-Apple desktop between Mac syncs. Git flags conflicts, but iCloud quietly makes duplicate copies, which vault-health reports (see [[Claude Skills]]).
- **Backup:** Git history is the real backup. iCloud is sync, not backup: a deletion syncs everywhere.

---
← [[Vault Templates]] · Next: [[Claude Skills]] →

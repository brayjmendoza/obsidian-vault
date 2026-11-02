---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.6"
---
# Privacy Boundary

Obsidian opens the whole vault; Claude is connected only to `Public/`, so it can't read anything in `Private/` because it is unreachable. This is the one hard guardrail (see [[Claude Guardrails]]).

```
Vault/         ← Obsidian opens this (sees everything); lives in iCloud Drive, synced to GitHub
├── Public/    ← the only folder connected to Claude
└── Private/   ← never connected; encrypted on GitHub with git-crypt
```

- Never connect the vault root itself. That would expose `Private/`.
- Private notes may link to Public notes. **Public notes never link to Private notes.** `vault-validate` reports any that do, in bodies and properties alike (see [[Schemas and Validation]]). It reads only `Private/`'s file names, never its notes, and only where it can see them: on your Mac and in CI. Claude's runs can't, so they catch only links written as a `Private/…` path. A GitHub Action checks the same rule on every push (see [[CI Workflows#`validate-links.yml`|validate-links.yml]]).
- Private holds: account numbers, salary and tax documents, health records, journal entries not for analysis, etc. Passwords belong in a password manager.
- `Private/` syncs through iCloud and GitHub like the rest of the vault (see [[Sync and Backup]]). On GitHub its contents are encrypted with git-crypt; file names, folder names, and commit messages are not, so keep sensitive details out of them.
- Meld Encrypt (see [[Vault Plugins]]) encrypts a whole note or parts of a note within Obsidian. Use it for single notes that should also be encrypted on your Apple devices.
- `.obsidian/` (settings, plugins) sits at the vault root, outside Claude's reach. Plugin changes are done by hand.

---
← [[Vault Principles]] · Next: [[Folder Structure]] →

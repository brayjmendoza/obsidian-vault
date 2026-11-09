---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Privacy Boundary

Obsidian opens the whole vault, but Claude is connected only to `Public/`, so it can never read `Private/`. This is the one hard guardrail (see [[Claude Guardrails]]). The binding rule is in [[CONVENTIONS]] (section 1).

```
Vault/         ← Obsidian opens this
├── Public/    ← the only folder connected to Claude
└── Private/   ← never connected, and encrypted on GitHub
```

- **Never connect the vault root:** that would expose `Private/`.
- **Public notes never link to Private ones.** Private notes may link to Public notes, and validation reports any link the other way (see [[Schemas and Validation]]).
- **What goes in Private:** account numbers, salary and tax documents, health records, and journal entries not meant for analysis. Passwords belong in a password manager.
- **Encrypted on GitHub:** `Private/` syncs like the rest of the vault, but its contents are encrypted on GitHub. File names and commit messages aren't, so keep sensitive details out of them (see [[Sync and Backup]]).
- **Single encrypted notes:** Meld Encrypt can also encrypt a note, or part of one, on your own devices (see [[Vault Plugins]]).
- **Plugin settings are out of reach too,** so plugin changes are made by hand.

---
← [[Vault Principles]] · Next: [[Folder Structure]] →

---
type: documentation
created: 2026-11-07
updated: 2026-11-08
aliases:
  - Templates
---
# Vault Templates

Templates make new notes that already pass the schemas, and a few automations keep notes you already have up to date. They live in `90 System/Templates/` and run through Templater (see [[Vault Plugins]]).

- **Type templates:** one per note type (e.g., [[Piece Template]]). Each asks for the note's properties, names the note to fit its type, and lays out its body.
- **Automations:** run on notes you already have (see [[#Automations]]).
- **Includes:** shared parts that other templates use, never run on their own.

Templates take their questions from the properties schema, so a schema change reaches every template without editing them. A required answer left blank tags the note `#inbox`, so inbox-triage finds it later.

## Automations

- **[[Add Properties]]:** adds the properties a note is missing.
- **[[Sync Last Practiced]]:** sets each piece's `last_practiced` from your practice notes. New practice notes run it on their own.
- **[[Sync Last Performed]]:** sets each exercise's `last_performed` from your session notes. Run it with the button at the end of a session note.

## Hotkeys

#inbox Come back and fill in the Templater hotkeys for the type templates and automations.

---
← [[Vault Plugins]] · Next: [[Sync and Backup]] →

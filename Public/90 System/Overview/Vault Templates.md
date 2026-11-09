---
type: system
created: 2026-11-07
updated: 2026-11-08
version: "0.22"
aliases:
  - Templates
---
# Vault Templates

All templates in this vault leverage the Templater plugin. Templates are stored in `90 System/Templates/` and they make new notes that already pass the schemas. Some can run small scripts on notes you already have. The folder layout is binding in `structure-schema.yaml`. Every template has the `template` type and is exempt from property checks beyond its `version` (see [[Schemas and Validation]]).

As an example:

```
90 System/Templates/
├── Piece Template.md        type templates: one per note type, run on a new note
├── Practice Template.md
├── …
├── Automations/             run on a note you already have
│   ├── Add Properties.md
│   ├── Sync Last Performed.md
│   └── Sync Last Practiced.md
└── Includes/                shared parts other templates include, never run alone
    ├── Frontmatter.md
    └── Session Table.md
```

## Three Kinds

| Kind | Where | Run on | Examples |
|---|---|---|---|
| Type template | Root of `Templates/`, named `<Type> Template` | A new note | [[Piece Template]], [[Hub Template]] |
| Automation | `Automations/` | Any existing note (Templater: Insert template) | [[Add Properties]], [[Sync Last Practiced]], [[Sync Last Performed]] |
| Include | `Includes/` | Nothing: other templates pull it in with `tp.file.include` | [[Frontmatter]], [[Session Table]] |

- **Type templates stay thin.** Most are a single line that includes [[Frontmatter]], so a schema change reaches every template without editing them.
- **Automations act more like scripts than templates.** They insert nothing into the note they run on, and they change other notes' properties instead.
- **Includes are building blocks.** Running one directly has no outer template to tell it what to do, so it fails or does the wrong thing.

# Automations

- **[[Add Properties]]:** adds a note's missing required properties, then offers the optional ones it doesn't have yet. It's [[Frontmatter]] in its adding mode.
- **[[Sync Last Practiced]]:** used for piece note types. It sets each piece's `last_practiced` to the latest practice note that lists it. Dates only move forward, so a later date set by hand is kept. The [[Practice Template]] runs it for one new note. Run it alone to sync every practice note (e.g., after adding pieces to an old one), since Templater can't react to property edits.
- **[[Sync Last Performed]]:** used for exercise notes. It sets each exercise's `last_performed` to the latest session note that logs it, meaning its row's Reps/Time/Distance cell is filled. Dates only move forward. Run it after logging a workout, with the button at the end of the session note or on its own: a new session note's table is still empty, so no template runs it.

# Hotkeys

#inbox Come back and fill in the Templater hotkeys for the type templates and automations.

## The Frontmatter Engine

Most templates include [[Frontmatter]], which handles setting up the correct properties for a given note type. It reads `properties-schema.yaml` on every run, so the questions the templates ask you always match the schema.

1. **Automatic values:** `type`, `created`, `updated`, and `version`, plus `date`, `week`, or `month` when the note's name holds one (e.g., `2026-11-07 Practice`)
2. **Required properties:** asked one at a time, with a list to pick from for vocabularies and links
3. **Optional properties:** offered from a list until you pick Done
4. **Name:** a new note is renamed to fit its type's filename pattern, built from its properties where possible (e.g., a practice note's date), or is asked for

A required property or name left blank tags the note `#inbox`, so inbox-triage finds it later.

---
← [[Vault Plugins]] · Next: [[Sync and Backup]] →

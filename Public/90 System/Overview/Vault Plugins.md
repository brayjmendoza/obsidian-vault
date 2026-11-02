---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.6"
aliases: [Obsidian plugins]
---
# Vault Plugins

Keep the plugin list short: every plugin with its own syntax is something Claude must also understand. Plugin settings live in `.obsidian/`, outside Claude's reach (see [[Privacy Boundary]]), so plugin changes are made by hand.

| Plugin                                                           | Kind      | Why                                                                                                                                                               |
| ---------------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Daily Notes, Templates, Properties, Backlinks, Canvas, Bookmarks | Core      | Basics                                                                                                                                                            |
| Bases                                                            | Core      | Database views over properties (e.g., repertoire, reading list); plain YAML Claude can edit. Powers the hub views (see [[Domain Skeleton#Hub Body\|Hub Body]])    |
| Obsidian Git                                                     | Community | Version history and sync between desktops (macOS, Windows, Linux); every Claude edit reviewable and reversible. Desktop only. Essential (see [[Sync and Backup]]) |
| Templater                                                        | Community | Templates with dates and prompts                                                                                                                                  |
| Periodic Notes + Calendar                                        | Community | Weekly and monthly notes, calendar sidebar                                                                                                                        |
| Tasks                                                            | Community | Queryable to-dos across the vault (see [[Everyday Lists]])                                                                                                        |
| QuickAdd                                                         | Community | One-keystroke capture into Inbox or a note type                                                                                                                   |
| Linter                                                           | Community | Consistent frontmatter and headings                                                                                                                               |
| Spaced Repetition                                                | Community | Flashcards from concept notes                                                                                                                                     |
| Zotero Integration                                               | Community | Paper citations and highlights, if using Zotero (see [[Vault Open Questions]])                                                                                    |
| Hide Folders                                                     | Community | Hide folders without real notes. Currently hides `91 Tooling/` and `98 Attachments/`.                                                                             |
| Meld Encrypt                                                     | Community | Encrypt single notes in Private                                                                                                                                   |
| Dataview, Excalidraw, Omnisearch, Homepage                       | Optional  | Only if a real need appears                                                                                                                                       |

---
← [[Claude Guardrails]] · Next: [[Sync and Backup]] →

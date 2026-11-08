---
type: system
created: 2026-10-25
updated: 2026-11-07
version: "0.6"
aliases:
  - Obsidian plugins
---
# Vault Plugins

Keep the plugin list short: every plugin with its own syntax is something Claude must also understand. Plugin settings live in `.obsidian/`, outside Claude's reach (see [[Privacy Boundary]]), so plugin changes are made by hand.

| Plugin                                                | By                   | Why                                                                                                                                                                                                   |
| ----------------------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Daily Notes, Properties, Backlinks, Canvas, Bookmarks | Obsidian (Core)      | Basics                                                                                                                                                                                                |
| Bases                                                 | Obsidian (Core)      | Database views over properties (e.g., repertoire, reading list); plain YAML Claude can edit. Powers the hub and map views (see [[Domain Skeleton#Hub Body\|Hub Body]])                                |
| Git                                                   | Vinzent              | Version history and sync between desktops (macOS, Windows, Linux); every Claude edit reviewable and reversible. Desktop only. Essential (see [[Sync and Backup]])                                     |
| Templater                                             | silentvoid13         | Templates with dates, prompt, commands, and more (see [[Vault Templates]])                                                                                                                                                   |
| Periodic Notes                                        | Community (TODO)     | Weekly and monthly notes                                                                                                                                                                              |
| Calendar                                              | Liam Cain            | Calendar sidebar                                                                                                                                                                                      |
| Tasks                                                 | obsidian-tasks-group | Queryable to-dos across the vault (see [[Everyday Lists]])                                                                                                                                            |
| QuickAdd                                              | chhoumann (TODO)     | One-keystroke capture into Inbox or a note type                                                                                                                                                       |
| Linter                                                | Community<br>(TODO)  | Consistent frontmatter and headings                                                                                                                                                                   |
| Spaced Repetition                                     | Community<br>(TODO)  | Flashcards from concept notes                                                                                                                                                                         |
| Zotero Integration                                    | Community<br>(TODO)  | Paper citations and highlights, if using Zotero (see [[Vault Open Questions]])                                                                                                                        |
| Hide Folders                                          | jonasdoesthings      | Hide folders without real notes. Currently hides `98 Attachments/`.                                                                                                                                   |
| Advanced Exclude                                      | Michael Naumov       | Treats files listed in `.obsidianignore` (at the vault root) as if they don't exist, so Obsidian never indexes them or rewrites their links. Keeps the test fixtures in `91 Tooling/tests/` untouched |
| Update modified date                                  | Alan Grainger        | Update the `created` and `updated` properties when modifying a file                                                                                                                                   |
| Meld Encrypt                                          | meld-cp              | Encrypt single notes in Private. Can also encrypt specific bits of text within a note                                                                                                                 |
| Dataview, Excalidraw, Omnisearch, Homepage            | Community (TODO)     | Only if a real need appears                                                                                                                                                                           |

---
← [[Claude Guardrails]] · Next: [[Vault Templates]] →

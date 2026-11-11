---
type: system
created: 2026-10-10
updated: 2026-11-11
version: "0.37"
---
# Vault Conventions

This file is the contract between you and every Claude skill that maintains this vault. **Every skill reads this file and all schemas before reading or writing any other note.** When this file and a skill disagree, this file wins.

| File | Holds |
|---|---|
| `90 System/Claude/CONVENTIONS.md` (this file) | Rules that need judgment: placement, linking, note bodies, and what Claude may and may not do |
| `91 Tooling/schemas/properties-schema.yaml` | Every note type's properties, their value types, and allowed values |
| `91 Tooling/schemas/structure-schema.yaml` | Every allowed folder, the note types each holds, the domain skeleton, and filename patterns |
| `90 System/Claude/STYLE.md` | How note bodies are written: voice, punctuation, headers, and links |
| `90 System/Claude/CODE_STYLE.md` | How Python is written: the checks it must pass, pydantic models, typing, docstrings, errors, and tests |
| `90 System/Overview/` (start at [[Vault Overview]]) | Why the vault is built this way. Background for people, and skills don't need it on every run |

The schemas are checked by scripts, so they win on anything they cover. This file doesn't restate them.

Status: **v0.37**. This file and all schemas share one version number. Bump all of them, and add a line to the top of section 8, whenever any of them changes.

---

## 1. Scope and Access

- Claude's access is limited to the `Public/` folder. Every path in this file is relative to `Public/`.
- A `Private/` folder exists outside Claude's access. Claude never asks for it and never guesses at its contents.
- **Public notes never link into `Private/`.** Private notes may link to Public ones, not the other way around. This covers every kind of link (i.e., wikilinks, embeds, and Markdown links), in note bodies and in properties. `vault-validate` reports one as `private-link`. A link written as a `Private/…` path is caught on every run, and a link by bare name is caught only where `Private/`'s file names are visible (i.e., your Mac and CI). Claude's runs can't see them, so its report lists that check under `skipped`. A name both folders have is an error too, since Obsidian could pick either.
- An unresolved link in `Public/` is either a broken link or a note not yet written. `vault-validate` reports each one, in note bodies and in properties, as a warning, never an error: `link-unresolved` when no note or file matches, and `anchor-unresolved` when the note lacks the heading (e.g., `[[Note#Heading]]` or a nested `[[Note#Part#Section]]`) or block (e.g., `[[Note#^id]]`) that the link names. Claude never "repairs" one by guessing its target.
- Plugin settings (i.e., `.obsidian/`) are outside Claude's access. Claude never assumes a plugin setting. If a skill depends on one, it tells you.

## 2. Placement

Ask these in order:

1. Does it have a finish line? → `10 Projects/`
2. Is it a hobby you keep doing? → `20 Hobbies/`
3. Is it a responsibility that never ends? → `30 Life Admin/`
4. Is it something learned? → `40 Knowledge/`
5. Is it something looked up? → `50 References/`

If none of these fits clearly, leave the note in `00 Inbox/` and ask with a `#question` line.

`structure-schema.yaml` lists every allowed folder and the note types each one holds. A folder it doesn't declare is an error.

### Domains

Every folder directly under `20 Hobbies/` or `30 Life Admin/` is a **domain**, and these band folders hold nothing but domains. Every domain follows the same skeleton:

- **Hub (required):** `<Domain>/<Domain>.md`, with type `hub`
- **About page (optional):** `<Domain>/About.md`, with type `documentation`. It explains how the domain's notes work together and which vault features (e.g., templates, scripts, and automations) serve it. It's the only documentation a domain holds, and it follows the same rules as the docs in `90 System/Overview/` (see [[STYLE]]). Since every About page shares one name, links to one use its path (e.g., `[[20 Hobbies/Fitness/About|About Fitness]]`)
- **Plan notes (optional):** standing plans at the domain root, with type `plan` (e.g., Budget, Schedule, Wishlist, and a practice rotation)
- **Task note (optional):** `<Domain>/To-Do's.md`, with type `task`: the domain's to-dos, one Tasks-plugin task per line. Priority, due dates, and the rest live in the tasks themselves, so it has no properties of its own. The hub's Tasks view lists its open tasks, and the hub's Add Task button adds to it
- **Items (optional role folders):** one note per thing you track or own, each with its own status or history (e.g., `Pieces/`, `Trips/`, and `Assets/`)
- **Logs (optional role folders):** one note per date or period (e.g., `Practice/`, `Sessions/`, and `Spending/`)
- **Plans (optional role folder):** a series of standing plans (e.g., workout routines in `Routines/`)
- **Subdomains (optional):** a nested domain with the same shape (e.g., `Music/Piano/`)

A domain holds only what is about your own doing or owning. Everything else lives once, elsewhere, and the domain links to it:

| If it is… | It goes in | The domain gets |
|---|---|---|
| A goal with an end | `10 Projects/`, with `area: "[[<Domain>]]"` | The project shows up in the hub's Projects view |
| Something learned | `40 Knowledge/` | A link to the map from the hub |
| A how-to or look-up | `50 References/` | A link from the hub or from the item that needs it |

Placement decisions that follow:

- Technique folders hold only drills you track. Explanations of technique go to Knowledge or References.
- Exercise notes hold your working weights and notes, and form how-tos go to References.
- Nutrition guidance goes to References, and your own eating plan is a Health plan note.
- A travel idea is a trip note with `status: idea`.
- Trips are items even though they end: one trip note is both plan and record.
- `reference` notes live only in `50 References/`. Notes about your own situation (e.g., accounts, contractors, and benefit elections) are items.
- Composers are items shared by every instrument in Music — biography and style analysis go to Knowledge.

New domains, role folders, top-level folders, or fields need your approval and a `structure-schema.yaml` edit before Claude creates them. Every new domain gets a hub.

### Empty Folders

**Empty folders keep a `.gitkeep`.** Git doesn't track empty folders, and CI only sees what Git tracks, so every innermost folder with nothing else in it holds an empty `.gitkeep` file. That keeps the vault's skeleton in the repository, and a domain folder without a hub fails in CI just as it does on your Mac. The validators ignore `.gitkeep`, so it can stay once notes arrive. When Claude creates a folder that stays empty, it adds one.

### Bands

Top-level folders are named `NN Name`. The first digit is the **band** (i.e., the kind of folder), and the second is the folder's position within the band. Numbers only set sort order. Subfolders aren't numbered.

| Band | Kind | Folders | Holds |
|---|---|---|---|
| 0 | Capture and logs | `00 Inbox/`, `01 Logs/` | Material ordered by time, not filed by topic: unsorted captures waiting for triage, and generated daily, weekly, and monthly logs |
| 1 | Projects | `10 Projects/` | Goals with a finish line |
| 2 | Hobbies | `20 Hobbies/` | Hobbies you keep doing, one domain each |
| 3 | Life Admin | `30 Life Admin/` | Responsibilities that never end, one domain each |
| 4 | Knowledge | `40 Knowledge/` | Things learned: sources, concepts, and maps |
| 5 | References | `50 References/` | Things looked up: how-tos and look-up info |
| 6–8 | Unused | none | Reserved for new kinds of content that fit none of bands 1–5 |
| 9 | System | `90 System/`, `91 Tooling/`, `92 Templates/`, `93 Views/`, `98 Attachments/`, `99 Archive/` | Not content. Counting up from 90: the vault's rules and docs, its tooling, then the templates and views that make it work. Storage for embedded files and retired notes counts down from 99 |

- Bands 1–5 match the placement questions above, in order.
- A new top-level folder takes the band that matches its kind and the next free position in it (e.g., a second capture folder would be `02 …`). Like any new folder, it needs your approval and a `structure-schema.yaml` edit first.
- Opening one of bands 6–8 is a new kind of content and needs your approval.
- Band 9 splits maintenance from function. `90 System/` holds only the rules (`system` notes) and the docs (`documentation` notes), and `91 Tooling/` checks them. `92 Templates/` makes notes, and `93 Views/` holds the bases and scripts that put live content in them.

## 3. File Naming

Filename patterns per type are in `structure-schema.yaml` under `filenames`. Types without a pattern use a plain descriptive title (e.g., `Water Heater.md`). Also:

- No characters Obsidian links dislike: `# ^ [ ] | \ :`
- Use the full title. No abbreviations unless they're the common name (e.g., `FFT` can be an alias of Fast Fourier Transform).
- Dates are always ISO `YYYY-MM-DD`.

## 4. Properties (Frontmatter)

The full schema is `properties-schema.yaml`. These rules apply on top of it.

- Every note outside `00 Inbox/` and `98 Attachments/` has a `type` from the schema.
- **Scratch notes aren't checked.** A note with `type: scratch` is scratch work. It may sit in any folder under any name, and it may carry the `common` properties (i.e., `created`, `updated`, `aliases`, `tags`, and `claude`). `vault-validate` checks nothing else about it, so its folder, filename, properties, links, tags, and URLs are never reported. Two rules still hold: it never links into `Private/` (see section 1), and it can't take a domain's hub name. Other notes can link to it, but a typed link to it (e.g., a piece's `composers`) is still the wrong type.
- **One property name, one value type, vault-wide.** Obsidian gives each property name a single type across the vault. A property never changes type between note types. If two meanings need different types, they get different names (e.g., `difficulty` is a number, and `grade` is text).
- **No nested objects.** Obsidian's properties panel doesn't handle maps or objects. Structured data goes in a table in the note body (see section 5).
- Property names are `snake_case`. Vocabulary values are lowercase and must match the schema exactly.
- Dates are `YYYY-MM-DD`. Lists are YAML lists, never comma strings.
- Links inside properties are quoted: `area: "[[Piano]]"`, and in a list, `composers: ["[[Johann Sebastian Bach]]", "[[Ferruccio Busoni]]"]`.
- Don't invent new properties, types, or vocabulary values. Propose them instead, and once you approve them, add them to the schema first, then use them.
- Prefer properties over tags. Tags are reserved for the short list in section 6.
- **URLs live only in `url`.** A URL never appears in any other property or in a note body. `url` holds exactly one http or https URL, and a note type that may hold one lists `url` in the properties schema. A note that needs several web pages links to one `reference` note per page instead.

## 5. Note Bodies and Linking

- **Note bodies follow their type's template** in `92 Templates/` (e.g., [[Routine Template]]). Start every new note from it, and keep to the format it lays out.
- **Link, don't duplicate.** Each fact lives in exactly one note, and other notes link to it.
- **Scripts** in `93 Views/Scripts/` are run by notes through Dataview (`dv.view`), so each behavior is written once. Paths in code are from the vault root, so they start with `Public/` (e.g., `dv.view("Public/93 Views/Scripts/last-time")`).
- **Links:** Link the first mention of a note per section, not every mention. Use `[[Note|display text]]` when grammar needs it.
- **No URLs in bodies.** To point at a web page, link to the note whose `url` holds it (see section 4). URLs inside code blocks and inline code are code, not links, and are allowed (e.g., a `curl` command in a how-to).
- **Attachments** go in `98 Attachments/`, named `YYYY-MM-DD description.ext`.
- **Tasks** use Tasks-plugin syntax: `- [ ] Do the thing 📅 2026-10-15`. Claude never ticks off a task you haven't reported done.

## 6. Tags (Reserved List)

Tags are only for things that cut across types. Use only these, exactly as written: lowercase and never nested (e.g., never `#idea/music`). `vault-validate` checks both the `tags` property and every inline `#tag` in note bodies, outside code.

- **`#inbox`:** Marks a note that needs triage but isn't in `00 Inbox/` (e.g., a QuickAdd capture made straight into a note type, or a note started in its folder but left unfinished). Notes in `00 Inbox/` don't need it, since the folder already says so. inbox-triage works through both the folder and this tag. Claude removes the tag once the note is complete (i.e., required properties, links, and body) and in the right folder. If a tagged note's placement, type, or status is ambiguous, Claude leaves it where it is, keeps the tag, and adds a `#question` line.
- **`#review`:** a note you want to revisit
- **`#idea`:** an unrefined idea anywhere in the vault
- **`#question`:** an open question Claude or you should answer

## 7. Rules for Claude

**Always**
- Read this file and all schemas (currently `properties-schema.yaml` and `structure-schema.yaml`) first.
- Skills that write or edit note bodies also read [[STYLE]].
- Skills and runs that write or edit code also read [[CODE_STYLE]] and don't finish until the checks in its first section pass.
- Write notes that pass both schemas: allowed folder and filename, required properties present, correct value types, and exact vocabulary values.
- At the end of every run, run the validators from `Public/`:
  `UV_PROJECT_ENVIRONMENT=$HOME/.venvs/vault-tools uv run --project "91 Tooling" vault-validate --json --skip-urls`.
  Fix anything the run broke and report the rest. Always set `UV_PROJECT_ENVIRONMENT` so uv never builds a virtual environment inside the vault, where iCloud would sync it.
- **Leave URL and private-link checks to your Mac and CI.** Claude's network can't reach most sites, and Claude can't see `Private/`. So Claude runs the validator with `--skip-urls`, ignores its `private-link` results and the `skipped` list, and leaves them all out of the run's report.
- Set `updated` on every note the run edits.
- Append one line per run to `90 System/Claude/changelog.md`:
  `- 2026-10-10 21:40 · inbox-triage · moved 4 notes from Inbox; created [[Fourier Transform]]`
- Cite note links when answering questions from the vault. If the vault doesn't contain the answer, say so instead of filling in from general knowledge without labeling it.
- Ask when a placement, type, or status is ambiguous: leave the note in `00 Inbox/` with a `#question` line describing what's unclear.

**Generated Notes**
- Daily and weekly notes are written entirely by skills. Claude may create them and rewrite them whole. Anything you want to keep by hand goes in another note, linked from the log.

**Never**
- Edit a note with `claude: read-only`.
- Edit this file, either schema, or anything else in `91 Tooling/` without your explicit approval of the specific change.
- Delete a note. Move it to `99 Archive/` with its original path mirrored.
- Rename a note without updating every link to it.
- Create folders, domains, fields, properties, types, or tags that the schemas don't declare.
- Mark tasks done, change a `status`, or change `confidence` unless you said so or the skill's instructions explicitly allow it.
- Store account numbers, government IDs, passwords, or similar in `Public/`. If such content shows up in `00 Inbox/`, leave it in place, don't repeat it, and tell you it belongs in `Private/`.

## 8. Changelog of This File

- 2026-11-11 · v0.37 · Added the `task` note type, for a domain's to-dos: `<Domain>/To-Do's.md` at the domain root, one Tasks-plugin task per line, with no properties of its own (see section 2). To-Do's is no longer a plan note. `structure-schema.yaml` allows `task` at domain roots and names it `To-Do's`. Added [[Task Template]].
- 2026-11-11 · v0.36 · Section 2: the to-do plan note is named To-Do's. No version bump: no rule or schema changed.
- 2026-11-11 · v0.36 · Section 7: Claude runs `vault-validate` with the new `--skip-urls` option, which leaves out the URL check. Without it, every `url` is still fetched (e.g., on your Mac and in CI). No version bump: no schema changed.
- 2026-11-11 · v0.36 · Section 7: Claude ignores the validator's URL and private-link results and leaves them out of its reports, since its network can't reach most sites and it can't see `Private/`. These checks are left to your Mac and CI. No version bump: no schema changed.
- 2026-11-08 · v0.36 · A session note's name is its date, a space, then anything (e.g., `2026-11-08 Pick-up Game with Friends`), not just one word.
- 2026-11-08 · v0.35 · A session note's name is its date and any one word (e.g., `2026-11-06 Basketball` or `2026-11-07 Swim`), not only Workout, Run, or Mobility. The Start Session button still picks one of those three.
- 2026-11-08 · v0.34 · Undoes two parts of v0.33: a session's `routine` is optional again, and type templates offer optional properties again. The Run, Mobility, and Workout session names stay, and only a routine's Start Session button uses them. It asks nothing and leaves optional properties for [[Add Properties]].
- 2026-11-08 · v0.33 · Session notes are named for what kind of workout they were: `YYYY-MM-DD Run` for running, `YYYY-MM-DD Mobility` for mobility, and `YYYY-MM-DD Workout` otherwise (e.g., calisthenics or weights), so one day can hold several. A session's `routine` is required. Type templates ask only for required properties, and [[Add Properties]] offers the optional ones.
- 2026-11-08 · v0.32 · `90 System/` holds only rules and docs. Templates (with `Automations/` and `Includes/`) moved to `92 Templates/`, and `Bases/` and `Scripts/` moved to `93 Views/` (see section 2). Every script and template path in notes, templates, and section 5 follows.
- 2026-11-08 · v0.31 · Every domain may have an About page, `<Domain>/About.md` with type `documentation`, explaining how its notes work together and which features serve it (see section 2). `structure-schema.yaml` adds `about: optional` to the domain skeleton, and `vault-validate` reports `about-wrong-type` and `about-misnamed`. [[20 Hobbies/Fitness/About|Fitness Tracking]] is now Fitness's About page.
- 2026-11-08 · v0.30 · Added the `documentation` note type, for notes that explain the vault to people. It has no `version`, and it's the only type `90 System/Overview/` holds. Section 5 points to each type's template for note bodies instead of describing them. [[20 Hobbies/Fitness/About|Fitness Tracking]] moved to the Fitness domain, and `90 System/Overview/` holds only vault-wide documentation.
- 2026-11-08 · v0.29 · The `muscle_group` vocabulary adds `lats`, `traps`, `lower-back`, `obliques`, `hip-flexors`, and `adductors`, and the `equipment` value `paralletes` is spelled `parallettes`. Added [[20 Hobbies/Fitness/About|Fitness Tracking]].
- 2026-11-08 · v0.28 · Exercise notes may take `pr`, your personal record as text (e.g., `3x25`). The `equipment` vocabulary adds `rings`, `dip-bars`, `plyo-box`, `jump-rope`, and `foam-roller`.
- 2026-11-08 · v0.27 · Routine `goal` is now `goals`, a list, and the `routine_goal` vocabulary adds `recovery`. Routines are named for the workout and follow the [[Routine Template]]: every exercise a linked list item with its target after ` — `, and every Core Workout block an H2 with a `Sets:` line. Session tables use `Reps/Time/Distance` and `Weight/Pace` columns, with units in the cells, so they fit runs, holds, and stretches as well as lifts (see section 5).
- 2026-11-08 · v0.26 · Routine notes have Warm-Up, Core Workout, and Cool-Down H1 sections, and session tables hold only the Core Workout, with a Target column, Sets filled from the routine, and a Sync Last Performed button (Meta Bind) after the table. Exercise notes end with a References section instead of the `form` property, which is gone from `properties-schema.yaml`. See section 5.
- 2026-11-08 · v0.25 · Exercise notes take `form` (a link to a reference note), `difficulty` (1–5), and `last_performed` (set by [[Sync Last Performed]]), with Last Time, Sessions, and Notes sections. Session tables take per-set values and are filled from the routine, whose exercises are links with the current tier highlighted (see section 5). `structure-schema.yaml` adds `90 System/Scripts/` for Dataview scripts (`js`). Added `Exercise.base`, [[Session Table]], and [[Sync Last Performed]].
- 2026-11-08 · v0.24 · Added the `scratch` note type, for scratch work that `vault-validate` doesn't check: any folder, any name, and the `common` properties (see section 4). The private-link check and the hub name still apply. Added [[Scratch Template]].
- 2026-11-08 · v0.23 · The `exercise_modality` vocabulary adds `mobility`, for routines and exercises that are stretching, foam rolling, or joint work rather than strength or running (e.g., [[Mobility Recovery]]).
- 2026-11-07 · v0.22 · `90 System/Templates/` has two subfolders in `structure-schema.yaml`: `Automations/` for templates run on an existing note (e.g., Add Properties and Sync Last Practiced) and `Includes/` for shared parts other templates include (e.g., Frontmatter). Type templates stay at the root of `Templates/`. Added [[Vault Templates]].
- 2026-11-07 · v0.21 · A hub's Plans view includes plan notes in its subdomains too (e.g., the Music hub lists Piano's and Violin's plans).
- 2026-11-07 · v0.20 · A hub's Plans section is a Bases view, `Plan.base`, of the plan notes in the hub's own folder, instead of hand-kept links.
- 2026-11-07 · v0.19 · Hub notes hold only links and queries, with H1 headings and no title or opening paragraph: Current, Projects, Plans, Recent, and Resources, which lists maps (shown as "<Field> Map") and references under separate `## Maps` and `## References` headings. A hub may add its own sections after Resources.
- 2026-11-07 · v0.18 · Piece notes are named with the piece's title alone (e.g., `Ballade No. 1 in G Minor`), since `composers` already records who wrote it. `structure-schema.yaml` no longer gives pieces a filename pattern.
- 2026-11-07 · v0.17 · Composer `eras` renamed `styles`, since periods alone don't describe every composer (e.g., Debussy is `impressionist`, Gardel is `tango`, John Williams is `film` and `romantic`). The `composer_era` vocabulary is now `composer_style`, adding `nationalist`, `expressionist`, `neoclassical`, `minimalist`, `film`, `jazz`, `ragtime`, `tango`, and `folk`.
- 2026-11-07 · v0.16 · Composer notes take `eras`, a list from the `composer_era` vocabulary, instead of `era`, so a transitional figure can have more than one (e.g., Beethoven: `classical` and `romantic`). `era` is gone from `properties-schema.yaml`.
- 2026-11-07 · v0.15 · Piece notes take `composers`, a list of links to composer notes, instead of `composer`: the original composer comes first, then any arrangers (e.g., Bach, then Busoni for the Bach–Busoni Chaconne). The piece filename uses the first composer's surname. `composer` is gone from `properties-schema.yaml`.
- 2026-11-07 · v0.14 · A `routine` is a workout you do, with no tie to a week: it has no `week` property, and `structure-schema.yaml` no longer gives routines a filename pattern, so they take a plain descriptive title (e.g., `Full-Body Strength`).
- 2026-11-07 · v0.13 · Piece notes are named `Title - Composer` with the composer's surname (e.g., `Ballade No. 1 in G Minor - Chopin`), noted beside the pattern in `structure-schema.yaml`. The pattern itself is unchanged. `routine` notes' `muscle_groups` now use the `muscle_group` vocabulary, like `exercise`.
- 2026-11-01 · v0.12 · Rewritten to follow [[STYLE]]: "you" for the vault's owner, title-case headers, e.g. and i.e. in parentheses, "see" cross-references, the Oxford comma, and fewer semicolons. Domains, Empty Folders, and Bands are now subsections of section 2. No version bump: no rule or schema changed.
- 2026-11-01 · v0.12 · Section 1: links to a heading or block that the target note lacks are reported too (`anchor-unresolved`). No version bump: no rule or schema changed.
- 2026-11-01 · v0.12 · Section 1: unresolved links in note bodies are now reported too, as warnings like those in properties. No version bump: no rule or schema changed.
- 2026-11-01 · v0.12 · Section 7: `vault-validate` fetches every `url` on every run, and the `--check-urls` option is gone. No version bump: no rule or schema changed.
- 2026-11-01 · v0.12 · Empty folders keep a `.gitkeep` so Git and CI see them (see section 2), and `structure-schema.yaml` ignores `.gitkeep`.
- 2026-11-01 · v0.11 · Section 6: inline `#tags` in note bodies are now checked against the four allowed tags, like the `tags` property. Spelled out that tags are lowercase and never nested. No version bump: the allowed tags are unchanged.
- 2026-11-01 · v0.11 · URLs live only in the `url` property, never in other properties or note bodies (see sections 4 and 5), and code is exempt. `vault-validate` now checks links into `Private/` (see section 1) and every URL's form, and fetches URLs with `--check-urls` (see section 7). `asset` notes may set `url`, and `manual` holds only an attachment link.
- 2026-11-01 · v0.10 · Added [[CODE_STYLE]] to the file table and to the reading rule in section 7. No version bump: [[CODE_STYLE]] keeps its own changelog and isn't schema-checked.
- 2026-11-01 · v0.10 · `91 Tooling/` is managed by uv: dependencies live in `pyproject.toml` (i.e., runtime) and its `dev` dependency group, `requirements.txt` is gone, and `.python-version` pins Python 3.14. `structure-schema.yaml` ignores `.python-version` and `.envrc`, and `91 Tooling/` allows only `toml` files. Section 7 now gives the validator command, with the virtual environment kept outside the vault.
- 2026-11-01 · v0.9 · Added [[STYLE]] to the file table and to the reading rule in section 7. No version bump: [[STYLE]] keeps its own changelog and isn't schema-checked.
- 2026-10-31 · v0.9 · Typed links: the `link:` constraint in `properties-schema.yaml` now names the target note type(s) instead of `true` (i.e., `project.area` → hub, `piece.composer` → composer, `practice.pieces` → piece, `session.routine` → routine, `trip.places` → place, and `concept.sources` → paper, book, course, or article). A wrong-type target is an error, and an unresolved link is a warning.
- 2026-10-31 · v0.8 · `reference` notes may set `url` (optional), for bookmarked tools and sites in `50 References/`.
- 2026-10-31 · v0.7 · `#inbox` now marks notes needing triage outside `00 Inbox/`, and inbox-triage works through both the folder and the tag. No schema content changed.
- 2026-10-25 · v0.6 · Added the `max_depth` folder key to `structure-schema.yaml`. `50 References/` allows one level of topic subfolders.
- 2026-10-25 · v0.5 · Added the bands table to section 2. The vault overview is now a folder of linked notes, `90 System/Overview/`, declared in `structure-schema.yaml`, and the old single note is archived.
- 2026-10-24 · v0.4 · Version shared with both schemas. `schema.yaml` split into `91 Tooling/schemas/properties-schema.yaml` and `structure-schema.yaml`. Folder map and naming table replaced by pointers to them. `20 Pursuits/` renamed `20 Hobbies/`, `30 Areas/` renamed `30 Life Admin/`, `01 Journal/` renamed `01 Logs/`, and `Classical Music/` renamed `Music/`. Added the domain skeleton, the `plan`, `account`, `contractor`, and `benefit` types, and the no-links-into-Private rule. `reference` limited to `50 References/`. Daily and weekly notes are fully generated, and the `## Claude` heading rule is gone. Added `90 System/Vault Overview.md`.
- 2026-10-11 · v0.2 · `Shared/` renamed `Public/`, `50 Reference/` renamed `50 References/`, and attachments moved to top-level `98 Attachments/`. Property schema moved to `90 System/schema.yaml`. Added one-type-per-property and no-nested-objects rules. `difficulty` is number-only, with a new `grade` text property. Spending categories moved from a property to a body table.
- 2026-10-10 · v0.1 · First draft

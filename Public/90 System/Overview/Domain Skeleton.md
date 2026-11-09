---
type: documentation
created: 2026-10-25
updated: 2026-11-08
aliases:
  - Hobby and Life Admin skeleton
---
# Domain Skeleton

Every folder directly under `20 Hobbies/` or `30 Life Admin/` (see [[Folder Structure]]) is a **domain**, and every domain has the same shape: one hub note plus up to three kinds of subfolder: Items, Logs, and Plans. A domain holds only what is about your own doing or owning; everything else lives once, elsewhere, and the hub links to it.

```
<Domain>/
├── <Domain>.md       hub (required): what this is, what's active, links out
├── <Plan>.md         standing plan notes (optional): Budget.md, Schedule.md
├── <Items>/          things you track or own, one note each (optional, any number)
├── <Logs>/           dated records of what you did (optional, any number)
├── <Plans>/          a series of standing plans, e.g. Routines/ (optional)
└── <Subdomain>/      a nested domain with the same shape (optional)
```

## Roles

Subfolders within a domain each have a role and are named for what they hold (e.g., for piano pieces, the folder has the "Items" role, but would be called `Pieces/`, not `Items/`); `structure-schema.yaml` records each folder's role and allowed note types (see [[Schemas and Validation]]).

| Role  | Holds                                              | Test                                   | Examples                                                  |
| ----- | -------------------------------------------------- | -------------------------------------- | --------------------------------------------------------- |
| Hub   | Overview, current focus, links out to other notes  | One per domain, named after the folder | Piano.md, Finance.md                                      |
| Items | One note per thing, with its own status or history | Do I track the state of this thing?    | Pieces/, Composers/, Exercises/, Trips/, Places/, Assets/ |
| Logs  | One note per date or period                        | Did this happen on a specific date?    | Practice/, Sessions/, Spending/                           |
| Plans | What you follow repeatedly until you change it     | Does it repeat with no end date?       | Routines/, Budget.md, Schedule.md                         |

## Hub Body

Every hub uses the same headings and holds only links and queries (see [[Vault Plugins|Bases and Tasks]] plugins), so nothing is copied. There's no title heading or opening paragraph: the note's name already says which domain it is. The [[Hub Template]] writes this shape, and the binding version is in [[CONVENTIONS]] (section 5). As an example:

```markdown
# Current       Bases view: items with an active status
# Tasks         Tasks query: TODO items found in this folder
# Projects      Bases view: open projects where area = [[Piano]]
# Plans         Bases view: plan notes in this domain and its subdomains
# Recent Logs   Bases view: the latest log notes
# Resources
## Maps         relevant maps in 40 Knowledge, e.g., [[Music Theory|Music Theory Map]]
## References   relevant notes in 50 References
```

The views live in `90 System/Bases/`, and each hub embeds them: `Hub.base` for Current, Projects, and Recent Logs (e.g., `![[Hub.base#Current]]`), and `Plan.base` for Plans (`![[Plan.base]]`). Plans includes subdomains, so the Music hub lists Piano's and Violin's plans too, with the folder each sits in. A hub may add sections of its own, such as a repertoire view in Piano.

## What Stays Out of a Domain

| If it is…                                                                     | It goes in...                          | Within the domain...                               |
| ----------------------------------------------------------------------------- | -------------------------------------- | -------------------------------------------------- |
| A goal with an end (e.g., a June recital program, a kitchen repaint)                | 10 Projects/, with `area: "[[Piano]]"` | It appears in the hub's Projects view on its own   |
| Something learned (e.g., harmony, training science, how index funds work)           | 40 Knowledge/                          | A link to the Knowledge Map under Links            |
| A how-to or look-up (e.g., scale fingerings, form cues, tax deadlines, policy text) | 50 References/                         | A link from the hub or from the item that needs it |

## Domain Examples

| Domain                    | Items                      | Logs             | Plans                  |
| ------------------------- | -------------------------- | ---------------- | ---------------------- |
| Music                     | Composers/                 |                  |                        |
| Music/Piano, Music/Violin | Pieces/, Technique/        | Practice/        | Practice Rotation      |
| Fitness                   | Exercises/                 | Sessions/        | Routines/, Weekly Rotation |
| Travel                    | Trips/, Places/            |                  |                        |
| Finance                   | Accounts/ (no numbers)     | Spending/        | Budget.md, Wishlist.md |
| Health                    |                            | Health Log/      | Eating Plan            |
| Home                      | Assets/, Contractors/      | Maintenance Log/ |                        |
| Planning                  |                            |                  | Schedule.md, To-dos.md |
| Work                      | Benefits/ (your elections) |                  |                        |

The note types for each of these folders are in [[Note Types and Properties]]. Planning's lists are described in [[Everyday Lists]].

## Placement Decisions that Follow

Using the above rules, here are a few examples of where certain folders/notes would be placed:

- **Technique/** holds only drills you track (e.g., a scale and its current tempo). Technique explanations live in `40 Knowledge/` or `50 References/`.
- **Exercises/** holds one note per movement: your last sets, the sessions that logged it, and your notes. Form videos live in `50 References/` and are linked from the exercise's References section (see [[Fitness Tracking]]).
- **Routines/** holds workouts named for what they are, not the day (e.g., Normal Run). Which day gets which routine is the Weekly Rotation plan note.
- **Nutrition** guidance lives in `50 References/`; your own eating plan is a Health plan note.
- **Travel ideas** are trip notes with `status: idea`; there is no Ideas/ folder.
- **Trips are items** even though they end: one trip note is both the plan and the record, so no project duplicates it.
- **`reference` is only for 50 References/.** Notes about your own situation (e.g., accounts, contractors, benefit elections) are items in their respective domains.
- **Composers are items** shared by every instrument in `Music/`; biography and style analysis go to `40 Knowledge/`.
- **Plan notes** (e.g., Budget.md, Schedule.md, Wishlist.md, To-dos.md, a practice rotation) have the `plan` type and sit at a domain root.

---
← [[Folder Structure]] · Next: [[Knowledge Structure]] →

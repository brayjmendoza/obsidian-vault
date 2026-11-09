---
type: documentation
created: 2026-10-25
updated: 2026-11-08
aliases:
  - Hobby and Life Admin skeleton
---
# Domain Skeleton

Every folder directly under `20 Hobbies/` or `30 Life Admin/` is a **domain**, and every domain has the same shape: a hub note, an optional About page, and optional folders for the things you track, the things you log, and the plans you follow. A domain holds only what is about your own doing or owning, and links to everything else. The binding rules are in [[CONVENTIONS]] (section 2). As an example:

```
<Domain>/
├── <Domain>.md     the hub
├── About.md        how the domain works (optional)
├── <Plan>.md       standing plans (e.g., Budget)
├── <Items>/        things you track or own
├── <Logs>/         dated records of what you did
├── <Plans>/        a series of plans (e.g., Routines/)
└── <Subdomain>/    a nested domain with the same shape
```

## Roles

Each folder in a domain has a role, and is named for what it holds (e.g., Piano's items folder is `Pieces/`).

| Role | Holds | Test | Examples |
|---|---|---|---|
| Hub | The domain's front page | One per domain, named after the folder | Piano, Finance |
| Items | One note per thing | Do I track the state of this thing? | Pieces/, Trips/, Assets/ |
| Logs | One note per date or period | Did this happen on a specific date? | Practice/, Sessions/, Spending/ |
| Plans | What you follow until you change it | Does it repeat with no end date? | Routines/, Budget, Schedule |

## Hub Body

A hub is the domain's front page. It holds only links and live views, so nothing is copied into it: what's active, open tasks and projects, the domain's plans, recent logs, and links to related maps and references. Every hub starts from the [[Hub Template]], and may add sections of its own (e.g., a repertoire view in Piano).

## About Page

A domain may have an About page explaining how its notes feed each other and which vault features serve it (e.g., [[Sync Last Practiced]] for Music). It's documentation, so it reads like these notes (see [[STYLE]]). For an example, see [[20 Hobbies/Fitness/About|About Fitness]].

## What Stays Out of a Domain

| If it is… | It goes in | The domain gets |
|---|---|---|
| A goal with an end (e.g., a recital) | `10 Projects/` | The project, in the hub's Projects view |
| Something learned (e.g., harmony) | `40 Knowledge/` | A link to the map from the hub |
| A how-to or look-up (e.g., form cues) | `50 References/` | A link from the hub or from the item that needs it |

A few cases this settles (see [[CONVENTIONS]], section 2, for the rest):

- **Trips are items** even though they end: one trip note is both the plan and the record.
- **Travel ideas are trips** with `status: idea`, not a separate folder.
- **Your own situation is an item,** not a reference (e.g., your accounts or benefit elections).

---
← [[Folder Structure]] · Next: [[Knowledge Structure]] →

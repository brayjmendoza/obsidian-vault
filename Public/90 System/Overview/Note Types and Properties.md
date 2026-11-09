---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Note Types and Properties

Every note outside `00 Inbox/` and `98 Attachments/` has a `type`, which decides where it lives and which properties it has. The schemas define every type (see [[Schemas and Validation]]), [[Note Properties]] says what each property means, and each type's template lays out its body (see [[Vault Templates]]).

| Note Type | Lives in | What it is |
|---|---|---|
| daily, weekly, monthly | `01 Logs/` | Generated logs of a day, week, or month |
| project | `10 Projects/` | A goal with a finish line, linked to the domain it serves |
| hub | Every domain | A domain's front page |
| plan | A domain's root | A standing plan you follow (e.g., a budget or schedule) |
| piece, technique, composer | Music | What you play, the drills you track, and who wrote it |
| practice | Music | One practice session |
| routine, exercise | Fitness | A workout, and one movement in it |
| session | Fitness | One workout you did |
| trip, place | Travel | A trip from idea to record, and a place you've been or want to go |
| paper, book, course, article | `40 Knowledge/` | Something you read or watched |
| concept | `40 Knowledge/` | One idea |
| map | `40 Knowledge/` | A field's table of contents |
| spending | Finance | One month's spending |
| account, asset, contractor, benefit | Finance, Home, and Work | Things you own, use, or rely on |
| log | Health and Home | A dated record (e.g., a checkup or a repair) |
| reference | `50 References/` | A how-to or look-up |
| system, template | `90 System/` and `91 Tooling/` | The vault's rules and templates |
| documentation | `90 System/Overview/`, and a domain's About page | Notes like this one, and a domain's own documentation |
| scratch | Anywhere | Scratch work that validation skips |

## Schema Rules that Shape Every Note

- **One property, one meaning:** a property has the same kind of value everywhere (e.g., `difficulty` is always a number, so a text grade is `grade`).
- **Fixed vocabularies:** statuses, fields, and other categories come from fixed lists, and new values need your approval (see [[Claude Guardrails]]).
- **Properties over tags:** only four tags exist, and everything else is a property (see [[Tags]]).

## Scratch Notes

A `scratch` note is a place to think without the schemas getting in the way. It can sit anywhere under any name, and validation skips it, except that it still can't link into `Private/` (see [[Privacy Boundary]]). When the work is ready to keep, give the note its real type.

---
← [[Knowledge Structure]] · Next: [[Note Properties]] →

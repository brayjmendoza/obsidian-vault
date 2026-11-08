---
type: system
created: 2026-10-25
updated: 2026-11-08
version: "0.6"
---
# Note Types and Properties

Every note outside `00 Inbox/` and `98 Attachments/` has a `type` property, which are defined in `properties-schema.yaml`. So, a note type is a note with a given `type` property. Each of these notes also has their type's properties. Every type requires `type`, `created`, and `updated`, and may additionally have `aliases`, `tags`, and `claude`. The one exception is `scratch` (see [[#Scratch Notes]]). Folders and filename patterns belong to `structure-schema.yaml`; the "Lives in" column in the table below summarizes it (see [[Folder Structure]] and [[Domain Skeleton]]). What each property means is in [[Note Properties]]. How the schemas are checked is described in [[Schemas and Validation]].

| Note Type         | Lives in                                         | Required                                | Optional Properties                                                                  |
| ----------------- | ------------------------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------ |
| daily             | 01 Logs/Daily                                    | date                                    | energy (1–5), sleep_hours                                                            |
| weekly            | 01 Logs/Weekly                                   | week                                    | practice_minutes, exercise_minutes, workouts, spending_total (computed, never typed) |
| monthly           | 01 Logs/Monthly                                  | month                                   | practice_minutes, exercise_minutes, workouts, spending_total (computed, never typed) |
| project           | 10 Projects                                      | status, area (link to a hub)            | start, due, outcome                                                                  |
| hub               | Every domain, named after its folder             |                                         |                                                                                      |
| plan              | Any domain root                                  |                                         | review_by                                                                            |
| piece             | Music/Piano/Pieces and Music/Violin/Pieces       | composers, status                       | difficulty (1–10), grade, started, last_practiced, memorized                         |
| practice          | Music/Piano/Practice and Music/Violin/Practice   | date, minutes, focus                    | pieces                                                                               |
| technique         | Music/Piano/Technique and Music/Violin/Technique | category                                | resources                                                                            |
| composer          | Music/Composers                                  | lived                                   | styles                                                                               |
| routine           | Fitness/Routines                                 | modality, muscle_groups, goal           |                                                                                      |
| session           | Fitness/Sessions                                 | date, kind                              | routine, duration_min                                                                |
| exercise          | Fitness/Exercises                                | muscle_groups                           | equipment                                                                            |
| trip              | Travel/Trips                                     | status                                  | start, end, places, companions, budget                                               |
| place             | Travel/Places                                    | country, visited                        | city, first_visit, rating (1–5)                                                      |
| paper             | Sources/Papers                                   | authors, year, fields, status           | url, venue                                                                           |
| book / course     | Sources/Books, Sources/Courses                   | authors, year, fields, status           | progress, started, finished, url                                                     |
| article           | Sources/Articles                                 | url, year, fields, status               | authors                                                                              |
| concept           | Knowledge/Concepts                               | fields, confidence (1–5), last_reviewed | sources                                                                              |
| map               | Knowledge/Maps                                   | field                                   |                                                                                      |
| spending          | Finance/Spending                                 | month, total                            | budget; categories go in a body table                                                |
| account           | Finance/Accounts                                 | url                                     | review_by                                                                            |
| asset             | Home/Assets                                      | purchased                               | warranty_until, manual, url                                                          |
| contractor        | Home/Contractors                                 |                                         | url                                                                                  |
| benefit           | Work/Benefits                                    |                                         | review_by                                                                            |
| log               | Health/Log, Home/Maintenance Log                 | date                                    |                                                                                      |
| reference         | 50 References                                    | topic                                   | url, review_by                                                                       |
| system / template | 90 System, 91 Tooling                            | version                                 |                                                                                      |
| scratch           | Any declared folder, under any name              | type only                               | the common properties; never validated (see [[#Scratch Notes]])                      |

## Schema Rules that Shape Every Note

- **One property name, one value type, vault-wide.** `difficulty` is always a number; a text grade gets its own name, `grade`.
- **No nested objects.** Structured data goes in a body table: spending categories, workout sets.
- **Fixed vocabularies.** Statuses, fields, focus areas, composer styles, muscle groups, equipment, categories, etc. come from lists in the schema. New values, properties, or types are proposed, approved, added to `properties-schema.yaml`, then used (see [[Claude Guardrails]]).
- **Four tags only:** `#inbox`, `#review`, `#idea`, `#question`. Everything else is a property.

## Scratch Notes

A `scratch` note is scratch work: a place to think without the schemas getting in the way. It needs only `type: scratch`, can sit in any declared folder under any name, and may carry the common properties. `vault-validate` skips it: no folder, filename, property, link, tag, or URL check runs on it, so nothing in it is reported. Two rules still apply. It never links into `Private/` (see [[Privacy Boundary]]), and it can't take a domain's hub name. It's still a link target, so other notes can link to it, but a typed link to one (e.g., a piece's `composers`) is the wrong type. When the work is ready to keep, give the note its real type and the validator checks it from then on.

---
← [[Knowledge Structure]] · Next: [[Note Properties]] →

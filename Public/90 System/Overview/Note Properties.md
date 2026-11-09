---
type: documentation
created: 2026-10-25
updated: 2026-11-08
aliases:
  - Property Reference
  - Properties
---
# Note Properties

This page contains a table of what every property in the vault means, grouped by area. [[Note Types and Properties]] shows which note types require or allow each one. How the schema files themselves work are described in header comments in the schemas themselves. What validation scripts are available and how code is packaged is described in the [[Public/91 Tooling/README|README]].

Each property has one value type across the whole vault: **text**, **number**, **date** (`YYYY-MM-DD`), **list**, or **checkbox**. Where a property only accepts certain values, they're listed under "Values". A **link** is a quoted wikilink to another note, like `"[[Frédéric Chopin]]"`.

## Common Properties

Every typed note has the properties `type`, `created`, and `updated`. The other four properties listed below are optional on any note.

| Property  | Type | Meaning                                                                                                                               | Values                                                 |
| --------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `type`    | text | What kind of note (i.e., note type) this is. It decides which properties the note must and may have, and which folders it may live in | One of the note types in [[Note Types and Properties]] |
| `created` | date | The day the note was first created                                                                                                    |                                                        |
| `updated` | date | The day the note was last edited. Claude sets it on every note it edits                                                               |                                                        |
| `aliases` | list | Other names the note goes by, so links and search find it (e.g., `FFT` for Fast Fourier Transform)                                          |                                                        |
| `tags`    | list | Cross-cutting flags. Everything else is a property                                                                                    | `inbox`, `review`, `idea`, `question`                  |
| `claude`  | text | Limits what Claude may do with the note                                                                                               | `read-only`: Claude may read but never edit it         |

## Logs

Properties for daily, weekly, and monthly notes in `01 Logs/`.

| Property           | Type   | Used by                       | Meaning                                                                                                           | Values                      |
| ------------------ | ------ | ----------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `date`             | date   | daily, practice, session, log | The day the note records                                                                                          |                             |
| `week`             | text   | weekly                        | The ISO week the note covers                                                                                      | `YYYY-Www`, e.g., `2026-W43` |
| `month`            | text   | monthly, spending             | The month the note covers                                                                                         | `YYYY-MM`                   |
| `energy`           | number | daily                         | How energetic you felt that day                                                                                   | 1–5                         |
| `sleep_hours`      | number | daily                         | Hours slept the night before                                                                                      | 0–24                        |
| `practice_minutes` | number | weekly, monthly               | Total amount of time spent practicing instruments in minutes. Computed from practice notes, never entered by hand |                             |
| `exercise_minutes` | number | weekly, monthly               | Total amount of time spent exercising in minutes. Computed from session notes, never entered by hand                   |                             |
| `workouts`         | number | weekly, monthly               | Number of workout sessions that week. Computed from session notes                                                 |                             |
| `spending_total`   | number | weekly, monthly               | Money spent that week. Computed from spending data                                                                |                             |

## Projects

Properties for projects with a defined goal in `10 Projects/`

| Property | Type | Used by | Meaning | Values |
|---|---|---|---|---|
| `status` | text | project | Where the project stands | `idea`, `active`, `paused`, `done`, `dropped` |
| `area` | text (link) | project | The domain hub this project serves, so it shows up in that hub's Projects view | Link to a hub |
| `start` | date | project | When work began | |
| `due` | date | project | The target finish date | |
| `outcome` | text | project | One line on how it ended: what was achieved, or why it was dropped | |

`status` is shared by several note types. It is always text, but each type has its own list of values (see pieces, trips, and sources below).

## Music

Properties for the music hobby in `20 Hobbies/Music`. These properties are for the pieces, practice, technique, and composers note types. Instrument is implied by folder and composers are shared by all instruments.

| Property         | Type         | Used by             | Meaning                                                                                   | Values                                                                                                         |
| ---------------- | ------------ | ------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `composers`      | list (links) | piece               | Who wrote the piece, then who arranged it                                                 | Links to composer notes, the original composer first (e.g., Tchaikovsky, then Pletnev)                         |
| `status`         | text         | piece               | Where the piece is in your repertoire                                                     | `wishlist`, `learning`, `polishing`, `repertoire`, `retired`, `relearning`                                     |
| `difficulty`     | number       | piece, exercise     | How hard it is for you, on your own scale                                                 | 1–10 for a piece, 1–5 for an exercise                                                                          |
| `grade`          | text         | piece               | A grade from an external syllabus, e.g., "ABRSM 8"                                        |                                                                                                                |
| `started`        | date         | piece, book, course | When you started learning or reading it                                                   |                                                                                                                |
| `last_practiced` | date         | piece               | The most recent day you practiced it. Set from practice notes by [[Sync Last Practiced]]  |                                                                                                                |
| `memorized`      | checkbox     | piece               | Whether you can play it from memory                                                       |                                                                                                                |
| `minutes`        | number       | practice            | Length of the practice session                                                            | 1–600                                                                                                          |
| `pieces`         | list (links) | practice            | The pieces worked on in the session                                                       | Links to piece notes                                                                                           |
| `focus`          | list         | practice            | What the session concentrated on                                                          | `technique`, `sight-reading`, `learning`, `memorization`, `performance`, `theory`                              |
| `category`       | text         | technique           | What kind of drill it is                                                                  | `scales`, `arpeggios`, `etudes`, `voicing`, `pedaling`, `bowing`, `shifting`, `vibrato`, `intonation`, `other` |
| `resources`      | list         | technique           | Material for the drill: books, videos, exercises                                          |                                                                                                                |
| `styles`         | list         | composer            | The composer's styles: periods, movements, and traditions, as many as fit (e.g., Beethoven: `classical`, `romantic`) | `medieval`, `renaissance`, `baroque`, `classical`, `romantic`, `nationalist`, `impressionist`, `expressionist`, `neoclassical`, `modern`, `minimalist`, `contemporary`, `film`, `jazz`, `ragtime`, `tango`, `folk` |
| `lived`          | text         | composer            | The years a composer lived                                                                | `YYYY-YYYY` or `YYYY-Present` (e.g., `1810-1839`)                                                              |

## Fitness

Properties for the fitness hobby in `20 Hobbies/Fitness`.

| Property        | Type        | Used by  | Meaning                                  | Values                                                                                                                                                    |
| --------------- | ----------- | -------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `modality`      | text        | routine  | The particular way the routine is done   | `running`, `calisthenics`, `weights`, `mobility`                                                                                                          |
| `goals`         | list        | routine  | What the routine trains for, as many as fit | `strength`, `hypertrophy`, `endurance`, `mobility`, `maintenance`, `recovery`                                                                          |
| `kind`          | text        | session  | What sort of workout it was              | `strength`, `cardio`, `mobility`, `sport`, `other`                                                                                                        |
| `routine`       | text (link) | session  | The routine this session followed        | Link to a routine note                                                                                                                                    |
| `duration_min`  | number      | session  | Length of the session in minutes         | 1–600                                                                                                                                                     |
| `muscle_groups` | list        | exercise, routine | The muscles it works              | `chest`, `back`, `lats`, `traps`, `lower-back`, `shoulders`, `biceps`, `triceps`, `forearms`, `core`, `obliques`, `hip-flexors`, `glutes`, `adductors`, `quads`, `hamstrings`, `calves`, `upper-body`, `lower-body`, `full-body` |
| `equipment`     | list        | exercise | What the exercise needs                  | `barbell`, `dumbbell`, `kettlebell`, `cable`, `machine`, `bands`, `bench`, `pull-up-bar`, `parallettes`, `rings`, `dip-bars`, `plyo-box`, `jump-rope`, `foam-roller` |
| `last_performed` | date       | exercise | The most recent day a session logged it. Set from session notes by [[Sync Last Performed]] |                                                                                                                                                 |
| `pr`           | text        | exercise | Your personal record, as you'd log it    | e.g., `3x25`, `185 lb x 5`, or `10 km in 44:10`                                                                                                           |

## Travel

Properties for the travel hobby in `20 Hobbies/Travel`.

| Property      | Type         | Used by        | Meaning                                                       | Values                               |
| ------------- | ------------ | -------------- | ------------------------------------------------------------- | ------------------------------------ |
| `status`      | text         | trip           | Where the trip stands. A trip idea is a trip note with `idea` | `idea`, `planning`, `booked`, `done` |
| `start`       | date         | trip           | Departure day                                                 |                                      |
| `end`         | date         | trip           | Return day                                                    |                                      |
| `places`      | list (links) | trip           | The places the trip visits                                    | Links to place notes                 |
| `companions`  | list         | trip           | Who you're traveling with                                    |                                      |
| `budget`      | number       | trip, spending | The amount planned to spend, in USD                           |                                      |
| `country`     | text         | place          | The country the place is in                                   |                                      |
| `city`        | text         | place          | The city, if the place is in or is one                        |                                      |
| `visited`     | checkbox     | place          | Whether you have been there                                   |                                      |
| `first_visit` | date         | place          | When you first went                                           |                                      |
| `rating`      | number       | place          | How much you liked it                                         | 1–5                                  |

## Knowledge

Properties for the sources, concepts, and maps note types in `40 Knowledge/` (see [[Knowledge Structure]]).

| Property        | Type         | Used by                                           | Meaning                                                                  | Values                                                              |
| --------------- | ------------ | ------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| `authors`       | list         | paper, book, course, article                      | Who wrote or taught it. For a course, the instructors                    |                                                                     |
| `year`          | number       | paper, book, course, article                      | Year of publication. For a course, the year you took it                  |                                                                     |
| `fields`        | list         | paper, book, course, article, concept             | Which fields the note belongs to. Decides which maps it should appear on | `computer-science`, `math`, `physics`, `music-theory`, `philosophy` |
| `field`         | text         | map                                               | The single field a map covers. Sub-maps keep their parent's field        | Same values as `fields`                                             |
| `status`        | text         | paper, book, course, article                      | Your reading progress                                                    | `to-read`, `reading`, `read`, `abandoned`                           |
| `url`           | text         | paper, book, course, article, account, asset, contractor, reference | Where to find it online. The only property, and the only place in a note, that may hold a URL |                                                                     |
| `venue`         | text         | paper                                             | Where the paper was published: journal, conference, arXiv                |                                                                     |
| `progress`      | text         | book, course                                      | How far through you are, e.g., "ch. 7" or "week 3 of 10"                  |                                                                     |
| `finished`      | date         | book, course                                      | When you finished it                                                     |                                                                     |
| `sources`       | list (links) | concept                                           | The source notes you learned the concept from                            | Links to source notes                                               |
| `confidence`    | number       | concept                                           | How well you understand the concept. Only changes when you say so        | 1–5                                                                 |
| `last_reviewed` | date         | concept                                           | When you last reviewed or were quizzed on it                             |                                                                     |

## Life Admin

Properties for areas in `30 Life Admin/`.

| Property         | Type   | Used by                           | Meaning                                                             | Values |
| ---------------- | ------ | --------------------------------- | ------------------------------------------------------------------- | ------ |
| `total`          | number | spending                          | Total spent that month, in USD                                      |        |
| `review_by`      | date   | plan, account, benefit, reference | When the note should be checked again because it may be out of date |        |
| `purchased`      | date   | asset                             | When you bought it                                                  |        |
| `warranty_until` | date   | asset                             | When the warranty runs out                                          |        |
| `manual`         | text   | asset                             | Where the manual is: a link to an attachment. An online manual goes in `url` |        |

## Reference

Properties for notes in `50 References/`.

| Property | Type | Used by   | Meaning                             | Values |
| -------- | ---- | --------- | ----------------------------------- | ------ |
| `topic`  | text | reference | What subject the reference is about |        |

## System

Properties for notes in `90 System/`.

| Property | Type | Used by | Meaning | Values |
|---|---|---|---|---|
| `version` | text | system, template | The vault conventions version the note matches, e.g., `"0.6"` | |

---
← [[Note Types and Properties]] · Next: [[Tags]] →

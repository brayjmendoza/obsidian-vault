---
type: documentation
created: 2026-10-25
updated: 2026-11-11
aliases:
  - Property Reference
  - Properties
---
# Note Properties

What every property in the vault means, grouped by area. [[Note Types and Properties]] shows which note types each area covers, and the properties schema lists every allowed value (see [[Schemas and Validation]]).

## Common Properties

Every note has `type`, `created`, and `updated`, and any note may have the rest.

| Property | Meaning |
|---|---|
| `type` | What kind of note this is, which decides its folder and properties |
| `created` | The day the note was created |
| `updated` | The day the note was last edited |
| `aliases` | Other names the note goes by (e.g., `FFT` for Fast Fourier Transform) |
| `tags` | One of the four reserved tags (see [[Tags]]) |
| `claude` | Limits what Claude may do with the note (e.g., `read-only`) |

## Logs

| Property | Used by | Meaning |
|---|---|---|
| `date` | daily, practice, session, meal, log | The day the note records |
| `duration_mins` | practice, session, meal, recipe | How long it took, in minutes |
| `week` | weekly | The week the note covers |
| `month` | monthly, spending | The month the note covers |
| `energy` | daily | How energetic you felt, 1–5 |
| `sleep_hours` | daily | Hours slept the night before |
| `practice_minutes`, `exercise_minutes`, `workouts`, `spending_total` | weekly, monthly | Totals for the period, computed from your logs and never typed |

## Projects

| Property | Used by | Meaning |
|---|---|---|
| `status` | project | Where the project stands (e.g., `active` or `done`) |
| `area` | project | The domain the project serves, so it shows up on that hub |
| `start`, `due` | project | When work began, and the target finish date |
| `outcome` | project | One line on how it ended |

`status` means something different on pieces, trips, recipes, and sources, and each has its own values.

## Music

| Property | Used by | Meaning |
|---|---|---|
| `composers` | piece | Who wrote the piece, then any arrangers |
| `status` | piece | Where the piece is in your repertoire (e.g., `learning` or `repertoire`) |
| `difficulty` | piece, exercise | How hard it is for you |
| `grade` | piece | A grade from an outside syllabus (e.g., ABRSM 8) |
| `started` | piece, book, course | When you started it |
| `last_practiced` | piece | The latest day you practiced it, set from your practice notes |
| `memorized` | piece | Whether you can play it from memory |
| `pieces` | practice | The pieces you worked on |
| `focus` | practice | What the session concentrated on (e.g., `technique`) |
| `category` | technique | What kind of drill it is (e.g., `scales`) |
| `resources` | technique | Material for the drill |
| `styles` | composer | The composer's periods and traditions (e.g., `classical` and `romantic`) |
| `lived` | composer | The years the composer lived |

## Fitness

| Property | Used by | Meaning |
|---|---|---|
| `modality` | routine | How the routine is done (e.g., `running` or `calisthenics`) |
| `goals` | routine | What the routine trains for (e.g., `strength`) |
| `kind` | session | What sort of workout it was |
| `routine` | session | The routine the session followed |
| `muscle_groups` | exercise, routine | The muscles it works |
| `equipment` | exercise | What the exercise needs |
| `last_performed` | exercise | The latest day a session logged it, set from your session notes |
| `pr` | exercise | Your personal record (e.g., `3x25`) |

## Travel

| Property | Used by | Meaning |
|---|---|---|
| `status` | trip | Where the trip stands, from `idea` to `done` |
| `start`, `end` | trip | When you leave and return |
| `places` | trip | The places the trip visits |
| `companions` | trip | Who you're traveling with |
| `budget` | trip, spending | How much you plan to spend |
| `country`, `city` | place | Where the place is |
| `visited`, `first_visit` | place | Whether you've been, and when you first went |
| `rating` | place | How much you liked it |

## Cooking

| Property | Used by | Meaning |
|---|---|---|
| `status` | recipe | Where the recipe stands for you, from `to-try` to `staple` or `retired` |
| `servings` | recipe | How many servings it makes |
| `url` | recipe | The web page the recipe came from |
| `last_cooked` | recipe | The latest day a meal note logged it, set from your meal notes |
| `recipes` | meal | The recipes you made |

## Knowledge

| Property | Used by | Meaning |
|---|---|---|
| `authors` | sources | Who wrote or taught it |
| `year` | sources | When it was published, or when you took the course |
| `fields` | sources, concept | Which fields it belongs to, and so which maps it goes on |
| `field` | map | The one field a map covers |
| `status` | sources | Your reading progress (e.g., `to-read` or `read`) |
| `url` | sources and several other types | The note's web page, and the only place a URL may go |
| `venue` | paper | Where the paper was published |
| `progress`, `finished` | book, course | How far through you are, and when you finished |
| `sources` | concept | The sources you learned the concept from |
| `confidence` | concept | How well you understand it, which only changes when you say so |
| `last_reviewed` | concept | When you last reviewed it |

## Life Admin and References

| Property | Used by | Meaning |
|---|---|---|
| `total` | spending | What you spent that month |
| `review_by` | plan, account, benefit, reference | When to check the note again in case it's out of date |
| `purchased`, `warranty_until` | asset | When you bought it, and when its warranty runs out |
| `manual` | asset | A link to its manual in `98 Attachments/` |
| `topic` | reference | What the reference is about |
| `version` | system, template | The conventions version the note matches |

---
← [[Note Types and Properties]] · Next: [[Tags]] →

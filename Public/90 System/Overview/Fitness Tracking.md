---
type: system
created: 2026-11-08
updated: 2026-11-08
version: "0.29"
aliases:
  - Workout Tracking
---
# Fitness Tracking

The Fitness domain is five kinds of note that feed each other. A routine says what a workout is, [[Weekly Rotation]] says which day gets which routine, a session note logs what you did, and an exercise note shows your progress on one movement over time. Form videos live in `50 References/`. The binding rules are in [[CONVENTIONS]] (section 5). This note explains how the pieces fit.

As an example:

```
Weekly Rotation ──▶ Routine ──Session Template──▶ Session ──▶ Exercise
 which day           what to do                    what you did   Last Time, Sessions,
                                                                  last_performed
                                                                  └──▶ Form video
```

## The Notes

| Note | Type | Lives in | Holds |
|---|---|---|---|
| [[Weekly Rotation]] | `plan` | `20 Hobbies/Fitness/` | Which routine goes on which day, with a goal for each day and overall |
| Routine | `routine` | `Fitness/Routines/` | One workout, named for what it is (e.g., [[Normal Run]]), with Warm-Up, Core Workout, and Cool-Down sections |
| Session | `session` | `Fitness/Sessions/` | One workout you did, named `YYYY-MM-DD Workout`: a table of its Core Workout and a sync button |
| Exercise | `exercise` | `Fitness/Exercises/` | One movement: Last Time, Sessions, Notes, and References sections, plus `muscle_groups`, `equipment`, `difficulty`, `last_performed`, and `pr` |
| Form video | `reference` | `50 References/Exercise Form/` | A YouTube video in `url`, played in the note body (e.g., [[Push-up Form]]) |

- **Routines aren't tied to a day.** A routine is a workout you can do any day, so it's named for the workout, and [[Weekly Rotation]] is the only note that says when.
- **One exercise note per movement.** The same movement in several routines (e.g., a kneeling hip flexor stretch) links to one note, so its history stays in one place. All runs log to [[Run]].
- **Exercise notes hold no copies.** Last Time and Sessions are queries over session notes, so nothing is typed twice.

## Routine Format

The [[Session Template]] reads routines, so every routine follows the [[Routine Template]]:

- **Three sections:** `# Warm-Up`, `# Core Workout`, and `# Cool-Down`. Only the Core Workout goes into session notes.
- **Blocks:** each part of the Core Workout is an H2 (e.g., `## Run` or `## Handstand Push-Up (HSPU) Progression`) ending with a `Sets:` line.
- **One exercise per list item:** a link to the exercise note, then ` — ` and the target (e.g., `- [[Run]] — 10km @ ~7:30/mi pace`).
- **Progressions:** the tiers are numbered, and the one you're on is highlighted (e.g., `1. ==[[Push-up|Push-ups]] — 3x20==`). Only the highlighted tier goes into session notes. To move up a tier, move the highlight.

## Logging a Workout

1. **Create the session note** with the [[Session Template]] and pick its routine. [[Session Table]] writes the table from the routine's Core Workout, with Exercise, Target, and Sets filled in.
2. **Fill in each row** as you go. Reps/Time/Distance is how much (e.g., `20, 18, 15`, `45s`, or `10 km`), and Weight/Pace is how hard (e.g., `185 lb` or `7:28/mi`). A row you skip can stay empty, since only filled rows count.
3. **Press Sync Last Performed** at the end of the note. It moves each logged exercise's `last_performed` forward to the session's date.
4. **Open an exercise** to see Last Time (your sets from the latest session that logged it) and Sessions (every session that lists it).

## What Fills What

| What | Filled by | When |
|---|---|---|
| Session Exercise, Target, and Sets | [[Session Table]], from the routine | When the session note is created |
| Exercise Last Time | `90 System/Scripts/last-time.js` (Dataview) | Every time the exercise note opens |
| Exercise Sessions | The Sessions view of `Exercise.base` | Every time the exercise note opens |
| `last_performed` | [[Sync Last Performed]], from the session's button | When you press it, or run the automation |
| Form video player | `90 System/Scripts/form-video.js` (Dataview), from `url` | Every time the reference note opens |
| `muscle_groups`, `equipment`, `difficulty`, `pr` | You | By hand |

The scripts in `90 System/Scripts/` run through Dataview, the button through Meta Bind, and the templates through Templater (see [[Vault Plugins]] and [[Vault Templates]]).

## Known Limits

- **Videos don't play on iPhone or iPad.** YouTube blocks embedded players there, so each form video also shows a plain link.
- **Sync is a button, not a trigger.** Templater can't react to edits, so `last_performed` only moves when you press the button or run [[Sync Last Performed]].
- **Routines with nothing linked give an empty table.** An unlinked item (e.g., plain text with no `[[…]]`) isn't picked up, so keep to the [[Routine Template]] format.

---
← [[Everyday Lists]] · Next: [[Schemas and Validation]] →

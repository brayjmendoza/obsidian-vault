---
type: documentation
created: 2026-11-08
updated: 2026-11-08
aliases:
  - Fitness Tracking
---
The Fitness domain tracks your workouts: routines say what to do, [[Weekly Rotation]] says when, session notes log what you did, and exercise notes show your progress on each movement. 

```
Weekly Rotation ──▶ Routine ──▶ Session ──▶ Exercise ──▶ Form video
 which day          what to do   what you did  your progress  how to do it
```

## The Notes

| Note | What it's for |
|---|---|
| Weekly Rotation | Which routine goes on which day |
| Routines | One workout each, named for what it is rather than the day (e.g., [[Normal Run]]) |
| Sessions | One workout you did, logged against its routine |
| Exercises | One movement each, with your latest sets, the sessions that logged it, and your personal record |
| Form videos | Reference notes in `50 References/` that play a how-to video (e.g., [[Push-up Form]]) |

- **One note per movement:** the same exercise in several routines links to one note, so its history stays in one place.
- **Nothing is typed twice:** an exercise's latest sets and its list of sessions are live views of your session notes.
- **Progressions:** a routine can hold tiers of an exercise, with the one you're on highlighted. To move up a tier, move the highlight.

## Logging a Workout

1. Press **Start Session** at the top of the routine. It creates a session note from the [[Session Template]] with the routine and its kind already filled in, asks for the date, and fills the table with the routine's exercises and targets.
2. Fill in what you did as you go.
3. Press the [[Sync Last Performed]] button at the end, which moves each exercise's `last_performed` to that day.

Open an exercise afterward to see the sets you just logged.

## Known Limits

- **Videos don't play on iPhone or iPad,** so each form video also shows a plain link.
- **Sync is a button, not a trigger:** `last_performed` moves only when you press it.
- **Only linked exercises reach a session:** an item without a link isn't picked up, so keep routines to the [[Routine Template]].

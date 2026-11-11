---
type: documentation
created: 2026-10-25
updated: 2026-11-11
---
# Everyday Lists

Three living lists never finish. A schedule and a wishlist are plan notes, which you keep following, and small to-dos are a task note, which you keep ticking off (see [[Domain Skeleton#Roles|Roles]]).

| List | Lives in | What it's for |
|---|---|---|
| Schedule | Planning | What you do each day and week. daily-note copies today's items into the daily note |
| Wishlist | Finance | Things to buy. spending-import can flag one when it shows up in a statement |
| To-Do's | Any domain (e.g., Planning) | Small tasks. daily-note lists the open and due ones |

The skills are described in [[Claude Skills]].

- **Schedule, not Routine:** a routine is a workout, so the schedule links to [[Weekly Rotation]] rather than repeating it.
- **Pieces stay pieces:** a piece you want to learn is a piece note with `status: wishlist`, so the Wishlist is only for things to buy.
- **One To-Do's per domain:** a `task` note at the domain's root, beside the hub. The hub's Add Task button adds to it, and the hub's Tasks view lists its open tasks.
- **Priority and dates live in the task:** the Tasks plugin keeps them on each task's line, so a task note has no properties of its own.
- **Tasks can still live anywhere:** a task tied to a project can sit in that note, and the to-do queries still find it. Claude never ticks a task off for you (see [[Claude Guardrails]]).

---
← [[Tags]] · Next: [[Schemas and Validation]] →

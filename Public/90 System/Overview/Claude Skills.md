---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Claude Skills

Ten skills, built in priority order (see [[Vault Rollout]]). All of them read [[CONVENTIONS]] and the schemas first, follow the [[Claude Guardrails]], and log to the [[changelog]].

| # | Skill | What it does | Cadence |
|---|---|---|---|
| 1 | vault-conventions | Loads the conventions and schemas for every other skill | Always |
| 2 | daily-note | Writes today's note: the schedule, open tasks, and due items (see [[Everyday Lists]]) | Daily, scheduled |
| 3 | inbox-triage | Turns captures into finished notes in the right folder (see [[Folder Structure#Placement Rules\|Placement Rules]] and [[Tags]]). Asks when unsure | Daily or on demand |
| 4 | recall | Answers questions from the vault, citing notes | On demand |
| 5 | weekly-review | Writes the weekly note, summing up the days, practice, workouts, and spending | Weekly, scheduled |
| 6 | ingest-source | Paper or chapter → source note, concept notes, and map links (see [[Knowledge Structure#The Learning Loop\|The Learning Loop]]) | On demand |
| 7 | hobby planners | Plans practice, workouts, and trips, and writes up trips afterward | Weekly or on demand |
| 8 | spending-import | Bank CSV → categorized monthly spending note | Monthly |
| 9 | quiz-me | Spaced review of concepts you know least or haven't seen lately | On demand |
| 10 | vault-health | Finds broken links, orphans, stale statuses, and duplicate copies (see [[Sync and Backup#Conflicts and Backup\|Conflicts and Backup]]). Fixes only with approval | Monthly, scheduled |

---
← [[Sync and Backup]] · Next: [[Vault Rollout]] →

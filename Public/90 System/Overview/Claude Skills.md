---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.12"
---
# Claude Skills

Ten skills, built in priority order (see [[Vault Rollout]]). All of them read [[CONVENTIONS]] and both schemas first, follow the [[Claude Guardrails]], and log to the [[changelog]].

| #   | Skill             | What it does                                                                                                                                                                                                                                               | Cadence            |
| --- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| 1   | vault-conventions | Loads CONVENTIONS.md and all schemas for every other skill                                                                                                                                                                                                 | Always             |
| 2   | daily-note        | Generates today's note in full: today's schedule, carries over open tasks, lists due items (see [[Everyday Lists]])                                                                                                                                        | Daily, scheduled   |
| 3   | inbox-triage      | Turns captures in `00 Inbox/` and notes tagged `#inbox` elsewhere into finished, typed notes in the right folder (see [[Folder Structure#Placement Rules\|Placement Rules]] & [[Tags]]); asks when unsure                                                  | Daily or on demand |
| 4   | recall            | Answers questions from the vault, citing notes                                                                                                                                                                                                             | On demand          |
| 5   | weekly-review     | Summarizes dailies, practice, workouts, spending; generates the weekly note in full                                                                                                                                                                        | Weekly, scheduled  |
| 6   | ingest-source     | Paper or chapter → source note + concept notes + map links (see [[Knowledge Structure#The Learning Loop\|The Learning Loop]])                                                                                                                              | On demand          |
| 7   | hobby planners    | Piano practice rotation, next week's workout, trip itinerary, and post-trip write-up                                                                                                                                                                       | Weekly / on demand |
| 8   | spending-import   | Bank CSV → categorized monthly spending note                                                                                                                                                                                                               | Monthly            |
| 9   | quiz-me           | Spaced review of low-confidence or stale concepts                                                                                                                                                                                                          | On demand          |
| 10  | vault-health      | Runs `vault-validate` and reads the latest CI results (see [[Schemas and Validation]]); finds broken links, orphans, stale statuses, and iCloud duplicate copies (see [[Sync and Backup#Conflicts and Backup\|Conflicts and Backup]]); fixes only with approval | Monthly, scheduled |

---
← [[Sync and Backup]] · Next: [[Vault Rollout]] →

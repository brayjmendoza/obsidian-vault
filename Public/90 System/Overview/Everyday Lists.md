---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.6"
---
# Everyday Lists

Three living lists — a schedule, a wishlist, and small to-dos — are plan notes (see [[Domain Skeleton#Roles|Roles]]): you keep following them, and they never finish. Each of them has the note type `plan`.

| Note                      | Path                                 | Format                                                                                                    | How skills use it                                                                                       |
| ------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Daily and weekly schedule | `30 Life Admin/Planning/Schedule.md` | A weekday table, or recurring tasks (`- [ ] Practice piano 🔁 every day`) if you want to tick habits off  | daily-note copies today's items into the daily note; weekly-review compares the plan with what happened |
| Wishlist                  | `30 Life Admin/Finance/Wishlist.md`  | Table: Item, Category, Est. price (USD), Priority, Link. Category uses the `spending_category` vocabulary | spending-import can flag a wishlist item when it shows up in a statement                                |
| Small to-dos              | `30 Life Admin/Planning/To-dos.md`   | Tasks, due date optional: `- [ ] Return library book 📅 2026-10-30`                                       | daily-note lists open and due items with a Tasks query                                                  |

The skills named here are described in [[Claude Skills]].

- **Planning domain:** band folders hold only domains, so Schedule and To-dos live in `30 Life Admin/Planning/`, with hub `Planning.md`.
- **Type:** all three use the `plan` type (see [[Note Types and Properties]]).
- **Naming:** it is Schedule, not Routine. `routine` is the weekly fitness plan; Schedule.md links to the current fitness routine rather than repeating it.
- **Not on the wishlist:** pieces you want to learn stay as `piece` notes with `status: wishlist`. `Wishlist.md` is for things to buy.
- **To-dos with a home:** a task tied to a domain or project (fix the faucet → Home) can live in that note instead; the Tasks query finds it anywhere. To-dos.md is the catch-all, and Claude never ticks a task off for you (see [[Claude Guardrails]]).

---
← [[Tags]] · Next: [[Schemas and Validation]] →

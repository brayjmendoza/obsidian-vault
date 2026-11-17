---
name: quiz-me
description: Quiz Brayden on concepts in his Obsidian vault that he knows least or hasn't reviewed in a month, about 15 minutes at a time, then update each quizzed concept's confidence and last_reviewed. Use when asked to quiz, review concepts, or run quiz-me, daily or on demand.
---

# Quiz Me

Spaced review of the concepts in `40 Knowledge/Concepts/` that Brayden knows least or hasn't reviewed lately. One run is a quiz that takes at most 15 minutes. It asks one question per concept, grades each answer against the concept note, and finishes by updating `confidence` and `last_reviewed`. CONVENTIONS lets a skill change `confidence` only when its instructions explicitly allow it, and this skill allows it, in step 6, once Brayden confirms.

## 1. Start

1. Run the vault-conventions skill. It loads CONVENTIONS and the schemas, and it defines how this run closes. This run edits only properties, so STYLE isn't needed.
2. Read any arguments. Each one is optional:
   - **Time or count** (e.g., "30 min" or "12 questions"): replaces the 15-minute budget.
   - **Focus** (e.g., a map name, a map section, or a field): limits the candidates to it.
   - **"Include today's":** keeps concepts already reviewed today (see step 2).

## 2. Find the Candidates

- **Scope (pilot):** for now, only the concepts linked from the [[Programming Languages]] map in `40 Knowledge/Maps/`. Collect every `[[…]]` link in its body, drop any `|alias` or `#heading` part, and resolve each link to a note in `40 Knowledge/Concepts/` by filename or alias. Once the pilot ends, the scope becomes every concept note.
- **Candidate:** a concept with `confidence` ≤ 3, or with `last_reviewed` more than 30 days before today.
- **Skip today's:** leave out concepts whose `last_reviewed` is today, so a second run on the same day brings up new concepts. Keep them only when Brayden asks.
- **No candidates:** say so, and offer a quiz on the oldest-reviewed concepts instead.

## 3. Pick the Quiz

- **Budget:** about two minutes per question, so 15 minutes holds 7 questions. A worked problem (e.g., a reduction or an evaluation by hand) counts as two. Scale the count to the time or count Brayden gave.
- **Priority:** lower `confidence` first, then older `last_reviewed`.
- **Spread:** pick round-robin across groups so the quiz covers as many groups as it can. Group by `fields` first. When every candidate shares a field (as in the pilot), group by the H1 section of the map that links the concept (e.g., Types, Parsing, and Lambda Calculus). Within a group, take the highest-priority concept that's still unpicked.
- **Order:** mix the groups rather than asking one section's questions back to back.

Don't show the list before starting. Say how many questions there are and roughly how long they'll take, then ask the first question.

## 4. Write the Questions

Read each picked concept's note in full before writing its question. A question tests what the note teaches, so it can be graded against the note. That means its definitions, its sources' material, and its Example section.

- **Kinds:** vary them across the quiz:
  - **Explain:** say what it is and why it exists (e.g., "What problem does a closure solve in an environment-based interpreter?").
  - **Predict:** give a small expression or program and ask for its result (e.g., what a Haskell expression evaluates to).
  - **Apply:** do a small step by hand (e.g., one beta reduction, or rewriting a left-recursive rule).
  - **Compare:** tell it apart from a nearby concept the note links in Connections.
  - **Spot the error:** give a short wrong claim or buggy code and ask what's wrong.
- **Match the level:** at `confidence` 1–2, prefer Explain and Compare. At 3 and above, prefer Predict, Apply, and Spot the Error.
- **One idea per question.** Small enough to answer in a minute or two, with no answer hidden in its wording.
- **Use the note's language and notation** (e.g., Haskell and [[Arith]] for the Programming Languages concepts).

## 5. Run the Quiz

- **One question per message.** Number it (e.g., "3/7") and name its map section, but not the concept when the name gives the answer away. Then wait for the answer.
- **After each answer:** give a verdict (i.e., correct, partial, or missed), then two to four sentences that fix or complete the answer, linking the concept note (or the section that covers the point). Then ask the next question in the same message.
- **"Hint":** give one hint. An answer after a hint is rated 3 at most.
- **"Skip":** move on. A skipped concept isn't graded or updated.
- **"I don't know":** a miss, rated 1. Give the answer.
- **"Stop":** end the quiz, and grade what was answered.
- **Note problems:** if an answer exposes a gap or an error in the note itself, say so and list it in the report. Don't edit the note's body.

## 6. Rate and Update

Rate each answered concept on this scale, from that answer alone:

| Rating | The answer |
|---|---|
| 1 | Couldn't recall the idea, or got its core wrong |
| 2 | Recognized it, but was vague or had a major error |
| 3 | Got the core idea right, with gaps or minor errors |
| 4 | Was correct and complete, and applied the idea to the example or problem |
| 5 | Was correct, complete, and fluent: covered an edge case or a connection without prompting |

- **New `confidence`:** if the rating is higher than the current `confidence`, add 1, since one good answer isn't mastery. Otherwise use the rating.
- **Confirm:** show a table of each concept (as a link), its verdict, and its old → new `confidence`. Ask Brayden to confirm or adjust. His numbers win.
- **Write:** on every graded concept, set `confidence`, set `last_reviewed` and `updated` to today, and change nothing else. Edit the frontmatter in place (e.g., `sed -i` on just those lines), never by retyping the file.
- **No answer to the confirmation** (e.g., an unattended run): write nothing, and report the proposed table.

## 7. Close

Close the run as vault-conventions says. The changelog line names the concepts quizzed with their old → new `confidence` (e.g., `- 2026-11-17 08:10 · quiz-me · 7 concepts: [[Closure (Programming Languages)]] 2 → 3, …`). The report lists any note problems from step 5.

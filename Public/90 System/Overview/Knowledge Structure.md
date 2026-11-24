---
type: documentation
created: 2026-10-25
updated: 2026-11-24
aliases:
  - Knowledge layer
  - How 40 Knowledge works
---
# Knowledge Structure

`40 Knowledge/` holds what you've learned. Unlike the domains, it isn't organized by topic folders: its folders sort notes by kind, and links organize them by subject. The binding rules are in [[CONVENTIONS]], and each kind of note starts from its own template (see [[Vault Templates]]).

## Why Links Instead of Folders

A folder gives a note one home, but ideas belong to several fields at once. The Fourier transform is math, physics, and music theory. Put it in one field's folder and the others lose it. Copy it into all three and the copies drift apart, which breaks [[Vault Principles|link, don't duplicate]]. So every idea is stored once, and maps link to it from every field it belongs to.

## The Three Kinds

```
Source ──key ideas──▶ Concept ◀──listed on── Map ◀── Domain hub
```

- **Sources:** one note per paper, book, course, or article. Each records what the source says, and their statuses double as a reading list.
- **Concepts:** one idea per note, kept small so it's easy to link to, review, and place on several maps.
- **Maps:** one per field, curated by hand. A map lists its concepts in learning order, so it doubles as a study path, and a section that grows large becomes its own sub-map.

Every concept appears on at least one map, so nothing is unreachable. Fields are a fixed list, and adding one needs your approval (see [[Claude Guardrails]]).

## How Knowledge Connects to the Rest of the Vault

- **From domains:** a hub links to the maps behind it, so the Music hub reaches music theory without copying it (see [[Domain Skeleton#What Stays Out of a Domain|What Stays Out of a Domain]]).
- **Knowledge or References:** ask whether you want to *understand* it or just *look it up*. Understanding goes in a concept, by way of a source, and a how-to or cheat sheet goes in `50 References/` (see [[#Sources or References]]).
- **Running examples:** an example that several concepts build on (e.g., [[Arith]]) is a reference in `51 Examples/`. It holds the whole example once, and each concept links to it.
- **Learning goals with a deadline:** "finish this course by June" is a project that links to the course note.

## Sources or References

A source and a reference can both come from a book or a web page, so the test is what the note is for. A **source** records something you read or watched, so its ideas can be pulled out into concepts. A **reference** is what you come back to look up, and the answer is in the note itself.

| | Source | Reference |
|---|---|---|
| Holds | What a paper, book, course, or article says | A how-to, cheat sheet, table, or bookmarked tool |
| Lives in | `40 Knowledge/Sources/`, sorted by kind | `50 References/`, sorted by topic |
| Tracks | Your reading, with `status` | When to check it again, with `review_by` |
| Leads to | A concept for each key idea | Nothing further, though it can link to the concept that explains it |

As an example:

| Note | Goes in | Why |
|---|---|---|
| Attention Is All You Need (Vaswani 2017) | Sources | Read to understand, and its key ideas become concepts (e.g., self-attention) |
| Gödel, Escher, Bach with `status: to-read` | Sources | On your reading list, with nothing to look up yet |
| [[uv Documentation\|The uv docs]] | Sources | Read to learn how uv works, and it feeds the [[uv]] concept |
| A git command cheat sheet | References | Opened for one command, then closed |
| Deadlift form cues | References | A how-to. Your working weights stay in the exercise note |
| A key signature chart | References | A look-up. Why the circle of fifths works belongs in a music theory concept |

One topic often lands in all three places. Reading Boas's Mathematical Methods gives a book source, the Fourier transform becomes a concept, and a table of transform pairs you keep checking goes in `50 References/`, linked to the concept. A web page can go either way: read it to learn and it's an article source, or bookmark it to look something up and it's a reference with the page in `url`.

## The Learning Loop

Two skills work on this band (see [[Claude Skills]]):

- **ingest-source** turns a paper or chapter into a source note, concept notes for its key ideas, and links from the right maps.
- **quiz-me** quizzes you on the concepts you know least or haven't reviewed lately.

Claude never changes how confident you are in a concept unless you say so (see [[Claude Guardrails]]).

---
← [[Domain Skeleton]] · Next: [[Note Types and Properties]] →

---
type: system
created: 2026-10-25
updated: 2026-11-01
version: "0.6"
aliases: [Knowledge layer, How 40 Knowledge works]
---
# Knowledge Structure

`40 Knowledge/` holds what you have learned. Unlike the domains in [[Domain Skeleton|Hobbies and Life Admin]], it is not organized by topic folders. Its folders sort notes by **what kind of note** they are, and **links** organize them by subject. This page explains why, and how the three kinds of knowledge note fit together. The binding rules for note bodies are in [[CONVENTIONS]] (section 5). The properties are in [[Note Types and Properties]].

## Why Links Instead of Folders

A folder gives a note exactly one home, but ideas belong to several fields at once. The Fourier transform is an interdisciplinary concept that belongs in math, physics, and music theory. Put it in `Math/` and the physics and music theory views lose it. Copy it into all three and you have three versions drifting apart, which breaks [[Vault Principles|link, don't duplicate]].

So, the knowledge band separates two things a folder tree mixes together:

- **Storage:** every concept sits once, in one flat folder: `Concepts/`. You never have to decide which field "owns" it.
- **Navigation:** maps are hand-written tables of contents that link to concepts. A concept can appear on as many maps as it belongs to, and each map can order it differently.

The `fields` property ties the two together: a note's fields say which maps it belongs in, so a Bases view or a Claude skill can find concepts that are missing from a map they should be on.

## The Three Layers

```
40 Knowledge/
├── Sources/      where you learned it   Papers/, Books/, Courses/, Articles/
├── Concepts/     what you learned       one idea per note, flat
└── Maps/         how it fits together   one map per field, plus sub-maps
```

```
 Source ──key ideas──▶ Concept ◀──listed on── Map ◀──Links── Domain hub
   ▲                     │  ▲
   └──── sources ────────┘  └── Connections ──▶ other concepts
```

### Sources

One note per thing you read or watched, in the subfolder for its kind. Each kind has its own type and filename pattern:

| Type | Folder | Filename | Required properties |
|---|---|---|---|
| paper | `Sources/Papers/` | `Author Year - Title` | authors, year, fields, status |
| book | `Sources/Books/` | `Title (Author)` | authors, fields, status |
| course | `Sources/Courses/` | `Title (Provider)` | authors, fields, status |
| article | `Sources/Articles/` | plain title | url |

`status` tracks your reading: `to-read`, `reading`, `read`, or `abandoned`. That makes the Sources folders double as a reading list.

A source note's body holds a **summary**, the **key ideas** (each one linking to a concept note), **open questions**, and **short quotes** with a page or section reference. The source note is a record of the source itself. The ideas get pulled out into concepts, so they can be reused beyond the one source.

### Concepts

One idea per note, named with its full title (`Fast Fourier Transform`, with `FFT` as an alias). The body always has the same shape:

1. A one-sentence definition
2. An explanation
3. An example
4. `## Connections`: links to related concepts, with a few words on how they relate
5. `## Sources`: where you learned it

Note properties: `fields` (a list, since one concept can belong to several fields), `sources` (links to source notes), and two for review: `confidence` (1–5, how well you know it) and `last_reviewed`.

Concepts are kept small on purpose. A small note is easy to link to precisely, easy to quiz yourself on, and easy to place on more than one map. If a note starts explaining two ideas, split it and link the two.

### Maps

One map per field, named `<Field>` (e.g., `Physics`), with `field` set to a single value. A map is curated by hand rather than generated, because the value is in the ordering and the commentary:

- Headings for subtopics (e.g., Classical Mechanics, Waves, Quantum Mechanics)
- Under each, links to concepts **in learning order**, so the map doubles as a study path
- A few words on how ideas connect ("reformulation of Newton; start after it")

When one section of a map grows too large, it becomes its own **sub-map** (e.g., `Quantum Mechanics`), and the parent map links to it in place of the section. Sub-maps keep the `field` of their parent. Every concept appears on at least one map, so nothing in `Concepts/` is unreachable.

## Fields

Fields are a fixed vocabulary (e.g., `computer-science`, `math`, `physics`, `music-theory`, etc.). Concepts and sources carry `fields` (a list); maps carry `field` (one value). Adding a field means adding it to the vocabulary in `properties-schema.yaml`, which needs your approval, then creating its map (see [[Schemas and Validation]]).

## How Knowledge Connects to the Rest of the Vault

- **From domains:** each domain hub's `## Links` section links to the relevant maps (the Music hub links to the music theory map; Fitness could link to a training-science sub-map). Domains hold your own doing; knowledge holds the understanding behind it (see [[Domain Skeleton#What Stays Out of a Domain|What Stays Out of a Domain]]).
- **Knowledge versus References:** ask whether you want to *understand* it or just *look it up* when needed. Understanding goes in a concept. A how-to, cheat sheet, or table goes in `50 References/`. A reference can link to the concept that explains why it works.
- **Learning goals with a deadline:** "finish this course by June" is a project in `10 Projects/` that links to the course note. The course note stays the record of the source.

## The Learning Loop

Two skills (see [[Claude Skills]]) work on this band:

1. **ingest-source:** you give it a paper or chapter. It writes the source note, creates or updates a concept note for each key idea, and adds new concepts to the right maps.
2. **quiz-me:** picks concepts with low `confidence` or an old `last_reviewed` and quizzes you on them.

Claude never changes `confidence` on its own (see [[Claude Guardrails]]). It updates only when you report how a review went, or when a skill's instructions explicitly allow it.

## Worked Example

You read a chapter on Fourier analysis:

1. The chapter becomes a book note, `Sources/Books/Mathematical Methods (Boas).md`, with `status: reading`.
2. Its key idea becomes `Concepts/Fourier Transform.md`, with `fields: [math, physics, music-theory]` and `sources: ["[[Mathematical Methods (Boas)]]"]`. Its Connections section links to Wave Equation and Harmonic Oscillator.
3. It is listed under Analysis on the math map, under Waves on the physics map, and under Timbre on the music theory map. Each map says something different about why it matters there.
4. The Music hub already links to Music Theory Map, so the idea is reachable from your piano hobby without being copied into the Music folder.

---
← [[Domain Skeleton]] · Next: [[Note Types and Properties]] →

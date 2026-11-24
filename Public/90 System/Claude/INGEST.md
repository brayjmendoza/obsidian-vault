---
type: system
created: 2026-11-15
updated: 2026-11-24
version: "1.11"
---
# Ingest Guide

What the ingest-source skill does differently for each kind of source and each field. The skill holds the steps that never change, and this file holds the specifics. [[CONVENTIONS]], the schemas, and [[STYLE]] win over both.

Sections marked **Draft** haven't been used on a real source yet. The first run that uses one confirms or fixes it, and then removes the mark. A kind of source or a field with no section here gets one at the end of its first run (see [[#Changelog]]).

## The Generality Test

Every run sorts what it reads into concepts and references:

- **Concept:** an idea that stays the same whichever tool, notation, language, or example presents it. Another source on the same subject would teach the same idea.
- **Reference:** material tied to one tool, language, or product, or something you look up rather than understand (e.g., syntax, tables, constants, how-tos, and recommendations).

Each field section below gives this test in its own terms.

## Names

- **Concepts take the field's standard term,** even when the source uses another, and the source's terms go in `aliases` (e.g., Algebraic Data Type, with the alias Data Type).
- **A term another subject also uses gets its area in parentheses** (e.g., `Closure (Programming Languages)`, since math has its own closures, and `Monad (Functional Programming)`, since philosophy has its own monads). The bare term goes in `aliases`. Check for a clash across every field, not just the one being ingested.

## Kinds of Source

### Courses

Tested on CS 131.

- **Source note:** `course` in `40 Knowledge/Sources/Courses/`, named `<Title> (<School> <Course Number>)` (e.g., `Programming Languages (HMC CS131)`). `authors` are the instructors, and `year` is when you took it.
- **Unit:** one module or week.
- **Inputs:** lecture slides (often annotated), instructor summaries, your handwritten notes.
- **Trust:** slides first, then instructor summaries, then your handwriting. Check all of them: CS 131's slides and summaries both had errors.
- **Key Ideas:** one section per unit, `## Module N: Title`.
- **Leave out:** logistics, homework instructions, and announcements.
- **Units follow the lecture numbering,** not the folders. A folder can hold slides for more than one lecture (e.g., CS 131's Module 4 folder held 4.1 and 4.2, and its summaries put environments in 5.1, the next unit).
- **Formulas on slides are often images,** with no text to extract. Render those pages at about 90 dpi, so subscripts and symbols are legible, and write the formulas in LaTeX (e.g., CS 131's typing rules).
- **Concepts don't mention the course.** The course's running examples appear by name instead (e.g., [[Arith]], the small language CS 131 builds an interpreter for), and a broken slide example is written correctly and reported.
- **Notes with no lecture numbering are split by topic.** When the material has no modules or weeks (e.g., the CS 70 archive), agree with you on topic units in the course's order before the first run, record them in the source note's Summary, and title each section `## Unit N: Title`.
- **Running examples get a reference** in `51 Examples/`, named for the example, that holds the whole example in one place: what it is, how it grows unit by unit, and its latest version. Each unit that extends the example updates the reference, and every concept that uses it links to the reference at its first mention.

### Books

**Draft.**

- **Source note:** `book` in `40 Knowledge/Sources/Books/`, named `<Title> (<Author Surname>)` (e.g., `Mathematical Methods in the Physical Sciences (Boas)`).
- **Unit:** one chapter, or one section of a long chapter.
- **Progress:** `status: reading` until you finish, with `progress` (e.g., `Chapter 4`), `started`, and `finished`. Claude sets `progress` only to the unit it just ingested.
- **Extract:** ask for the chapter's page range, then extract that range.
- **Key Ideas:** one section per unit, `## Chapter N: Title`.

### Papers

**Draft.**

- **Source note:** `paper` in `40 Knowledge/Sources/Papers/`, named `<First Author Surname> <Year> - <Title>`, with `authors`, `year`, and, where known, `venue` and `url`.
- **Unit:** one paper. A series of papers gets one source note each.
- **Claims are attributed** (e.g., "Smith and Jones show…"). When papers disagree, the concept states each position with its source rather than choosing one.
- **Key Ideas:** no unit sections.

### Articles and Websites

**Draft.** [[uv Documentation]] is the model.

- **Source note:** `article` in `40 Knowledge/Sources/Articles/`, with `url` and `year`.
- **Unit:** one article. Several pages of one site's documentation can share one note, with the pages as Markdown links in the body.
- **Extract:** WebFetch. If a site can't be reached, ask you for a PDF or a saved copy of the page instead of working around the block.

### Handwritten Notes

Tested on CS 131's annotations.

- **Not a source of their own.** Handwritten notes belong to the course, book, or paper they were taken from. If there isn't one, ask which source note they go with.
- **Extract:** GoodNotes exports carry the handwriting as text. Look at a page as an image only when its text is junk or empty.

### Old Obsidian Notes

Tested on the CS 131 and CS 70 archives.

- **Cross-check only.** They fill gaps and confirm the main material, but they can be wrong.
- **Unless they're all there is.** When old notes are the only material for a source (e.g., CS 70), they're the main input. Check every claim and example against what's actually true, since nothing else will catch their mistakes: CS 70's notes had a wrong primality loop, a wrong `double` precision, and a mislabeled bug.
- **They stay where they are,** in `99 Archive/`, and new notes never link to them.

## Fields

A concept from another field gets that field too (e.g., Russell's Paradox, met in a programming languages course, has `fields: [math, computer-science]`). It goes on the map of the source being ingested, and the other field's map lists it as unmapped until a run there places it.

### Computer Science

Tested on CS 131 (i.e., programming languages).

- **The test:** a concept's definition would stay the same with examples from another language. Syntax, commands, and library functions go in `50 References/<Language>/` (e.g., `50 References/Haskell/`).
- **Map:** [[Computer Science]], with a sub-map per area (e.g., [[Programming Languages]]). Data structures and their analysis go on [[Data Structures and Algorithms]], language features for memory (e.g., pointers and object lifetime) go in [[Programming Languages]]'s Memory section, building and testing programs goes on [[Software Engineering]], and how data is stored in bits (e.g., [[Floating-Point Arithmetic]]) goes in Computer Science's Data Representation section.
- **Tools outside one language** get their own reference folder, named for the tool (e.g., `50 References/Git/`). Make stays with the language it builds (e.g., [[Makefiles]] in `50 References/C++/`). Look-up tables about algorithms in general go in `50 References/Algorithms/` (e.g., [[Orders of Complexity]]).
- **Asymptotic notation is math too,** so [[Asymptotic Analysis]] has `fields: [computer-science, math]`. Concepts that only apply it (e.g., [[Amortized Analysis]]) stay `computer-science`.
- **Examples:** in the source's language. Other languages go in the "More generally," paragraph.
- **Visuals:** code blocks, Mermaid for trees and pipelines, and math for typing rules.
- **Pitfalls:** recheck every example's result by hand.

### Math

**Draft.**

- **The test:** definitions, theorems, and techniques are concepts. Tables (e.g., of integrals or identities) and notation guides are references.
- **Theorems state their hypotheses,** and a proof idea goes in the concept when the source gives one.
- **Visuals:** LaTeX for everything mathematical, inline (`$…$`) or as blocks (`$$…$$`).
- **Examples:** a worked problem from the source.

### Physics

**Draft.**

- **The test:** laws, principles, and models are concepts, each with the limits where it holds. Constants, unit conversions, and formula sheets are references.
- **Visuals:** LaTeX with units. A figure Mermaid can't draw is cropped into `98 Attachments/`.

### Music Theory

**Draft.**

- **The test:** harmonic functions, forms, and voice-leading principles are concepts. Charts of keys, intervals, or scales are references.
- **Notation:** note names, Roman numerals, and chord symbols in text. Obsidian can't render a staff, so a passage of notation is cropped into `98 Attachments/`.
- **Hobbies stay separate.** Piece and practice notes in `20 Hobbies/Music/` can link to concepts, but concepts never hold practice material.

### Philosophy and the Humanities

**Draft.**

- **The test:** ideas, arguments, and movements are concepts. Timelines and glossaries are references.
- **Positions are attributed** (e.g., "Kant argues…"). A contested question gets each side, with who holds it.
- **Fields:** only `philosophy` is in the `field` vocabulary. Another humanities field needs your approval for a schema change first.


## Changelog

- 2026-11-24 · 1.11 · Running examples get their reference in `51 Examples/`, not `50 References/Examples/`.
- 2026-11-24 · 1.10 · From CS 70, Unit 5: algorithm look-up tables go in `50 References/Algorithms/`, and asymptotic notation also counts as math.
- 2026-11-23 · 1.9 · From CS 70, Unit 2: computer science adds the [[Data Structures and Algorithms]] sub-map, and memory concepts go in [[Programming Languages]]'s Memory section.
- 2026-11-23 · 1.8 · From CS 70, Unit 1: courses without lecture numbering are split into topic units, titled `## Unit N: Title`. Old Obsidian notes that are a source's only material are its main input. Computer science adds the [[Software Engineering]] sub-map, the Data Representation section, and reference folders for tools outside one language.

- 2026-11-16 · 1.7 · Courses: running examples get a reference in `50 References/Examples/` (e.g., [[Arith]]). The Names example for a shared term is now Monad, since Map and Filter merged into Higher-Order Function.
- 2026-11-15 · 1.6 · Fields: a concept from another field also lists that field.
- 2026-11-15 · 1.5 · Courses: formulas that are images on slides are rendered at about 90 dpi and rewritten in LaTeX.
- 2026-11-15 · 1.4 · The rule for names shared with other subjects moved from Computer Science to a new general Names section, which also restates the standard-term rule.
- 2026-11-15 · 1.3 · Computer science: terms shared with other fields get the area in parentheses.
- 2026-11-15 · 1.2 · Courses: units follow the lecture numbering rather than the folders, and concepts name the course's examples instead of the course.
- 2026-11-15 · 1.1 · Dataview's inline query prefixes are now "dv:" and "dvjs:", so computer science notes no longer avoid inline code starting with `=`.
- 2026-11-15 · 1.0 · First version, from the CS 131 pilots (Modules 2 and 3). Courses, handwritten notes, old Obsidian notes, and computer science are tested. The rest are drafts.

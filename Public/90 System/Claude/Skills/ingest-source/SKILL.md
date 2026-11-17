---
name: ingest-source
description: Turn learning material from any field (course notes, slides, handwritten notes, textbook chapters, papers, articles, or websites) into source, concept, reference, and map notes in Brayden's Obsidian vault. Use when asked to ingest, import, or make notes from a source.
---

# Ingest Source

Turns one **unit** of a source (e.g., a course module, a book chapter, a paper, or an article) into notes in `40 Knowledge/` and `50 References/`. One unit per run, so each is read closely, and the source note shows which units are done.

This skill holds the steps. `90 System/Claude/INGEST.md` holds what varies: a section for each kind of source (e.g., where its source note goes and what a unit is) and each field (e.g., what counts as a concept, and how ideas are shown). Each run follows the sections that match, and adds to INGEST.md when it makes a call no section covers.

## 1. Start

1. Run the vault-conventions skill. It loads CONVENTIONS, the schemas, and STYLE, and it defines how this run closes.
2. Read `90 System/Claude/INGEST.md`, and the templates for the types this run writes: Concept, the source's type with `Includes/Source Body`, Map, and Reference.

## 2. Identify the Source and Unit

- **The source:** a course, a book, a paper, an article or website, or one of a series. Each gets its own source note. Handwritten and old Obsidian notes belong to the source they were taken from.
- **The unit:** as INGEST.md defines it for this kind of source.
- **The field:** it picks the map, and the INGEST.md section to follow. A field missing from the `field` vocabulary needs Brayden's approval of a schema change before any concept is written.
- **What exists:** the source note if earlier units were ingested (match its headings and any edits Brayden made), the field's map and sub-maps, every concept's filename and `aliases` in `40 Knowledge/Concepts/`, and the references for the topic.
- **The plan:** when Brayden is present, state it in a line or two (i.e., the inputs, the unit, the source note, and the map) before writing.
- **Missing properties:** ask for values the material doesn't give (e.g., a course's instructors and year). With no answer, write a placeholder and a `#question` line at the top of the source note.

If no INGEST.md section covers this kind of source or this field, make the calls with Brayden as they come up, and record them in step 8.

## 3. Extract

- **Text first.** Read Markdown directly. Run `pdftotext -layout -f N -l N` on PDFs page by page. Fetch web pages with WebFetch, and if a site can't be reached, ask for a PDF or saved page instead of working around it.
- **Images only where needed.** Look at a page when its text is junk (scattered letters, meaning pure handwriting or a drawing) or empty (e.g., a screenshot of code). Stage the PDF, render just those pages with `pdftoppm -r 75 -png -f N -l N`, tile up to four per image, and read the tiles.
- **Keep a list** of every error or disagreement found in the material while reading.

## 4. Reconcile

- **Within one source:** follow INGEST.md's order of trust for its kind, and check everything against what's actually true. Write the correct version, and report every fix instead of making it silently. If the right answer is unclear, add a `#question` line to the source note.
- **Across sources:** state settled facts plainly. On a contested point, give each position with who holds it, rather than choosing one.

## 5. Decide What Each Idea Becomes

- **The generality test:** a concept is an idea that stays the same whichever tool, notation, language, or example presents it. Material tied to one tool or product, or something looked up rather than understood (e.g., syntax, tables, constants, and recommendations), is a reference. INGEST.md gives the test in each field's terms.
- **One idea per concept.** A sub-idea folds into its parent unless it would be linked on its own. Ideas too small to stand alone go in a reference.
- **Update before creating.** If a concept already covers the idea (check names and aliases), extend it, and rewrite its body when new material broadens it.
- **Instances fold in.** A candidate concept that's only an example or special case of another concept goes into that concept (e.g., cons lists into Recursive Data Type, and map and filter into Higher-Order Function). Its distinct part becomes a concept of its own only if the source teaches it as one.
- **Overlapping concepts each keep what's distinct.** A derivation or example two concepts could share goes in the concept it motivates, and the other links to it (e.g., deriving `compose` belongs to Function Composition, not Higher-Order Function).
- **Merging an existing concept** moves it to `99 Archive/` (mirroring its path), adds its name to the surviving concept's `aliases`, and repoints every link to it, maps, the source note, and references included. The archived filename still wins over the new alias for a link typed later, so say so in the report.
- **Names:** title a concept with the field's standard term, and put the source's own terms in `aliases`. Disambiguate a name that would collide with another subject (e.g., `Closure (Programming Languages)`).
- **Placement:** personal material (e.g., your own plans or practice) goes to its domain by CONVENTIONS section 2, not to `40 Knowledge/`. Tool bookmarks go in `50 References/Bookmarks/`.
- **Leave out** logistics, assignments, and announcements.

## 6. Write

### Concepts

In `40 Knowledge/Concepts/`, following the Concept Template and STYLE:

- **Properties:** `aliases` (the source's terms), `fields` (broad fields only: a sub-map keeps its parent's field), `confidence: 2` on creation (never change an existing one), `last_reviewed` today, and `sources` (a link to each source note it draws on).
- **Body:** a one-sentence definition with the term in bold, then what the listed sources teach, then a paragraph starting "More generally," for everything else (e.g., standard terms the sources don't use, history, and other languages or fields).
- `# Example`: the source's own examples where it has them. An outside example says so (e.g., "For comparison, in Python:").
- `# Connections`: related concepts, each with a few words on how they relate. Links to concepts not written yet are fine.
- `# Sources`, then `# Maps` with `![[Map.base#Maps]]`.

Show ideas the way INGEST.md says for the field. In general: math notation for rules and formulas, Mermaid for structure and flow, tables or code blocks, and only last a cropped image in `98 Attachments/`, named `YYYY-MM-DD description.ext`.

### References

In `50 References/<Topic>/`, with `type: reference` and a `topic`. They use the default voice ("you" is fine): tables, short rules, and links to the concepts that explain the ideas.

**Running examples:** an example the source builds up across units (e.g., Arith, the language CS 131 grows one feature at a time) gets a reference in `50 References/Examples/`, named for the example. It holds the whole example in one place: what it is, how it grows, and its latest version. Each unit that extends the example updates it, and every concept that uses the example links to it at its first mention.

### Source Note

Where, how it's named, and its properties come from INGEST.md for the kind of source, checked against `structure-schema.yaml`'s `filenames`. Following Source Body:

- **Summary:** what the source covers, in the third person. Written on the first unit, and extended only when a unit changes the picture.
- **Key Ideas:** a section per unit when the source has units. Each idea is a sentence linking its concept. When the source's term differs from the concept's title, give the source's term first and the general one in parentheses (e.g., "A data type (in general, an [[Algebraic Data Type|algebraic data type]])…").
- **Open Questions and Quotes:** empty unless something adds value. Quotes are under 15 words, with a page, slide, or section.

### Map

Add each concept to its field's map or sub-map, under subject headings rather than unit headings, as a numbered list in learning order: `1. [[Concept]] — a few words on how it connects`. The sections themselves are in learning order too, the most foundational first (e.g., Functions opens Programming Languages, since the rest builds on it). A new sub-map follows the Map Template: it starts with `↑ [[Parent]]`, keeps the parent's `field`, and is linked from the parent in place of a section.

### Links Back

For each new concept, add a Connections line to every existing concept it relates to, and update references that should point to it. This is the easiest step to skip and the one that keeps the vault connected.

## 7. Check

1. Close the run as vault-conventions says (i.e., validate and log).
2. Recheck every example's result and every attributed claim against the material.
3. Reread each new or changed concept as a reader who hasn't seen any other note, against STYLE's Clear Explanations: every term defined or linked before it's relied on, every earlier example linked, every cross-reference leading to an explanation, no "one" standing in for a noun, and symbols in LaTeX outside code.

## 8. Grow INGEST.md

If the run made a call INGEST.md doesn't cover (e.g., the first book, or the first music theory notes), add it to the matching section as a short rule with an example. Remove a section's **Draft** mark once a run has confirmed it, bump INGEST.md's minor version, and add a line to its changelog. Additions are fine without asking. A change to an existing rule needs Brayden's approval.

## 9. Report

- the notes created and updated
- every error or disagreement found in the material, and how it was resolved
- the standard terms and outside material added beyond the sources
- any `#question` lines left
- anything added to INGEST.md
- the next unit

---
type: system
created: 2026-11-01
updated: 2026-11-08
version: "1.0"
---
# Writing Style

How notes in this vault should read. Every skill that writes or edits a note body reads this file after [[CONVENTIONS]]. CONVENTIONS and the schemas decide what a note holds and where it goes, and this file decides how it's written. When the two disagree, CONVENTIONS wins.

These rules come from the notes in `90 System/Overview/`, which you've edited into your own style. When a rule here doesn't cover something, imitate those notes (see [[#Model Notes]]). This file will change as you write more notes of your own (see [[#Changelog]]).

## Voice

- **Plain and direct.** Short declarative sentences. State the rule, then the reason. No filler openers (e.g., "It's worth noting that"), no hype, and no closing sentence that repeats the section.
- **The reason is one clause.** A rule usually comes with a short why, joined by a colon, a comma, or an em dash (e.g., "Keep `.git` out of iCloud: iCloud can corrupt Git's many small object files").
- **You and Claude.** Notes address you as "you" (e.g., "the pieces you want to learn"). Claude is always "Claude," in the third person, never "I" or "we."
- **Contractions are fine** (e.g., doesn't, can't, it's).
- **American spelling** (e.g., traveling, organize, catalog).

## Voice by Note Type

The voice above is the default: system and documentation notes, hubs, plans, items, projects, and references use it. Two kinds of note differ.

- **Concepts and sources read like a textbook.** Full paragraphs over bullets, precise definitions, and a neutral, impersonal voice — no "you." Define a term before using it, and build from the simple case to the general one. Source notes describe the source in the third person (e.g., "Boas derives the transform from Fourier series").
- **Logs are looser and more direct.** Daily, weekly, and monthly notes, practice and session logs, spending notes, and health and maintenance logs record what happened. Fragments are fine, numbers come first, and there's no opening paragraph (e.g., "45 min, mostly the Chopin coda. Left hand still rushes in bar 112.").

## Documentation

Documentation notes (i.e., the `documentation` type) are concise, high-level overviews. Their reader cares about what the vault does, not how it works.

- **Features, not implementation.** Say what something does and why it exists, then stop. Don't explain how code works, how a file is laid out, or what a template's body holds (e.g., [[Schemas and Validation]] says what the schemas check and that scripts enforce them, not how the YAML is structured).
- **Name things, don't inventory them.** Say that templates, scripts, or automations exist and what they're for. Skip sections that list their contents (e.g., an "Includes" section or a template's note body).
- **A few examples, not every item.** When an example makes a point, one to three are enough. Leave the full list to the schema or folder that holds it.
- **Link to the details.** When someone needs the specifics, point to [[CONVENTIONS]], the schemas, or the template rather than restating them.
- **Vault-wide only in `90 System/Overview/`.** Documentation about one domain (e.g., [[Fitness Tracking]]) lives in that domain's folder.

## Punctuation

- **Oxford comma, always:** "sources, concepts, and maps," not "sources, concepts and maps."
- **e.g., and i.e., for examples and restatements in parentheses,** each followed by a comma: "(e.g., `Physics`)" and "(i.e., the kind of folder it is)," never a bare "(`Physics`)." Use e.g. when giving one example among others, and i.e. when restating the only meaning.
- **Em dashes and commas over semicolons.** An em dash, spaced on both sides, sets off an aside or a sharp turn (e.g., "Three living lists — a schedule, a wishlist, and small to-dos — are plan notes"). Semicolons aren't banned, but reach for a comma, an em dash, or a new sentence first.
- **Colons** introduce a list, an explanation, or an example: "Three living lists: Schedule, Wishlist, and To-dos."
- **En dashes for ranges:** 1–5, 1–600, bands 6–8.
- **Arrows for mappings and next steps:** "Has a finish line → `10 Projects/`" and "Bank CSV → categorized monthly spending note."
- **"And" in prose, "&" in names.** Write "and" in sentences. "&" is for titles, names, abbreviations, and citations (e.g., Q&A, R&D, Smith & Jones 2020).

## Headers

- **Title case for every header**, the H1 included:
	- Always capitalize the first and last words.
	- Never capitalize prepositions (e.g., of, to, in, by, for, from, with, about) unless they're first or last.
	- Lowercase small function words: articles (a, an, the), conjunctions (and, but, or, nor, that), and small verbs (e.g., is, are, be).
	- Capitalize everything else, short nouns and adjectives included (e.g., Cat, Sly, Four).
	- Examples: "Knowledge is Organized by Links," "Placement Decisions that Follow," "What Stays Out of a Domain."
- **Short headers.** A noun phrase for a topic (e.g., "Setup," "Conflicts and Backup"), or a short claim when the section argues a point (e.g., "Why Only Four").
- **No "Introduction" or "Overview" header.** The opening paragraph sits directly under the H1.

## Note Shape

- **Opening paragraph:** one to four sentences under the H1 saying what the note covers. If the note summarizes a rule, it says where the binding version lives (e.g., "The binding rule is in [[CONVENTIONS]] (section 6)").
- **Structure first:** when a note describes a layout, a code-block tree or diagram comes early, introduced with a colon or "As an example:".
- **Bold-label bullets** for a set of related rules or facts. Bold the label, add a colon, then write the sentence: "**Backup:** Git history is the real backup." When the label is a full statement, end it with a period inside the bold and continue: "**CI reports; it doesn't block.** Phone edits reach GitHub through…"
- **Bullets use `-`.** Leave existing `*` bullets as they are.
- **Numbered lists** only for steps, ordered questions, or reading order.
- **Tables** for anything compared across the same attributes (e.g., note types, properties, roles). Cells are fragments with no final period. A cell with two sentences gets a period between them but none at the end.
- **Bullet endings:** a full sentence ends with a period, a fragment doesn't.
- **Bold** marks a key term where it's defined (e.g., "is a **domain**") or the main rule of a paragraph. *Italics* are only for contrast (e.g., "*understand* it or just *look it up*").
- **Overview footer:** documentation notes in `90 System/Overview/` end with `---`, then `← [[Previous]] · Next: [[Next]] →`.

## Names and Code

- **Inline code** for paths and folders (with a trailing slash, e.g., `00 Inbox/`), filenames, property names and values (e.g., `status: idea`), tags in prose (e.g., `#idea`), and commands.
- **Plain text** for skill names (e.g., inbox-triage, daily-note) and plugin names (e.g., Obsidian Git, Bases).
- **Note types:** inline code when naming the value (e.g., "has the `plan` type"), plain text when used as a word (e.g., "a plan note").
- **Notes are links, not code.** Write [[CONVENTIONS]], not `CONVENTIONS.md`, unless you're giving the path.
- **Vault vocabulary, used exactly:** domain, hub, band, item, log, plan, map, concept, source, Public, and Private. Don't swap in synonyms (e.g., "area" for domain).

## Links

- **Cross-references in parentheses start with "see":** "(see [[Privacy Boundary]])," not "([[Privacy Boundary]])." Several links share one "see" and follow the Oxford comma: "(see [[Schemas and Validation]], [[CI Workflows]], and [[Claude Guardrails]])."
- **Links to a header in another note are aliased to the header text:** `[[Domain Skeleton#Hub Body|Hub Body]]`, not `[[Domain Skeleton#Hub Body]]`. The part after `#` matches the header's exact capitalization.
- **Links to a header in the same note need no alias.** Obsidian already shows `[[#Placement Rules]]` as "Placement Rules."
- **Header aliases are display text only.** Never add them to the target note's `aliases` property, which names the whole note, not its headers.
- **Links inside a sentence** read as part of it, with display text when grammar needs it (e.g., "which breaks [[Vault Principles|link, don't duplicate]]").
- **Link the first mention per section only** (see [[CONVENTIONS]], section 5).
- **No URLs in the body.** Link to the note whose `url` holds the page instead (see [[CONVENTIONS]], section 4). A URL inside code is fine.

## Model Notes

When in doubt, write like these:

- [[Tags]]: an explanatory note that builds an argument with headers, tables, and short reasons
- [[Sync and Backup]]: bold-label bullets, each with a one-clause reason
- [[Domain Skeleton]]: a tree, comparison tables, and worked placement examples
- [[Knowledge Structure]]: prose, a diagram, and bold-label bullets that build one argument

There are no model concept, source, or log notes yet. Add some here once you've written them.

## Changelog

- 2026-11-08 · Added the Documentation section: concise, high-level overviews of what the vault does, not how it works, with a few examples instead of full lists.
- 2026-11-01 · No URLs in the body: link to the note whose `url` holds the page.
- 2026-11-01 · Title case defined: prepositions, articles, conjunctions, and small verbs lowercase. Em dashes and commas preferred over semicolons. "&" only in titles, names, abbreviations, and citations. Added voice by note type, `-` bullets, and the same-note header link exception.
- 2026-11-01 · First draft, from the notes in `90 System/Overview/` and your rules for the Oxford comma, e.g. and i.e., title-case headers, "see" links, and header link aliases.

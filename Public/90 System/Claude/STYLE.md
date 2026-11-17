---
type: system
created: 2026-11-01
updated: 2026-11-16
version: "1.1"
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
- **A concept says where its content comes from.** A concept is titled with the field's standard term, and the terms its sources use go in `aliases` (e.g., Algebraic Data Type, with the alias Data Type). After the opening definition, the body holds what the listed sources teach. Anything else, such as standard terms the sources don't use, history, or comparisons with other languages, goes in a paragraph that starts "More generally," after the source material. An added example from outside the sources says so (e.g., "For comparison, in Python:").
- **Logs are looser and more direct.** Daily, weekly, and monthly notes, practice and session logs, spending notes, and health and maintenance logs record what happened. Fragments are fine, numbers come first, and there's no opening paragraph (e.g., "45 min, mostly the Chopin coda. Left hand still rushes in bar 112.").

## Clear Explanations

These rules matter most in concepts and sources, where a reader is learning the idea, but they hold in every note.

- **Say exactly when a claim holds.** Name the cases it covers, and don't present one approach's constraints as general (e.g., only recursive-descent parsers need a grammar without left recursion, not every parser).
- **Make an abstract term concrete where it first appears,** with a small example (e.g., a parser's "result" is shown as `digit "7abc"` giving `Just ('7', "abc")`).
- **Say why an example shows its point.** After an example, name the part of it that proves the claim (e.g., "the inner scope doesn't bind `x`, so `x` is the outer one").
- **Spell out comparisons in full** (e.g., "a subtype of the other pair's corresponding component," not "a subtype of the other").
- **Tie a term's name to its meaning** when the name explains it (e.g., a parametrically polymorphic definition takes types as parameters).
- **Name the thing instead of writing "one."** Write "heating to a temperature," not "heating to one," and "keep the first parser's result or the second's," not "keep just one."
- **Don't assume the reader has seen something.** Introduce a term or example before referring to it. A sentence that relies on an example elsewhere links to it, in the same note (e.g., `(see the [[#Example|example]])`) or another note (e.g., "the grammar in [[Context-Free Grammar#Example|Context-Free Grammar]]"). A running example used across notes (e.g., [[Arith]]) links to its reference note at its first mention in each note.
- **A cross-reference leads to the explanation.** Point only to a note or section that actually covers the point it's attached to. If none does, explain the point in place.

## Documentation

Documentation notes (i.e., the `documentation` type) are concise, high-level overviews. Their reader cares about what the vault does, not how it works.

- **Features, not implementation.** Say what something does and why it exists, then stop. Don't explain how code works, how a file is laid out, or what a template's body holds (e.g., [[Schemas and Validation]] says what the schemas check and that scripts enforce them, not how the YAML is structured).
- **Name things, don't inventory them.** Say that templates, scripts, or automations exist and what they're for. Skip sections that list their contents (e.g., an "Includes" section or a template's note body).
- **A few examples, not every item.** When an example makes a point, one to three are enough. Leave the full list to the schema or folder that holds it.
- **Link to the details.** When someone needs the specifics, point to [[CONVENTIONS]], the schemas, or the template rather than restating them.
- **Vault-wide only in `90 System/Overview/`.** Documentation about one domain goes in that domain's About page (e.g., [[20 Hobbies/Fitness/About|About Fitness]]). It says how the domain's notes feed each other and which features serve it (e.g., [[Sync Last Practiced]] for Music), without explaining how those features work.
- **About pages are titled for their domain:** the H1 reads "About <Domain>" (e.g., "About Fitness"), since every About page shares one filename.

## Punctuation

- **Oxford comma, always:** "sources, concepts, and maps," not "sources, concepts and maps."
- **e.g., and i.e., for examples and restatements in parentheses,** each followed by a comma: "(e.g., `Physics`)" and "(i.e., the kind of folder it is)," never a bare "(`Physics`)." Use e.g. when giving one example among others, and i.e. when restating the only meaning.
- **Em dashes and commas over semicolons.** An em dash, spaced on both sides, sets off an aside or a sharp turn (e.g., "Three living lists — a schedule, a wishlist, and small to-dos — are plan notes"). Semicolons aren't banned, but reach for a comma, an em dash, or a new sentence first.
- **Colons** introduce a list, an explanation, or an example: "Three living lists: Schedule, Wishlist, and To-Do's."
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
- **Source sections earn their place.** In a source note, Open Questions and Quotes stay empty unless something relevant adds value. Leave the heading with nothing under it rather than filling it.
- **Overview footer:** documentation notes in `90 System/Overview/` end with `---`, then `← [[Previous]] · Next: [[Next]] →`.

## Names and Code

- **Inline code** for paths and folders (with a trailing slash, e.g., `00 Inbox/`), filenames, property names and values (e.g., `status: idea`), tags in prose (e.g., `#idea`), and commands.
- **Plain text** for skill names (e.g., inbox-triage, daily-note) and plugin names (e.g., Obsidian Git, Bases).
- **Note types:** inline code when naming the value (e.g., "has the `plan` type"), plain text when used as a word (e.g., "a plan note").
- **Notes are links, not code.** Write [[CONVENTIONS]], not `CONVENTIONS.md`, unless you're giving the path.
- **Symbols are LaTeX in concepts and sources,** especially in STEM (e.g., $\beta$, $\varepsilon$, and $\to$ rather than β, ε, and →). Inside inline code and code blocks, symbols stay plain characters, since LaTeX doesn't render there, and so do properties (e.g., `aliases`). Arrows for mappings in other notes follow [[#Punctuation]].
- **Vault vocabulary, used exactly:** domain, hub, band, item, log, plan, map, concept, source, Public, and Private. Don't swap in synonyms (e.g., "area" for domain).

## Links

- **Cross-references in parentheses start with "see":** "(see [[Privacy Boundary]])," not "([[Privacy Boundary]])." Several links share one "see" and follow the Oxford comma: "(see [[Schemas and Validation]], [[CI Workflows]], and [[Claude Guardrails]])."
- **Links to a header in another note are aliased to the header text:** `[[Domain Skeleton#Hub Body|Hub Body]]`, not `[[Domain Skeleton#Hub Body]]`. The part after `#` matches the header's exact capitalization.
- **Links to a header in the same note need no alias.** Obsidian already shows `[[#Placement Rules]]` as "Placement Rules."
- **Header aliases are display text only.** Never add them to the target note's `aliases` property, which names the whole note, not its headers.
- **Links inside a sentence** read as part of it, with display text when grammar needs it (e.g., "which breaks [[Vault Principles|link, don't duplicate]]").
- **Grammar follows the displayed text.** Articles and agreement match the alias that shows, not the note's title (e.g., "a [[Algebraic Data Type|data type]]," not "an").
- **Link the first mention per section only** (see [[CONVENTIONS]], section 5).
- **Web links read as text.** When a body holds a URL, write it as a Markdown link with the page's title (e.g., `[Locking and Syncing](https://…)`), not a bare URL.

## Model Notes

When in doubt, write like these:

- [[Tags]]: an explanatory note that builds an argument with headers, tables, and short reasons
- [[Sync and Backup]]: bold-label bullets, each with a one-clause reason
- [[Domain Skeleton]]: a tree, comparison tables, and worked placement examples
- [[Knowledge Structure]]: prose, a diagram, and bold-label bullets that build one argument

There are no model concept, source, or log notes yet. Add some here once you've written them.

## Changelog

- 2026-11-16 · 1.1 · From the review of the CS 131 concepts: added Clear Explanations (exact claims, concrete terms, examples that show their point, full comparisons, names tied to meanings, no "one" for a noun, links to earlier examples, and cross-references that explain). Symbols are LaTeX in concepts and sources, except in code and properties. Link aliases set the grammar around them.
- 2026-11-15 · Concepts separate what their sources teach from general knowledge: standard terms as titles, source terms as aliases, and outside material in a "More generally," paragraph.
- 2026-11-11 · URLs in bodies are allowed, so the no-URLs rule is gone: a body URL is a Markdown link with the page's title. A source note's Open Questions and Quotes stay empty unless something there adds value.
- 2026-11-11 · The to-do list's note is named To-Do's in examples.
- 2026-11-08 · Domain documentation goes in the domain's About page, titled "About <Domain>."
- 2026-11-08 · Added the Documentation section: concise, high-level overviews of what the vault does, not how it works, with a few examples instead of full lists.
- 2026-11-01 · No URLs in the body: link to the note whose `url` holds the page.
- 2026-11-01 · Title case defined: prepositions, articles, conjunctions, and small verbs lowercase. Em dashes and commas preferred over semicolons. "&" only in titles, names, abbreviations, and citations. Added voice by note type, `-` bullets, and the same-note header link exception.
- 2026-11-01 · First draft, from the notes in `90 System/Overview/` and your rules for the Oxford comma, e.g. and i.e., title-case headers, "see" links, and header link aliases.

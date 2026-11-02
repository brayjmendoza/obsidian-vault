---
type: system
created: 2026-10-31
updated: 2026-11-01
version: "0.7"
aliases: [Tag Rules, Reserved Tags]
---
# Tags

Tags are labels you can put on any note, in any folder. This vault allows only four of them. This page explains what tags are, what they're good for, and why the list is kept so short. The binding rule is in [[CONVENTIONS]] (section 6); the `tags` property is listed in [[Note Properties]].

## What a Tag Is

A tag is added in one of two ways:

- **In the body:** write `#idea` anywhere in a note, even in the middle of a sentence or on a single list item.
- **In the frontmatter:** list it under the `tags` property, without the `#` (e.g., `tags: [review]`).

Obsidian indexes every tag. Clicking one shows every note that carries it; you can also search for it (e.g., `tag:#review`), browse all tags in the Tags pane, and filter on tags in Bases views and Tasks queries (see [[Vault Plugins]]).

## Why Tags are Useful

- **They work across folders.** A folder gives a note one home. A tag gathers notes from anywhere: an idea in a piano practice log sits next to an idea in a physics concept note.
- **A note can have several.** One note can be both `#review` and `#question`.
- **They can mark a single line.** A tag in the body marks that spot, not just the whole note. In a concept note you can write `#question does this hold for discrete signals?` exactly where the doubt comes up. A property can't do this, because properties belong to the whole note.
- **They need no setup.** Type one and it exists. That is handy while capturing, and it is also the problem.

## Why Only Four

Because tags cost nothing to create, they spread. Nothing stops `#todo`, `#to-do`, and `#todos` from all appearing, and no validator can tell which one is right. Tags also tend to repeat what the vault's typed structure already says:

| A tag you might be tempted to use | What the vault uses instead                                      |
| --------------------------------- | ---------------------------------------------------------------- |
| `#piano`, `#finance`              | The domain folder (see [[Domain Skeleton]])                      |
| `#math`, `#physics`               | The `fields` property and the maps (see [[Knowledge Structure]]) |
| `#to-read`, `#done`               | The `status` property, which only accepts allowed values         |
| `#book`, `#paper`                 | The `type` property (see [[Note Types and Properties]])          |

Properties have a value type and a list of allowed values, and the validators check them (see [[Schemas and Validation]]). Tags carry no value type, so the most a validator can do is hold them to a fixed list. So the rule is: **prefer properties over tags.** Tags are kept only for what properties handle badly: flags that apply to any note type, often to one spot inside a note, and that are meant to be removed later.

A nested tag such as `#idea/music` counts as a different tag, so it isn't on the list either. To tie an idea to a subject, link the note it's about instead.

## The Four Tags

Each tag answers one question: *what should I look at next?*

| Tag | Means | Added by | Removed when |
|---|---|---|---|
| `#inbox` | Needs triage, but isn't in `00 Inbox/` | You, or a QuickAdd capture made straight into a note type | Claude finishes the note (properties, links, body) and confirms it's in the right folder |
| `#review` | You want to come back to this | You | You've revisited it |
| `#idea` | A rough idea that isn't worked out yet | You, anywhere in the vault | The idea becomes a note of its own (e.g., a project, a trip with `status: idea`, a concept), or you drop it |
| `#question` | An open question for you or Claude | You, or Claude when it can't place a note and leaves it in `00 Inbox/` with a `#question` line | The question is answered |

### Why `#inbox` Exists When `00 Inbox/` Does

The folder already marks everything inside it as untriaged, so notes in `00 Inbox/` don't need the tag. The tag is for the notes the folder can't catch: a capture that went straight into a note type's folder (QuickAdd can do this, see [[Vault Plugins]]), or a note you started in place and didn't finish. The inbox-triage skill works through both: everything in `00 Inbox/`, and every note tagged `#inbox` anywhere else. If a tagged note's placement is unclear, Claude leaves it where it is, keeps the tag, and adds a `#question` line.

Don't use `#inbox` on a single line of a daily or weekly note: those are generated, and skills may rewrite them whole. Capture to the Inbox instead.

### Why the Short List Matters

Because the list is fixed and short, clicking any of these tags gives a complete, trustworthy list: every open question in the vault, every note waiting for review, whatever kind of note it lives in.

## How Tags are Checked

`vault-validate` holds every tag to the four, wherever it's written:

- **In the frontmatter:** the `tags` property only accepts values from the `tag` vocabulary in `properties-schema.yaml`.
- **In the body:** every inline `#tag` is checked against the same vocabulary and reported with its line. Tags are recognized the way Obsidian recognizes them: `#` at the start of a line or after a space, so `C#`, `issue #123`, `[[Note#Heading]]`, and headings don't count. Tags inside code blocks and inline code are ignored.
- **Near misses get a hint:** `#Idea` must be lowercase, and `#idea/music` is a nested tag, so it's reported too.

## Adding a Tag

Claude never creates a tag that isn't on the list (see [[Claude Guardrails]]). A new tag is a change to the vocabulary in `properties-schema.yaml` and to [[CONVENTIONS]], and needs your approval like any other schema change. Before proposing one, check whether a property or a link would do the job; it usually will.

---
← [[Note Properties]] · Next: [[Everyday Lists]] →

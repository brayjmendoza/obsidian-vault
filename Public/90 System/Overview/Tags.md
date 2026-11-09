---
type: documentation
created: 2026-10-31
updated: 2026-11-08
aliases: [Tag Rules, Reserved Tags]
---
# Tags

Tags are labels you can put on any note, in any folder, and this vault allows only four of them. This note explains what tags are good for and why the list is so short. The binding rule is in [[CONVENTIONS]] (section 6).

## What a Tag Is

A tag goes in a note's body (e.g., `#idea` mid-sentence or on one list item) or in its `tags` property. Obsidian indexes every tag, so clicking one lists every note that carries it, and Bases views and Tasks queries can filter on them (see [[Vault Plugins]]).

## Why Tags are Useful

- **They work across folders.** A tag gathers notes from anywhere, so an idea in a practice log sits next to one in a physics concept.
- **They can mark a single line.** A tag in the body marks that spot, which a property can't do (e.g., `#question does this hold for discrete signals?` right where the doubt comes up).
- **They need no setup.** Type one and it exists. That's handy while capturing, and it's also the problem.

## Why Only Four

Because tags cost nothing to create, they spread (e.g., `#todo`, `#to-do`, and `#todos`), and they tend to repeat what the vault's structure already says:

| A tag you might be tempted to use | What the vault uses instead |
|---|---|
| `#piano`, `#finance` | The domain folder (see [[Domain Skeleton]]) |
| `#math`, `#physics` | The `fields` property and the maps (see [[Knowledge Structure]]) |
| `#to-read`, `#done` | The `status` property |
| `#book`, `#paper` | The `type` property (see [[Note Types and Properties]]) |

Properties have allowed values that validation can check, and tags don't. So the rule is: **prefer properties over tags.** Tags are kept for flags that apply to any note, often to one spot inside it, and that are meant to be removed later. Because the list is short and fixed, clicking a tag gives a complete list you can trust (e.g., every open question in the vault).

## The Four Tags

Each tag answers one question: *what should I look at next?*

| Tag | Means | Removed when |
|---|---|---|
| `#inbox` | Needs triage, but isn't in `00 Inbox/` | Claude finishes the note and files it |
| `#review` | You want to come back to this | You've revisited it |
| `#idea` | A rough idea that isn't worked out yet | It becomes a note of its own, or you drop it |
| `#question` | An open question for you or Claude | The question is answered |

### Why `#inbox` Exists When `00 Inbox/` Does

The folder already marks everything inside it, so the tag is for notes the folder can't catch: a capture made straight into a note type's folder, or a note you started in place and didn't finish. inbox-triage works through both (see [[Claude Skills]]).

## Checking and Adding Tags

Validation holds every tag to the four, in properties and note bodies alike (see [[Schemas and Validation]]). Claude never creates a new tag, and adding one needs your approval like any other schema change. A property or a link usually does the job instead.

---
← [[Note Properties]] · Next: [[Everyday Lists]] →

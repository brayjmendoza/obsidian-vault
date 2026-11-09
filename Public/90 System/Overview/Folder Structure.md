---
type: documentation
created: 2026-10-25
updated: 2026-11-08
---
# Folder Structure

`Public/` uses a numbered, PARA-style layout that separates projects, hobbies, life admin, knowledge, and references. Every top-level folder belongs to a band, and the [[#Placement Rules]] decide which folder a note goes in. The binding rules are in [[CONVENTIONS]] (section 2), and the structure schema lists every allowed folder (see [[Schemas and Validation]]). As an example:

```
Public/
├── 00 Inbox/          quick captures waiting for triage
├── 01 Logs/           daily, weekly, and monthly notes
├── 10 Projects/       goals with a finish line
├── 20 Hobbies/        one domain per hobby (e.g., Music, Fitness)
├── 30 Life Admin/     one domain per responsibility (e.g., Finance, Home)
├── 40 Knowledge/      sources, concepts, and maps
├── 50 References/     how-tos and look-up info
├── 90 System/         the rules and these docs
├── 91 Tooling/        the schemas and the scripts that check them
├── 92 Templates/      templates for new notes, and automations
├── 93 Views/          bases and scripts that show live content in notes
├── 98 Attachments/    files embedded in notes
└── 99 Archive/        retired notes
```

## Bands

The first digit of a top-level folder is its **band** (i.e., the kind of folder it is), and the second is its position within the band. The numbers only set sort order.

| Band | Kind | Holds |
|---|---|---|
| 0 | Capture and logs | Material ordered by time: captures and generated logs |
| 1–5 | Content | Projects, hobbies, life admin, knowledge, and references, in the order of the placement rules |
| 6–8 | Unused | Room for a new kind of content without renumbering anything |
| 9 | System | What runs the vault rather than what's in it: its rules and docs, tooling, templates, and views, then attachments and the archive |

A new top-level folder takes the band that matches its kind, and needs your approval first (see [[Claude Guardrails]]).

## Placement Rules

Ask in order:

1. Has a finish line → `10 Projects/`
2. A hobby you keep doing → `20 Hobbies/`
3. A responsibility that never ends → `30 Life Admin/`
4. Something learned → `40 Knowledge/`
5. Something looked up → `50 References/`

If nothing fits clearly, the note stays in `00 Inbox/` and Claude asks where it goes.

## Domains and Knowledge

The folders under `20 Hobbies/` and `30 Life Admin/` are domains, and they all share one shape (see [[Domain Skeleton]]). `40 Knowledge/` is the one content band without topic folders: links organize it by subject instead (see [[Knowledge Structure]]).

---
← [[Privacy Boundary]] · Next: [[Domain Skeleton]] →

---
name: vault-conventions
description: Load the rules of Brayden's Obsidian vault (CONVENTIONS, schemas, and STYLE) before reading or writing any note in it, and close the run by validating and logging. Run first in every vault skill, and for any task that touches the vault.
---

# Vault Conventions

Every vault skill starts with this one. It loads the vault's rules, lists the ones runs most often break, and says how to close a run. The binding rules live in the vault, not here: when this skill and the vault's files disagree, follow the files and tell Brayden this skill is out of date.

## Reach the Vault

- **Where it is:** the vault's `Public/` folder is connected from Brayden's Mac (`…/iCloud~md~obsidian/Documents/Obsidian Vault/Public`). Work in it with device_bash at `$HOME/mnt/Public`. Read, Write, Edit, and Bash act on the cloud container, not the vault. Every path below is relative to `Public/`.
- **Container steps:** stage a file only for a step the device shell can't do (e.g., viewing an image or a PDF page), and copy a result back with device_commit_files.
- **No device tools:** ask Brayden to open the chat in the Claude desktop app with the folder connected.
- **`Private/` is off-limits.** Never ask for it, guess at it, or link into it.

## Load the Rules

At the start of every run, read in full:

1. `90 System/Claude/CONVENTIONS.md`
2. `91 Tooling/schemas/properties-schema.yaml`
3. `91 Tooling/schemas/structure-schema.yaml`
4. `90 System/Claude/STYLE.md`, if the run writes or edits note bodies
5. `90 System/Claude/CODE_STYLE.md`, if the run writes or edits code
6. The template in `92 Templates/` for each note type the run creates

The calling skill may name more files (e.g., ingest-source reads `90 System/Claude/INGEST.md`).

## Rules Runs Most Often Break

These summarize CONVENTIONS, which is binding:

- **Valid notes only:** every note has a `type` from the schema, sits in a folder that allows it, matches its filename pattern, and has exactly the properties its type allows. Links inside properties are quoted (e.g., `area: "[[Piano]]"`), and dates are `YYYY-MM-DD`.
- **Nothing new without approval:** no new folders, domains, properties, types, vocabulary values, or tags until Brayden approves the specific change and the schema is edited first. A change to CONVENTIONS or either schema bumps the version in all three and in every template, and adds a line to CONVENTIONS section 8.
- **Hands off:** never edit a note with `claude: read-only`, and never change CONVENTIONS, the schemas, or anything in `91 Tooling/` without Brayden's approval of the specific change.
- **His calls stay his:** never tick off a task, or change a `status` or `confidence`, unless he says so or the skill allows it.
- **No deletes:** move a note to `99 Archive/`, mirroring its original path. Renaming a note means updating every link to it.
- **Check names first:** a new note's filename must not match an existing note's name or alias.
- **Ask, don't guess:** an unclear placement stays in `00 Inbox/` with a `#question` line.
- **Link, don't duplicate:** each fact lives in one note.
- **`updated`:** set it on every note the run edits.
- **Empty folders** get a `.gitkeep`.
- **Secrets never go in `Public/`:** account numbers, IDs, and passwords. Report them instead of repeating them.

## Rendering Pitfalls

- **Dataview:** inline code that starts with "dv:" or "dvjs:" runs as a query (the prefixes are set in Dataview's settings, see [[Vault Plugins]]). Only write those prefixes to make a query. To mention one, write it as plain text in quotes, not as inline code.
- **Pipes in tables:** `\|` inside inline code shows its backslash in Live Preview, so write `<code>(&#124;&#124;)</code>` for `||`. A wikilink alias inside a table is `[[Note\|alias]]`.
- **Embeds:** a concept's Maps section is `![[Map.base#Maps]]`, never hand-written links.

## Close the Run

1. From `Public/`, run `UV_PROJECT_ENVIRONMENT=$HOME/.venvs/vault-tools uv run --project "91 Tooling" vault-validate --json --skip-urls`. Always set `UV_PROJECT_ENVIRONMENT` so no virtual environment is built inside iCloud.
2. Fix every error the run caused. Ignore `private-link` results and the `skipped` list, and leave them out of the report. Warnings for links to notes not written yet are fine.
3. If the run changed code, also run the checks in CODE_STYLE's first section (e.g., `uv run pytest` in `91 Tooling/`).
4. Append one line to `90 System/Claude/changelog.md`: `- YYYY-MM-DD HH:MM · <skill> · <what changed>`, linking notes by name.
5. Report what changed, anything left with a `#question`, and any validator results the run couldn't fix.

## Skill Copies

`90 System/Claude/Skills/<skill>/SKILL.md` holds a local copy of every vault skill. The skill saved in claude.ai is the one that runs, so the two must never drift apart:

- **Every change to a skill updates its copy in the same turn.** When a run or a chat proposes a change to a skill, write the same change to the local copy right away, so the copy matches what Brayden saves. Say in the reply that the copy already has it.
- **A new skill gets a copy** in `Skills/<skill>/SKILL.md` when it's first proposed.
- **A declined change is undone** in the copy.
- **Out of step:** if the skill loaded in a session differs from its copy, tell Brayden which is newer and propose whichever version he wants to keep, so both end up the same.

Never edit only the copy expecting the skill to change: a skill changes only when Brayden saves a proposal.

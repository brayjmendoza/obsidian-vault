---
type: template
created: 2026-11-07
updated: 2026-11-09
version: "0.36"
---
<%* tR = "" -%>
<% await tp.file.include("[[Frontmatter]]") -%>
<%* const root = tp.config.template_file.path.split("92 Templates/")[0]; -%>
```meta-bind-button
label: Start Session
style: primary
actions:
  - type: runTemplaterFile
    templateFile: "<% root %>92 Templates/Automations/Start Session.md"
```

%% Routine format (binding in CONVENTIONS section 5). The Session Table reads it, so keep to it:
- Scripts read only the Warm-Up, Core Workout, and Cool-Down sections above the `---`. Anything below it (e.g., progression ladders) is free-form, and a routine without any leaves out the `---`.
- One exercise per list item, starting with its link. Words between the link and " — " are display only, e.g., `- [[Push-up|Push-ups]] — Reps: 20`.
- Fields are `Label: value`, either inline after " — " and separated by commas (Warm-Up and Cool-Down), or one per sub-bullet (Core Workout). Values are free text.
- Rename each placeholder to the specific label: Volume → Reps, Time, or Distance, Intensity → Weight, Pace, Assistance, or RPE, and Detail → Cue or Tempo (added to the session's Target column).
- A value that's the same every set is written once. One that changes lists a value per set, separated by commas, e.g., `Reps: 20, 18, 15`.
- Leave out what doesn't apply (e.g., Sets and Rest on a run or a stretch). A session table gets a column only for what at least one of its exercises sets, and Sets defaults to 1.
- A sub-bullet with any other label (e.g., `Progression:`, `Benchmark:`, or `Alternative:`) is a note for you, and scripts skip it.
- `Format:` under a block heading says how the block runs when it isn't straight sets (e.g., superset, circuit, or EMOM). In a circuit, `Rounds:` and `Rest:` there apply to the whole block.
- H2 blocks are optional. A section without one is a single block.
- Progressions: put each ladder below the `---` under `# Progressions`, highlight the tier you're on (e.g., `2. ==[[Pull-up|Pull-ups]] — Sets: 3, Reps: 10, Rest: 3 min==`), and link it from the Core Workout exercise with `Progression: [[#Ladder Name]]`. When you move up a tier, update both.
- The Start Session button above creates today's session note for this routine. Keep it at the top.
- Delete this comment once the routine is written. %%
# Warm-Up

## Block

1. [[Exercise]] — Volume: 

# Core Workout

## Block

Format: 

1. [[Exercise]]
	- Sets: 
	- Volume: 
	- Intensity: 
	- Rest: 
	- Detail: 

# Cool-Down

## Block

1. [[Exercise]] — Volume: 

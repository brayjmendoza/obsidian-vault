---
type: template
created: 2026-11-07
updated: 2026-11-08
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

%% Routine format (binding in CONVENTIONS section 5). The Session Template reads it, so keep to it:
- One exercise per list item: a link to its exercise note, then " — " and the target, e.g., `- [[Push-up|Push-ups]] — 3x20` or `- [[Run]] — 10km @ ~7:30/mi pace`. Words between the link and the " — " are kept as wording, e.g., `- [[Arm Circle|Arm circles]] (forward/backward) — 15s each direction`.
- Each section becomes its own table in session notes. A list item counts as an exercise only when it starts with its link, so a sub-note like `- Alternative: [[…]]` doesn't get a row.
- Each block of the Core Workout is an H2 with a `Sets:` line, e.g., `Sets: 3` (use `Sets: 1` for a run or a single hold). A `Sets:` line in the Warm-Up or Cool-Down fills in Sets there too.
- In a progression, number the tiers and highlight the one you're on: `2. ==[[Push-up|Push-ups]] — 3x20==`. Only the highlighted tier goes into session notes. A block or section with nothing highlighted puts in every exercise.
- The Start Session button above creates today's session note for this routine. Keep it at the top.
- Delete this comment once the routine is written. %%
# Warm-Up

- 

Rest: None  
Total time: 

# Core Workout

## Block

1. 

Rest:   
Sets:   
Total time: 

# Cool-Down

- 

Rest: None  
Total time: 

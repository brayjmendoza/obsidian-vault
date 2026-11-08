---
type: template
created: 2026-11-07
updated: 2026-11-08
version: "0.28"
---
<%* tR = "" -%>
<% await tp.file.include("[[Frontmatter]]") -%>
%% Routine format (binding in CONVENTIONS section 5). The Session Template reads it, so keep to it:
- One exercise per list item: a link to its exercise note, then " — " and the target, e.g., `- [[Push-up|Push-ups]] — 3x20` or `- [[Run]] — 10km @ ~7:30/mi pace`. Words between the link and the " — " are kept as wording, e.g., `- [[Arm Circle|Arm circles]] (forward/backward) — 15s each direction`.
- Only the Core Workout goes into session notes. Each block in it is an H2 with a `Sets:` line, e.g., `Sets: 3` (use `Sets: 1` for a run or a single hold).
- In a progression, number the tiers and highlight the one you're on: `2. ==[[Push-up|Push-ups]] — 3x20==`. Only the highlighted tier goes into session notes. A block with nothing highlighted puts in every exercise.
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

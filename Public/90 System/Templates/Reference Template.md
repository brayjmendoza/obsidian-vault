---
type: template
created: 2026-11-07
updated: 2026-11-08
version: "0.30"
---
<%* tR = "" -%>
<% await tp.file.include("[[Frontmatter]]") -%>
%% For a form video: put the video in `url` and replace this comment with a dataviewjs block that runs `await dv.view("Public/90 System/Scripts/form-video")`, which plays it with Obsidian's own player. %%

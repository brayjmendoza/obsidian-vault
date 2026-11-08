---
type: template
created: 2026-11-07
updated: 2026-11-08
version: "0.24"
---
<%*
// Add Properties: run on an existing note (Templater: Insert template) to add
// any required properties it's missing, then pick from the optional ones it
// doesn't have yet. A note with no type is asked for one first.
tR = "";
-%>
<% await tp.file.include("[[Frontmatter]]") %>

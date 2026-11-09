---
type: template
created: 2026-11-07
updated: 2026-11-08
version: "0.32"
---
<%* tR = "" -%>
<% await tp.file.include("[[Frontmatter]]") %>
<%*
// Each composer has a Pieces.base view named after their surname: the last word of the
// note's name, read after Frontmatter has renamed it (e.g., "Frédéric Chopin" → "Chopin").
// If Pieces.base has no view by that name yet, this adds one.
const Notice = tp.obsidian.Notice;
const composer = tp.config.target_file.basename.trim();
const surname = composer.split(/\s+/).pop();
const root = tp.config.template_file.path.split("92 Templates/")[0];
const base = app.vault.getAbstractFileByPath(`${root}93 Views/Bases/Pieces.base`);
const link = `link(${JSON.stringify(composer)})`;

if (/^Untitled( \d+)?$/.test(composer)) {
  new Notice("Composer Template: the note has no name yet, so no Pieces.base view was added.", 10000);
} else if (!base) {
  new Notice("Composer Template: 93 Views/Bases/Pieces.base is missing, so no view was added.", 10000);
} else {
  const views = tp.obsidian.parseYaml(await app.vault.read(base))?.views ?? [];
  const existing = views.find((v) => String(v.name) === surname);
  if (!existing) {
    const view = [
      "  - type: table",
      `    name: ${JSON.stringify(surname)}`,
      "    filters:",
      "      and:",
      '        - type == "piece"',
      `        - composers.contains(${link})`,
      "    groupBy:",
      "      property: status",
      "      direction: ASC",
      "    groupOrder:",
      ...["repertoire", "learning", "retired", "wishlist"].map((s) => `      - ${s}`),
    ].join("\n");
    await app.vault.process(base, (text) => `${text.replace(/\s*$/, "")}\n${view}\n`);
    new Notice(`Composer Template: added the ${surname} view to Pieces.base.`, 6000);
  } else if (!JSON.stringify(existing.filters ?? "").includes(composer)) {
    // Two composers share a surname (e.g., Clara and Robert Schumann).
    new Notice(`Composer Template: Pieces.base already has a ${surname} view for another composer. Give this one its own view by hand.`, 12000);
  }
}
-%>
# Pieces
![[Pieces.base#<% surname %>]]

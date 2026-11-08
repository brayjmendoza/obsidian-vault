---
type: template
created: 2026-11-02
updated: 2026-11-08
version: "0.24"
---
<%*
// Map Template: a field map, or a sub-map split off an existing map.
// The note is named and moved into 40 Knowledge/Maps/ for you.

// Drop this template's own properties (type: template) from the output.
tR = "";

const Notice = tp.obsidian.Notice;
const today = tp.date.now("YYYY-MM-DD");
const root = tp.config.template_file.path.split("90 System/")[0];
const mapsFolder = `${root}40 Knowledge/Maps`;
const frontmatter = (file) => app.metadataCache.getFileCache(file)?.frontmatter ?? {};

// Title case per STYLE: small words stay lowercase unless first or last.
const small = new Set(["a", "an", "the", "and", "but", "or", "nor", "that", "is", "are", "be",
  "of", "to", "in", "on", "at", "by", "for", "from", "with", "about", "as", "into"]);
const titleCase = (text) => {
  const words = text.split(/[-\s]+/).filter(Boolean);
  return words
    .map((w, i) => (i > 0 && i < words.length - 1 && small.has(w) ? w : w[0].toUpperCase() + w.slice(1)))
    .join(" ");
};

// The field vocabulary, read from the properties schema so it never drifts.
let fields = null;
try {
  const schema = tp.obsidian.parseYaml(
    await app.vault.adapter.read(`${root}91 Tooling/schemas/properties-schema.yaml`)
  );
  fields = schema.vocabularies.field;
} catch (error) {
  new Notice("Map Template: couldn't read the field vocabulary from the properties schema.", 10000);
}

const maps = app.vault.getMarkdownFiles()
  .filter((f) => f.parent?.path === mapsFolder && frontmatter(f).type === "map")
  .sort((a, b) => a.basename.localeCompare(b.basename));

// Field map or sub-map.
const kind = maps.length
  ? await tp.system.suggester(["Field map", "Sub-map of an existing map"], ["field", "sub"], true, "What kind of map is this?")
  : "field";

let field;
let name;
let parent = null;
if (kind === "sub") {
  // A sub-map keeps its parent's field.
  parent = await tp.system.suggester(maps.map((m) => m.basename), maps, true, "Which map is this a sub-map of?");
  field = frontmatter(parent).field;
  const suggested = tp.file.title.startsWith("Untitled") ? "" : tp.file.title;
  name = (await tp.system.prompt("What's the sub-map called? (e.g., Quantum Mechanics)", suggested, true)).trim();
} else {
  const mapped = new Set(maps.map((m) => frontmatter(m).field));
  field = fields
    ? await tp.system.suggester(
        fields.map((f) => (mapped.has(f) ? `${f} (already has a map)` : f)), fields, true, "Which field does this map cover?"
      )
    : (await tp.system.prompt("Which field does this map cover? (e.g., physics)", "", true)).trim();
  name = titleCase(field);
}

// Name the note and move it into Maps/.
let needsTriage = false;
const target = `${mapsFolder}/${name}`;
if (tp.file.path(true) !== `${target}.md`) {
  if (app.vault.getAbstractFileByPath(`${target}.md`)) {
    new Notice(`Map Template: ${name} already exists, so this note keeps its name and is tagged inbox.`, 10000);
    needsTriage = true;
  } else {
    await tp.file.move(target);
  }
}
const mapPath = tp.file.path(true);

// Subtopics, each its own heading.
const subtopics = ((await tp.system.prompt(
  "What are its subtopics, in learning order? (separate with commas, optional)", "", false
)) ?? "").split(",").map((s) => s.trim()).filter(Boolean);

const parentLink = parent ? app.fileManager.generateMarkdownLink(parent, mapPath) : "";
// A sub-map starts with a link up to its parent map.
const up = parent ? `↑ ${parentLink}\n\n` : "";

const conceptHint = "%% Concepts in learning order, as a numbered list of links, each with a few words on how it connects. %%";
const sections = subtopics.length
  ? subtopics.map((s) => `# ${s}\n\n${conceptHint}`).join("\n\n")
  : `%% One heading per subtopic. ${conceptHint.slice(3)}`;

if (parent) {
  new Notice(`Map Template: link ${name} from ${parent.basename} in place of its section.`, 10000);
}
-%>
---
type: map
created: <% today %>
updated: 2026-11-08
field: <% field %>
<% needsTriage ? "tags: [inbox]\n" : "" %>---
<% up %><% sections %>
<%* if (!parent) { -%>

# Unmapped Concepts

![[Map.base#Unmapped Concepts]]
<%* } -%>

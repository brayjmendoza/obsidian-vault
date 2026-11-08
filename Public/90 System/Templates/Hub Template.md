---
type: template
created: 2026-11-02
updated: 2026-11-08
version: "0.23"
---
<%*
// Hub Template: the hub for the domain folder the new note sits in.
// Create the note inside the domain folder (e.g., 20 Hobbies/Music/Piano/).
// The note is renamed to the folder's name, as the domain rule requires.

// Drop this template's own properties (type: template) from the output.
tR = "";

const Notice = tp.obsidian.Notice;
const today = tp.date.now("YYYY-MM-DD");
const root = tp.config.template_file.path.split("90 System/")[0];
const folderPath = tp.file.folder(true);
const domain = tp.file.folder(false);
const frontmatter = (file) => app.metadataCache.getFileCache(file)?.frontmatter ?? {};

// A domain is any folder below 20 Hobbies/ or 30 Life Admin/.
const isDomain = ["20 Hobbies", "30 Life Admin"].some(
  (band) => folderPath.startsWith(`${root}${band}/`)
);
if (!isDomain) {
  new Notice(`Hub Template: ${folderPath} isn't a domain folder under 20 Hobbies/ or 30 Life Admin/.`, 10000);
}

// Name the hub after its folder.
if (tp.file.title !== domain) {
  if (app.vault.getAbstractFileByPath(`${folderPath}/${domain}.md`)) {
    new Notice(`Hub Template: ${domain} already has a hub, so this note keeps its name.`, 10000);
  } else {
    await tp.file.rename(domain);
  }
}
const hubPath = `${folderPath}/${domain}.md`;
const linkTo = (file) => app.fileManager.generateMarkdownLink(file, hubPath);

// Every note except 91 Tooling/, whose test vaults hold sample notes.
const notes = app.vault.getMarkdownFiles().filter((f) => !f.path.startsWith(`${root}91 Tooling/`));

// Links: pick maps and references to link, one at a time, until Done or Esc.
const linkable = notes
  .filter((f) => ["map", "reference"].includes(frontmatter(f).type))
  .sort((a, b) => a.basename.localeCompare(b.basename));
const picked = [];
while (linkable.length > picked.length) {
  const left = linkable.filter((f) => !picked.includes(f));
  const labels = left.map((f) => `${frontmatter(f).type === "map" ? "Map" : "Reference"} · ${f.basename}`);
  const choice = await tp.system.suggester(
    ["Done", ...labels], [null, ...left], false, `Which maps or references should ${domain} link to? (pick one at a time, then Done)`
  );
  if (!choice) break;
  picked.push(choice);
}
// Maps and references are listed apart. A map's link reads "<Field> Map"
// (e.g., [[Computer Science|Computer Science Map]]).
const isMap = (f) => frontmatter(f).type === "map";
const mapLinks = picked.filter(isMap)
  .map((f) => `- ${app.fileManager.generateMarkdownLink(f, hubPath, "", `${f.basename} Map`)}`);
const referenceLinks = picked.filter((f) => !isMap(f)).map((f) => `- ${linkTo(f)}`);
-%>
---
type: hub
created: <% today %>
updated: <% today %>
---
# Current

![[Hub.base#Current]]


# Tasks

```tasks
not done
folder includes {{query.file.folder}}
sort by priority
```


# Projects

![[Hub.base#Projects]]


# Plans

![[Plan.base]]


# Recent Logs

![[Hub.base#Recent]]


# Resources

## Maps

<% mapLinks.length ? mapLinks.join("\n") : "%% Relevant maps in 40 Knowledge, each shown as \\<Field> Map. %%" %>

## References

<% referenceLinks.length ? referenceLinks.join("\n") : "%% Relevant notes in 50 References. %%" %>

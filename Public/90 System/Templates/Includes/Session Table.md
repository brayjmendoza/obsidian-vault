---
type: template
created: 2026-11-08
updated: 2026-11-08
version: "0.25"
---
<%*
// Session Table: writes a new session note's sets table (CONVENTIONS.md section 5),
// with the Exercise column filled from the routine in its `routine` property.
// In a routine section with a highlighted item (i.e., a progression), only the
// highlighted items go in. In any other section (e.g., a warm-up), every linked
// exercise does. The Session Template includes it after Frontmatter, so it runs
// once the note's properties are written. Never run it alone.
tR = "";

const { Notice, parseYaml } = tp.obsidian;
const target = tp.config.target_file;
const header = ["| Exercise | Sets | Reps | Weight (lb) | Notes |", "|---|---|---|---|---|"];

// The link targets of a routine's exercises, in order.
const routineExercises = (text) => {
  const body = text.replace(/^---\r?\n[\s\S]*?\r?\n---/, "");
  const names = [];
  for (const section of body.split(/^#{1,6}\s.*$/m)) {
    const items = section.split("\n")
      .filter((line) => /^\s*(?:[-*+]|\d+[.)])\s/.test(line) && line.includes("[["));
    const current = items.filter((line) => /==.*\[\[.*==/.test(line));
    for (const line of current.length ? current : items) {
      const name = line.match(/\[\[([^\]|#]+)/)?.[1].trim();
      if (name) names.push(name);
    }
  }
  return names;
};

tp.hooks.on_all_templates_executed(async () => {
  // Read the note directly, since Obsidian may not have indexed it yet.
  const text = await app.vault.read(target);
  const block = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  let fm = {};
  try {
    fm = block ? parseYaml(block[1]) ?? {} : {};
  } catch (error) {
    new Notice("Session Table: couldn't read this note's properties, so the table is empty.", 10000);
  }
  const linkpath = String(fm.routine ?? "").replace(/^\s*\[\[|\]\]\s*$/g, "").split("|")[0].split("#")[0].trim();
  const routine = linkpath ? app.metadataCache.getFirstLinkpathDest(linkpath, target.path) : null;
  if (linkpath && !routine) new Notice(`Session Table: ${linkpath} doesn't exist yet, so the table is empty.`, 10000);
  const exercises = routine ? routineExercises(await app.vault.read(routine)) : [];
  const rows = exercises.length
    ? exercises.map((name) => `| [[${name}]] |  |  |  |  |`)
    : ["|  |  |  |  |  |"];
  await app.vault.process(target, (current) => {
    const trimmed = current.trimEnd();
    return `${trimmed}${trimmed.endsWith("---") ? "\n" : "\n\n"}${[...header, ...rows].join("\n")}\n`;
  });
});
-%>

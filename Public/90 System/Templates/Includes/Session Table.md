---
type: template
created: 2026-11-08
updated: 2026-11-08
version: "0.26"
---
<%*
// Session Table: writes a new session note's sets table (CONVENTIONS.md section 5)
// from the routine in its `routine` property, then a button that runs Sync Last
// Performed. Only the routine's Core Workout goes in, never its Warm-Up or
// Cool-Down. Within each Core Workout section (e.g., a progression):
//   - Exercise: the highlighted items if there are any, else every linked item
//   - Target:   the item's text after its link (e.g., "3x20")
//   - Sets:     the number at the start of the section's `Sets:` line
// The Session Template includes it after Frontmatter, so it runs once the
// note's properties are written. Never run it alone.
tR = "";

const { Notice, parseYaml } = tp.obsidian;
const target = tp.config.target_file;
const root = tp.config.template_file.path.split("90 System/")[0];
const sync = `${root}90 System/Templates/Automations/Sync Last Performed.md`;
const header = ["| Exercise | Target | Sets | Reps | Weight (lb) | Notes |", "|---|---|---|---|---|---|"];
const button = [
  "```meta-bind-button",
  "label: Sync Last Performed",
  "style: primary",
  "actions:",
  "  - type: runTemplaterFile",
  `    templateFile: "${sync}"`,
  "```",
];

// The text of a routine's `# Core Workout` section, or null.
const coreWorkout = (text) => {
  const match = text.match(/^# Core Workout[ \t]*\r?\n([\s\S]*?)(?=^# |(?![\s\S]))/m);
  return match ? match[1] : null;
};

// One row per exercise in the Core Workout: { name, target, sets }.
const routineRows = (core) => {
  const rows = [];
  for (const section of core.split(/^#{2,6}\s.*$/m)) {
    const lines = section.split("\n");
    const sets = lines.map((line) => line.match(/^\s*Sets:\s*(\d+)/)?.[1]).find(Boolean) ?? "";
    const items = lines.filter((line) => /^\s*(?:[-*+]|\d+[.)])\s/.test(line) && line.includes("[["));
    const current = items.filter((line) => /==.*\[\[.*==/.test(line));
    for (const line of current.length ? current : items) {
      const name = line.match(/\[\[([^\]|#]+)/)?.[1].trim();
      if (!name) continue;
      const after = line.replaceAll("==", "").split("]]").slice(1).join("]]").trim()
        .replace(/^[,;:—–-]+\s*/, "").replace(/^\(([^()]*)\)$/, "$1").replaceAll("|", "\\|");
      rows.push({ name, target: after, sets });
    }
  }
  return rows;
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
  let rows = [];
  if (routine) {
    const core = coreWorkout(await app.vault.read(routine));
    if (core == null) new Notice(`Session Table: ${routine.basename} has no Core Workout section, so the table is empty.`, 10000);
    else rows = routineRows(core);
  }
  const lines = rows.length
    ? rows.map((row) => `| [[${row.name}]] | ${row.target} | ${row.sets} |  |  |  |`)
    : ["|  |  |  |  |  |  |"];
  await app.vault.process(target, (current) => {
    const trimmed = current.trimEnd();
    const gap = trimmed.endsWith("---") ? "\n" : "\n\n";
    return `${trimmed}${gap}${[...header, ...lines].join("\n")}\n\n${button.join("\n")}\n`;
  });
});
-%>

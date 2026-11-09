---
type: template
created: 2026-11-08
updated: 2026-11-08
version: "0.36"
---
<%*
// Session Table: writes a new session note's body from the routine in its
// `routine` property: one H1 section per routine section, each with its own
// table, then a button that runs Sync Last Performed:
//   # Warm-Up        the routine's Warm-Up exercises
//   # Core Workout   the routine's Core Workout exercises
//   # Cool-Down      the routine's Cool-Down exercises
// Within each block of a section (an H2, e.g., a progression, or the whole
// section when it has none):
//   - Exercise: the highlighted items if there are any, else every item that
//               starts with a link. An item that doesn't start with one (e.g.,
//               "Alternative: [[…]]") isn't an exercise of its own.
//   - Target:   the item's text after " — " (e.g., "3x20"), or after its link
//               if it has no " — "
//   - Sets:     the number at the start of the block's `Sets:` line, if any
// Filling in the table, one row per exercise:
//   - Reps/Time/Distance: how much you did: reps (e.g., 20), a time (e.g., 45s
//     or 46:30), or a distance with its unit (e.g., 10 km)
//   - Weight/Pace: how hard: a weight with its unit (e.g., 185 lb) or a pace
//     (e.g., 7:28/mi). Blank for bodyweight
//   - Per set: one value for every set, or one per set separated by commas
//     (e.g., 20, 18, 15)
//   - A row counts once Reps/Time/Distance is filled. That's what an exercise's
//     Last Time and Sync Last Performed read, so a skipped row can stay empty.
// The Session Template includes it after Frontmatter, and Start Session
// includes it in the note it writes, so it runs once the note's properties
// are written. Never run it alone.
tR = "";

const { Notice, parseYaml } = tp.obsidian;
const target = tp.config.target_file;
// The vault root: from the template file, or from the note itself when the
// note was made from text (e.g., by Start Session).
const root = (tp.config.template_file?.path ?? target.path).split(/92 Templates\/|20 Hobbies\//)[0];
const sync = `${root}92 Templates/Automations/Sync Last Performed.md`;
const SECTIONS = ["Warm-Up", "Core Workout", "Cool-Down"];
const header = ["| Exercise | Target | Sets | Reps/Time/Distance | Weight/Pace | Notes |", "|---|---|---|---|---|---|"];
const button = [
  "```meta-bind-button",
  "label: Sync Last Performed",
  "style: primary",
  "actions:",
  "  - type: runTemplaterFile",
  `    templateFile: "${sync}"`,
  "```",
];

// The text of a routine's `# <name>` section, or null.
const sectionOf = (text, name) => {
  const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = text.match(new RegExp(`^# ${escaped}[ \\t]*\\r?\\n([\\s\\S]*?)(?=^# |(?![\\s\\S]))`, "m"));
  return match ? match[1] : null;
};

// One row per exercise in a routine section: { name, target, sets }.
const routineRows = (section) => {
  const rows = [];
  for (const block of section.split(/^#{2,6}\s.*$/m)) {
    const lines = block.split("\n");
    const sets = lines.map((line) => line.match(/^\s*Sets:\s*(\d+)/)?.[1]).find(Boolean) ?? "";
    const items = lines.filter((line) => /^\s*(?:[-*+]|\d+[.)])\s+(?:==)?\[\[/.test(line));
    const current = items.filter((line) => /==.*\[\[.*==/.test(line));
    for (const line of current.length ? current : items) {
      const name = line.match(/\[\[([^\]|#]+)/)?.[1].trim();
      if (!name) continue;
      const rest = line.replaceAll("==", "").split("]]").slice(1).join("]]");
      const after = (rest.includes(" — ") ? rest.split(" — ").slice(1).join(" — ") : rest).trim()
        .replace(/^[,;:—–-]+\s*/, "").replace(/^\(([^()]*)\)$/, "$1").replaceAll("|", "\\|");
      rows.push({ name, target: after, sets });
    }
  }
  return rows;
};

// A section of the session note: its heading and table.
const sessionSection = (name, rows) => {
  const lines = rows.length
    ? rows.map((row) => `| [[${row.name}]] | ${row.target} | ${row.sets} |  |  |  |`)
    : ["|  |  |  |  |  |  |"];
  return [`# ${name}`, "", ...header, ...lines].join("\n");
};

tp.hooks.on_all_templates_executed(async () => {
  // Read the note directly, since Obsidian may not have indexed it yet.
  const text = await app.vault.read(target);
  const block = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  let fm = {};
  try {
    fm = block ? parseYaml(block[1]) ?? {} : {};
  } catch (error) {
    new Notice("Session Table: couldn't read this note's properties, so the tables are empty.", 10000);
  }
  const linkpath = String(fm.routine ?? "").replace(/^\s*\[\[|\]\]\s*$/g, "").split("|")[0].split("#")[0].trim();
  const routine = linkpath ? app.metadataCache.getFirstLinkpathDest(linkpath, target.path) : null;
  if (linkpath && !routine) new Notice(`Session Table: ${linkpath} doesn't exist yet, so the tables are empty.`, 10000);
  const routineText = routine ? await app.vault.read(routine) : "";
  const missing = [];
  const sections = SECTIONS.map((name) => {
    const section = routine ? sectionOf(routineText, name) : null;
    if (routine && section == null) missing.push(name);
    return sessionSection(name, section == null ? [] : routineRows(section));
  });
  if (missing.length) new Notice(`Session Table: ${routine.basename} has no ${missing.join(" or ")} section, so that table is empty.`, 10000);
  await app.vault.process(target, (current) => {
    const trimmed = current.trimEnd();
    const gap = trimmed.endsWith("---") ? "\n" : "\n\n";
    return `${trimmed}${gap}${sections.join("\n\n")}\n\n${button.join("\n")}\n`;
  });
});
-%>

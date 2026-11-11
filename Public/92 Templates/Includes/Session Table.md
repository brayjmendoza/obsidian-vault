---
type: template
created: 2026-11-08
updated: 2026-11-11
version: "0.39"
---
<%*
// Session Table: writes a new session note's body from the routine in its
// `routine` property: one H1 section per routine section, each with its own
// table, then a button that runs Sync Last Performed. It reads only the
// routine's Warm-Up, Core Workout, and Cool-Down sections above its first
// `---`, in the Routine Template's format:
//   - Exercise: every list item that starts with a link. A sub-bullet whose
//               label is in LABELS is one of its fields, and any other line
//               (e.g., "Progression: [[…]]") is a note for you.
//   - Fields:   `Label: value`, inline after " — " and separated by commas, or
//               one per sub-bullet. A comma starts a new field only when a
//               label follows it, so "Reps: 20, 18, 15" stays one field.
//   - Block:    a field line under a block's heading (e.g., `Format: circuit,
//               Rounds: 3, Rest: 2 min`) gives Sets, Rest, and Format to every
//               exercise in the block that doesn't set its own.
// Each table's columns, in this order:
//   Exercise | Target | Sets | <volume> | <intensity> | Rest | Notes
//   - Target:    sets x volume @ intensity, then any detail and format
//                (e.g., "3x12, no kip" or "10 km @ ~7:30/mi")
//   - Sets:      only if an exercise in the table sets it, and 1 for the rest
//   - volume:    always, named for the labels used (e.g., "Reps" or
//                "Reps/Time"). You log what you did here, and a row counts
//                once it's filled
//   - intensity: only if an exercise sets it, named the same way (e.g., "Pace")
//   - Rest:      only if an exercise sets it, filled from the routine
// Last Time (93 Views/Scripts/last-time.js) and Sync Last Performed find the
// volume column as the first that isn't Exercise, Target, Sets, Rest, or
// Notes, and intensity as the next: keep the three in step.
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
const button = [
  "```meta-bind-button",
  "label: Sync Last Performed",
  "style: primary",
  "actions:",
  "  - type: runTemplaterFile",
  `    templateFile: "${sync}"`,
  "```",
];

// Every field label, by category. The Routine Template's placeholders (e.g.,
// Volume and Intensity) are labels too.
const LABELS = {
  sets: ["Sets", "Rounds"],
  volume: ["Volume", "Reps", "Time", "Distance", "Duration"],
  intensity: ["Intensity", "Weight", "Load", "Pace", "Speed", "Assistance", "RPE", "Heart Rate", "HR", "Zone", "Incline"],
  rest: ["Rest"],
  detail: ["Detail", "Cue", "Tempo", "Grip", "Stroke"],
  format: ["Format"],
};
const escape = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const CATEGORY = new Map(Object.entries(LABELS).flatMap(([category, labels]) => labels.map((label) => [label.toLowerCase(), category])));
const labelPattern = Object.values(LABELS).flat().sort((a, b) => b.length - a.length).map(escape).join("|");
const FIELD = new RegExp(`(?:^|,\\s*)(${labelPattern})\\s*:\\s*`, "gi");
const ITEM = /^([\t ]*)(?:[-*+]|\d+[.)])\s+(.*)$/;

// A table cell: a `|` would end the cell, so it's escaped (e.g., in a link's alias).
const cell = (text) => String(text ?? "").replaceAll("|", "\\|");
const indentOf = (line) => line.match(/^[\t ]*/)[0].replaceAll("\t", "    ").length;

// The fields in a line of text: { lead, fields }, where lead is any text before the first label.
const parseFields = (text) => {
  const matches = [...text.matchAll(FIELD)];
  const lead = (matches.length ? text.slice(0, matches[0].index) : text).trim();
  const fields = matches
    .map((match, i) => ({
      category: CATEGORY.get(match[1].toLowerCase()),
      label: match[1],
      value: text.slice(match.index + match[0].length, matches[i + 1]?.index ?? text.length).trim(),
    }))
    .filter((field) => field.value);
  return { lead, fields };
};

// The part of a routine scripts read: its body above the first `---`.
const workoutOf = (text) => {
  const body = text.replace(/\r\n/g, "\n").replace(/^---\n[\s\S]*?\n---[ \t]*(?:\n|$)/, "");
  const rule = body.search(/^[ \t]*(?:(?:-[ \t]*){3,}|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,})$/m);
  return rule >= 0 ? body.slice(0, rule) : body;
};

// The text of a routine's `# <name>` section, or null.
const sectionOf = (text, name) => {
  const match = text.match(new RegExp(`^# ${escape(name)}[ \\t]*\\n([\\s\\S]*?)(?=^# |(?![\\s\\S]))`, "m"));
  return match ? match[1] : null;
};

// One exercise's table row, from its own fields and its block's.
const toRow = (exercise, blockFields) => {
  const own = new Set(exercise.fields.map((field) => field.category));
  const inherited = blockFields.filter((field) => ["sets", "rest", "format"].includes(field.category) && !own.has(field.category));
  const fields = [...exercise.fields, ...inherited];
  const of = (category) => fields.filter((field) => field.category === category);
  const joined = (category) => of(category).map((field) => field.value).join(", ");
  const sets = joined("sets");
  const volume = of("volume");
  const volumeText = joined("volume");
  const intensity = joined("intensity");
  let main = volumeText;
  if (sets && volume.length === 1 && !volumeText.includes(",")) main = `${sets}x${volumeText}`;
  else if (sets && volumeText) main = `${sets} sets of ${volumeText}`;
  else if (sets) main = `${sets} sets`;
  if (intensity) main = main ? `${main} @ ${intensity}` : intensity;
  return {
    name: exercise.name,
    target: [main, exercise.lead, joined("detail"), joined("format")].filter(Boolean).join(", "),
    sets,
    rest: joined("rest"),
    volumeLabels: volume.map((field) => field.label),
    intensityLabels: of("intensity").map((field) => field.label),
  };
};

// One row per exercise in a routine section.
const routineRows = (section) => {
  const rows = [];
  for (const block of section.split(/^#{2,6}\s.*$/m)) {
    const exercises = [];
    const blockFields = [];
    let current = null;
    for (const line of block.split("\n")) {
      if (!line.trim()) continue;
      const item = line.match(ITEM);
      const indent = indentOf(line);
      if (current && indent > current.indent) {
        if (item) {
          const { lead, fields } = parseFields(item[2]);
          if (!lead) current.fields.push(...fields);
        }
        continue;
      }
      current = null;
      if (!item) {
        const { lead, fields } = parseFields(line.trim());
        if (!lead) blockFields.push(...fields);
        continue;
      }
      const content = item[2].replaceAll("==", "");
      const link = content.match(/^\[\[([^\]|#]+)[^\]]*\]\]/);
      if (!link) continue;
      const after = content.slice(link[0].length);
      const dash = after.indexOf(" — ");
      const parsed = dash >= 0 ? parseFields(after.slice(dash + 3)) : { lead: "", fields: [] };
      current = { indent, name: link[1].trim(), lead: parsed.lead, fields: parsed.fields };
      exercises.push(current);
    }
    rows.push(...exercises.map((exercise) => toRow(exercise, blockFields)));
  }
  return rows;
};

// Labels joined for a header, each once and in LABELS order (e.g., "Reps/Time").
const ORDER = Object.values(LABELS).flat().map((label) => label.toLowerCase());
const headerOf = (labels) => [...new Map(labels.map((label) => [label.toLowerCase(), label])).entries()]
  .sort(([a], [b]) => ORDER.indexOf(a) - ORDER.indexOf(b))
  .map(([, label]) => label)
  .join("/");

// A section of the session note: its heading and table.
const sessionSection = (name, rows) => {
  const hasSets = rows.some((row) => row.sets);
  const hasRest = rows.some((row) => row.rest);
  const volume = headerOf(rows.flatMap((row) => row.volumeLabels)) || "Reps/Time/Distance";
  const intensity = headerOf(rows.flatMap((row) => row.intensityLabels));
  const header = ["Exercise", "Target", ...(hasSets ? ["Sets"] : []), volume, ...(intensity ? [intensity] : []), ...(hasRest ? ["Rest"] : []), "Notes"];
  const line = (cells) => `| ${cells.join(" | ")} |`;
  const body = rows.length
    ? rows.map((row) => line([
      `[[${row.name}]]`,
      cell(row.target),
      ...(hasSets ? [cell(row.sets || "1")] : []),
      "",
      ...(intensity ? [""] : []),
      ...(hasRest ? [cell(row.rest)] : []),
      "",
    ]))
    : [line(header.map(() => ""))];
  return [`# ${name}`, "", line(header), line(header.map(() => "---")), ...body].join("\n").replace(/ {2,}\|/g, "  |");
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
  const workout = routine ? workoutOf(await app.vault.read(routine)) : "";
  const missing = [];
  const sections = SECTIONS.map((name) => {
    const section = routine ? sectionOf(workout, name) : null;
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

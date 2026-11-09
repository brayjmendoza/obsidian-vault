---
type: template
created: 2026-11-08
updated: 2026-11-08
version: "0.31"
---
<%*
// Sync Last Performed: keeps each exercise's `last_performed` at the latest date
// of the session notes that log it. A session logs an exercise when the
// exercise's row in its table has Reps/Time/Distance filled (CONVENTIONS.md section 5), so a
// new session note, whose table is still empty, changes nothing. Dates only move
// forward, so a later date you set by hand is kept. Run it on its own
// (Templater: Insert template, on any note) after logging a workout. It checks
// every session note in the vault. Session notes in 91 Tooling/ (test vaults)
// are skipped. The Last Time script (90 System/Scripts/last-time.js) reads
// session tables the same way: keep the two in step.
tR = "";

const { Notice } = tp.obsidian;
const today = tp.date.now("YYYY-MM-DD");
const root = tp.config.template_file.path.split("90 System/")[0];
const frontmatter = (file) => app.metadataCache.getFileCache(file)?.frontmatter ?? {};
const inTooling = (file) => file.path.startsWith(`${root}91 Tooling/`);

// A YAML date as YYYY-MM-DD, or null.
const isoDate = (value) => {
  if (value instanceof Date) return Number.isNaN(value.getTime()) ? null : value.toISOString().slice(0, 10);
  const text = String(value ?? "").trim().slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(text) ? text : null;
};

// The cells of a table row. A `\|` inside a link (i.e., an alias) isn't a column break.
const cellsOf = (line) => line.trim().replace(/^\||\|$/g, "").split(/(?<!\\)\|/).map((cell) => cell.trim());

// The exercise notes a session note's tables log, i.e., rows with Reps/Time/Distance filled.
const loggedExercises = (text, source) => {
  const exercises = [];
  let columns = null;
  for (const line of text.split("\n")) {
    if (!line.trim().startsWith("|")) {
      columns = null;
      continue;
    }
    const cells = cellsOf(line);
    if (!columns) {
      columns = cells.map((cell) => cell.toLowerCase());
      continue;
    }
    if (cells.every((cell) => /^:?-+:?$/.test(cell))) continue;
    const cell = (name) => cells[columns.findIndex((column) => column.startsWith(name))] ?? "";
    if (!columns.includes("exercise") || !cell("reps")) continue;
    const linkpath = cell("exercise").match(/\[\[([^\]]+?)\]\]/)?.[1].split(/\\?\|/)[0].split("#")[0].trim();
    const file = linkpath && app.metadataCache.getFirstLinkpathDest(linkpath, source.path);
    if (file && !inTooling(file) && frontmatter(file).type === "exercise") exercises.push(file);
  }
  return exercises;
};

// Latest logged date per exercise, keyed by path, across every session note.
const latest = new Map();
const sessions = app.vault.getMarkdownFiles()
  .filter((file) => !inTooling(file) && frontmatter(file).type === "session");
for (const session of sessions) {
  const date = isoDate(frontmatter(session).date);
  if (!date) continue;
  for (const exercise of loggedExercises(await app.vault.cachedRead(session), session)) {
    const seen = latest.get(exercise.path);
    if (!seen || seen.date < date) latest.set(exercise.path, { exercise, date });
  }
}

// Move each exercise's `last_performed` forward to its date.
const changed = [];
for (const { exercise, date } of latest.values()) {
  await app.fileManager.processFrontMatter(exercise, (fm) => {
    const current = isoDate(fm.last_performed);
    if (current && current >= date) return;
    fm.last_performed = date;
    fm.updated = today;
    changed.push(exercise.basename);
  });
}

const names = changed.length > 3 ? `${changed.slice(0, 3).join(", ")}, and ${changed.length - 3} more` : changed.join(", ");
new Notice(changed.length
  ? `Sync Last Performed: updated ${names}.`
  : "Sync Last Performed: every exercise is already up to date.", 8000);
-%>

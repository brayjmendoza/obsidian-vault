// Last Time: shows this exercise's sets from the latest session note that logs it.
// An exercise note runs it in its Last Time section:
//   ```dataviewjs
//   await dv.view("Public/93 Views/Scripts/last-time")
//   ```
// A session row counts once its Reps/Time/Distance cell is filled (CONVENTIONS.md
// section 5). Columns are found by the start of their header (e.g., "reps" or
// "weight"), so older tables with Reps and Weight (lb) headers still read.
// Sync Last Performed reads session tables the same way: keep the two in step.

const here = dv.current().file.path;

// The cells of a table row. A `\|` inside a link (i.e., an alias) isn't a column break.
const cellsOf = (line) => line.trim().replace(/^\||\|$/g, "").split(/(?<!\\)\|/).map((cell) => cell.trim());

// The note a cell's first wikilink points to, as a path, or null.
const linkedPath = (cell, from) => {
  const match = cell.match(/\[\[([^\]]+?)\]\]/);
  if (!match) return null;
  const linkpath = match[1].split(/\\?\|/)[0].split("#")[0].trim();
  return app.metadataCache.getFirstLinkpathDest(linkpath, from)?.path ?? null;
};

// This exercise's logged rows in a session note's tables.
const loggedRows = (text, from) => {
  const rows = [];
  let columns = null;
  let labels = null;
  for (const line of text.split("\n")) {
    if (!line.trim().startsWith("|")) {
      columns = null;
      continue;
    }
    const cells = cellsOf(line);
    if (!columns) {
      labels = cells;
      columns = cells.map((cell) => cell.toLowerCase());
      continue;
    }
    if (cells.every((cell) => /^:?-+:?$/.test(cell))) continue;
    const cell = (name) => cells[columns.findIndex((column) => column.startsWith(name))] ?? "";
    if (!columns.includes("exercise") || !cell("reps")) continue;
    if (linkedPath(cell("exercise"), from) !== here) continue;
    const label = (name) => labels[columns.findIndex((column) => column.startsWith(name))] ?? name;
    rows.push({
      sets: cell("sets"), reps: cell("reps"), weight: cell("weight"), notes: cell("notes"),
      repsLabel: label("reps"), weightLabel: label("weight"),
    });
  }
  return rows;
};

// One value per set: "20, 18, 15" stays as is, and "20" over 3 sets is 20 three times.
const perSet = (value, count) => {
  const items = value.split(",").map((item) => item.trim()).filter(Boolean);
  return items.length === 1 && count > 1 ? Array(count).fill(items[0]) : items;
};

const sessions = dv.pages('-"91 Tooling"')
  .where((page) => page.type === "session" && page.date && page.file.outlinks.some((link) => link.path === here))
  .sort((page) => `${page.date} ${page.file.name}`, "desc");

let shown = false;
for (const page of sessions) {
  const rows = loggedRows(await dv.io.load(page.file.path), page.file.path);
  if (!rows.length) continue;
  dv.paragraph(dv.fileLink(page.file.path));
  for (const row of rows) {
    const count = Number.parseInt(row.sets, 10) || 0;
    const reps = perSet(row.reps, count);
    const weight = perSet(row.weight, count);
    const total = Math.max(count, reps.length, weight.length);
    const sets = Array.from({ length: total }, (_, i) => [i + 1, reps[i] ?? "", weight[i] ?? ""]);
    if (weight.length) dv.table(["Set", row.repsLabel, row.weightLabel], sets);
    else dv.table(["Set", row.repsLabel], sets.map(([set, rep]) => [set, rep]));
    if (row.notes) dv.paragraph(row.notes);
  }
  shown = true;
  break;
}
if (!shown) dv.paragraph("Not logged yet.");

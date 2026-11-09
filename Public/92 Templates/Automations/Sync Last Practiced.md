---
type: template
created: 2026-11-07
updated: 2026-11-08
version: "0.36"
---
<%*
// Sync Last Practiced: keeps each piece's `last_practiced` at the latest date of
// the practice notes that list it in `pieces`. Dates only move forward, so a
// later date you set by hand is kept. The template that runs it picks the mode:
//   Practice Template    includes it, so creating a practice note updates the
//                        pieces it lists, once the note is written.
//   Sync Last Practiced  run on its own (Templater: Insert template, on any
//                        note), it checks every practice note in the vault,
//                        e.g., after adding pieces to an old practice note.
// Practice notes in 91 Tooling/ (test vaults) are skipped.
tR = "";

const { Notice, parseYaml } = tp.obsidian;
const today = tp.date.now("YYYY-MM-DD");
const outer = tp.config.template_file;
const target = tp.config.target_file;
const root = outer.path.split("92 Templates/")[0];
const frontmatter = (file) => app.metadataCache.getFileCache(file)?.frontmatter ?? {};
const inTooling = (file) => file.path.startsWith(`${root}91 Tooling/`);

// A YAML date as YYYY-MM-DD, or null.
const isoDate = (value) => {
  if (value instanceof Date) return Number.isNaN(value.getTime()) ? null : value.toISOString().slice(0, 10);
  const text = String(value ?? "").trim().slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(text) ? text : null;
};

// The piece notes a practice note's `pieces` links to.
const linkedPieces = (pieces, source) => [].concat(pieces ?? []).flatMap((link) => {
  const linkpath = String(link).replace(/^\s*\[\[|\]\]\s*$/g, "").split("|")[0].split("#")[0].trim();
  const file = linkpath && app.metadataCache.getFirstLinkpathDest(linkpath, source.path);
  return file && !inTooling(file) && frontmatter(file).type === "piece" ? [file] : [];
});

// Latest practice date per piece, from a list of { file, fm } practice notes.
const latestDates = (practices) => {
  const latest = new Map();
  for (const { file, fm } of practices) {
    const date = isoDate(fm.date);
    if (fm.type !== "practice" || !date) continue;
    for (const piece of linkedPieces(fm.pieces, file)) {
      if (!latest.has(piece) || latest.get(piece) < date) latest.set(piece, date);
    }
  }
  return latest;
};

// Moves each piece's `last_practiced` forward to its date. Returns the pieces changed.
const apply = async (latest) => {
  const changed = [];
  for (const [piece, date] of latest) {
    await app.fileManager.processFrontMatter(piece, (fm) => {
      const current = isoDate(fm.last_practiced);
      if (current && current >= date) return;
      fm.last_practiced = date;
      fm.updated = today;
      changed.push(piece.basename);
    });
  }
  return changed;
};

const report = (changed, scope) => {
  const names = changed.length > 3 ? `${changed.slice(0, 3).join(", ")}, and ${changed.length - 3} more` : changed.join(", ");
  new Notice(changed.length
    ? `Sync Last Practiced: updated ${names}.`
    : `Sync Last Practiced: ${scope} already up to date.`, 8000);
};

if (outer.basename === "Sync Last Practiced") {
  // Run on its own: every practice note in the vault.
  const practices = app.vault.getMarkdownFiles()
    .filter((file) => !inTooling(file) && frontmatter(file).type === "practice")
    .map((file) => ({ file, fm: frontmatter(file) }));
  report(await apply(latestDates(practices)), "every piece is");
} else {
  // Included by a template: the note it's creating, once its properties are written.
  // The file is read directly, since Obsidian may not have indexed it yet.
  tp.hooks.on_all_templates_executed(async () => {
    const text = await app.vault.read(target);
    const block = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    let fm = {};
    try {
      fm = block ? parseYaml(block[1]) ?? {} : {};
    } catch (error) {
      new Notice("Sync Last Practiced: couldn't read this note's properties, so no pieces were updated.", 10000);
      return;
    }
    const latest = latestDates([{ file: target, fm }]);
    if (latest.size) report(await apply(latest), "its pieces are");
  });
}
-%>
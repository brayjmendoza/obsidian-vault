---
type: template
created: 2026-11-11
updated: 2026-11-11
version: "0.39"
---
<%*
// Sync Last Cooked: keeps each recipe's `last_cooked` at the latest date of the
// meal notes that list it in `recipes`. Dates only move forward, so a
// later date you set by hand is kept. The template that runs it picks the mode:
//   Meal Template        includes it, so creating a meal note updates the
//                        recipes it lists, once the note is written.
//   Sync Last Cooked     run on its own (Templater: Insert template, on any
//                        note), it checks every meal note in the vault,
//                        e.g., after adding recipes to an old meal note.
// Meal notes in 91 Tooling/ (test vaults) are skipped.
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

// The recipe notes a meal note's `recipes` links to.
const linkedRecipes = (recipes, source) => [].concat(recipes ?? []).flatMap((link) => {
  const linkpath = String(link).replace(/^\s*\[\[|\]\]\s*$/g, "").split("|")[0].split("#")[0].trim();
  const file = linkpath && app.metadataCache.getFirstLinkpathDest(linkpath, source.path);
  return file && !inTooling(file) && frontmatter(file).type === "recipe" ? [file] : [];
});

// Latest meal date per recipe, from a list of { file, fm } meal notes.
const latestDates = (meals) => {
  const latest = new Map();
  for (const { file, fm } of meals) {
    const date = isoDate(fm.date);
    if (fm.type !== "meal" || !date) continue;
    for (const recipe of linkedRecipes(fm.recipes, file)) {
      if (!latest.has(recipe) || latest.get(recipe) < date) latest.set(recipe, date);
    }
  }
  return latest;
};

// Moves each recipe's `last_cooked` forward to its date. Returns the recipes changed.
const apply = async (latest) => {
  const changed = [];
  for (const [recipe, date] of latest) {
    await app.fileManager.processFrontMatter(recipe, (fm) => {
      const current = isoDate(fm.last_cooked);
      if (current && current >= date) return;
      fm.last_cooked = date;
      fm.updated = today;
      changed.push(recipe.basename);
    });
  }
  return changed;
};

const report = (changed, scope) => {
  const names = changed.length > 3 ? `${changed.slice(0, 3).join(", ")}, and ${changed.length - 3} more` : changed.join(", ");
  new Notice(changed.length
    ? `Sync Last Cooked: updated ${names}.`
    : `Sync Last Cooked: ${scope} already up to date.`, 8000);
};

if (outer.basename === "Sync Last Cooked") {
  // Run on its own: every meal note in the vault.
  const meals = app.vault.getMarkdownFiles()
    .filter((file) => !inTooling(file) && frontmatter(file).type === "meal")
    .map((file) => ({ file, fm: frontmatter(file) }));
  report(await apply(latestDates(meals)), "every recipe is");
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
      new Notice("Sync Last Cooked: couldn't read this note's properties, so no recipes were updated.", 10000);
      return;
    }
    const latest = latestDates([{ file: target, fm }]);
    if (latest.size) report(await apply(latest), "its recipes are");
  });
}
-%>
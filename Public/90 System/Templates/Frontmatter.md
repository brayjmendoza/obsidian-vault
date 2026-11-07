---
type: template
created: 2026-11-07
updated: 2026-11-07
version: "0.12"
---
<%*
// Frontmatter: the property engine every type template includes. It reads
// properties-schema.yaml each run, so a schema change reaches every template.
// The template that includes it picks the mode:
//   <Type> Template  writes a new note's properties: each required property is
//                    prompted for, then optional ones are offered from a list.
//   Add Properties   adds properties to the current note: any missing required
//                    ones, then optional ones it doesn't have yet.

// Drop this file's own properties (type: template) from the output.
tR = "";

const { Notice, parseYaml } = tp.obsidian;
const today = tp.date.now("YYYY-MM-DD");
const outer = tp.config.template_file;
const target = tp.config.target_file;
const root = outer.path.split("90 System/")[0];
const frontmatter = (file) => app.metadataCache.getFileCache(file)?.frontmatter ?? {};
const fail = (message) => {
  new Notice(`Frontmatter: ${message}`, 10000);
  throw new Error(message);
};

let schema;
try {
  schema = parseYaml(await app.vault.adapter.read(`${root}91 Tooling/schemas/properties-schema.yaml`));
} catch (error) {
  fail("couldn't read 91 Tooling/schemas/properties-schema.yaml.");
}
const kinds = schema.property_types;
const vocab = (name) => schema.vocabularies[name] ?? [];

// --- Which note type ---------------------------------------------------------
const adding = outer.basename === "Add Properties";
const current = adding ? { ...frontmatter(target) } : {};
let noteType = adding ? current.type : outer.basename.replace(/ Template$/, "").toLowerCase();
if (adding && !noteType) {
  const types = vocab("note_type").filter((t) => t !== "template");
  noteType = await tp.system.suggester(types, types, false, "This note has no type yet. Pick one");
  if (!noteType) fail("no type picked, so nothing was added.");
}
const spec = schema.types?.[noteType];
if (!spec) fail(`"${noteType}" isn't a note type in the properties schema. Run a <Type> Template or Add Properties instead.`);

const constraints = { ...(schema.common.constraints ?? {}), ...(spec.constraints ?? {}) };
const required = [...schema.common.required, ...(spec.required ?? [])];
const optional = [...(spec.optional ?? []), ...(schema.common.optional ?? [])];

// --- Values the engine fills in without asking -------------------------------
const title = target.basename;
const automatic = {
  type: noteType,
  created: today,
  updated: today,
  version: schema.version,
  // Log notes carry their date in the filename (e.g., 2026-11-07 Practice).
  date: title.match(/^\d{4}-\d{2}-\d{2}/)?.[0],
  week: title.match(/^\d{4}-W\d{2}/)?.[0],
  month: title.match(/^\d{4}-\d{2}(?![-\d])/)?.[0],
};

// Hints for free-text properties, shown in the prompt.
const hints = {
  lived: "e.g., 1810-1849, or 1946-Present",
  week: "e.g., 2026-W45",
  month: "e.g., 2026-11",
  url: "one http or https URL",
  manual: "the attachment's name in 98 Attachments/, e.g., 2026-11-07 Dishwasher Manual.pdf",
  grade: "e.g., ABRSM Grade 7",
  progress: "e.g., chapter 4, or 60%",
  outcome: "what done looks like",
  topic: "what the reference is about, e.g., cooking",
  venue: "where it was published, e.g., NeurIPS",
  version: "e.g., 0.12",
};

// What a property holds, for the optional list and the prompts.
const describe = (prop) => {
  const kind = kinds[prop];
  const c = constraints[prop] ?? {};
  const list = kind === "list" ? "list of " : "";
  if (c.vocab) {
    const values = vocab(c.vocab);
    const shown = values.length > 6 ? `${values.slice(0, 6).join(", ")}, …` : values.join(", ");
    return `${list}${shown}`;
  }
  if (c.link) return `${list}links to ${[].concat(c.link).join(" or ")} notes`;
  if (c.range) return `${kind}, ${c.range[0]}–${c.range[1]}`;
  return hints[prop] ? `${kind}, ${hints[prop]}` : kind;
};

// --- Asking for one value ----------------------------------------------------
// Each returns the value, or null when you press Esc or leave it blank.
const DONE = Symbol("done");
const NEW = Symbol("new");

async function pickMany(labels, values, label, extra = null) {
  const chosen = [];
  for (;;) {
    const left = values.map((v, i) => i).filter((i) => !chosen.includes(values[i]));
    const options = ["Done", ...left.map((i) => labels[i])];
    const results = [DONE, ...left.map((i) => values[i])];
    if (extra) {
      options.push(extra.label);
      results.push(NEW);
    }
    if (options.length === 1) break;
    let value = await tp.system.suggester(options, results, false, `${label}: pick one at a time, then Done`);
    if (value == null || value === DONE) break;
    if (value === NEW) {
      value = await extra.ask();
      if (value == null) continue;
    }
    chosen.push(value);
  }
  return chosen.length ? chosen : null;
}

async function promptUntilValid(label, initial, parse) {
  let text = initial;
  for (;;) {
    text = (await tp.system.prompt(label, text, false))?.trim();
    if (!text) return null;
    const result = parse(text);
    if (result.ok) return result.value;
    new Notice(`Frontmatter: ${result.why}`, 6000);
  }
}

async function ask(prop, isRequired) {
  const kind = kinds[prop];
  const c = constraints[prop] ?? {};
  const label = `${noteType} · ${prop}${isRequired ? "" : " (optional)"} · ${describe(prop)}`;

  if (c.vocab) {
    const values = vocab(c.vocab);
    if (kind === "list") return pickMany(values, values, label);
    return tp.system.suggester(values, values, false, label);
  }

  if (c.link) {
    const types = [].concat(c.link);
    const notes = app.vault.getMarkdownFiles()
      .filter((f) => f !== target && types.includes(frontmatter(f).type))
      .sort((a, b) => a.basename.localeCompare(b.basename));
    const links = notes.map((f) => `[[${app.metadataCache.fileToLinktext(f, target.path, true)}]]`);
    const unwritten = {
      label: "A note not written yet: type its name",
      ask: async () => {
        const name = (await tp.system.prompt(`${prop}: name of the note`, "", false))?.trim();
        return name ? `[[${name}]]` : null;
      },
    };
    if (kind === "list") return pickMany(notes.map((f) => f.basename), links, label, unwritten);
    const value = await tp.system.suggester(
      [...notes.map((f) => f.basename), unwritten.label], [...links, NEW], false, label
    );
    return value === NEW ? unwritten.ask() : value;
  }

  switch (kind) {
    case "checkbox":
      return tp.system.suggester(["true", "false"], [true, false], false, label);
    case "number":
      return promptUntilValid(label, "", (text) => {
        const n = Number(text);
        if (Number.isNaN(n)) return { ok: false, why: `${prop} needs a number.` };
        if (c.range && (n < c.range[0] || n > c.range[1])) {
          return { ok: false, why: `${prop} must be ${c.range[0]}–${c.range[1]}.` };
        }
        return { ok: true, value: n };
      });
    case "date":
      return promptUntilValid(label, today, (text) =>
        /^\d{4}-\d{2}-\d{2}$/.test(text) && !Number.isNaN(Date.parse(text))
          ? { ok: true, value: text }
          : { ok: false, why: `${prop} needs a date written YYYY-MM-DD.` }
      );
    case "list":
      return promptUntilValid(`${label} (separate items with commas)`, "", (text) => {
        const items = text.split(",").map((s) => s.trim()).filter(Boolean);
        return { ok: true, value: items };
      });
    default:
      return promptUntilValid(label, "", (text) => {
        if (c.pattern && !new RegExp(c.pattern).test(text)) {
          return { ok: false, why: `${prop} doesn't match ${hints[prop] ?? c.pattern}.` };
        }
        if (prop === "manual" && !text.startsWith("[[")) return { ok: true, value: `[[${text}]]` };
        return { ok: true, value: text };
      });
  }
}

// --- Collect the values ------------------------------------------------------
const values = {};
const blank = [];
const has = (prop) => current[prop] != null && current[prop] !== "" &&
  !(Array.isArray(current[prop]) && current[prop].length === 0);

// Required properties: filled in automatically where possible, else asked for.
for (const prop of required) {
  if (has(prop)) continue;
  const value = automatic[prop] ?? (await ask(prop, true));
  if (value == null) blank.push(prop);
  else values[prop] = value;
}

// Optional properties: a list of the ones the note doesn't have, until Done.
for (;;) {
  const left = optional.filter((prop) => !has(prop) && !(prop in values));
  if (!left.length) break;
  const prop = await tp.system.suggester(
    ["Done", ...left.map((p) => `${p} · ${describe(p)}`)], [DONE, ...left], false,
    `${noteType}: add an optional property, or Done`
  );
  if (prop == null || prop === DONE) break;
  const value = await ask(prop, false);
  if (value != null) values[prop] = value;
}

// A required property left blank makes the note unfinished, so it's tagged inbox.
if (blank.length && !adding) {
  const tags = values.tags ?? [];
  if (!tags.includes("inbox")) values.tags = [...tags, "inbox"];
  new Notice(`Frontmatter: ${blank.join(", ")} left blank, so the note is tagged inbox.`, 10000);
} else if (blank.length) {
  new Notice(`Frontmatter: ${blank.join(", ")} still missing.`, 10000);
}

// --- Write them --------------------------------------------------------------
if (adding) {
  // Edit the existing note's properties once Templater has finished with it.
  tp.hooks.on_all_templates_executed(async () => {
    await app.fileManager.processFrontMatter(target, (fm) => {
      Object.assign(fm, values);
      if (Object.keys(values).length) fm.updated = today;
    });
  });
} else {
  // Properties in schema order: required, then optional, then common optional.
  const order = [...required, ...optional];
  const scalar = (prop, value) => {
    if (typeof value === "number" || typeof value === "boolean") return String(value);
    if (kinds[prop] === "date" || constraints[prop]?.vocab) return value;
    return JSON.stringify(value);   // quoted, so links and odd text stay text
  };
  const lines = ["---"];
  for (const prop of order.filter((p) => p in values)) {
    const value = values[prop];
    if (Array.isArray(value)) {
      lines.push(`${prop}:`, ...value.map((item) => `  - ${scalar(prop, item)}`));
    } else {
      lines.push(`${prop}: ${scalar(prop, value)}`);
    }
  }
  lines.push("---", "");
  tR += lines.join("\n");
}
-%>

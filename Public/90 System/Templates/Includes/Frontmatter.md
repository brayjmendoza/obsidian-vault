---
type: template
created: 2026-11-07
updated: 2026-11-08
version: "0.26"
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
// Notes you can link to: everything except 91 Tooling/, whose test vaults hold
// sample notes (e.g., a second Frédéric Chopin) that aren't yours.
const vaultNotes = () => app.vault.getMarkdownFiles()
  .filter((f) => !f.path.startsWith(`${root}91 Tooling/`));
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
  noteType = await tp.system.suggester(types, types, false, "This note has no type yet. What type is it?");
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

// --- Questions -----------------------------------------------------------------
// Every prompt is a question. A property can be asked differently by note type
// (e.g., `status` on a piece versus a trip); otherwise the shared question is used.
const questions = {
  type: "What type of note is this?",
  aliases: "What other names should this note go by?",
  tags: "Which tags does this note need?",
  claude: "Should Claude treat this note as read-only?",
  date: "What date is this for?",
  week: "Which week is this for?",
  month: "Which month is this for?",
  energy: "How was your energy?",
  sleep_hours: "How many hours did you sleep?",
  practice_minutes: "How many minutes did you practice?",
  exercise_minutes: "How many minutes did you exercise?",
  workouts: "How many workouts did you do?",
  spending_total: "How much did you spend in total, in USD?",
  status: "What's its status?",
  area: "Which domain hub does this project serve?",
  start: "When does it start?",
  due: "When is it due?",
  outcome: "What does done look like?",
  composers: "Who composed it, and who arranged it? (original composer first)",
  styles: "Which styles does this composer write in? (pick all that fit, e.g., classical and romantic)",
  lived: "When did this composer live?",
  difficulty: "How difficult is it?",
  grade: "What grade is it?",
  started: "When did you start it?",
  finished: "When did you finish it?",
  last_practiced: "When did you last practice it?",
  memorized: "Have you memorized it?",
  minutes: "How many minutes did you practice?",
  pieces: "Which pieces did you practice?",
  focus: "What did you focus on?",
  category: "What kind of technique is it?",
  resources: "Which resources help with it?",
  modality: "What kind of training is this routine?",
  goal: "What's the routine's goal?",
  routine: "Which routine did you follow?",
  kind: "What kind of workout was it?",
  duration_min: "How many minutes did the workout take?",
  muscle_groups: "Which muscle groups does it work?",
  equipment: "What equipment does it need?",
  last_performed: "When did you last do it?",
  end: "When does it end?",
  places: "Which places does the trip include?",
  companions: "Who's going with you?",
  budget: "What's the budget, in USD?",
  country: "Which country is it in?",
  city: "Which city is it in?",
  visited: "Have you been there?",
  first_visit: "When did you first visit?",
  rating: "How would you rate it?",
  authors: "Who wrote it?",
  year: "What year was it published?",
  fields: "Which fields does it belong to?",
  field: "Which field does this map cover?",
  url: "What's its URL?",
  venue: "Where was it published?",
  progress: "How far along are you?",
  sources: "Which sources did you learn it from?",
  confidence: "How well do you know it?",
  last_reviewed: "When did you last review it?",
  total: "How much did you spend this month, in USD?",
  topic: "What's it about?",
  review_by: "When should it be reviewed next?",
  purchased: "When did you buy it?",
  warranty_until: "When does the warranty end?",
  manual: "What's the manual's file called?",
  version: "Which conventions version does it match?",
};
const questionsByType = {
  daily: { date: "Which day is this note for?" },
  project: { status: "Where does the project stand?", start: "When did the project start?" },
  piece: { status: "Where are you with this piece?", started: "When did you start learning it?" },
  practice: { date: "When did you practice?" },
  session: { date: "When did you work out?" },
  exercise: { difficulty: "How hard is it for you right now?" },
  trip: { status: "Where is the trip in planning?", start: "When does the trip start?",
          end: "When does the trip end?", budget: "What's the trip's budget, in USD?" },
  place: { rating: "How much did you like it?" },
  paper: { status: "Where are you in reading it?" },
  book: { status: "Where are you in reading it?" },
  course: { status: "Where are you in the course?", authors: "Who teaches it?", year: "What year is it from?" },
  article: { status: "Where are you in reading it?", year: "What year was it published?" },
  spending: { month: "Which month does this spending cover?", budget: "What was this month's budget, in USD?" },
  account: { url: "What's the account's website?", review_by: "When should you next review this account?" },
  asset: { url: "What's the product's web page?" },
  contractor: { url: "What's their website?" },
  benefit: { review_by: "When should you next review this election?" },
  log: { date: "When did this happen?" },
  reference: { url: "Which web page does it point to?" },
};

// Examples for free-text properties, shown after the question.
const hints = {
  lived: "e.g., 1810-1849, or 1946-Present",
  week: "e.g., 2026-W45",
  month: "e.g., 2026-11",
  manual: "e.g., 2026-11-07 Dishwasher Manual.pdf in 98 Attachments/",
  grade: "e.g., ABRSM Grade 7",
  progress: "e.g., chapter 4, or 60%",
  topic: "e.g., cooking",
  venue: "e.g., NeurIPS",
  version: "e.g., 0.12",
};

// The question for a property, with any notes in parentheses, e.g.,
// "When did this composer live? (e.g., 1810-1849, or 1946-Present)".
const question = (prop, isRequired, extra = []) => {
  const kind = kinds[prop];
  const c = constraints[prop] ?? {};
  const text = questionsByType[noteType]?.[prop] ?? questions[prop] ??
    `What's its ${prop.replaceAll("_", " ")}?`;
  const notes = isRequired ? [] : ["optional"];
  if (c.range) notes.push(`${c.range[0]}–${c.range[1]}`);
  else if (hints[prop]) notes.push(hints[prop]);
  else if (kind === "date") notes.push("YYYY-MM-DD");
  notes.push(...extra);
  return notes.length ? `${text} (${notes.join(", ")})` : text;
};

// What a property holds, shown beside it in the list of optional properties.
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
const PICK_MANY = "pick one at a time, then Done";

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
    let value = await tp.system.suggester(options, results, false, label);
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
    new Notice(result.why, 6000);
  }
}

async function ask(prop, isRequired) {
  const kind = kinds[prop];
  const c = constraints[prop] ?? {};
  const many = kind === "list" && (c.vocab || c.link);
  const label = question(prop, isRequired, many ? [PICK_MANY] : kind === "list" ? ["separate with commas"] : []);

  if (c.vocab) {
    const values = vocab(c.vocab);
    if (kind === "list") return pickMany(values, values, label);
    return tp.system.suggester(values, values, false, label);
  }

  if (c.link) {
    const types = [].concat(c.link);
    const notes = vaultNotes()
      .filter((f) => f !== target && types.includes(frontmatter(f).type))
      .sort((a, b) => a.basename.localeCompare(b.basename));
    // A bare name, unless two of your notes share it.
    const shared = (f) => notes.filter((g) => g.basename === f.basename).length > 1;
    const linktext = (f) => (shared(f) ? app.metadataCache.fileToLinktext(f, target.path, true) : f.basename);
    const links = notes.map((f) => `[[${linktext(f)}]]`);
    const unwritten = {
      label: "A note not written yet: type its name",
      ask: async () => {
        const name = (await tp.system.prompt(`What's the name of the ${types.join(" or ")} note to link?`, "", false))?.trim();
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
      return tp.system.suggester(["Yes", "No"], [true, false], false, label);
    case "number":
      return promptUntilValid(label, "", (text) => {
        const n = Number(text);
        if (Number.isNaN(n)) return { ok: false, why: "That isn't a number. Try again." };
        if (c.range && (n < c.range[0] || n > c.range[1])) {
          return { ok: false, why: `That's outside ${c.range[0]}–${c.range[1]}. Try again.` };
        }
        return { ok: true, value: n };
      });
    case "date":
      return promptUntilValid(label, today, (text) =>
        /^\d{4}-\d{2}-\d{2}$/.test(text) && !Number.isNaN(Date.parse(text))
          ? { ok: true, value: text }
          : { ok: false, why: "Dates are written YYYY-MM-DD. Try again." }
      );
    case "list":
      return promptUntilValid(label, "", (text) => {
        const items = text.split(",").map((s) => s.trim()).filter(Boolean);
        return { ok: true, value: items };
      });
    default:
      return promptUntilValid(label, "", (text) => {
        if (c.pattern && !new RegExp(c.pattern).test(text)) {
          return { ok: false, why: `That doesn't fit the format${hints[prop] ? ` (${hints[prop]})` : ""}. Try again.` };
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
    "Do you want to add an optional property? (pick one at a time, then Done)"
  );
  if (prop == null || prop === DONE) break;
  const value = await ask(prop, false);
  if (value != null) values[prop] = value;
}

// --- Name the note -------------------------------------------------------------
// New notes only. A note that already has a name fitting its type keeps it.
// Names fully set by properties (e.g., a practice log's date) are filled in;
// otherwise you're asked for the part of the name that isn't a property.
let unnamed = false;
if (!adding) {
  let structure = null;
  try {
    structure = parseYaml(await app.vault.adapter.read(`${root}91 Tooling/schemas/structure-schema.yaml`));
  } catch (error) {
    new Notice("Frontmatter: couldn't read structure-schema.yaml, so names aren't checked against it.", 10000);
  }
  const source = structure?.filenames?.[noteType];
  const pattern = source ? new RegExp(source) : null;
  const forbidden = /[#^[\]|\\:/]/;
  const folder = target.parent?.path ?? "";
  const taken = (name) => {
    const file = app.vault.getAbstractFileByPath(`${folder ? `${folder}/` : ""}${name}.md`);
    return file && file !== target;
  };
  const check = (name) => {
    if (forbidden.test(name)) return "Names can't use # ^ [ ] | \\ : or /. Try again.";
    if (pattern && !pattern.test(name)) return `That doesn't fit the pattern for ${noteType} notes. Try again.`;
    if (taken(name)) return `${name} already exists here. Try another name.`;
    return null;
  };

  // The last word of a name or link, e.g., "[[Frédéric Chopin]]" → "Chopin".
  const surname = (value) => String(value ?? "")
    .replace(/^\[\[|\]\]$/g, "").split("|")[0].split("/").pop().trim().split(/\s+/).pop();
  const thisMonth = tp.date.now("YYYY-MM");
  const examples = {
    daily: "2026-11-07", weekly: "2026-W45", monthly: "2026-11",
    practice: "2026-11-07 Practice",
    session: "2026-11-07 Workout", trip: "2026-11 Kyoto",
    place: "Kyoto, Japan", paper: "Vaswani 2017 - Attention Is All You Need",
    book: "Mathematical Methods in the Physical Sciences (Boas)",
    course: "Linear Algebra (MIT OpenCourseWare)", spending: "2026-11 Spending",
    log: "2026-11-07 Annual Checkup",
  };
  const titleQuestions = {
    project: "What's the project called?",
    plan: "What's the plan called? (e.g., Budget)",
    technique: "What's the drill called? (e.g., C Major Scale)",
    composer: "What's the composer's full name? (e.g., Frédéric Chopin)",
    exercise: "What's the exercise called? (e.g., Back Squat)",
    article: "What's the article's title?",
    concept: "What's the concept called? (its full name, e.g., Fast Fourier Transform)",
    account: "What's the account called? (e.g., Chase Checking)",
    asset: "What is it? (e.g., Dishwasher)",
    contractor: "Who are they? (e.g., Bay Area Plumbing)",
    benefit: "What's the benefit? (e.g., Dental Plan)",
    reference: "What's the reference called?",
    system: "What's the note called?",
    routine: "What's the routine called? (e.g., Full-Body Strength)",
    piece: "What's the piece called? (e.g., Ballade No. 1 in G Minor)",
  };

  // How each type is named: `auto` is the whole name, or `ask` and `build`
  // turn your answer into one. A plan that can't be used falls through to
  // asking for the whole name.
  const plans = {
    daily: { auto: values.date },
    weekly: { auto: values.week },
    monthly: { auto: values.month },
    practice: { auto: values.date && `${values.date} Practice` },
    session: { auto: values.date && `${values.date} Workout` },
    spending: { auto: values.month && `${values.month} Spending` },
    log: {
      ask: "What happened, in a few words? (e.g., Annual Checkup)",
      build: async (what) => `${values.date ?? today} ${what}`,
    },
    trip: {
      ask: "Where are you going? (e.g., Kyoto)",
      build: async (where) => {
        const month = values.start?.slice(0, 7) ?? (await promptUntilValid(
          "Which month is the trip? (e.g., 2026-11)", thisMonth,
          (text) => (/^\d{4}-\d{2}$/.test(text) ? { ok: true, value: text } : { ok: false, why: "Months are written YYYY-MM. Try again." })
        ));
        return month && `${month} ${where}`;
      },
    },
    place: values.country && {
      ask: `What's the place called? (e.g., Kyoto)`,
      initial: values.city ?? "",
      build: async (place) => `${place}, ${values.country}`,
    },
    paper: values.authors?.length && values.year && {
      ask: "What's the paper's title?",
      build: async (title) => `${surname(values.authors[0])} ${values.year} - ${title}`,
    },
    book: values.authors?.length && {
      ask: "What's the book's title?",
      build: async (title) => `${title} (${surname(values.authors[0])})`,
    },
    course: {
      ask: "What's the course called?",
      build: async (title) => {
        const provider = await promptUntilValid(
          "Who offers it? (e.g., MIT OpenCourseWare)", "", (text) => ({ ok: true, value: text })
        );
        return provider && `${title} (${provider})`;
      },
    },
  };
  const plan = plans[noteType] || (pattern ? null : {
    ask: titleQuestions[noteType] ?? "What should this note be called?",
    build: async (title) => title,
  });

  const untitled = /^Untitled( \d+)?$/.test(title);
  if (untitled || check(title)) {
    let name = plan?.auto ?? null;
    let skipped = false;   // Esc on a naming question leaves the note unnamed
    if (!name && plan?.ask) {
      const part = await promptUntilValid(plan.ask, plan.initial ?? (untitled ? "" : title), (text) =>
        forbidden.test(text) ? { ok: false, why: "Names can't use # ^ [ ] | \\ : or /. Try again." } : { ok: true, value: text }
      );
      if (part) name = await plan.build(part);
      skipped = !name;
    }
    // The whole name, when the parts didn't make one that fits.
    if (name && check(name)) {
      new Notice(check(name), 8000);
      name = null;
    }
    if (!name && !skipped) {
      const example = examples[noteType] ? ` (e.g., ${examples[noteType]})` : "";
      name = await promptUntilValid(`What should this note be called?${example}`, untitled ? "" : title, (text) => {
        const why = check(text);
        return why ? { ok: false, why } : { ok: true, value: text };
      });
    }
    if (name) await tp.file.rename(name);
    else unnamed = true;
  }
}

// A required property or name left blank makes the note unfinished, so it's tagged inbox.
if (unnamed) blank.push("name");
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
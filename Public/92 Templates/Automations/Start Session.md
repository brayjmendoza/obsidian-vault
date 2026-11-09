---
type: template
created: 2026-11-08
updated: 2026-11-08
version: "0.35"
---
<%*
// Start Session: creates today's session note for the routine you're on, in
// 20 Hobbies/Fitness/Sessions/, without asking anything. A routine's Start
// Session button runs it (Meta Bind: runTemplaterFile). It doesn't go through
// the Session Template or Frontmatter, which still ask as usual when you use
// them directly. Instead it writes the note itself:
//   - name: today's date and the routine's kind of workout, i.e.,
//           `YYYY-MM-DD Run` for running, `YYYY-MM-DD Mobility` for mobility,
//           and `YYYY-MM-DD Workout` otherwise (e.g., calisthenics or weights)
//   - properties: type, created, updated, date, kind (from the routine's
//           modality), and routine. Optional ones are left for Add Properties.
//   - body: the Session Table include, i.e., the routine's Core Workout table
//           and the Sync Last Performed button
// If that note already exists (e.g., a second run today), it's opened instead.
tR = "";

const { Notice } = tp.obsidian;
const root = tp.config.template_file.path.split("92 Templates/")[0];
const today = tp.date.now("YYYY-MM-DD");
const isRoutine = (file) => file && app.metadataCache.getFileCache(file)?.frontmatter?.type === "routine";
const routine = [tp.config.target_file, tp.config.active_file].find(isRoutine);

if (!routine) {
  new Notice("Start Session: run it from a routine note, e.g., with its Start Session button.", 10000);
} else {
  const modality = app.metadataCache.getFileCache(routine)?.frontmatter?.modality;
  const word = { running: "Run", mobility: "Mobility" }[modality] ?? "Workout";
  const kind = { running: "cardio", mobility: "mobility" }[modality] ?? "strength";
  const name = `${today} ${word}`;
  const folderPath = `${root}20 Hobbies/Fitness/Sessions`;
  const path = `${folderPath}/${name}.md`;
  const existing = app.vault.getAbstractFileByPath(path);
  const folder = app.vault.getAbstractFileByPath(folderPath);
  if (existing) {
    new Notice(`Start Session: ${name} already exists, so it's opened instead.`, 8000);
    await app.workspace.getLeaf(false).openFile(existing);
  } else if (!folder) {
    new Notice("Start Session: couldn't find the Sessions folder.", 10000);
  } else {
    const link = app.metadataCache.fileToLinktext(routine, path, true);
    const note = [
      "---",
      "type: session",
      `created: ${today}`,
      `updated: ${today}`,
      `date: ${today}`,
      `kind: ${kind}`,
      `routine: ${JSON.stringify(`[[${link}]]`)}`,
      "---",
      '<' + '% await tp.file.include("[[Session Table]]") %' + '>',
      "",
    ].join("\n");
    await tp.file.create_new(note, name, true, folder);
  }
}
-%>

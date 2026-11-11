---
type: template
created: 2026-11-11
updated: 2026-11-11
version: "0.38"
---
<%*
// Add Task: adds a task to the To-Do's note (type `task`) of the hub you're on, so it
// shows in the hub's Tasks view instead of sitting in the hub itself. A hub's
// Add Task button runs it (Meta Bind: runTemplaterFile).
//   - Editor: the Tasks plugin's own task editor (i.e., description, priority,
//             and dates), or a plain prompt if the Tasks API isn't available
//   - Note:   To-Do's.md beside the hub, created as a `task` note the first time
// Cancelling the editor adds nothing.
tR = "";

const { Notice } = tp.obsidian;
const today = tp.date.now("YYYY-MM-DD");
const isHub = (file) => file && app.metadataCache.getFileCache(file)?.frontmatter?.type === "hub";
const hub = [tp.config.target_file, tp.config.active_file].find(isHub);

// The task line, from the Tasks editor or a prompt, or "" when cancelled.
const askForTask = async () => {
  const tasks = app.plugins.plugins["obsidian-tasks-plugin"]?.apiV1;
  if (tasks?.createTaskLineModal) return (await tasks.createTaskLineModal()) ?? "";
  const text = (await tp.system.prompt("New task"))?.trim();
  return text ? `- [ ] ${text}` : "";
};

if (!hub) {
  new Notice("Add Task: run it from a hub, e.g., with its Add Task button.", 10000);
} else {
  const line = (await askForTask()).trim();
  if (line) {
    const path = `${hub.parent.path}/To-Do's.md`;
    const existing = app.vault.getAbstractFileByPath(path);
    if (existing) {
      await app.vault.process(existing, (text) =>
        `${text.trimEnd()}\n${line}\n`.replace(/^updated: .*$/m, `updated: ${today}`));
    } else {
      await app.vault.create(path, `---\ntype: task\ncreated: ${today}\nupdated: ${today}\n---\n${line}\n`);
    }
    new Notice(`Add Task: added to ${hub.parent.name}'s To-Do's.`, 5000);
  }
}
-%>

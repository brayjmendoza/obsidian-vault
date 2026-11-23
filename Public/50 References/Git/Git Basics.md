---
type: reference
created: 2026-11-23
updated: 2026-11-23
topic: git
---
The Git commands for the everyday loop of copying a repository, changing it, and sharing the changes.

| Command | Does |
|---|---|
| `git clone <url>` | Copies a repository (e.g., from GitHub over HTTPS) into a new folder |
| `git status` | Shows which files have changed, which are staged, and which Git doesn't track yet |
| `git add <file>` | Stages a file's changes for the next commit (`git add .` stages everything in the current folder) |
| `git commit -m "message"` | Records the staged changes as a commit, with a message saying what changed |
| `git push` | Sends your commits to the remote repository |
| `git pull` | Fetches others' commits from the remote and merges them into yours |

The usual loop: `git pull`, make your changes, `git status` to check them, `git add`, `git commit`, then `git push`.

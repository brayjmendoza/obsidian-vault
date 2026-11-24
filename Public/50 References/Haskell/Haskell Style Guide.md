---
type: reference
created: 2026-11-24
updated: 2026-11-24
topic: haskell
url: https://kowainik.github.io/posts/2019-02-06-style-guide
---
Kowainik's style guide for formatting and writing Haskell, drawn from commercial and open-source projects. In code that already has a style, follow the file you're editing.

**Reach for it when:** you're unsure how to lay out a module (e.g., how to order imports or indent a `where`), or you want sensible GHC warnings and default extensions for a new project.

# Key Points

- Indent blocks 4 spaces, and `where` 2 spaces on its own line
- Lines are at most 90 characters
- Imports are explicit or qualified, in four groups separated by blank lines
- Every module has an explicit export list
- Functions and variables are lowerCamelCase, and types, classes, and constructors are UpperCamelCase. A `newtype` field is `un` plus the type's name (e.g., `unName`)
- Constructor fields are strict (`!`), and every `deriving` names its strategy

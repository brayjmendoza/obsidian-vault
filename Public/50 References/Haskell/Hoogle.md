---
type: reference
created: 2026-11-15
updated: 2026-11-24
topic: haskell
url: https://hoogle.haskell.org/
---
Search engine for Haskell's libraries. Find a function by its name, or by its approximate type signature when you know what it should do but not what it's called.

**Reach for it when:** you need a function you suspect already exists (e.g., `(a -> b) -> [a] -> [b]` finds `map`), or you want a function's type and documentation.

# Key Points

- Searches the standard libraries by default, and every Stackage package is available
- `+Data.Map` limits a search to one module, and `-System` excludes modules (e.g., `fold +Data.Map`)
- `name :: type` searches by both (e.g., `id :: a -> a`)
- Operators are listed in their function form (e.g., `(++)`)

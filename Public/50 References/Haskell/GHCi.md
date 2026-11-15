---
type: reference
created: 2026-11-11
updated: 2026-11-15
topic: haskell
---
GHCi is the interactive environment of GHC, the Glasgow Haskell Compiler. It's a **REPL** (i.e., read-eval-print loop): it reads an expression, evaluates it, prints the result, and loops back for the next one.

# Commands

To find a function you don't have yet, search [[Hoogle]] by name or type.

| Command | Does |
|---|---|
| `:load <file>` or `:l <file>` | Loads a `.hs` file's top-level bindings |
| `:reload` or `:r` | Reloads the last file you loaded, after you've edited it |
| `:type <expr>` or `:t <expr>` | Shows an expression's type (e.g., `:t True` prints `True :: Bool`) |
| `:{` … `:}` | Starts and ends a multi-line input |
| `:quit` or `:q` | Leaves GHCi |

# Multi-Line Input

A `let` expression with several bindings needs more than one line. Wrap it in `:{` and `:}`:

```
ghci> :{
ghci| let x = 21
ghci|     y = 7 * 3
ghci| in x + y
ghci| :}
42
```

The bindings must line up in the same column.

# Quirks

- **Each line starts a new scope.** GHCi lets you bind a name again, which a file doesn't allow (see [[Name Binding]]). A line like `x = x + 1` is accepted, but `x` then refers to itself, and asking for it loops forever.
- **Bindings are lazy.** `x = undefined` succeeds, and the error appears only when you evaluate `x` (see [[Lazy Evaluation]]).
- **Expressions are named `it`.** GHCi binds each expression you enter to the name `it`, which is why error messages mention `it = …`.
- **Load files instead of pasting.** Top-level bindings go in a `.hs` file you `:load`. A file can't hold bare expressions, so you try those at the prompt.

# Reading an Error

```
<interactive>:27:14: error:
    • Couldn't match expected type ‘Bool’ with actual type ‘Char’
    • In the expression: 'a'
      In the expression: [True, True, 'a']
      In an equation for ‘it’: it = [True, True, 'a']
```

- **Location:** `<interactive>:27:14` is the file name (here, the prompt), the line, and the column.
- **What went wrong:** "expected `Bool`, found `Char`." The list's earlier elements made Haskell expect `Bool`.
- **Where:** each "In the expression" line steps outward, from the offending piece (`'a'`) to the whole expression it was checking.

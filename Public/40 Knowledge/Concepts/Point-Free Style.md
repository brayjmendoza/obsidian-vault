---
type: concept
created: 2026-11-11
updated: 2026-11-16
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-11
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Point-free style** is defining a function in terms of other functions, without naming the function's parameters.

The "points" are the arguments a function is applied to. A definition in point-free style says what a function *is*, a combination of other functions, rather than what it does to a named argument. Three tools make that possible:

- **Partial application:** a function given fewer arguments than it takes is itself a function (see [[Currying]]). A **section** is a partial application of an operator (e.g., `(+ 1)`, the function that adds one).
- **Dropping a trailing parameter:** when a definition's parameter appears only at the end of both sides (e.g., `f n = g n`), it can be removed (e.g., `f = g`), since both sides are then the same function.
- **Composition:** chaining functions with `(.)` instead of nesting calls on an argument (see [[Function Composition]]).

Point-free definitions are often shorter and put the structure of a computation in front. Pushed too far, they get harder to read, so whether to use them is a matter of style.

# Example

Rewriting `increment` step by step, each line equivalent to the last:

| Definition | What changed |
|---|---|
| `increment n = 1 + n` | The starting definition |
| `increment n = (+) 1 n` | `+` used as a two-argument function |
| `increment n = ((+) 1) n` | Explicit currying: `(+) 1` is a function |
| `increment n = (+ 1) n` | Written as a section |
| `increment = (+ 1)` | `n` ends both sides, so it's dropped |

The last line is point-free: `(+ 1)` already has type `Integer -> Integer`, the same as `increment`. Composition does the same for a chain of calls:

```haskell
incrementDouble n = increment (double n)  -- with a point
incrementDouble = increment . double      -- point-free
```

# Connections

- [[Currying]]: partial application is what makes most point-free definitions possible
- [[Function Composition]]: the main way to chain functions without naming their arguments

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

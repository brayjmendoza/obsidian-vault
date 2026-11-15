---
type: concept
created: 2026-11-15
updated: 2026-11-15
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **partial function** is a function that has no result for some arguments of its type, while a **total function** has a result for every argument.

Calling a partial function on an argument it has no result for fails at run time: the program raises an error instead of returning a value. The type checker can't catch this, since the argument has the right type. Haskell has several sources of these failures:

- **An empty structure.** `head []` and `tail []` have no first element or rest to return.
- **Missing cases.** A [[Pattern Matching|pattern match]] that doesn't cover every possible value fails on the values it leaves out. A wildcard case catches the rest.
- **Undefined values.** `undefined` causes an error when evaluated, so a definition can use it where there's no sensible result.

More generally, the terms come from mathematics, where a partial function is defined on only part of its domain. A partial function weakens the guarantee that well-typed code produces a result (see [[Static and Dynamic Typing]]). It can be made total by handling every input, either with a default for the missing cases or with a result type that can represent "no result" (e.g., Haskell's `Maybe`, Rust's `Option`, or Java's `Optional`).

# Example

`head` and `tail` are partial on lists, since an empty list has no head or tail:

```haskell
intListHead :: IntList -> Int
intListHead Empty       = undefined   -- no sensible result
intListHead (Cons x _)  = x

head [3]   -- 3
head []    -- error: empty list
```

A pattern match with a missing case is partial too:

```haskell
describe n = case n of
  5  -> "I love 5!"
  10 -> "10 is okay"

describe 100  -- error: non-exhaustive patterns
```

Adding a wildcard case (`_ -> "I don't know that number"`) makes `describe` total.

# Connections

- [[Pattern Matching]]: matches that miss a case are the most common source of partial functions
- [[Cons List]]: `head` and `tail` are partial on lists
- [[Static and Dynamic Typing]]: a partial function fails at run time even in a type-safe program
- [[Option Type]]: a result type that can say "no result" instead of failing

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - filter
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Filter** is a higher-order function that takes a predicate and a list, and returns the elements of the list for which the predicate is true, in their original order.

A **predicate** is a function that returns a Boolean (e.g., `even` or `(< 3)`). Filter applies it to each element and keeps the ones it accepts. In Haskell:

```haskell
filter :: (a -> Bool) -> [a] -> [a]
filter _ [] = []
filter p (x : xs) =
  if p x
  then x : filter p xs
  else filter p xs
```

Unlike map, filter never changes an element or its type: the result is a list of the same type, possibly shorter. More generally, like map, it appears in nearly every language with first-class functions (e.g., Python's `filter` and list comprehensions, and JavaScript's `Array.prototype.filter`).

# Example

```haskell
filter even [8, -13, 25, 16, 0, 2]   -- [8, 16, 0, 2]
filter (< 3) [8, -13, 25, 16, 0, 2]  -- [-13, 0, 2]
filter ((< 3) . length) ["oh", "hi", "there!"]  -- ["oh", "hi"]
```

The last predicate is a [[Function Composition|composition]]: take the string's length, then check whether it's less than 3.

# Connections

- [[Map (Higher-Order Function)]]: the companion operation, which transforms every element instead of selecting some
- [[Higher-Order Function]]: filter takes a function as an argument
- [[Function Composition]]: predicates are often built by composing smaller functions

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

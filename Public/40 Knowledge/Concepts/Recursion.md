---
type: concept
created: 2026-11-15
updated: 2026-11-24
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Recursion** is defining something in terms of itself: a recursive function calls itself on a smaller input until it reaches a case it can answer directly.

A recursive definition has two parts. The **base case** answers the smallest inputs directly, without a recursive call. The **recursive case** reduces a larger input to a smaller one, calls the function on it, and builds the answer from the result. The recursion terminates when every recursive call moves closer to a base case. A missing or unreachable base case makes evaluation diverge.

In functional languages, recursion takes the place of loops. A loop repeats by changing a variable, which a pure language doesn't allow (see [[Name Binding]]), so repetition is written as a function that calls itself with new arguments instead. Recursion over a [[Recursive Data Type]] is especially direct: the base case handles the alternative with no recursive field (e.g., the empty list), and the recursive case handles the rest.

# Examples

## Recursion on a Number

Factorial recurs on a number:

```haskell
fact 0 = 1                  -- base case
fact n = n * fact (n - 1)   -- recursive case: n - 1 is closer to 0
```

## Recursion on a List

Checking whether a list contains an element recurs on the list:

```haskell
inList e list =
  if null list then False                -- base case: nothing left to check
  else if head list == e then True
  else inList e (tail list)              -- recursive case: the rest of the list
```

Written with [[Pattern Matching]], the same function shows its two cases side by side:

```haskell
inList _ []       = False
inList e (x : xs) = x == e || inList e xs
```

# Connections

- [[Recursive Data Type]]: data defined recursively, which recursive functions follow case by case
- [[Pattern Matching]]: the usual way to separate base and recursive cases
- [[Functional Programming]]: recursion replaces the loops of imperative programming
- [[Higher-Order Function]]: map and filter are common recursion patterns over lists, each abstracted into a single function
- [[Recursive-Descent Parser]]: a parser built from mutually recursive functions, one per grammar rule
- [[Fixed-Point Combinator]]: recursion for anonymous functions, which can't refer to themselves

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

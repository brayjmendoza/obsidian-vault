---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - map
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Map** is a higher-order function that applies a function to every element of a list, producing a list of the results in the same order.

Map is an [[Abstraction]] of a common pattern. Functions that transform every element of a list share their structure: the empty list stays empty, and a non-empty list becomes the transformed head followed by the transformed tail. Only the transformation differs, so it becomes a parameter, and the parameter is a function. In Haskell:

```haskell
map :: (a -> b) -> [a] -> [b]
map _ []       = []
map f (x : xs) = f x : map f xs
```

The type says that map takes a function from `a` to `b` and a list of `a`s, and returns a list of `b`s. The two types may differ (e.g., mapping `length` over a list of strings gives a list of numbers). The result always has as many elements as the input.

More generally, nearly every language with first-class functions has map (e.g., Python's `map`, JavaScript's `Array.prototype.map`, and Java's `Stream.map`). The idea also extends beyond lists to any structure with elements in it (e.g., applying a function at every node of a tree).

# Example

Three functions with the same shape, differing only in what they do to each element:

```haskell
add3List list      = if null list then list else (+ 3)   (head list) : add3List (tail list)
doubleList list    = if null list then list else (* 2)   (head list) : doubleList (tail list)
emphasizeList list = if null list then list else (++ "!") (head list) : emphasizeList (tail list)
```

Each is map with a different function:

```haskell
add3List      = map (+ 3)
doubleList    = map (* 2)
emphasizeList = map (++ "!")

map length ["Haskell", "Python", "Java"]  -- [7, 6, 4]
```

# Connections

- [[Higher-Order Function]]: map takes a function as an argument
- [[Abstraction]]: map is what's left when the varying part of a recursion pattern becomes a parameter
- [[Filter (Higher-Order Function)]]: map's companion, which keeps elements instead of transforming them
- [[Recursion]]: map is structural recursion over a list, written once
- [[Point-Free Style]]: partial applications like `map (* 2)` define list functions without naming the list
- [[Functor (Functional Programming)]]: generalizes map from lists to any structure, as `fmap`

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-11
updated: 2026-11-21
aliases:
  - First-Class Function
  - map
  - filter
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **higher-order function** is a function that takes another function as an argument or returns one as its result.

A language that supports higher-order functions has **first-class functions**: functions are values like any other, so they can be passed as arguments, returned as results, and bound to names. In Haskell, functions are values in exactly this sense. Every function of several arguments is already higher-order, since [[Currying]] makes it a function that returns a function.

Higher-order functions are [[Abstraction]] applied to behavior. Where an ordinary function abstracts over the values that vary between copies of some code, a higher-order function abstracts over the operations that vary. In a type, parentheses mark where a function is passed in: `(Integer -> Integer) -> Integer` takes a function, while `Integer -> Integer -> Integer` takes two integers.

The two standard higher-order functions on lists come from exactly this kind of abstraction:

- **Map** applies a function to every element of a list and returns the results in the same order. Functions that transform every element share their structure: the empty list stays empty, and a non-empty list becomes the transformed head followed by the transformed tail. Only the transformation differs, so it becomes a parameter. The result always has as many elements as the input, but the element type may change (e.g., mapping `length` over a list of strings gives a list of numbers).
- **Filter** takes a **predicate**, a function that returns a Boolean (e.g., `even` or `(< 3)`), and keeps the elements the predicate accepts, in their original order. Unlike map, filter never changes an element or its type: the result is a list of the same type, possibly shorter.

```haskell
map :: (a -> b) -> [a] -> [b]
map _ []       = []
map f (x : xs) = f x : map f xs

filter :: (a -> Bool) -> [a] -> [a]
filter _ [] = []
filter p (x : xs) =
  if p x
  then x : filter p xs
  else filter p xs
```

More generally, nearly every language with first-class functions has map and filter (e.g., Python's `map`, `filter`, and list comprehensions, and JavaScript's `Array.prototype.map` and `Array.prototype.filter`). Map also extends beyond lists to any structure with elements in it (e.g., applying a function at every node of a tree), which is what a [[Functor (Functional Programming)|functor]] generalizes.

# Example

Three list functions with the same shape, differing only in what they do to each element:

```haskell
add3List list      = if null list then list else (+ 3)   (head list) : add3List (tail list)
doubleList list    = if null list then list else (* 2)   (head list) : doubleList (tail list)
emphasizeList list = if null list then list else (++ "!") (head list) : emphasizeList (tail list)
```

The part that differs is a function, so each is map with a different function argument:

```haskell
add3List      = map (+ 3)
doubleList    = map (* 2)
emphasizeList = map (++ "!")

map length ["Haskell", "Python", "Java"]  -- [7, 6, 4]
```

Filter with different predicates:

```haskell
filter even [8, -13, 25, 16, 0, 2]              -- [8, 16, 0, 2]
filter (< 3) [8, -13, 25, 16, 0, 2]             -- [-13, 0, 2]
filter ((< 3) . length) ["oh", "hi", "there!"]  -- ["oh", "hi"]
```

The last predicate is a [[Function Composition|composition]]: take the string's length, then check whether it's less than 3.

# Connections

- [[Currying]]: why every multi-argument Haskell function is higher-order
- [[Function Composition]]: the most common higher-order function, built into Haskell as `(.)`
- [[Abstraction]]: higher-order functions abstract over operations the way functions abstract over values
- [[Recursion]]: map and filter are recursion patterns over a list, written once
- [[Point-Free Style]]: partial applications like `map (* 2)` define list functions without naming the list
- [[Functor (Functional Programming)]]: generalizes map from lists to any structure, as `fmap`
- [[Closure (Programming Languages)]]: a function returned by another function keeps the outer function's bindings in a closure
- [[Parser Combinator]]: higher-order functions that build parsers from parsers
- [[Monad (Functional Programming)]]: bind takes the next step as a function
- [[Church Encoding]]: in the lambda calculus, even Booleans and numbers are higher-order functions

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

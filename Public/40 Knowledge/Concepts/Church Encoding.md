---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Church Numeral
  - Church Boolean
  - Functional Encoding
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **Church encoding** represents data (e.g., Booleans, pairs, lists, and numbers) as functions, defined by what the data does rather than what it is.

The lambda calculus has nothing but functions, so data has to be built from them. The trick is to encode each kind of data by how it's used:

- **Booleans** are used to choose, as in `if b then x else y`. So a Boolean is a function of two arguments that returns one of them: `TRUE ≜ (λa . (λb . a))` returns the first, `FALSE ≜ (λa . (λb . b))` returns the second, and `if b then x else y` is just `((b x) y)`. Logical operators follow from writing them as conditionals (e.g., `and a b = if a then b else False`).
- **Pairs** are used to pick a component. A pair is a function waiting for a Boolean to choose with: `MKPAIR ≜ (λx . (λy . (λb . ((b x) y))))` builds one, `FST ≜ (λp . (p TRUE))` takes the first part, and `SND ≜ (λp . (p FALSE))` takes the second.
- **Lists** are built from pairs: the empty list is a pair whose first part is `TRUE` (meaning "nil"), and a non-empty list is a pair of `FALSE` and a pair of the head and the tail.
- **Natural numbers** are used to repeat. The **Church numeral** $n$ is the ability to apply a function $f$ to a starting value $b$, $n$ times: `0 ≜ (λf . (λb . b))`, `1 ≜ (λf . (λb . (f b)))`, `2 ≜ (λf . (λb . (f (f b))))`, and so on. The successor applies $f$ one more time, and addition applies the successor repeatedly.
- **Sets** are used to test membership. A set is a function that returns `TRUE` for its members and `FALSE` otherwise, so union and intersection are just `OR` and `AND` on the results (see [[Russell's Paradox]]).

Each encoding only makes sense in context: `TRUE` on its own is just a function that returns its first argument. Names like `TRUE` (written with ≜) are shorthand for people, not part of the pure calculus.

More generally, the encodings are named for Alonzo Church. They show that data and control are interchangeable: a value can be represented by the operation that uses it, the same idea behind the visitor pattern in object-oriented design and behind continuation-passing style. In the typed setting, these encodings correspond to the algebraic data types they simulate (see [[Algebraic Data Type]]).

# Example

The Boolean and pair encodings:

```
TRUE   ≜ (λa . (λb . a))
FALSE  ≜ (λa . (λb . b))
NOT    ≜ (λb . ((b FALSE) TRUE))
AND    ≜ (λa . (λb . ((a b) FALSE)))
OR     ≜ (λa . (λb . ((a TRUE) b)))
MKPAIR ≜ (λx . (λy . (λb . ((b x) y))))
FST    ≜ (λp . (p TRUE))
SND    ≜ (λp . (p FALSE))
SUCC   ≜ (λn . (λf . (λx . (f ((n f) x)))))
```

Checking `NOT TRUE`:

```
(NOT TRUE)  →  ((TRUE FALSE) TRUE)  →  ((λb . FALSE) TRUE)  →  FALSE
```

Sets as functions, in Haskell:

```haskell
empty _            = False
universe _         = True
singleton          = (==)
complement s       = not . s
union s t x        = s x || t x
intersection s t x = s x && t x
```

# Connections

- [[Lambda Calculus]]: the function-only language these encodings are for
- [[Higher-Order Function]]: every encoded value is a function that takes functions
- [[Algebraic Data Type]]: the data types the encodings simulate
- [[Fixed-Point Combinator]]: the encoding of recursion, which numbers and lists need for most operations
- [[Russell's Paradox]]: what happens when sets as functions are applied to themselves

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

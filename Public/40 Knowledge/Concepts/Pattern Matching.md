---
type: concept
created: 2026-11-11
updated: 2026-11-15
aliases:
  - Case Expression
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Pattern matching** checks a value against a series of patterns that describe its possible shapes, and runs the code for the first pattern that fits, binding names to the parts of the value it matched.

A **pattern** looks like the way a value is built, with names or wildcards in place of the parts. Matching works in the opposite direction from construction: where a constructor builds a value from parts, a pattern takes a value apart into them. Patterns come in a few kinds:

- **Literal:** a value (e.g., `0` or `True`), which matches only a value equal to it.
- **Variable:** a name (e.g., `n`), which matches anything and binds the name to it.
- **Wildcard:** `_`, which matches anything without binding it. It says the code doesn't use that part.
- **Constructor:** a constructor applied to patterns (e.g., `CoolTo t` or `Leaf _`), which matches a value built with that constructor, then matches its fields against the inner patterns (see [[Algebraic Data Type]]).
- **List:** `[]` matches the empty list, and `x : xs` matches a non-empty one, binding its head and tail (see [[Cons List]]).
- **Tuple:** `(a, b, c)` matches a tuple of that size and binds each component.

Patterns nest, so one pattern can reach several levels into a value (e.g., `(x : y : rest)` matches a list with at least two elements).

Patterns are tried from top to bottom, and the first match wins. A variable or wildcard matches everything, so it acts as a **fall-through** case and goes after the more specific ones. A match that leaves out a possible value fails at run time on that value, which makes its function partial (see [[Partial Function]]).

Haskell offers pattern matching in several places:

- **Function equations:** one equation per case, each with patterns for its parameters.
- **`case` expressions:** `case e of` followed by one `pattern -> result` line per case, usable anywhere an expression is. Every result must have the same type.
- **Bindings:** a pattern on the left of an equals sign takes a value apart into names (e.g., `(name, course, acted) = prof1`).

Together with [[Recursive Data Type|recursive data types]] and [[Recursion]], pattern matching is the main way functional programs process data: each case of the data gets a case in the function.

More generally, many other languages have pattern matching too (e.g., Rust's `match`, OCaml's `match`, Scala's `match`, and Python's `match` statement), and a match that covers every possible value is called **exhaustive**.

# Example

Factorial with a conditional, then with pattern matching on literals:

```haskell
fact n = if n == 0 then 1 else n * fact (n - 1)

fact 0 = 1                 -- base case: matches only 0
fact n = n * fact (n - 1)  -- fall-through: matches anything else
```

The same function on a data type, written as equations and as a `case` expression:

```haskell
isRunning :: ThermostatSetting -> Bool
isRunning Off = False
isRunning _   = True

isRunning setting = case setting of
  Off -> False
  _   -> True
```

Taking a list apart into head and tail:

```haskell
myLength :: [a] -> Int
myLength []       = 0
myLength (_ : xs) = 1 + myLength xs
```

Taking a tuple apart, using wildcards for the parts that aren't needed:

```haskell
isRightTriangle (a, b, c) = a * a + b * b == c * c
getCourse (_, course, _)  = course

isRightTriangle (5, 12, 13)  -- True
```

# Connections

- [[Algebraic Data Type]]: constructor patterns take apart the values that constructors build
- [[Recursion]]: pattern matching separates a recursive function's base case from its recursive case
- [[Partial Function]]: a match that misses a case makes its function partial
- [[Name Binding]]: a variable pattern binds its name for the code of its case
- [[Interpreter]]: an evaluator has one pattern-matched case per kind of expression

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

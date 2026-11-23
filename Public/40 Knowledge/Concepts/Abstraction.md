---
type: concept
created: 2026-11-11
updated: 2026-11-23
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Abstraction** is replacing code that repeats with one named definition, turning the parts that vary into parameters.

Its simplest form is the function. A function is a **parameterized expression**: an expression with some of its values left as names, filled in at each call. Turning repeated code into a function is called **refactoring**, and it follows the same steps every time:

1. Find the repeated code, and split it into the part that stays the same and the parts that differ.
2. Make each part that differs a parameter, and decide its type.
3. Decide the type of the result.
4. Write the function, with the part that stays the same as its body.
5. Replace each copy of the repeated code with a call to the function.

More generally, the same move works at every level. A function abstracts over values, a [[Higher-Order Function|higher-order function]] abstracts over functions (e.g., [[Function Composition]] captures "apply one function, then another"), and later constructs abstract over types and whole patterns of computation. Much of programming language design is deciding what a language lets its programmers abstract over.

# Example

Four expressions share a shape:

```haskell
2 * 2 + 1
3 * 2 + 1
(4 * 2 + 1)
5 * 2 + 1
```

The part that stays the same is `_ * 2 + 1`, and the number in front differs. So the function needs one `Integer` parameter, and its result is an `Integer`:

```haskell
f :: Integer -> Integer
f n = n * 2 + 1
```

Each copy then becomes a call: `f 2`, `f 3`, `(f 4)`, and `f 5`. A change to the shared part (e.g., `* 3` instead of `* 2`) is now made once.

# Connections

- [[Higher-Order Function]]: abstraction one level up, with functions as the parameters (e.g., map, what's left when the operation that varies between several list functions becomes a parameter)
- [[Function Composition]]: an abstraction of the pattern "apply `f`, then `g`"
- [[Functional Programming]]: the style built around functions as the main unit of abstraction
- [[Parser Combinator]]: combinators abstract away the state-handling that hand-written parsers repeat
- [[Functor (Functional Programming)]] and [[Monad (Functional Programming)]]: abstractions over repeated mapping and repeated failure-checking
- [[Zero-Overhead Principle]]: the demand that an abstraction cost nothing over the code it replaces
- [[Black-Box Testing]]: testing an abstraction through its interface alone
- [[Abstract Data Type]]: an interface abstracts away how a data structure is stored and implemented

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

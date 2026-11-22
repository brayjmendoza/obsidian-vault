---
type: concept
created: 2026-11-11
updated: 2026-11-21
aliases:
  - Curried Function
  - Partial Application
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Currying** is representing a function of several arguments as a function that takes one argument and returns a function that takes the rest.

A **curried function** takes its arguments one at a time. In Haskell, every function takes exactly one argument, and every function of several arguments is curried. The technique is named after the logician Haskell Curry, though Moses Schönfinkel described it earlier.

Two associativity rules make curried functions read like ordinary ones (see [[Operator Precedence and Associativity]]):

- **The function-type arrow is right-associative.** `->` is an operator on types: its left operand is the parameter's type, and its right operand is the result's type. So `Double -> Double -> Double` means `Double -> (Double -> Double)`, a function that takes a `Double` and returns a function from `Double` to `Double`.
- **Function application is left-associative.** Its left operand is the function, and its right operand is the argument. So `average 1.0 2.0` means `(average 1.0) 2.0`: apply `average` to `1.0`, then apply the resulting function to `2.0`.

Each argument applied peels one arrow off the type. Supplying fewer arguments than a function can take is **partial application**, and its result is a function waiting for the rest. Partial application is how new functions are made from old ones without writing a definition with parameters (see [[Point-Free Style]]). Since a curried function returns a function, every multi-argument function in Haskell is a [[Higher-Order Function|higher-order function]].

# Example

`average` can be read two ways, and both are correct:

```haskell
average :: Double -> Double -> Double
average x y = (x + y) / 2
```

1. `average` takes two `Double`s and results in a `Double`.
2. `average` takes a `Double` and results in a function that takes a `Double` and results in a `Double`.

The second reading is what happens when it's applied:

| Expression | Type |
|---|---|
| `average` | `Double -> Double -> Double` |
| `average 1.0` | `Double -> Double` |
| `average 1.0 2.0` | `Double` |

So `average 1.0` can be bound and used on its own:

```haskell
halfwayFromOne = average 1.0
halfwayFromOne 2.0  -- 1.5
```

# Connections

- [[Higher-Order Function]]: a curried function returns a function, so it's higher-order
- [[Point-Free Style]]: partial application lets a function be defined without naming its arguments
- [[Operator Precedence and Associativity]]: the arrow and function application associate in opposite directions, which is what makes currying work
- [[Interpreter]]: an interpreter can support multi-argument functions by nesting one-argument functions
- [[Closure (Programming Languages)]]: each partial application of a curried function is a closure holding the arguments so far
- [[Curry-Howard Correspondence]]: another idea named for Haskell Curry, connecting programs and proofs
- [[Lambda Calculus]]: every function takes one argument, so curried functions are the only kind

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

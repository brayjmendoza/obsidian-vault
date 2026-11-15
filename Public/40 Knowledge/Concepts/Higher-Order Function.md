---
type: concept
created: 2026-11-11
updated: 2026-11-15
aliases:
  - First-Class Function
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-11
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **higher-order function** is a function that takes another function as an argument or returns one as its result.

A language that supports higher-order functions has **first-class functions**: functions are values like any other, so they can be passed as arguments, returned as results, and bound to names. In Haskell, functions are values in exactly this sense. Every function of several arguments is already higher-order, since [[Currying]] makes it a function that returns a function.

Higher-order functions are [[Abstraction]] applied to behavior. Where an ordinary function abstracts over the values that vary between copies of some code, a higher-order function abstracts over the operations that vary. In a type, parentheses mark where a function is passed in: `(Integer -> Integer) -> Integer` takes a function, while `Integer -> Integer -> Integer` takes two integers.

# Example

Three expressions share a pattern, apply one function and then another to `1`, but differ in which functions:

```haskell
increment (double 1)
double (increment 1)
increment (square 1)
```

The parts that differ are functions, so they become parameters of type `Integer -> Integer`:

```haskell
compose1 :: (Integer -> Integer) -> (Integer -> Integer) -> Integer
compose1 g f = g (f 1)
```

Making the starting value a parameter too generalizes it further:

```haskell
compose :: (Integer -> Integer) -> (Integer -> Integer) -> Integer -> Integer
compose g f n = g (f n)
```

`compose` takes two functions as arguments, and since it's curried, `compose increment double` returns a function. That's [[Function Composition]], which Haskell provides built in.

# Connections

- [[Currying]]: why every multi-argument Haskell function is higher-order
- [[Function Composition]]: the most common higher-order function, built into Haskell as `(.)`
- [[Abstraction]]: higher-order functions abstract over operations the way functions abstract over values
- [[Map (Higher-Order Function)]] and [[Filter (Higher-Order Function)]]: the standard higher-order functions on lists
- [[Closure (Programming Languages)]]: a function returned by another function keeps the outer function's bindings in a closure
- [[Parser Combinator]]: higher-order functions that build parsers from parsers
- [[Monad (Functional Programming)]]: bind takes the next step as a function
- [[Church Encoding]]: in the lambda calculus, even Booleans and numbers are higher-order functions

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

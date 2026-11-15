---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Maybe
  - Maybe Type
  - Optional
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
An **option type** is a type whose values are either "no value" or "a value of some type," so that a missing result is part of the type instead of an error.

Haskell's option type is `Maybe`, a built-in [[Parametric Polymorphism|parameterized type]]:

```haskell
data Maybe a = Nothing | Just a
```

`Nothing` says "there is no value," and `Just x` says "there is a value, and here it is." The type parameter says what kind of value: `Just True` has type `Maybe Bool`, `Just 1` has a numeric type like `Maybe Integer`, and `Nothing` alone can be a `Maybe` of any type. Code that receives a `Maybe` has to handle both cases, usually with [[Pattern Matching|pattern matching]] or a `case` expression.

`Maybe` gives functions a way to fail without crashing. Looking up a key in a `Data.Map` returns `Nothing` when the key is missing. A parser returns `Nothing` for a failed parse and `Just` a result and the remaining input for a success, which is clearer than picking some special value to mean failure (see [[Parser Combinator]]).

More generally, option types appear in many languages (e.g., Rust's `Option`, Swift's optionals, OCaml's `option`, and Java's `Optional`). They're the standard alternative to a **null** value that can stand in for any type: with an option type, the type checker knows which values might be missing and makes the code handle them. Using one is how a [[Partial Function|partial function]] becomes total.

# Example

A lookup with a default value, handling both cases:

```haskell
initialEnv :: Map.Map String Double
initialEnv = Map.insert "x" 42 Map.empty

defaultLookup :: String -> Map.Map String Double -> Double
defaultLookup var env = case Map.lookup var env of
  Just value -> value
  Nothing    -> 0

defaultLookup "x" initialEnv  -- 42.0
defaultLookup "y" initialEnv  -- 0.0
```

`Data.Map` already has this function, as `Map.findWithDefault`.

# Connections

- [[Partial Function]]: an option type turns a partial function into a total one
- [[Algebraic Data Type]]: `Maybe` is an algebraic data type with two constructors
- [[Parametric Polymorphism]]: `Maybe a` works for any type `a`
- [[Parser Combinator]]: parsers use `Maybe` to report failure
- [[Monad (Functional Programming)]]: `Maybe` is a monad, so `>>=` chains computations that might fail
- [[Functor (Functional Programming)]]: `fmap` applies a function inside a `Just` and leaves `Nothing` alone
- [[Top and Bottom Types]]: a catch-all type says nothing, while an option type says exactly what might be missing

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

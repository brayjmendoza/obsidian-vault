---
type: concept
created: 2026-11-11
updated: 2026-11-24
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Type inference** is a form of type checking that works out the types of a program's expressions without requiring the programmer to annotate them.

A statically typed language checks types before a program runs (see [[Static and Dynamic Typing]]). Without inference, that means annotating every variable and function. With inference, the checker deduces types from how values are used: in `successor n = n + 1`, `n` is added to a number, so `n` must be a number, and so is the result. Haskell is statically typed and uses type inference, so most annotations are optional.

Annotations are still worth writing on top-level functions:

- **Documentation:** a function's type says what it takes and returns.
- **Intent:** the checker compares the code against the annotation, so a mistake is reported where it happens instead of somewhere it causes a later mismatch.
- **Precision:** an annotation can pin a type down further than inference would. Without one, `successor` gets the most general type that works for any number, `Num a => a -> a`, not just `Integer -> Integer` (see [[Type Class]]).

In Haskell, `::` reads "has type," and `->` builds a function type: `Integer -> Integer` is the type of a function that takes an `Integer` and results in an `Integer`. A function of two arguments has two arrows (e.g., `Double -> Double -> Double`), for reasons [[Currying]] explains.

C++ infers types in a more limited way. A variable declared with `auto` takes the type of the value it's initialized with (see [[Initialization (Programming Languages)]]). The compiler works the type out at compile time, and the variable can't change type while the program runs. `auto` declutters code where a type is long, but it can also hide information a reader needs, so it's best used sparingly:

- **Use `auto`** when the type is complicated, genuinely doesn't matter, or is clear from context (e.g., an iterator's type in a loop).
- **Avoid `auto`** when the type is simple and known, important for understanding the code, or unclear from context.

# Examples

## Inference in Haskell

No annotations are needed for Haskell to check these:

```haskell
successor n = n + 1
average x y = (x + y) / 2
```

With annotations, the intended types are stated and checked:

```haskell
successor :: Integer -> Integer
successor n = n + 1

average :: Double -> Double -> Double
average x y = (x + y) / 2
```

In GHCi, `:type` (or `:t`) shows the type Haskell infers for any expression (e.g., `:t True` prints `True :: Bool`).

## Auto in C++

In C++, `auto` saves writing the long type of an [[Iterator|iterator]], an object that steps through a container's items. Here the type is clear from `begin()`, which gives an iterator to a list's first item:

```c++
std::list<double> values{1.5, 2.5};
for (auto p = values.begin(); p != values.end(); ++p) {   // p is a std::list<double>::iterator
    *p *= 2;
}
```

# Connections

- [[Static and Dynamic Typing]]: type inference is a way of doing static type checking
- [[Currying]]: why a function of several arguments has a chain of arrows in its type
- [[Parametric Polymorphism]]: Haskell infers the most general type a definition allows, with type variables where any type works
- [[Type Class]]: inferred types can carry class constraints (e.g., `Num a => a -> a` for `successor`)
- [[Typing Rule]]: inference finds a typing derivation without annotations
- [[Initialization (Programming Languages)]]: C++'s `auto` takes a variable's type from its initializer

# Sources

- [[Programming Languages (HMC CS131)]]
- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

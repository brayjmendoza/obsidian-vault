---
type: concept
created: 2026-11-11
updated: 2026-11-15
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-11
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Lazy evaluation** is an evaluation strategy that evaluates a sub-expression only when its result is needed.

Most languages use **eager evaluation**, also called **strict evaluation**, which evaluates sub-expressions first. Under eager evaluation, an expression is evaluated before it's bound to a name, and a function's arguments are evaluated before the call. Lazy evaluation does neither. A name is bound to the unevaluated expression, and arguments are passed to a function unevaluated:

| Code | Eager | Lazy |
|---|---|---|
| `x = 1 + 2` | `x` holds `3` | `x` is bound to the expression `1 + 2` |
| `f (1 + 2) (3 * 4)` | `f` is called with `3` and `12` | `f` is called with `1 + 2` and `3 * 4`, evaluated only if `f` uses them |

Haskell is lazy. Delaying evaluation is safe there because of [[Referential Transparency]]: an expression with no side effects has the same value whenever it's evaluated, or if it's never evaluated at all.

Lazy evaluation has four main benefits:

- **No unnecessary computation.** A program evaluates only what its result depends on.
- **No repeated computation of a bound expression.** Once a bound expression is evaluated, its result is kept, so later uses of the name don't evaluate it again. This applies to names, not to calls: calling `f 37` twice evaluates it twice.
- **Parallel evaluation.** Without side effects, independent expressions can be evaluated in any order.
- **Large and infinite data structures.** A program builds only the part of a structure it uses (e.g., `take 3 [1 ..]` evaluates to `[1, 2, 3]`, though `[1 ..]` is infinite).

Laziness also changes which programs terminate. An expression that would diverge or fail is harmless as long as nothing needs its value.

# Example

A function that ignores its first argument never evaluates it:

```haskell
ignoreFirstArgument :: Integer -> Integer -> Integer
ignoreFirstArgument _ y = y

ignoreFirstArgument (1 + 2) (3 * 4)  -- 1 + 2 is never evaluated
ignoreFirstArgument undefined 5      -- 5, even though undefined is an error
```

In GHCi, binding a name is instant, and the work happens the first time the name is used. With a slow function `expensive`:

```
ghci> y = expensive 37   -- returns at once: y is bound, not evaluated
ghci> y                  -- slow: the first use evaluates y
1021
ghci> y                  -- instant: the result was kept
1021
```

# Connections

- [[Referential Transparency]]: what makes delaying evaluation safe
- [[Name Binding]]: a lazy binding associates a name with an expression, not a value
- [[Functional Programming]]: purity is what lets Haskell be lazy by default
- [[Recursive Data Type]]: laziness lets a list be infinite, with only the elements a program uses ever built
- [[Evaluation Strategy]]: lazy evaluation is call by need, call by name with each argument evaluated at most once
- [[Beta Reduction]]: reducing the outermost application first is what lets a lazy language finish where an eager one loops

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

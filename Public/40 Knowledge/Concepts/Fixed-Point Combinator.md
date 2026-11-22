---
type: concept
created: 2026-11-15
updated: 2026-11-21
aliases:
  - Y Combinator
  - Fixpoint Combinator
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **fixed-point combinator** is a function that, given a function $g$, produces a fixed point of $g$: a value $x$ with $x = g\,x$  (i.e., $x=g(x)$). Its standard example, the **Y combinator**, is how anonymous functions can be recursive.

A recursive function refers to itself by name (e.g., `factorial` calls `factorial`). In the lambda calculus, functions have no names, so a function can't mention itself. The Y combinator gets around this by repeating a function as many times as needed.

It comes from generalizing Russell's paradox (see [[Russell's Paradox]]). The expression `(R R)`, with `R = (λx . (Not (x x)))`, reduces to `(Not (R R))`, then `(Not (Not (R R)))`, and so on, applying `Not` forever. Nothing depends on `Not` in particular, so making it a parameter gives:

```
Y ≜ (λf . ((λx . (f (x x))) (λx . (f (x x)))))
```

and `(Y g)` reduces to `(g (Y g))`, then `(g (g (Y g)))`: $g$ applied to $g$ applied to $g$, as many times as needed.

That's exactly what a **fixed point** is. A fixed point of a function $g$ is a value $x$ with $x = g\,x$. For $g(x) = 20 - x^2$, 4 is a fixed point, since $20 - 4^2 = 4$, so $4 = g(4) = g(g(4)) = \cdots$. Recursion works the same way. Factor the recursive call out of a definition into a parameter. For example, with factorial:

```haskell
fact = (\f -> \n -> if n == 0 then 1 else n * f (n - 1)) fact
--      \________________________ g _____________________/
```

so `fact = g fact`: `fact` is a fixed point of `g`. The Y combinator finds it, so `fact = Y g` defines factorial without `fact` mentioning itself. The recipe works for any recursive definition: replace each recursive call with a parameter `f`, wrap the body in `\f -> …`, and apply `Y`.

More generally, this Y diverges under call-by-value evaluation, since `(Y g)` keeps expanding before `g` ever runs, so eager languages use a variant called the **Z combinator**, which delays the self-application behind a lambda. In Haskell, the self-application `x x` can't be typed at all, so `Y` can't be written as above. Instead, recursion supplies the fixed point directly: `fix f = f (fix f)` (in `Data.Function`), which laziness makes work. Haskell Curry discovered the Y combinator, and the startup accelerator Y Combinator is named after it.

# Example

Recursive functions written with a fixed-point combinator (in Haskell, with `fix` playing the role of `Y`):

```haskell
import Data.Function (fix)

fact    = fix (\f -> \n -> if n == 0 then 1 else n * f (n - 1))
sum0toN = fix (\f -> \n -> if n == 0 then 0 else n + f (n - 1))
sumList = fix (\f -> \list -> if null list then 0 else head list + f (tail list))

fact 5     -- 120
sum0toN 4  -- 10
```

# Connections

- [[Recursion]]: a fixed-point combinator provides recursion without self-reference
- [[Russell's Paradox]]: the self-applying expression the Y combinator generalizes
- [[Lambda Calculus]]: where functions are anonymous, so recursion needs a combinator
- [[Beta Reduction]]: `(Y g)` reduces to `(g (Y g))`
- [[Evaluation Strategy]]: under call by value, `Y` loops before doing any work
- [[Lazy Evaluation]]: what lets Haskell's `fix` work

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

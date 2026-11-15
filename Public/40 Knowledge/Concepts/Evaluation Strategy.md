---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Call by Value
  - Call by Name
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
An **evaluation strategy** decides when a function's argument is evaluated: in **call by value**, before it's passed in, and in **call by name**, only where the function's body uses it.

In an interpreter that applies functions by [[Substitution|substitution]], the difference is one line:

- **Call by name:** substitute the unevaluated argument for the parameter, then evaluate the body.
- **Call by value:** evaluate the argument first, then substitute its value for the parameter, then evaluate the body.

In most cases, the two give the same result, but they can cost different amounts of work:

| Situation | Call by name | Call by value |
|---|---|---|
| The argument is expensive, and the parameter appears many times | Evaluates it once per use: more work and space | Evaluates it once |
| The argument is expensive, or never finishes, and the parameter is unused | Never evaluates it | Evaluates it anyway: wasted work, or no result at all |

More generally, the strategies give different results when evaluating the argument fails or never finishes but the function doesn't use it: call by name returns a result, and call by value doesn't. With side effects, they can also differ in what happens and how often. Most languages use call by value (e.g., C, Java, and Python). Haskell uses **call by need**, which is [[Lazy Evaluation|lazy evaluation]]: call by name, plus remembering an argument's value once it's computed, so it's evaluated at most once.

# Example

The two versions of `eval` for function application, from Arith's interpreter:

```haskell
-- Call by name: substitute the unevaluated argument
eval (Apply (FuncDef v body) arg) =
  eval (substitute arg (Var v) body)

-- Call by value: evaluate the argument, then substitute
eval (Apply (FuncDef v body) arg) =
  let val = eval arg
  in eval (substitute val (Var v) body)
```

# Connections

- [[Lazy Evaluation]]: Haskell's strategy, call by name with sharing
- [[Substitution]]: the step both strategies share
- [[Interpreter]]: where the choice of strategy is made
- [[Beta Reduction]]: the same choice of order, in the lambda calculus, decides whether `((λy . pig) Ω)` ends

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

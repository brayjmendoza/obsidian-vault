---
type: concept
created: 2026-11-15
updated: 2026-11-16
aliases:
  - Desugaring
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Syntactic sugar** is a construct a language provides for convenience, whose meaning is defined by translating it into constructs the language already has.

Adding a feature to a language usually means two things: new abstract syntax, and new semantics for it. With syntactic sugar, only the first is new. The new construct's meaning is given by rewriting it into existing syntax, whose semantics is already defined, so the evaluator gains a feature without new evaluation logic. The new problem reduces to one already solved.

A `let` expression is the standard example. `let x = 100 in x + 17` binds `x` to `100` and evaluates the body, which is just what applying a function does: substitute the argument for the parameter in the body. So a `let` is the same as applying a one-parameter function, whose parameter is the variable and whose body is the `let` body, to the bound value. In an [[Interpreter|interpreter]], adding `let` takes one new constructor and one line of `eval`.

More generally, translating sugar into the language's core is called **desugaring**, and the smaller language left after it is the **core language**. Many familiar features are sugar in some language (e.g., list comprehensions in Haskell and Python, `for` loops over `while` loops, and `+=`). Keeping the core small keeps the semantics small too, since only the core has to be defined and implemented directly.

# Example

`let` added to [[Arith]], with its meaning defined by function application:

```haskell
data Exp
  = …
  | Let VarName Exp Exp   -- variable, bound expression, body
  | FuncDef VarName Exp
  | Apply Exp Exp

eval env (Let v e body) = eval env (Apply (FuncDef v body) e)
```

So `Let "x" (Num 100) (BinOp (Var "x") PlusOp (Num 17))` evaluates exactly like `Apply (FuncDef "x" (BinOp (Var "x") PlusOp (Num 17))) (Num 100)`, to `Num 117`.

# Connections

- [[Interpreter]]: where desugaring happens, as a rewrite inside `eval`
- [[Scope]]: a `let` creates a scope, just as a function's parameter does
- [[Closure (Programming Languages)]]: a function bound with `let` is how functions get names
- [[Monad (Functional Programming)]]: `do` notation is sugar for chains of `>>=`

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

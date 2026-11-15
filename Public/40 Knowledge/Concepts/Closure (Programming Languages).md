---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Closure
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **closure** is a function packaged together with the environment in which it was defined, so its free variables keep the values they had there.

In an evaluator that uses [[Environment (Programming Languages)|environments]], evaluating a function definition can't just return the function's parameter and body. The body may use variables bound outside it, and if the evaluator drops the environment, those bindings are lost. Two things then go wrong:

- **Curried functions break.** Applying a two-parameter function to its first argument returns the inner function, but the binding for the first parameter is gone. Applying the result fails with "unbound identifier."
- **Scope is dynamic.** When the body finally runs, its free variables are looked up in whatever environment exists at the call (see [[Static and Dynamic Scope]]).

A closure fixes both. Evaluating a function definition produces a closure holding the current environment, the parameter name, and the body. Applying a closure evaluates the argument, extends the *closure's* environment (not the caller's) with the parameter bound to it, and evaluates the body there. The result is static scope: the body sees the bindings from where it was written.

Closures also give functions names. Binding a function with `let` puts it in the environment like any value, so `let f = (function) in f 100` looks up `f` and applies it.

More generally, closures are how every language with first-class functions and static scope implements them (e.g., JavaScript, Python, and Haskell). A closure can outlive the call that created it, which is why its environment has to be stored with the function rather than on a stack frame that disappears. Closures are a common way to keep private state in languages that allow mutation (e.g., a counter function that increments a variable only it can see).

# Example

Arith with closures:

```haskell
data Exp
  = …
  | FuncDef VarName Exp
  | Apply Exp Exp
  | Closure Env VarName Exp   -- environment, parameter, body

eval env (FuncDef v body) = Closure env v body     -- save the environment

eval env (Apply fexp arg) =
  let Closure closureEnv v body = eval env fexp
      argval = eval env arg
  in eval (envInsert v argval closureEnv) body     -- use the saved environment
```

The curried application that failed without closures now works:

```haskell
eval [] (Apply (Apply (FuncDef "a" (FuncDef "b" (BinOp (Var "b") PlusOp (Var "a")))) (Num 100)) (Num 42))
-- the inner Apply gives Closure [("a", Num 100)] "b" (BinOp (Var "b") PlusOp (Var "a"))
-- applying it to Num 42 evaluates the body with a ↦ 100 and b ↦ 42: Num 142
```

# Connections

- [[Environment (Programming Languages)]]: the bindings a closure carries
- [[Static and Dynamic Scope]]: closures are how an interpreter gets static scope
- [[Higher-Order Function]]: a function returned by another function needs a closure to keep the outer function's bindings
- [[Currying]]: a curried function's partial applications are closures
- [[Interpreter]]: where closures are created and applied
- [[Free and Bound Variables]]: a closure stores the values of its function's free variables

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

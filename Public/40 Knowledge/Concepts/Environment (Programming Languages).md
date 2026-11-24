---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Environment
  - Env
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
An **environment** is a mapping from variable names to their values, which an evaluator carries along instead of substituting values into expressions.

Evaluating by [[Substitution|substitution]] is slow. Applying a function of $N$ curried parameters, whose body has size $O(N)$, means searching the whole body once per parameter, for $O(N^2)$ work in total. An environment avoids the rewriting: instead of substituting an argument into the body right away, the evaluator remembers the binding and looks the variable up when the body actually needs it.

An environment-based evaluator changes in three places:

- **`eval` takes the environment** as an extra argument and passes it along to every recursive call.
- **A variable** evaluates to its value in the environment, and a missing name is an "unbound identifier" error.
- **Applying a function** evaluates the argument, adds a binding from the parameter to that value, and evaluates the body in the extended environment.

How fast this is depends on how the environment is stored. As a list of pairs, each lookup scans the list, so evaluation is still $O(N^2)$. With a structure that looks up in constant time, it falls to $O(N)$.

Evaluating with environments raises a new question: which environment a function's body should use. If it's the one at the call, a function's free variables can pick up whatever the caller has bound (see [[Static and Dynamic Scope]]). Fixing that takes [[Closure (Programming Languages)|closures]].

More generally, environments are how nearly every real interpreter works, and compilers have a matching structure, the **symbol table**, built before the program runs. Persistent maps (e.g., Haskell's `Data.Map`, a balanced tree with $O(\log n)$ lookups) suit environments in a functional language, since extending one for a function call leaves the caller's environment unchanged.

# Examples

## Applying a Four-Parameter Function

Applying a four-parameter function, one argument at a time:

```haskell
eval [] (Apply (Apply (Apply (Apply
  (FuncDef "a" (FuncDef "b" (FuncDef "c" (FuncDef "d"
    (BinOp (Var "a") PlusOp (BinOp (Var "b") PlusOp (BinOp (Var "c") PlusOp (Var "d"))))))))
  (Num 1)) (Num 2)) (Num 3)) (Num 4))
```

| Step | Environment | Left to evaluate |
|---|---|---|
| Apply to `Num 1` | `a ↦ 1` | The functions of `b`, `c`, and `d` |
| Apply to `Num 2` | `a ↦ 1`, `b ↦ 2` | The functions of `c` and `d` |
| Apply to `Num 3` | `a ↦ 1`, `b ↦ 2`, `c ↦ 3` | The function of `d` |
| Apply to `Num 4` | `a ↦ 1`, `b ↦ 2`, `c ↦ 3`, `d ↦ 4` | `a + (b + (c + d))` |
| Look up the variables | | `Num 10` |

The body is never rewritten. Each variable is looked up once, when the sum is computed. The table shows the idea, but the first environment-based `eval` doesn't get there: evaluating the inner function returns it without the binding for `a`, so the sum fails with "unbound identifier: a." Keeping each function's environment with it, in a [[Closure (Programming Languages)|closure]], fixes that.

## The Environment as a List

The environment and its operations, as a list of pairs:

```haskell
type Env = [(VarName, Exp)]

envLookup :: VarName -> Env -> Exp
envLookup v [] = error ("unbound identifier: " ++ v)
envLookup v ((key, val) : rest) = if v == key then val else envLookup v rest

envInsert :: VarName -> Exp -> Env -> Env
envInsert v e [] = [(v, e)]
envInsert v e ((key, val) : rest) =
  if v == key then (v, e) : rest else (key, val) : envInsert v e rest
```

# Connections

- [[Substitution]]: the approach environments replace
- [[Interpreter]]: an environment is an extra argument to `eval`
- [[Static and Dynamic Scope]]: which environment a function's body is evaluated in
- [[Closure (Programming Languages)]]: a function paired with the environment it was defined in
- [[Name Binding]]: an environment records a program's bindings while it runs
- [[Typing Rule]]: a type environment maps variables to types, as a value environment maps them to values
- [[Associative Array]]: an environment is a map from names to values

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

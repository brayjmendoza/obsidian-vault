---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Desugaring
  - Range-Based for Loop
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Syntactic sugar** is a construct a language provides for convenience, whose meaning is defined by translating it into constructs the language already has.

Adding a feature to a language usually means two things: new abstract syntax, and new semantics for it. With syntactic sugar, only the first is new. The new construct's meaning is given by rewriting it into existing syntax, whose semantics is already defined, so the evaluator gains a feature without new evaluation logic. The new problem reduces to one already solved.

A `let` expression is the standard example. `let x = 100 in x + 17` binds `x` to `100` and evaluates the body, which is just what applying a function does: substitute the argument for the parameter in the body. So a `let` is the same as applying a one-parameter function, whose parameter is the variable and whose body is the `let` body, to the bound value. In an [[Interpreter|interpreter]], adding `let` takes one new constructor and one line of `eval`.

C++'s **range-based `for` loop** is sugar for a loop over [[Iterator|iterators]]. `for (double v : values) { … }` visits each item of `values` without naming an iterator. The compiler rewrites it into a loop that starts an iterator at `std::begin(values)`, stops at `std::end(values)`, and initializes `v` from each item in turn, so any type that provides `begin` and `end` works with it.

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

A range-based `for` loop in C++:

```c++
for (TYPE var : thing) {
    ... var ...
}
```

means the same as:

```c++
{
    auto _past_end = std::end(thing);
    for (auto _i = std::begin(thing); _i != _past_end; ++_i) {
        TYPE var = *_i;
        ... var ...
    }
}
```

`var` is copy-initialized from each item, so changing it changes only the copy. Declaring it as a reference, like `double& var`, makes `var` another name for each item instead, so changes reach the container.

# Connections

- [[Interpreter]]: where desugaring happens, as a rewrite inside `eval`
- [[Scope]]: a `let` creates a scope, just as a function's parameter does
- [[Closure (Programming Languages)]]: a function bound with `let` is how functions get names
- [[Monad (Functional Programming)]]: `do` notation is sugar for chains of `>>=`
- [[Iterator]]: what a range-based `for` loop desugars into

# Sources

- [[Programming Languages (HMC CS131)]]
- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

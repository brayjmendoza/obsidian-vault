---
type: concept
created: 2026-11-15
updated: 2026-11-21
aliases:
  - λ-Calculus
  - Lambda Abstraction
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
The **lambda calculus** is a formal system of computation built from nothing but anonymous functions: variables, function definitions, and function applications.

It came out of the early-twentieth-century question of whether everything could be computed. David Hilbert believed every mathematical question could be settled mechanically. Alonzo Church (1935) showed that no general algorithm can decide whether two lambda expressions are equivalent, and Alan Turing (1936) showed that no general procedure can decide whether an arbitrary Turing machine halts. The two answers came from two models of computation at opposite ends of a **ladder of abstraction**: Turing machines are simple, low-level, and stateful, like engineering, while the lambda calculus is abstract and mathematical. Real languages sit in between, from assembly and C up through Python, Racket, and Haskell, with the lambda calculus above even pure functional languages.

Its grammar has just three kinds of expression:

```
expr ::= var              -- a variable
       | (expr expr)      -- function application
       | (λ var . expr)   -- lambda abstraction: a function with parameter var
var  ::= a | b | c | … | z
```

That's everything, and every computable function can be expressed in it. Studying it is an instance of a general principle: reduce a problem to a minimal set of parts, and anything proved about those parts holds for everything built from them (e.g., $\{\land, \lnot\}$ is enough for all of Boolean logic).

The vocabulary:

- **Lambda abstraction** `(λx . M)`: a function with **parameter** `x` and **body** `M`. Functions have no names, and every function takes one argument, so a function of several arguments is curried (e.g., `(λa . (λb . a))`) (see [[Currying]]).
- **Function application** `(M N)`: applying the function `M` to the argument `N`.
- **Bound and free variables:** a variable is bound by the nearest enclosing `λ` with its name, and free otherwise. A **closed** expression has no free variables, and an **open** one does (see [[Free and Bound Variables]]).
- **$\alpha$-equivalence:** renaming a bound variable throughout doesn't change an expression's meaning, so `(λx . x)` and `(λy . y)` are $\alpha$-equivalent. Renaming must not capture a free variable: `(λx . (x y))` is not $\alpha$-equivalent to `(λy . (y y))`.
- **≜:** a shorthand name for an expression (e.g., `TRUE ≜ (λa . (λb . a))`). Names are for people, not part of the calculus itself.

Computation is **$\beta$-reduction**, applying a function by substituting the argument for the parameter (see [[Beta Reduction]]). Data like Booleans, pairs, and numbers can all be represented as functions (see [[Church Encoding]]), and recursion comes from a fixed-point combinator (see [[Fixed-Point Combinator]]).

More generally, the claim that the lambda calculus and Turing machines capture everything that can be computed is the **Church–Turing thesis**. It's a thesis rather than a theorem, since "computable" has no formal definition outside such models, but every model proposed since has turned out equivalent. Functional languages are lambda calculi with extras: Haskell's compiler translates programs into a typed lambda calculus, an extension of **System F** called System FC, and typed lambda calculi are the setting for [[Typing Rule|typing rules]] and the [[Curry-Howard Correspondence|Curry–Howard correspondence]].

# Example

Some lambda expressions:

| Expression        | Reading                                                                             |
| ----------------- | ----------------------------------------------------------------------------------- |
| `(λx . x)`        | The identity function. Closed                                                       |
| `(λx . y)`        | A function that ignores its argument and returns `y`. Open, since `y` is free       |
| `(λx . (λy . x))` | A curried function that returns its first argument                                  |
| `((λx . x) a)`    | The identity function applied to `a`, which reduces to `a` (as the identity should) |
| `(x x)`           | `x` applied to itself. Open                                                         |

# Connections

- [[Beta Reduction]]: how lambda expressions compute
- [[Free and Bound Variables]]: which `λ` each variable refers to
- [[Church Encoding]]: representing data with nothing but functions
- [[Fixed-Point Combinator]]: recursion without names
- [[Currying]]: every lambda-calculus function takes one argument
- [[Functional Programming]]: functional languages are lambda calculi with conveniences added
- [[Interpreter]]: [[Arith]]'s `FuncDef` and `Apply` are lambda abstraction and application

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

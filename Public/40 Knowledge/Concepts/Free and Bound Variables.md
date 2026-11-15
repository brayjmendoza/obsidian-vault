---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Free Variable
  - Bound Variable
  - Closed Expression
  - Open Expression
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
In an expression, a variable occurrence is **bound** if a function definition around it introduces that name as its parameter, and **free** if nothing in the expression introduces it.

In the lambda calculus, `λx . M` binds `x` in the body `M`, so every `x` in `M` refers to that parameter (unless an inner `λx` binds it again). In `(λx . x)`, `x` is bound. In `(λx . y)`, `y` is free: no `λy` surrounds it, so its meaning has to come from outside the expression. An expression with no free variables is **closed**, and one with free variables is **open**. Whether a variable is free depends on the expression being looked at: in `((λx . ((x y) z)) h)`, `x` is bound, but in the body `((x y) z)` on its own, `x` is free.

The distinction matters whenever expressions are rewritten. [[Substitution]] replaces only free occurrences of a variable, since a bound occurrence refers to its own parameter. β-reduction removes a `λ`, so the variable it bound is substituted away (see [[Beta Reduction]]). And renaming a bound variable is safe only if the new name doesn't capture a free variable of the same name (see [[Lambda Calculus]], on α-equivalence).

More generally, the same distinction runs through all of programming. A function's free variables are exactly what its environment must supply: [[Static and Dynamic Scope|static and dynamic scope]] are two answers to where they come from, and a [[Closure (Programming Languages)|closure]] stores the bindings for them. In logic, quantifiers bind variables the same way (e.g., $x$ is bound in $\forall x . P(x)$), and in calculus, the variable of integration is bound.

# Example

| Expression | Bound | Free | Closed? |
|---|---|---|---|
| `(λx . x)` | `x` | none | Yes |
| `(λx . y)` | `x` (unused) | `y` | No |
| `(x y)` | none | `x`, `y` | No |
| `(λx . (λy . (x y)))` | `x`, `y` | none | Yes |
| `((λx . ((x y) z)) h)` | `x` | `y`, `z`, `h` | No |

# Connections

- [[Substitution]]: replaces free occurrences only, and must avoid capturing free variables
- [[Lambda Calculus]]: where bound and free variables are defined most simply
- [[Closure (Programming Languages)]]: a function packaged with the values of its free variables
- [[Static and Dynamic Scope]]: two rules for where a function's free variables get their values
- [[Name Binding]]: binding is how a name gets its meaning

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

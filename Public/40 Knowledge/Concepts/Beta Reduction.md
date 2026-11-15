---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - β-Reduction
  - Normal Form
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**β-reduction** is the lambda calculus's one rule of computation: applying a function to an argument by substituting the argument for the parameter in the function's body.

Applying `(λx . M)` to `N` reduces to $M[x \mapsto N]$, the body $M$ with every free $x$ replaced by $N$:

$$
((\lambda x . M) \; N) \;\to_\beta\; M[x \mapsto N]
$$

It's the same as applying a function in an interpreter by [[Substitution|substitution]]: plug in the argument, then keep evaluating. The `λx` disappears in the step, so the occurrences of `x` it bound are the ones replaced (see [[Free and Bound Variables]]).

An expression that can't be β-reduced any further is in **normal form**. Reducing an expression step by step usually reaches one, but not always. `((λx . (x x)) (λx . (x x)))` reduces to itself in one step, so reduction never ends, and the expression has no normal form.

Which part of an expression to reduce first can change whether reduction ends. In `((λy . pig) Ω)`, where Ω is the expression above with no normal form:

- **Substituting first** (call by name) drops Ω, since the function ignores its argument, and reaches `pig`.
- **Reducing the argument first** (call by value) tries to reduce Ω, and loops forever.

This is the same choice an interpreter makes (see [[Evaluation Strategy]]).

More generally, the **Church–Rosser theorem** says that whenever two orders of reduction both reach a normal form, they reach the same one, up to renaming bound variables. **Normal-order** reduction, which always reduces the leftmost outermost application first, is guaranteed to find a normal form if one exists. Substitution in β-reduction has to avoid capturing variables, renaming bound variables first when needed (i.e., α-conversion).

# Example

Reducing step by step:

```
((λx . ((x y) z)) h)     →  ((h y) z)                      normal form
(((λx . x) (λa . b)) y)  →  ((λa . b) y)  →  b             normal form
((λx . (x x)) (λx . (x x)))  →  ((λx . (x x)) (λx . (x x)))  →  …   no normal form
```

A curried two-argument function, applied one argument at a time:

```
(((λa . (λb . a)) pig) cow)  →  ((λb . pig) cow)  →  pig
(((λa . (λb . b)) pig) cow)  →  ((λb . b) cow)    →  cow
```

# Connections

- [[Lambda Calculus]]: β-reduction is its rule of computation
- [[Substitution]]: the operation each β-reduction step performs
- [[Evaluation Strategy]]: the order of reduction, by name or by value
- [[Lazy Evaluation]]: Haskell reduces in an order that finds a result whenever one exists, with sharing
- [[Free and Bound Variables]]: only free occurrences of the parameter are replaced

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

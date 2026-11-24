---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Russell's Set
  - Russell Paradox
fields:
  - math
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Russell's paradox** is the contradiction in naive set theory that comes from the set of all sets that aren't members of themselves.

Let $R = \{x \mid x \notin x\}$. If $R \in R$, then by its definition $R \notin R$. If $R \notin R$, then by its definition $R \in R$. Either answer contradicts itself.

A library version makes it concrete. Some libraries list their own catalog in their catalog, and some don't. The Library of Congress makes a catalog of every catalog that doesn't list itself. Should that catalog list itself? If it does, it shouldn't be in it, and if it doesn't, it should.

The paradox can be written in the lambda calculus by encoding sets as functions: a set is a function that returns `TRUE` for its members and `FALSE` otherwise (see [[Church Encoding]]). Russell's set returns `TRUE` exactly for the sets that don't contain themselves:

```
R ≜ (λx . (Not (x x)))
```

Asking whether $R$ contains itself means reducing `(R R)`, which gives `(Not (R R))`, then `(Not (Not (R R)))`, forever. In the lambda calculus the paradox isn't a contradiction. It's an expression with no normal form (see [[Beta Reduction]]): a question that never gets an answer.

More generally, Bertrand Russell found the paradox in 1901, in Gottlob Frege's system for founding mathematics on logic. It led to axiomatic set theories (e.g., Zermelo–Fraenkel set theory), which restrict how sets can be formed so that $R$ can't be built, and to Russell's theory of types, an early ancestor of type systems: in a typed lambda calculus, `(x x)` can't be typed, so the paradox can't be written. It's closely related to the liar paradox ("this statement is false") and to the diagonal arguments behind Cantor's theorem and the halting problem.

# Examples

## Applying R to Itself

`(R R)` reducing without end:

```
(R R)  =  ((λx . (Not (x x))) R)
       →  (Not (R R))
       →  (Not (Not (R R)))
       →  (Not (Not (Not (R R))))
       →  …
```

Smaller cases do have answers: `(R empty)` is `TRUE`, since the empty set doesn't contain itself, and `(R universe)` is `FALSE`, since the universe contains everything, itself included.

# Connections

- [[Church Encoding]]: sets as functions, which lets the paradox be written in the lambda calculus
- [[Fixed-Point Combinator]]: generalizes `(R R)`'s endless repetition into recursion
- [[Beta Reduction]]: `(R R)` has no normal form
- [[Type (Programming Languages)]]: Russell's theory of types, an answer to the paradox, began the idea of types

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

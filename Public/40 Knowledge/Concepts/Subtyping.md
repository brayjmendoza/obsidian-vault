---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Subtype
  - Substitutability
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Subtyping** is a relation between types, written $t_1 \sqsubseteq t_2$, saying that a value of type $t_1$ can safely be used wherever a value of type $t_2$ is expected.

The test is **substitutability**: nothing breaks if a value of the subtype arrives where the supertype was expected. An `int` can go anywhere a `double` is expected, so `int` is a subtype of `double`. A shop expecting dessert is happy to receive pie, so pie is a subtype of dessert. The reverse fails: a shop expecting pie might receive some other dessert. Subtyping resembles the subset relation in set theory, and every type is a subtype of itself.

A type system with subtyping adds one typing rule, called **subsumption**: if an expression has a type, it also has every supertype of that type.

$$
\frac{\Gamma \vdash e :: t_1 \qquad t_1 \sqsubseteq t_2}{\Gamma \vdash e :: t_2}
$$

With it, `if x < 10 then 3 else 3.14` type-checks as a `double`, though its two branches have different types: `3` is an `int`, and so also a `double`. Without subtyping, the `if` rule would reject it, since it requires both branches to have the same type.

Compound types get subtyping rules of their own. A pair is a subtype of another pair when each component is a subtype of the other pair's corresponding component (e.g., `(int, pie)` ⊑ `(double, dessert)`), and a list type is a subtype when its element type is a subtype (e.g., `[int]` ⊑ `[double]`). Function types follow a different rule (see [[Covariance and Contravariance (Type Systems)|Covariance and Contravariance]]). The subtype relationships among a set of types can be drawn as a lattice (see [[Top and Bottom Types]]).

More generally, subtyping is central to object-oriented languages, where a subclass is a subtype of its superclass, and the substitutability test is known there as the **Liskov substitution principle**. Haskell has no subtyping: its numeric types are separate, and conversions between them are explicit (e.g., `fromIntegral`). Languages also differ in whether subtyping is declared by name (**nominal**, as in Java) or follows from a type's structure (**structural**, as in TypeScript).

# Example

A function of a `double`, applied to an `int`:

```
(\r :: double -> r * r * 3.14) 7
```

Since `int` ⊑ `double`, subsumption gives `7` the type `double`, and the application type-checks.

# Connections

- [[Typing Rule]]: subtyping adds the subsumption rule
- [[Covariance and Contravariance (Type Systems)]]: how subtyping extends to function and container types
- [[Top and Bottom Types]]: the greatest and least types, and the lattice between them
- [[Type System]]: subtyping is one way a type system allows flexibility

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

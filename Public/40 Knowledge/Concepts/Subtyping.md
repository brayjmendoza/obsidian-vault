---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Subtype
  - Substitutability
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Subtyping** is a relation between types, written $t_1 \sqsubseteq t_2$, saying that a value of type $t_1$ can safely be used wherever a value of type $t_2$ is expected.

The test is **substitutability**: nothing breaks if a value of the subtype arrives where the supertype was expected. An `int` can go anywhere a `double` is expected, so `int` is a subtype of `double`. A shop expecting dessert is happy to receive pie, so pie is a subtype of dessert. The reverse fails: a shop expecting pie might receive some other dessert. Subtyping resembles the subset relation in set theory, and every type is a subtype of itself.

A type system with subtyping adds one typing rule, called **subsumption**: if an expression has a type, it also has every supertype of that type.

$$
\frac{\Gamma \vdash e :: t_1 \qquad t_1 \sqsubseteq t_2}{\Gamma \vdash e :: t_2}
$$

With it, `if x < 10 then 3 else 3.14` type-checks as a `double`, though its two branches have different types: `3` is an `int`, and so also a `double`. Without subtyping, the `if` rule would reject it, since it requires both branches to have the same type.

Compound types get subtyping rules of their own. A pair is a subtype of another pair when each component is a subtype of the other pair's corresponding component (e.g., `(int, pie)` ⊑ `(double, dessert)`). A list type is a subtype when its element type is a subtype (e.g., `[int]` ⊑ `[double]`). Function types follow a different rule (see [[Covariance and Contravariance (Type Systems)|Covariance and Contravariance]]). The subtype relationships among a set of types can be drawn as a lattice (see [[Top and Bottom Types]]).

In C++, a class derived from another is a subtype of it, so a `Student` derived from `Person` can be passed wherever a `Person` is expected, by pointer or by reference (see [[Inheritance (Object-Oriented Programming)]]). Numeric types follow the same pattern: wherever a `double` is wanted, a `float` can be given, much as `int` is a subtype of `double` above. C++ itself implements that case by promotion, converting the value to the wider type rather than treating it as a subtype (see [[Type Conversion]]).

More generally, subtyping is central to object-oriented languages, where a subclass is a subtype of its superclass, and the substitutability test is known there as the **Liskov substitution principle**. Haskell has no subtyping: its numeric types are separate, and conversions between them are explicit (e.g., `fromIntegral`). Languages also differ in whether subtyping is declared by name (**nominal**, as in Java) or follows from a type's structure (**structural**, as in TypeScript).

# Examples

## An Int as a Double

A function of a `double`, applied to an `int`:

```
(\r :: double -> r * r * 3.14) 7
```

Since `int` ⊑ `double`, subsumption gives `7` the type `double`, and the application type-checks.

## A Derived Class

In C++, a function written for `Person` accepts a `Student`, since a derived class is a subtype of its base class:

```c++
void greet(const Person& p);
Student ada{"Ada"};
greet(ada);    // fine: every Student is a Person
```

The reverse fails: a function that wants a `Student` can't be given an arbitrary `Person`.

# Connections

- [[Typing Rule]]: subtyping adds the subsumption rule
- [[Covariance and Contravariance (Type Systems)]]: how subtyping extends to function and container types
- [[Top and Bottom Types]]: the greatest and least types, and the lattice between them
- [[Type System]]: subtyping is one way a type system allows flexibility
- [[Type Conversion]]: using a value where another type is expected by changing its representation, instead of treating it as a subtype
- [[Inheritance (Object-Oriented Programming)]]: how C++ declares that one class is a subtype of another
- [[Polymorphism (Computer Science)]]: subtyping gives subtype polymorphism
- [[Dynamic Dispatch]]: a call through a supertype reaching the subtype's own implementation

# Sources

- [[Programming Languages (HMC CS131)]]
- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

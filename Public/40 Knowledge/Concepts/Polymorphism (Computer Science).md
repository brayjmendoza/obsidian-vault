---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Polymorphism
  - Polymorphic Function
  - Static Polymorphism
  - Dynamic Polymorphism
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Polymorphism**, from the Greek for "many forms," is the ability of one piece of code to work with values of more than one type: a function is **polymorphic** if it has at least one parameter that accepts arguments of more than one type.

C++ offers three kinds, each with its own mechanism:

| Kind | How one name handles many types | C++ mechanism |
|---|---|---|
| **Subtype polymorphism** | Code written for a type also accepts its subtypes, since every subtype value can be seen as the supertype | Inheritance: a derived class is a subtype of its base class (see [[Inheritance (Object-Oriented Programming)]]) |
| **Parametric polymorphism** | One definition takes a type as a parameter and works the same way for every type filled in | Templates (see [[Parametric Polymorphism]]) |
| **Ad hoc polymorphism** | Separate definitions share a name, one for each type they handle | Overloading (see [[Function Overloading]]) |

Subtype polymorphism is what lets a function that wants a `Person` accept a `Student`, when `Student` is derived from `Person`. Parametric polymorphism lets a single `max` template work for `int`s, `double`s, and strings, and people often call such code **generic**. Ad hoc polymorphism gives `max` separate definitions for `int` and `double`: it works only for the types someone wrote a definition for, which is why it's called *ad hoc*, "for this purpose."

The kinds also differ in when the choice of code is made. Templates and overloading are resolved when the program is compiled, from the types written in the code, so they're **static polymorphism**. Subtype polymorphism with virtual member functions is resolved while the program runs, from the type of the object actually present, so it's **dynamic polymorphism** (see [[Dynamic Dispatch]]).

More generally, Christopher Strachey distinguished parametric from ad hoc polymorphism in 1967, and Luca Cardelli and Peter Wegner's 1985 survey added subtyping as a third kind. In Haskell, parametric polymorphism uses type variables, and [[Type Class|type classes]] give a disciplined form of ad hoc polymorphism, where each type supplies its own implementation of the class's operations. Java has all three kinds: inheritance, generics, and overloading.

# Examples

## Max through Templates and Overloads

The same operation, `max`, through parametric and ad hoc polymorphism:

```cpp
// Parametric: one template for every type with >
template <typename T>
const T& max(const T& x, const T& y) {
    return x > y ? x : y;
}

// Ad hoc: one definition per type
int max(int x, int y);
double max(double x, double y);
```

The template works for any type that supports `>`, including types written after it, since the compiler fills in `T` at each use. The overloads work only for `int` and `double`: calling `max` on two strings would need a third definition.

# Connections

- [[Parametric Polymorphism]]: one definition for every type
- [[Function Overloading]]: one name, a definition per type
- [[Subtyping]]: what makes a value of one type usable as another
- [[Inheritance (Object-Oriented Programming)]]: how C++ declares subtypes
- [[Dynamic Dispatch]]: choosing a member function's implementation at run time
- [[Type Class]]: Haskell's structured form of ad hoc polymorphism

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

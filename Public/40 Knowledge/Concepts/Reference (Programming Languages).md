---
type: concept
created: 2026-11-23
updated: 2026-11-23
aliases:
  - Reference
  - Referent
  - Aliasing
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **reference** is another name for an existing object: the reference and the object it refers to, its **referent**, are the same thing in memory.

In C++, `&` in a type means "reference to," and a reference is bound to its referent when it's initialized:

```c++
int x = 5;
int& z = x;   // z is a reference to an int, and its referent is x
```

From then on, `x` and `z` are interchangeable: they name the same memory, so a change through either name is seen through both. A reference **never changes its referent**. Assigning to a reference assigns to the referent, so `z = y;` copies `y`'s value into `x` rather than making `z` refer to `y`. Initializing a reference from another reference gives a third name for the same referent, not a reference to a reference.

References compare with [[Pointer (Programming Languages)|pointers]] this way:

| | Reference | Pointer |
|---|---|---|
| Is | Another name for an object | An object holding an address |
| Its own storage | None | Yes, like any other variable |
| Must be initialized | Yes, to a referent | No (but a default-initialized pointer is invalid) |
| Can change what it refers to | Never | Yes |
| Can refer to nothing | No | Yes, as a null pointer |
| Arithmetic | No | Yes, within an array |

So a pointer is the more general of the two, and a reference is simpler and safer where it suffices. References are used mostly for function parameters: a reference parameter lets a function change the caller's variable or avoid copying a large object (see [[Evaluation Strategy]]). A reference to `const` gives access that can only read (see [[Const-Correctness]]).

More generally, the C++ reference is one form of **aliasing**, two names for the same storage. Languages like Java and Python call their hidden pointers "references," but those can be null and can be made to refer to another object, so they're closer to C++ pointers. Aliasing makes programs harder to reason about, since a change through one name affects another, which is part of why [[Referential Transparency|pure functional languages]] avoid mutable state altogether.

# Example

`a` and `b` name the same `int`:

```c++
int a = 2;
int& b = a;
int c = 31;
a = 8;
std::cout << a << " " << b;          // 8 8
b = c;
std::cout << " " << a << " " << b;   // 31 31
```

This prints `8 8 31 31`. Assigning to `a` changes `b`, since they're the same memory. `b = c` doesn't make `b` refer to `c`: it copies 31 into `b`'s referent, `a`, so afterward `a` is 31 too, while `c` is still a separate variable.

# Connections

- [[Pointer (Programming Languages)]]: the more general tool, which holds an address and can change it
- [[Evaluation Strategy]]: reference parameters make call by reference
- [[Const-Correctness]]: `const` references give read-only access through one name
- [[Name Binding]]: like a binding, a reference is attached to its referent once and never rebound
- [[Object Lifetime]]: a reference adds no lifetime of its own

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Const
  - const Reference
  - const Pointer
  - const Member Function
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Const-correctness** is marking every name that shouldn't be used to change data as read-only, so the compiler rejects any attempt to change data through it.

In C++, `const` in a type makes access through that name read-only. A `const` variable can't be changed at all, and a reference to `const` or a pointer to `const` can read its target but not change it. The key idea is that **`const` affects access through that name only**. It doesn't make the data itself unchangeable: other, non-`const` names for the same data can still change it.

```c++
int a = 3;
const int& b = a;
++a;   // fine: a isn't const, and b sees the new value, 4
++b;   // compile error: b is a const reference
```

The compiler checks what code *could* do, not what it does. A function whose parameter is a non-`const` pointer could change the data it's given, so the compiler won't pass it a pointer to `const` data, even if the function never actually writes. This gives one rule: **`const` can be added but not removed.** A `const` reference to a non-`const` variable is fine, since it only restricts access. A non-`const` reference to a `const` variable, or to a `const` reference, is a compile error, since it would be a way around the `const`.

For a pointer, where `const` goes matters, since two things could be read-only (see [[Reading C++ Declarations]]):

| Declaration | Can't change |
|---|---|
| `const float* p` | The `float`, through `p` |
| `float* const p` | `p` itself: it always points to the same place |
| `const float* const p` | Both |

The usual use is function parameters. Passing a large object by `const` reference avoids copying it (see [[Evaluation Strategy]]) and promises the caller it won't be changed. A function that only reads should take `const` parameters, or it can't be called with `const` data at all.

A member function can be `const` too, written at the end of its declaration (e.g., `int getAge() const;`), in both the header and the source file. It promises not to change the object it's called on: inside it, the object, and so every member variable, is treated as `const`. This has three uses:

- **Checking:** the compiler rejects any change to a member inside it, so a function meant only to read can't write by mistake.
- **A contract:** anyone using the class knows a `const` member function leaves the object as it was.
- **`const` objects:** a `const` object can call only `const` member functions. A class with none can still have `const` objects, but nothing can be done with them, so every member function that can be `const` should be.

More generally, the term "const-correctness" comes from the C++ community, and C has `const` too. Other languages offer read-only access in other ways: Java's `final` fixes a variable but not the object it refers to, much like `float* const`, and Rust makes every reference read-only unless it's marked `&mut`, which inverts C++'s default. In a pure functional language, nothing can be changed, so the question never comes up (see [[Referential Transparency]]).

# Examples

## A Read-Only Array Parameter

`max_value` only reads the array, but its parameters are plain pointers:

```c++
float max_value(float* firstValPtr, float* pastEndPtr);

const float temps[3]{1.5, 3.5, 2.5};
max_value(temps, temps + 3);   // compile error
```

The call fails because `*firstValPtr` *could* be used to change a `const` array. Declaring the parameters as pointers to `const` fixes it:

```c++
float max_value(const float* firstValPtr, const float* pastEndPtr);
```

Now the function promises not to change the floats, the compiler checks that promise inside it, and both `const` and non-`const` arrays can be passed in.

# Connections

- [[Reference (Programming Languages)]]: a `const` reference reads its referent without copying it
- [[Pointer (Programming Languages)]]: `const` can apply to the pointer, to its target, or to both
- [[Evaluation Strategy]]: pass by `const` reference avoids a copy without allowing changes
- [[Class (Programming Languages)]]: `const` member functions, the only ones a `const` object can call
- [[Type System]]: `const` is part of a type, so the type checker enforces it
- [[Referential Transparency]]: where nothing can change, there's nothing for `const` to protect

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

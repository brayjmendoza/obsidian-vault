---
type: concept
created: 2026-11-23
updated: 2026-11-23
aliases:
  - Lvalue
  - Rvalue
  - Temporary
  - Temporary Object
  - Value Category
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An **lvalue** is an expression that names an object with a location in memory, and an **rvalue** is a result value, often held in a short-lived unnamed **temporary**.

The names come from the two sides of an assignment like `x = y + z`. The left side must be something with a location, so the new value has somewhere to go: `x` is an lvalue. The right side only needs to produce a value: `y + z` is an rvalue. An rvalue has no lasting name or location of its own, so some operations that need one reject it. For instance, `&(x + y)` is an error, since there's no address to take, and error messages report it in these terms.

Whenever C++ calls a function or operator that returns a value, or calls a constructor directly, and the result isn't put straight into a named variable, the result is stored in a **temporary**: an unnamed object that lasts until the end of the line of code that made it. A call like `passByConstRef(x + y)` can be modeled as:

```c++
{
    int _temp1 = x + y;
    passByConstRef(_temp1);
}
```

Since a temporary is gone after its line, a non-`const` reference can't be bound to it: the change it allowed would be lost. A `const` reference can be, which is why a function taking a `const` reference accepts rvalues like `x + y`.

The model also shows how calls are evaluated: one function call at a time, with intermediate results in hidden temporaries. A chain like `cout << 42 << 'x'` is a call whose result, a reference to `cout`, is the left argument of the next call.

More generally, the terms come from the language CPL and passed through C to C++. Modern C++ refines them into **value categories** (lvalue, xvalue, and prvalue), and C++11 added **rvalue references** (`&&`), which bind only to temporaries so their contents can be moved rather than copied, since nothing else will use them.

# Example

Each `<<` returns a reference to its left-hand stream, so a chain of them is a chain of calls on temporaries:

```c++
std::cout << 42 << 'x';
```

can be modeled as:

```c++
{
    std::ostream& _temp1 = std::cout << 42;
    _temp1 << 'x';
}
```

`_temp1` is a reference to `std::cout` itself, so the second `<<` writes to the same stream.

# Connections

- [[Object Lifetime]]: a temporary's lifetime is one line, and returning a value initializes an object in the caller
- [[Reference (Programming Languages)]]: only `const` references can refer to temporaries
- [[Const-Correctness]]: why a `const` reference parameter accepts rvalues
- [[Expressions and Statements]]: every expression either names a location or produces a value

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

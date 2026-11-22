---
type: concept
created: 2026-11-15
updated: 2026-11-21
aliases:
  - Well-Typed
  - Type Error
  - Type Conflict
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **type system** is a set of rules that assigns types to a program's expressions and governs how values of different types may be combined.

A program is **well-typed** when the type system finds no type conflicts in it. A **type conflict** (or type error) is a use of a value its type doesn't allow: assigning a string to an integer variable, or applying a function to an argument it can't handle (e.g., `String s = 10;` in Java, or `True.upper()` in Python). `let x = 1 in x + 1` is well-typed, since `x` is an integer and `+` is defined on integers. Haskell won't run a program unless it's well-typed.

Type systems differ in what they do with an expression like `"one" + 2`:

| Language | Result |
|---|---|
| JavaScript | `"one2"`: the number becomes a string |
| Perl | `2`: a non-numeric string counts as 0 |
| Haskell, Python | A type error |

They also differ in when they report a conflict: before the program runs, or as it runs (see [[Static and Dynamic Typing]]). A type system can be specified precisely as a set of [[Typing Rule|typing rules]], one per kind of expression, and checking that a program is well-typed means building a proof from those rules.

More generally, a language that converts values between types implicitly, as JavaScript and Perl do, is often called **weakly typed**, and one that reports a conflict instead is **strongly typed**, though the terms have no exact definition. Strength is a separate question from when checking happens: Python is dynamically and strongly typed, and C is statically but fairly weakly typed. In C++, `"one" + 2` isn't an error at all: it compiles to pointer arithmetic, giving the string `"e"`.

# Example

Two type conflicts, in Java and in Python:

```java
String s;
s = 10;           // type error: an int isn't a String
```

```python
True.upper()      # type error: a bool has no upper method
```

# Connections

- [[Type (Programming Languages)]]: what a type system classifies
- [[Static and Dynamic Typing]]: when a type system's checks happen
- [[Typing Rule]]: how a type system is written down precisely
- [[Type Inference]]: working out types the programmer didn't write
- [[Subtyping]]: rules that let a value of one type stand in for another

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-15
updated: 2026-11-21
aliases:
  - Type
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **type** is a classification of values that says how their data is interpreted and what can be done with them.

The same data can mean entirely different things depending on its type. One sequence of 32 bits can be read as a big-endian integer, a little-endian integer, a floating-point number, text in ASCII or UTF-16, or machine instructions for several different processors. Nothing in the bits says which: the type is what tells a program how to interpret the data in memory.

A type is many things at once:

- **An abstraction:** every integer has the same properties, whatever its value.
- **A set of allowed values,** and **a set of operations** on them.
- **A representation:** what to put in memory, and how.
- **A label for people** reading the code, and **a context** for the data.
- **A composition of other types** (e.g., a pair of an `Int` and a `Bool`, or a list of strings).

Types serve several purposes. They catch programming errors, they let compilers generate more efficient code, they give an interpretation to information, and they restrict what can be done with it. The rules for how a language's types behave make up its [[Type System|type system]].

More generally, type theory, the mathematical study of types, began as a foundation for mathematics (e.g., Russell's theory of types, which avoided paradoxes in set theory), well before programming languages existed. In programming, the "set of values" view is the usual starting point, and the "set of operations" view leads to abstract data types and interfaces.

# Example

One 32-bit pattern, read as different types:

| Interpretation | Value |
|---|---|
| Raw bits | `01100000 01110000 01001110 01110001` |
| Hexadecimal | `0x60704E71` |
| Big-endian integer | `1617972849` |
| Little-endian integer | `1900965984` |
| 32-bit floating point, little-endian | about `1.02e30` |
| ASCII text | `` `pNq `` |

# Connections

- [[Type System]]: the rules a language applies to its types
- [[Static and Dynamic Typing]]: when a language checks how values are used against their types
- [[Algebraic Data Type]]: building new types from alternatives and combinations of existing ones
- [[Russell's Paradox]]: Russell's theory of types, an early answer to it, began the idea of types

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

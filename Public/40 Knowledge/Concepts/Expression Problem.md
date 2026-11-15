---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Functional vs Object-Oriented Programming
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
The **expression problem** is the tradeoff between two ways of organizing a program that has several kinds of data and several operations on them: grouping the code by kind of data, or grouping it by operation.

Take shapes (i.e., circles, squares, and right triangles) and two operations on them (i.e., computing the area and shifting the position). Object-oriented and functional programming organize the same program from two points of view:

| | Object-oriented | Functional |
|---|---|---|
| Unit of code | A class for each kind of data, with a method for each operation | An [[Algebraic Data Type\|algebraic data type]] for the data, and a function for each operation |
| Point of view | "A circle knows how to compute its own area and perform a shift" | "The `shift` function knows how to shift a square, circle, or right triangle" |
| Top-level concept | Objects, which perform different operations on themselves | Functions, which compute over different kinds of data |

The two aren't opposites: they slice the same grid of data and operations in different directions. The comparison also shows that a data type is not a class. A data type only describes the shape of its values, and the operations live outside it, in functions.

More generally, each organization makes one kind of change easy and the other hard:

- **Object-oriented:** a new kind of data is one new class, but a new operation means a new method in every class.
- **Functional:** a new operation is one new function, but a new kind of data means a new case in every function.

The right choice depends on which changes a program expects. The name comes from Philip Wadler, who posed it as the problem of getting both kinds of extension at once without editing existing code.

# Example

The functional organization, in Haskell:

```haskell
data Shape
  = Circle Double Double Double                -- x, y, radius
  | Square Double Double Double                -- x, y, side
  | RightTriangle Double Double Double Double   -- x, y, legs

area :: Shape -> Double
area shape = case shape of
  Circle _ _ r          -> pi * r * r
  Square _ _ s          -> s * s
  RightTriangle _ _ a b -> a * b / 2
```

Adding a `perimeter` function touches nothing else. Adding a `Rectangle` means a new case in `area`, `shift`, and every other function on shapes. In the object-oriented version (e.g., an abstract `Shape` class in Java, with `Circle`, `Square`, and `RightTriangle` subclasses that each implement `area`), the reverse holds: `Rectangle` is one new class, and `perimeter` is a new method in every class.

# Connections

- [[Algebraic Data Type]]: the functional side's way of defining data by its alternatives
- [[Pattern Matching]]: how each function handles every alternative of the data
- [[Functional Programming]]: puts operations, not objects, at the top level of a program

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-15
updated: 2026-11-15
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Code as data** is the idea that a program can be represented as a data structure, so that other programs can take it as input, inspect it, transform it, or run it.

Most programs take ordinary data as input (e.g., a list of numbers to average, or a text file to spell-check). But a program's input can also be source code. A line counter, a code formatter, a compiler that translates source code into machine code, and an interpreter that computes a program's value all take code as their input. To do any of that, a program needs code in a form it can work with: a data structure that records the code's parts and how they fit together, rather than the raw text (see [[Concrete and Abstract Syntax]]).

In Haskell, that data structure is an [[Algebraic Data Type|algebraic data type]] with a constructor for each kind of expression. An expression in the language being represented becomes a tree of constructors, and an evaluator is a function over that tree (see [[Interpreter]]). Functions themselves can be represented this way too, as a constructor holding a parameter name and a body.

More generally, the idea runs through all of language implementation: compilers, linters, and refactoring tools all treat programs as data. In the Lisp family of languages, code is written directly in the language's own list syntax, so a program can build and run code with the same operations it uses on lists.

# Example

The expression `(2 + 2) * 7 - 11`, as data:

```haskell
data Op  = PlusOp | MinusOp | TimesOp | DivOp
data Exp = Num Double | BinOp Exp Op Exp

BinOp (BinOp (BinOp (Num 2) PlusOp (Num 2)) TimesOp (Num 7)) MinusOp (Num 11)
```

A program can now count its operators, print it, or compute its value, all by pattern matching on `Exp`.

# Connections

- [[Concrete and Abstract Syntax]]: abstract syntax is the data structure that code becomes
- [[Interpreter]]: a program that takes code as data and computes its value
- [[Algebraic Data Type]]: how Haskell defines the data structure for a language's code

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

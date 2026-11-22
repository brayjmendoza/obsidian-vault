---
type: concept
created: 2026-11-15
updated: 2026-11-21
aliases:
  - Syntax
  - Semantics
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A language's **syntax** is what a programmer is allowed to write, and its **semantics** is what that writing means.

Syntax answers "is this valid code?", and semantics answers "what does it do?" In C++, the fact that `int x;` is valid code is syntax, and the fact that it declares a new integer variable `x` is semantics. Some facts are both: a semicolon on its own is a legal statement (syntax) that does nothing (semantics).

Implementing a language means handling both. Syntax comes in two forms: the text the programmer writes, and the tree structure that text represents (see [[Concrete and Abstract Syntax]]). Semantics can be defined by an evaluator, a function that takes the tree and computes its meaning (see [[Interpreter]]).

More generally, there are several formal ways to define semantics. Defining a language's meaning with an evaluation function, as an [[Interpreter|interpreter]] does (e.g., [[Arith]]'s `eval`), is a kind of **operational semantics**, which defines meaning by how a program runs. Others define meaning mathematically (**denotational semantics**) or by what can be proved about a program (**axiomatic semantics**). The gap between symbol and meaning reaches beyond programming, into linguistics and the philosophy of mind.

# Example

Statements about C++, sorted:

| Statement | Syntax or semantics |
|---|---|
| `^` is a valid binary operator | Syntax: it says what you may write |
| On two integers, `^` computes bitwise exclusive-or | Semantics: it says what the code does |
| Adding two `int`s whose sum doesn't fit in an `int` is undefined | Semantics |
| A semicolon by itself is a legal statement that does nothing | Both |
| `new int` allocates an uninitialized integer, and `new int()` allocates `0` | Mostly semantics |

# Connections

- [[Concrete and Abstract Syntax]]: the two forms syntax takes
- [[Interpreter]]: an evaluator defines a language's semantics
- [[Expressions and Statements]]: two kinds of syntax with different semantics
- [[Context-Free Grammar]]: the usual way to specify a language's syntax

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

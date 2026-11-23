---
type: concept
created: 2026-11-15
updated: 2026-11-23
aliases:
  - Expression
  - Statement
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
An **expression** is a computation that produces a value, and a **statement** is a computation performed for its effect, such as changing a variable.

Expressions can combine: `10 * z + 4` is one large expression built from smaller ones, and every part has a value. A statement doesn't have a value of its own. It may change values (e.g., `x = x - 1` changes `x`), but it can't be used where a value is expected: a `while` loop can't be assigned to a variable. A **side effect** is anything an expression does besides produce its value.

The two divide programming styles. In imperative programming, computation means executing a series of statements. In [[Functional Programming|functional programming]], computation means evaluating expressions, and functional languages allow few side effects (e.g., Racket) or none (e.g., Haskell). Some code is both: in C, `x++` is an expression, since it has a value, and it also has the side effect of incrementing `x`.

More generally, languages differ in how much they make into expressions. In expression-oriented languages (e.g., Haskell, Rust, and Ruby), constructs like `if` produce values, so `if` can appear inside an arithmetic expression. In statement-oriented languages (e.g., C and Java), `if` is a statement, and a separate operator (`?:`) serves as the expression form.

# Example

In C and C++:

| Code | Kind | Why |
|---|---|---|
| `10 * z + 4` | Expression | It evaluates to a value |
| `x++;` | Statement, containing an expression with a side effect | It increments `x`, and `x++` alone also has a value |
| `while (x > 3) { x = x - 1; y = y + 1; }` | Statement | It has no value: `x = (while …)` isn't valid |

# Connections

- [[Functional Programming]]: computation by evaluating expressions instead of executing statements
- [[Referential Transparency]]: an expression without side effects can be replaced by its value
- [[Syntax and Semantics]]: whether something is an expression or a statement is part of a language's syntax, and what it does is its semantics
- [[Lvalues and Rvalues]]: an expression either names a location or produces a value

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

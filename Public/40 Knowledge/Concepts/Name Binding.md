---
type: concept
created: 2026-11-11
updated: 2026-11-21
aliases:
  - Binding
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Binding** a name associates it with an expression, and that expression is the name's **value**.

Binding resembles assignment in an imperative language, but the two differ. Assignment stores a value in a variable, and a later assignment can replace it. Binding associates the name with an entire expression, and a name can be bound at most once in a given [[Scope]]. So in a pure language like Haskell, every "variable" is a constant.

A few related terms:

- **Reference:** to use a name in an expression (e.g., `y = 2 * x` references `x`).
- **Look up** or **resolve:** to evaluate a name, finding its value. During evaluation, a name is just an alias for its expression.
- **Variable names:** in Haskell, they start with a lowercase letter. Type names start with an uppercase letter, though not every uppercase name is a type (e.g., the values `True` and `False`).

Since a name can't be rebound, an apparent update is something else. `x = x + 1` doesn't add one to `x`. It defines `x` in terms of itself, so evaluating `x` requires evaluating `x` first, and evaluation never finishes.

# Example

Two top-level bindings, read as "bind `x` to the expression `21`" and "bind `y` to the expression `2 * x`":

```haskell
x = 21
y = 2 * x
```

Binding `x` again in the same file is an error, not an update:

```haskell
x = 24
x = 41     -- error: Multiple declarations of `x'
x = x + 1  -- error: Multiple declarations of `x'
```

GHCi accepts these lines one at a time, since each line it reads starts a new scope. But after the third line, `x` refers to itself, and asking for its value loops forever.

# Connections

- [[Scope]]: where a binding is visible, and why a name can be bound only once in each
- [[Lazy Evaluation]]: in Haskell, a binding holds an unevaluated expression until the name is needed
- [[Referential Transparency]]: why a name can stand in for its expression
- [[Substitution]]: a function's parameter is a binding, which substitution must not replace inside the function
- [[Environment (Programming Languages)]]: the record of bindings an evaluator keeps while a program runs
- [[Free and Bound Variables]]: an occurrence is bound if some enclosing binding introduces its name

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

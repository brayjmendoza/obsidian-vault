---
type: concept
created: 2026-11-11
updated: 2026-11-15
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-11
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
The **scope** of a binding is the region of a program where its name can be referenced.

Where a name is bound decides its scope. In Haskell:

| Binding | Scope |
|---|---|
| Top-level binding (e.g., `x = 21` in a file) | The entire file, or the rest of a GHCi session, like a global variable |
| Function parameter (e.g., `n` in `successor n = n + 1`) | The function's body |
| `let` binding (e.g., `let x = 21 in x + x`) | The body of the `let` expression, after `in`, and the `let`'s own bindings |
| `where` binding | The function's whole body, including the `where` clause |

A **let expression** binds names for one expression: `let` introduces the bindings, and `in` introduces the **body**. The result of the whole `let` expression is the result of its body (e.g., `let x = 21 in x + x` evaluates to `42`). A `where` clause does the same job at the end of a function definition. Choosing between them is mostly a matter of style.

**Scopes nest.** A `let` inside another `let` has its own scope, and Haskell resolves a name from the innermost scope outward. An inner binding of a name **shadows** an outer one: inside the inner scope, the outer binding can't be referenced. Each scope can still bind a name only once (see [[Name Binding]]).

Which binding a function's free variables refer to, the one where it's defined or the one where it's called, is a separate choice (see [[Static and Dynamic Scope]]).

# Example

Three ways to define $f(x) = x^2 + \frac{1}{x^2}$:

```haskell
f x = x * x + 1 / (x * x)

f x = let value = x * x
      in value + 1 / value        -- value's scope: the let body

f x = value + 1 / value
  where value = x * x             -- value's scope: all of f's body
```

Nested scopes resolve from the inside out:

```haskell
let x = 21 in let x = 10000 in x  -- 10000: the inner x shadows the outer one
```

A single `let` can bind several names, aligned in the same column, and one can reference another:

```haskell
let x = 21
    y = x * 3
in x + y  -- 84
```

Binding the same name twice in one `let` (e.g., `let x = 2; x = 3 in x`) is an error.

# Connections

- [[Name Binding]]: what a scope contains, and why each name is bound only once in it
- [[Functional Programming]]: with no reassignment, scope alone decides what a name means
- [[Substitution]]: substituting into a function has to respect which binding each variable refers to
- [[Static and Dynamic Scope]]: whether a function's free variables use the bindings at its definition or at its call

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

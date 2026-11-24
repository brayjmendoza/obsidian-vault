---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Static Scope
  - Dynamic Scope
  - Lexical Scope
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
Under **static scope**, a function's variables refer to the bindings in effect where the function was defined, and under **dynamic scope**, to the bindings in effect where it's called.

The two only differ for a function's **free variables**: names its body uses but doesn't bind itself (e.g., `v` in a function of `x` whose body is `v + x`). The parameter is always bound by the call. A free variable has to be looked up somewhere else, and the two rules disagree about where:

- **Dynamic scope:** use the closest enclosing binding at the time of the call.
- **Static scope:** use the closest enclosing binding at the time of the definition.

An interpreter that evaluates a function's body in the caller's [[Environment (Programming Languages)|environment]] gets dynamic scope without meaning to. Getting static scope means remembering the environment from the definition, which is what a [[Closure (Programming Languages)|closure]] does. Haskell uses static scope.

More generally, static scope is also called **lexical scope**, since the bindings a name can refer to can be read off the program's text. Nearly every modern language uses it (e.g., Haskell, Python, JavaScript, and Java), because a function then means the same thing wherever it's called. Dynamic scope survives in a few places (e.g., Emacs Lisp without lexical binding turned on, and `local` variables in Bash), and it began in early Lisp largely by accident.

# Examples

## A Function Called in Another Scope

```haskell
let v = 42 in
let f x = v + x in
let v = 3 in
f 100
```

The function `f` is defined where `v` is 42 and called where `v` is 3:

| Rule | `v` inside `f` | Result |
|---|---|---|
| Dynamic scope | The binding at the call: 3 | `103` |
| Static scope | The binding at the definition: 42 | `142` |

Haskell gives `142`.

# Connections

- [[Scope]]: what a scope is, and how nested scopes resolve a name
- [[Closure (Programming Languages)]]: what an interpreter needs to implement static scope
- [[Environment (Programming Languages)]]: the bindings a function's body is evaluated in
- [[Substitution]]: substituting into a function's body faces the same question of which binding a name means
- [[Free and Bound Variables]]: the two rules differ only on free variables

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

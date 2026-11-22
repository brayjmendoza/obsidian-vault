---
type: concept
created: 2026-11-11
updated: 2026-11-21
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Functional programming** is a style of programming in which computation proceeds by evaluating expressions, rather than by updating state.

An **expression** is a piece of computation (e.g., `1 + 2` or `f 3`), and to **evaluate** it is to try to compute its result. Evaluation either terminates with a result or **diverges**, running forever. In **imperative programming**, a program is a sequence of statements that change the machine's state: variables are assigned, reassigned, and read back. Functional programming puts expressions at the center instead, and its main building block is the function, an expression with parameters (see [[Abstraction]]).

A **side effect** is anything an evaluation does to change state besides producing its result (e.g., modifying a variable or printing a message). A **pure** expression has no side effects. In **pure functional programming**, evaluating pure expressions is the only way computation proceeds. Haskell is a pure functional language, and several of its traits follow from that:

- **Variables are constants.** A name is bound once and never reassigned (see [[Name Binding]]).
- **Programs are easier to reason about.** With no hidden state, an expression means the same thing wherever it appears (see [[Referential Transparency]]).
- **Evaluation order is free.** No expression can observe another's effects, so evaluation can wait until a result is needed (see [[Lazy Evaluation]]) or run in parallel.
- **Output needs separate machinery.** Printing is a side effect, so ordinary expressions can't print. Haskell handles input and output with the `IO` type, a [[Monad (Functional Programming)|monad]] that keeps effects out of ordinary expressions.

# Example

Factorial, written imperatively in Python and functionally in Haskell:

```python
def fact(n):
    result = 1
    while n > 0:
        result = result * n
        n = n - 1
    return result
```

```haskell
fact 0 = 1
fact n = n * fact (n - 1)
```

The Python version reaches its answer by changing `result` and `n` on every pass through the loop. The Haskell version changes nothing: `fact 3` is an expression equal to `3 * fact 2`, and evaluation rewrites it, step by step, until only `6` is left.

# Connections

- [[Referential Transparency]]: the property purity guarantees, which lets an expression be replaced by its result
- [[Lazy Evaluation]]: an evaluation strategy that purity makes safe
- [[Higher-Order Function]]: functions treated as values, the other half of functional programming's toolkit
- [[Abstraction]]: functions as parameterized expressions, the basic tool for removing repetition
- [[Recursion]]: the functional replacement for loops
- [[Expression Problem]]: how organizing a program around functions differs from organizing it around objects
- [[Expressions and Statements]]: functional programs compute with expressions, imperative ones with statements
- [[Monad (Functional Programming)]]: how Haskell sequences input and output while staying pure
- [[Lambda Calculus]]: the formal model functional languages descend from

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

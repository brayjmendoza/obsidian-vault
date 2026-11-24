---
type: concept
created: 2026-11-11
updated: 2026-11-24
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-11
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Referential transparency** is the property of an expression that can be replaced by its result without changing the result of the expression around it.

A sub-expression that is referentially transparent works as an alias for its result: wherever it appears, its value could be written instead. Every pure expression (i.e., one with no side effects) is referentially transparent, since its value is the only thing it contributes. An expression with side effects isn't, because replacing it with its result would drop the effect.

In a purely functional language like Haskell, every expression is referentially transparent. That has three consequences:

- **Equational reasoning.** Programs can be reasoned about the way algebra is, by substituting equals for equals.
- **Evaluation can be delayed or shared.** When an expression is evaluated can't change its value, so evaluation can wait until the value is needed and reuse a result once computed (see [[Lazy Evaluation]]).
- **Evaluation order is free.** Independent expressions can be evaluated in any order, or in parallel.

# Examples

## Replacing an Expression

In Haskell, `3 * 4` can be swapped for its result anywhere:

```haskell
double x = x + x

double (3 * 4)  -- = double 12 = 12 + 12 = 24
```

## A Counter with a Side Effect

A function with a side effect breaks this. In Python, a counter that increments on every call isn't an alias for any one value:

```python
count = 0
def next_id():
    global count
    count = count + 1
    return count

next_id() + next_id()  # 1 + 2 = 3, 
2 * next_id()          # 2 * 3 = 6, replacing next_id() with its result is not
                       #            the same because count doesn't get updated
```

# Connections

- [[Functional Programming]]: pure functional programming makes every expression referentially transparent
- [[Lazy Evaluation]]: the evaluation strategy that referential transparency makes safe
- [[Name Binding]]: a bound name is an alias for its expression, which only works because that expression is transparent
- [[Substitution]]: replacing a name by its expression, the basis of evaluating by substitution
- [[Monad (Functional Programming)]]: `IO` actions describe effects, so evaluating expressions stays free of them
- [[Reference (Programming Languages)]]: aliasing, which makes changes hard to track, is harmless when nothing can change

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

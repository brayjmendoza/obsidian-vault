---
type: reference
created: 2026-11-15
updated: 2026-11-15
topic: haskell
---
Haskell's list syntax and the standard list functions. The ideas behind them are in [[Cons List]], [[Map (Higher-Order Function)]], and [[Filter (Higher-Order Function)]].

# Writing Lists

| Syntax | Means |
|---|---|
| `[4, 9, -13]` | A list. Every element must have the same type |
| `[]` | The empty list |
| `x : xs` | `x` in front of the list `xs` (e.g., `3 : [7, 15]` is `[3, 7, 15]`) |
| `xs ++ ys` | `xs` followed by `ys` (e.g., `[1, 3] ++ [7]` is `[1, 3, 7]`) |
| `[1 .. 10]` | The numbers from 1 to 10 |
| `[1 ..]` | Every number from 1 up, an infinite list. Use it with something like `take` |
| `"hello"` | The list `['h', 'e', 'l', 'l', 'o']`: a `String` is a list of `Char` |

- **`:` needs a list on its right.** `3 : 7` is an error. Write `3 : 7 : []` or `3 : [7]`.
- **`:` groups from the right.** `3 : 7 : []` means `3 : (7 : [])`.

# List Functions

| Function | Does | Example |
|---|---|---|
| `length` | Counts the elements | `length "Hello"` is `5` |
| `null` | Checks for the empty list | `null []` is `True` |
| `head` | Returns the first element. Fails on `[]` | `head [3, 7]` is `3` |
| `tail` | Returns everything after the first element. Fails on `[]` | `tail [3, 7]` is `[7]` |
| `take` | Returns the first `n` elements | `take 3 [5, 8, 9, 1]` is `[5, 8, 9]` |
| `drop` | Returns all but the first `n` elements | `drop 2 [5, 8, 9, 1]` is `[9, 1]` |
| `elem` | Checks whether an element is in the list | ``10 `elem` [5, 10, 15]`` is `True` |
| `map` | Applies a function to every element | `map (* 2) [19, 7]` is `[38, 14]` |
| `filter` | Keeps the elements a predicate accepts | `filter even [8, -13, 16]` is `[8, 16]` |
| `sum`, `product` | Adds or multiplies the elements | `sum [1, 2, 3]` is `6` |
| `minimum`, `maximum` | Returns the smallest or largest element | `maximum [3, 9, 4]` is `9` |

Before writing a list function, check whether one already exists: search [[Hoogle]] by the type you need (e.g., `[a] -> Int -> [a]`).

# Splitting Lists

| Function | Does | Example |
|---|---|---|
| `span` | Splits off the longest prefix whose elements pass a test, and returns it with the rest | `span isDigit "42+1"` is `("42", "+1")` |
| `takeWhile` | Returns that prefix | `takeWhile isDigit "42+1"` is `"42"` |
| `dropWhile` | Returns what's left after it | `dropWhile isDigit "42+1"` is `"+1"` |

# Pattern Matching on Lists

```haskell
myLength :: [a] -> Int
myLength []       = 0                  -- the empty list
myLength (_ : xs) = 1 + myLength xs    -- a head and a tail

first : rest = [13, 10, 20]            -- first is 13, rest is [10, 20]
```

Patterns on `:` need parentheses in function equations: `myLength (x : xs)`, not `myLength x : xs`.

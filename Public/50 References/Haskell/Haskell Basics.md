---
type: reference
created: 2026-11-11
updated: 2026-11-15
topic: haskell
---
Basic Haskell syntax: values and types, calling and defining functions, local bindings, and files. Input and output are in [[Haskell IO]]. The ideas behind it are in the concept notes linked in each section.

# Values and Types

| Values                     | Type             | Notes                                           |
| -------------------------- | ---------------- | ----------------------------------------------- |
| `1`, `-42`, `100000000000` | `Integer`        | Whole numbers of any size                       |
| `3.14`, `-2.718`           | `Double`         | Floating-point numbers                          |
| `True`, `False`            | `Bool`           |                                                 |
| `'a'`, `'z'`               | `Char`           | Single quotes                                   |
| `"hello"`                  | `String`         | Double quotes. A `String` is a list of `Char`   |
| `[1, 2, 3]`                | `[Integer]`      | A list: any length, every element the same type (see [[Haskell Lists]]) |
| `(True, 0.5)`              | `(Bool, Double)` | A tuple: fixed length, elements of any types (see [[Haskell Data Types]]) |

- **Case matters.** Type names start uppercase, and variable names start lowercase. Not every uppercase name is a type (e.g., `True`).
- **Operators:** arithmetic (e.g., `1 + 2`), comparison (e.g., `x == y` and `x /= y`, read "not equal"), logic (e.g., `a && b` and `a || b`), and `++` to join lists and strings (see [[Haskell Operators]]).

# Calling Functions

- **Spaces separate the function from its arguments:** `sqrt 4`, `min 0 42`, and `not True`. No parentheses or commas.
- **Parenthesize compound arguments.** Function application binds tightest, so `max 100 42 + 1` means `(max 100 42) + 1`. Write `max 100 (42 + 1)`.
- **Parenthesize negative numbers.** `max -42 42` and `2 * -1` are errors. Write `max (-42) 42` and `2 * (-1)`.
- **Division:** `/` divides floating-point numbers, `div` divides integers (e.g., `div 7 2` is `3`), and `mod` gives the remainder (e.g., `mod (10 + 7) 12` is `5`).
- **To a string:** `show 42` is `"42"`.

# Defining Functions

```haskell
average :: Double -> Double -> Double  -- type declaration: optional, but recommended
average x y = (x + y) / 2              -- name, parameters, then the body
```

- **The body is an expression.** A call's result is the body's value, with the arguments bound to the parameters (see [[Scope]]).
- **Conditionals:** `if n == 0 then 1 else n * fact (n - 1)`. The `else` is required.
- **Cases:** write one equation per case, tried top to bottom, and use `_` for an argument you don't use (see [[Pattern Matching]]).

```haskell
fact :: Integer -> Integer
fact 0 = 1
fact n = n * fact (n - 1)
```

- **Failing on purpose:** `error "bad substitution"` stops the program with a message, and `undefined` stops it without one (see [[Partial Function]]).

# Guards, As-Patterns, and Anonymous Functions

```haskell
classify c
  | isSpace c = "space"     -- guards: tried top to bottom
  | isDigit c = "digit"
  | otherwise = "other"     -- otherwise is just True

tokenize s@(c : rest) = …   -- s is the whole list, c its head, rest its tail

map (\x -> x * 2) [1, 2, 3]  -- an anonymous function: \params -> body
```

- **Guards** pick an equation's result by condition, after its patterns match.
- **An as-pattern** (`name@pattern`) names the whole value while also taking it apart.
- **A lambda** (`\x -> …`) is a function with no name, written where it's used.

# Characters

`import Data.Char` for tests on a `Char`: `isDigit`, `isLetter`, `isSpace`, `isUpper`, and `isLower` each return a `Bool`. Prefer `isDigit` to `isNumber` for parsing numbers: `isNumber` also accepts characters like `½` that `read` can't turn into a number.

# Local Bindings

```haskell
f x = let value = x * x
      in value + 1 / value

f x = value + 1 / value
  where value = x * x
```

- **`let … in …` is an expression.** Its bindings are visible in its body, after `in` (see [[Scope]]).
- **`where` goes at the end of a definition.** Its bindings are visible in the whole body.
- **Several bindings line up.** Each one starts in the same column, and the indentation is required.

# Files and Comments

- **Files end in `.hs`** and hold top-level bindings, not bare expressions. Load one into [[GHCi]] with `:load`.
- **Comments:** `--` to the end of the line, or `{- … -}` across lines.

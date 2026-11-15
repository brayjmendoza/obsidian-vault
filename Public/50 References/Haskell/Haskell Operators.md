---
type: reference
created: 2026-11-11
updated: 2026-11-15
topic: haskell
---
How Haskell's operators group, how operators and functions turn into each other, and how to declare your own. The idea behind the table is in [[Operator Precedence and Associativity]].

# Precedence and Associativity

Higher numbers bind tighter. Function application binds tighter than any operator. Operators are written in their function form (e.g., `(+)`), the way [[Hoogle]] lists them.

| Operators | Precedence | Associativity |
|---|---|---|
| Function application (e.g., `f x`) | Above all operators | Left |
| `(.)` | 9 | Right |
| `(^)`, `(^^)`, `(**)` | 8 | Right |
| `(*)`, `(/)`, `` `div` ``, `` `mod` `` | 7 | Left |
| `(+)`, `(-)` | 6 | Left |
| `(:)`, `(++)` | 5 | Right |
| `(==)`, `(/=)`, `(<)`, `(<=)`, `(>)`, `(>=)` | 4 | None: can't be chained |
| `(&&)` | 3 | Right |
| <code>(&#124;&#124;)</code> | 2 | Right |
| `(>>=)`, `(>>)` | 1 | Left |
| `($)` | 0 | Right |

The course slides list comparisons, `&&`, and `||` as left-associative. The table above has the Prelude's actual fixities. For `&&` and `||`, the result is the same either way.

# Operators as Functions

A binary operator is a function of two arguments. Wrap a symbol in parentheses to use it like one:

```haskell
(+) 1 2      -- 3
(&&) False True
:t (&&)      -- (&&) :: Bool -> Bool -> Bool
```

# Functions as Operators

Any two-argument function works as an operator in backticks, called **infix notation**:

```haskell
4 `div` 2    -- 2
17 `mod` 12  -- 5
```

# Sections

Put an operator in parentheses with one operand to make a one-argument function (see [[Point-Free Style]]):

| Section | Means |
|---|---|
| `(+ 1)` | `\x -> x + 1` |
| `(* 2)` | `\x -> x * 2` |
| `(^ 2)` | `\x -> x ^ 2` |
| `(2 ^)` | `\x -> 2 ^ x` |

`(- 1)` is negative one, not a section. Use `(subtract 1)` instead.

# Fixity Declarations

A fixity declaration sets an operator's associativity and precedence: `infixl` (left), `infixr` (right), or `infix` (none), then a level from 0 to 9, then the operator.

```haskell
infixl 7 `addMod60`  -- left-associative, same precedence as `mod`

addMod60 :: Integer -> Integer -> Integer
addMod60 x y = (x + y) `mod` 60
```

An operator without a declaration is `infixl 9`.

# Composition

`(g . f) x` is `g (f x)`: the right function runs first (see [[Function Composition]]).

```haskell
(increment . double) 1  -- 3
(double . increment) 1  -- 4
```

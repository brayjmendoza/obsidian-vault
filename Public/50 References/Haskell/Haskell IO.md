---
type: reference
created: 2026-11-15
updated: 2026-11-15
topic: haskell
---
Input and output in Haskell, and the `do` notation used to sequence it. The ideas behind them are in [[Monad (Functional Programming)]].

# Output and Input

| Function | Type | Does |
|---|---|---|
| `putStr` | `String -> IO ()` | Prints a string |
| `putStrLn` | `String -> IO ()` | Prints a string and a newline |
| `print` | `Show a => a -> IO ()` | Prints any `Show` value. The same as `putStrLn . show`, so strings print with quotes |
| `getLine` | `IO String` | Waits for a line of input and returns it |

- **`IO a` is an action** that does some input or output and produces an `a`.
- **`()` is the unit type,** with one value, also written `()`. `IO ()` means "does input or output, with no useful result."
- **`putStrLn` takes only a `String`.** `putStrLn 3` is a type error, so write `print 3` or `putStrLn (show 3)`.

# Do Notation

```haskell
main :: IO ()
main = do
  putStr "Enter a string: "
  input <- getLine                       -- run an action and name its result
  let reversed = reverse input           -- let for ordinary, non-IO values
  putStrLn ("Reversed: " ++ reversed)
```

- **`name <- action`** runs the action and binds its result. The right side has type `IO String`, and `name` has type `String`.
- **`let`** in a `do` block binds a plain value, with no `in`.
- **Every line lines up** in the same column.
- **`do` works in any monad,** not just `IO` (e.g., `Maybe` and parsers). `do x <- p1; p2` means `p1 >>= \x -> p2`.

# Running a Program

Name the top-level action `main`, then run the file with `runhaskell <file>.hs`, or compile it with `ghc <file>.hs` and run the result. In [[GHCi]], typing an action's name runs it.

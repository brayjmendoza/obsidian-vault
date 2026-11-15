---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Monad
  - Bind
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **monad** is a type of computation that can be chained: it has a way to wrap a plain value, and a **bind** operation that takes a computation's result and passes it to the next step.

The pattern shows up with `Maybe`. Functions that might fail (e.g., "keep this number only if it's odd") return a `Maybe`. Chaining two of them means checking the first result by hand each time: if it's `Nothing`, the whole thing is `Nothing`, and if it's `Just n`, pass `n` to the next function. That check repeats in every chain, so it can be refactored into a helper, `andThen`, that does the pattern matching once. Haskell already has that helper: the bind operator, `>>=`, from the [[Type Class|type class]] `Monad`. A type is a monad when it provides two operations:

```haskell
return :: Monad m => a -> m a                    -- wrap a value
(>>=)  :: Monad m => m a -> (a -> m b) -> m b    -- run, then pass the result on
```

Each monad decides what "pass the result on" means. Built-in monads include `Maybe` (stop at the first `Nothing`), lists, and `IO`. A parser is a monad too: bind runs one parser and, if it succeeds, hands its result and the remaining input to the next parser, so every sequencing combinator can be written with `>>=` and `return` (see [[Parser Combinator]]).

**`do` notation** is [[Syntactic Sugar|syntactic sugar]] for chains of `>>=`. `do var <- p1; p2` means `p1 >>= \var -> p2`: run `p1`, name its result `var`, then run `p2`. Code in `do` blocks looks imperative, a sequence of steps, but it's still expressions underneath.

`IO` is how Haskell does input and output despite being pure. A value of type `IO a` is an **action**: a description of some input or output that produces an `a` when run (e.g., `getLine :: IO String`, and `putStrLn :: String -> IO ()`, where `()` is the **unit** type, meaning no useful result). Actions are sequenced with `>>=` or `do`, and running the program runs its `main` action. Evaluating expressions stays free of side effects, which keeps [[Referential Transparency|referential transparency]].

More generally, monad instances should obey three **monad laws**, which Haskell can't check: `return` is an identity for bind on the left and on the right, and bind is associative. Monads can represent many kinds of effects, such as failure, non-determinism (lists), state, and I/O. In current Haskell, every `Monad` must also be a [[Functor (Functional Programming)|Functor]] and an `Applicative`, and `return` defaults to `Applicative`'s `pure`. The name comes from category theory. Similar ideas elsewhere include JavaScript's promise chaining with `then`, Rust's `?` operator on `Option` and `Result`, and Scala's `for` comprehensions.

# Example

Chaining functions that might fail, by hand and with bind:

```haskell
doubleMaybe :: Integer -> Maybe Integer
doubleMaybe n = Just (2 * n)

onlyOdd :: Integer -> Maybe Integer
onlyOdd n = if odd n then Just n else Nothing

-- by hand
doubleOnlyOdd n = case onlyOdd n of
  Nothing -> Nothing
  Just n' -> doubleMaybe n'

-- with bind, and with do notation
doubleOnlyOdd n = onlyOdd n >>= doubleMaybe

doubleOnlyOdd n = do
  n' <- onlyOdd n
  doubleMaybe n'

doubleOnlyOdd 3  -- Just 6
doubleOnlyOdd 4  -- Nothing
```

The same `do` notation in `IO`:

```haskell
main :: IO ()
main = do
  putStr "Enter a string: "
  input <- getLine
  let qualifier = if input == reverse input then " is " else " is not "
  putStrLn (input ++ qualifier ++ "a palindrome")
```

# Connections

- [[Functor (Functional Programming)]]: every monad is a functor, and adds sequencing
- [[Option Type]]: `Maybe` is the simplest monad, chaining computations that might fail
- [[Parser Combinator]]: a parser is a monad, and bind is the core sequencing combinator
- [[Syntactic Sugar]]: `do` notation is sugar for `>>=`
- [[Functional Programming]]: monads are how a pure language sequences effects like I/O
- [[Referential Transparency]]: `IO` actions keep evaluation free of side effects

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

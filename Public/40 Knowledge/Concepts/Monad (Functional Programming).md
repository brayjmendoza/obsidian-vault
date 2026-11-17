---
type: concept
created: 2026-11-15
updated: 2026-11-16
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

`IO` is how Haskell does input and output despite being pure. The key is that a value of type `IO a` is an **action**: a *description* of some input or output that would produce an `a`, not the input or output itself. `getLine :: IO String` isn't a string read from the keyboard. It's a recipe that says "read a line." `putStrLn "hi" :: IO ()` doesn't print anything when it's evaluated. It's a recipe that says "print hi" (`()`, the **unit** type, means the recipe produces no useful result). Evaluating an expression only ever builds recipes, so evaluation has no side effects. Only the program's `main` action is ever carried out, by the runtime, outside the world of evaluation.

That's what makes `IO` a monad with the same shape as `Maybe`. Bind combines two steps into one bigger value, and each monad decides what combining means:

| | `Maybe` | Parser | `IO` |
|---|---|---|---|
| A value of type `m a` | Maybe a result | A function from input to maybe a result and the rest of the input | A recipe that, when carried out, produces a result |
| `return x` | `Just x` | Succeed with `x` without consuming input | A recipe that does nothing and produces `x` |
| `m >>= f` | If `m` is `Just v`, continue with `f v`. If `Nothing`, stop | Run `m`, and if it succeeds, run `f` on its result with the rest of the input | A recipe: carry out `m`, pass its result to `f` to get the next recipe, and carry that out |

In each case, `f` decides the next step from the previous step's result, and bind handles the plumbing (i.e., failure, remaining input, or the order of effects). For `IO`, bind's result is still just a recipe: `getLine >>= putStrLn` is a value describing "read a line, then print it," built without reading or printing anything.

Because actions are values, [[Referential Transparency|referential transparency]] survives. A name bound to an action can be replaced by the action wherever it appears, and nothing changes: naming the recipe doesn't run it, so using the name twice runs it twice (see the example below).

More generally, monad instances should obey three **monad laws**, which Haskell can't check: `return` is an identity for bind on the left and on the right, and bind is associative. Monads can represent many kinds of effects, such as failure, non-determinism (lists), state, and I/O. In current Haskell, every `Monad` must also be a [[Functor (Functional Programming)|Functor]] and an `Applicative`, and `return` defaults to `Applicative`'s `pure`. The name comes from category theory. Similar ideas elsewhere include JavaScript's promise chaining with `then`, Rust's `?` operator on `Option` and `Result`, and Scala's `for` comprehensions. One way to picture `IO` is as a function from the state of the world to a result and a new state of the world, `World -> (a, World)`, which is a parser's shape with the world in place of the input string. GHC implements `IO` essentially this way, with a token standing for the world that it threads through every step, so the steps can't be reordered or skipped.

# Example

Chaining functions that might fail, by hand and with bind:

```haskell
doubleMaybe :: Integer -> Maybe Integer
doubleMaybe n = Just (2 * n)

onlyOdd :: Integer -> Maybe Integer
onlyOdd n = if odd n then Just n else Nothing

-- by hand
doubleOnlyOdd :: Integer -> Maybe Integer
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

An action named and used twice runs twice, since the name only stands for the recipe:

```haskell
greet :: IO ()
greet = putStrLn "hi"   -- defines the recipe, prints nothing

main :: IO ()
main = do
  greet                 -- prints "hi"
  greet                 -- prints "hi" again
```

Replacing each `greet` with `putStrLn "hi"` gives the same program, which is what referential transparency requires. For comparison, in Python, `greet = print("hi")` prints once, when the line runs, and `greet` holds `None`: the effect happened during evaluation, so the name can't stand in for it.

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

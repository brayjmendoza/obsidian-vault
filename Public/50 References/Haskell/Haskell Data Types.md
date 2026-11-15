---
type: reference
created: 2026-11-15
updated: 2026-11-15
topic: haskell
---
Syntax for declaring your own types in Haskell and taking their values apart. The ideas behind it are in [[Algebraic Data Type]], [[Type Class]], and [[Pattern Matching]].

# Declaring a Data Type

```haskell
data CoinFlip = Heads | Tails
  deriving (Show, Eq)

data ThermostatSetting
  = Off
  | CoolTo Int
  | HeatTo Int
  | OutOfService String
  deriving (Show, Eq)
```

- **Names start uppercase:** both the type (e.g., `ThermostatSetting`) and its constructors (e.g., `CoolTo`).
- **`|` separates the alternatives.** Put each one on its own line once there are several.
- **A constructor's fields follow its name:** `CoolTo Int` carries one `Int`. Build a value by applying it (e.g., `CoolTo 20`).
- **A type can refer to itself:** `data IntList = Empty | Cons Int IntList`.
- **A type can take a type parameter:** `data List a = Empty | Cons a (List a)`.

# Deriving

Without a `deriving` clause, a new type can't be printed in GHCi or compared. List the type classes it should join:

| Class | Lets you | Derived behavior |
|---|---|---|
| `Show` | `show x`, and see values in GHCi | Prints the constructor and its fields |
| `Eq` | `x == y`, `x /= y` | Equal when built from the same constructor with equal fields |
| `Ord` | `x < y`, `compare x y`, `maximum` | Constructors are ordered as declared. Needs `Eq` |
| `Read` | `read "Clubs" :: CardSuit` | Parses what `Show` prints. Annotate the type you want |

# Instances

Write a type class instance by hand when the derived one won't do (see [[Type Class]]):

```haskell
instance Show Op where
  show PlusOp  = "+"
  show MinusOp = "-"
  show TimesOp = "*"
  show DivOp   = "/"

instance Functor Tree where
  fmap _ Empty                 = Empty
  fmap f (Branch v left right) = Branch (f v) (fmap f left) (fmap f right)
```

- **Drop the class from `deriving`** when you write its instance, or the two clash.
- **Deriving `Functor`** needs a language extension, `{-# LANGUAGE DeriveFunctor #-}`, at the top of the file (see [[Functor (Functional Programming)]]).
- **A constraint goes before `=>`** in a type: `Num a => a -> a`, or several as a tuple, `(Functor f, Show a) => f a -> f String`.

# Case Expressions

```haskell
isRunning setting = case setting of
  Off -> False
  _   -> True
```

- **Every result has the same type,** and every pattern must match the type of the value being examined.
- **Cases are tried in order,** so a wildcard `_` goes last.
- **Missing a case fails at run time** with a non-exhaustive patterns error.

# Tuples

```haskell
prof = ("Ben Wiedermann", 131, True)   -- type (String, Integer, Bool)
(name, course, acted) = prof           -- binds all three
getCourse (_, course, _) = course
```

Tuples have a fixed size and may mix types, unlike lists.

# Maybe

`Maybe` marks a value that might be missing (see [[Option Type]]):

```haskell
data Maybe a = Nothing | Just a

safeHead :: [a] -> Maybe a
safeHead []      = Nothing
safeHead (x : _) = Just x

case safeHead xs of
  Just x  -> …   -- there was a value, x
  Nothing -> …   -- there wasn't
```

# Maps

`Data.Map` stores key-value pairs in a balanced tree, with $O(\log n)$ lookup and insert. Import it qualified, since its names clash with the Prelude's:

```haskell
import qualified Data.Map as Map

type Env = Map.Map String Exp

envLookup :: String -> Env -> Exp
envLookup v env = case Map.lookup v env of
  Just val -> val
  Nothing  -> error ("unbound identifier: " ++ v)

envInsert :: String -> Exp -> Env -> Env
envInsert = Map.insert   -- replaces any existing value for the key
```

- **`Map.lookup` returns a `Maybe`:** `Just` the value, or `Nothing` if the key is missing.
- **Inserting returns a new map.** The old one is unchanged, so a function call can extend an environment without affecting its caller's.
- **For a true hash map,** with constant-time operations on average, use `Data.HashMap.Strict` from the unordered-containers package.

# Type Aliases

`type` gives an existing type a new name, without creating a new type:

```haskell
type Card = (FaceValue, CardSuit)
```

---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Typeclass
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **type class** is a named family of types that all support a common set of operations, each type with its own implementation.

Values belong to types, much as members belong to a set, and types in turn belong to type classes. Membership in a class is what lets a type use the class's operations. A type joins a class by implementing at least the class's **minimal functions**, and the class supplies the rest from those. Some of Haskell's standard classes:

| Class | Purpose | Minimal functions |
|---|---|---|
| `Eq` | Equality | `(==)` |
| `Ord` | Comparison. Every `Ord` type must also be `Eq` | `(<=)` |
| `Show` | Converting to a `String` | `show` |
| `Read` | Converting from a `String` | `readsPrec` |
| `Num` | Integer operations | `(+)`, `(-)`, `(*)`, `abs`, `signum`, `fromInteger` |
| `Fractional` | Fractional operations | `(/)`, and everything in `Num` |

A type joins a class in one of two ways. A `deriving` clause on a [[Algebraic Data Type|data type]] generates the implementations (e.g., a derived `Ord` orders constructors as the declaration lists them). An `instance` declaration writes them by hand, which lets a type behave its own way (e.g., showing an expression tree in prefix notation instead of as constructors).

A **type constraint** limits a type variable to the members of a class. `(+) :: Num a => a -> a -> a` reads "with the requirement that `a` is a `Num`, `(+)` has type `a -> a -> a`." A function can have several constraints, written as a tuple (e.g., `(Functor f, Show a) => f a -> f String`). Constraints are how a function stays general while still using a class's operations. Since `read` turns a string into a value of some type, Haskell has to know which type: `read "4" + 2` works, because `+` needs a number, but `read "4"` alone doesn't say what to read it as.

Despite the name, a type class is not a class in the object-oriented sense. An object-oriented class describes objects that bundle data with behavior. A type class describes a set of types and the operations they share, which makes it more like an interface in Java.

More generally, type classes give a kind of polymorphism different from [[Parametric Polymorphism]]. A parametrically polymorphic function runs the same code for every type. An operation from a type class, like `(==)`, has a separate implementation for each member type, chosen by the type it's used at. This is **ad hoc polymorphism**, or overloading. Similar mechanisms in other languages include Rust's traits and Swift's protocols. A class can also describe type constructors rather than types (e.g., [[Functor (Functional Programming)|Functor]] and [[Monad (Functional Programming)|Monad]], whose members are types like `Maybe` and lists that take a type parameter).

# Example

Deriving the standard classes:

```haskell
data CardSuit = Clubs | Diamonds | Hearts | Spades
  deriving (Show, Eq, Ord, Read)

show Hearts              -- "Hearts", from Show
Clubs < Hearts           -- True, from Ord: Clubs is declared first
read "Clubs" :: CardSuit -- Clubs, from Read. Without the annotation, it's ambiguous
```

Writing a `Show` instance by hand, so Arith expressions print in prefix notation instead of as constructors:

```haskell
data Exp = Num Double | BinOp Exp Op Exp deriving (Eq)
data Op  = PlusOp | MinusOp | TimesOp | DivOp deriving (Eq)

instance Show Op where
  show PlusOp  = "+"
  show MinusOp = "-"
  show TimesOp = "*"
  show DivOp   = "/"

instance Show Exp where
  show (Num n)               = show n
  show (BinOp left op right) = show op ++ " " ++ show left ++ " " ++ show right

show (BinOp (Num 1) PlusOp (Num 2))  -- "+ 1.0 2.0"
```

# Connections

- [[Parametric Polymorphism]]: the other kind of polymorphism, where one definition works the same for every type
- [[Algebraic Data Type]]: new data types join type classes through `deriving`
- [[Type Inference]]: inferred types carry class constraints (e.g., `successor n = n + 1` gets the type `Num a => a -> a`)
- [[Functor (Functional Programming)]] and [[Monad (Functional Programming)]]: type classes for types that hold or produce values of another type

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

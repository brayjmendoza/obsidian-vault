---
type: concept
created: 2026-11-15
updated: 2026-11-21
aliases:
  - Data Type
  - Haskell Datatype
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
An **algebraic data type** is a type defined by listing its alternatives, where each alternative is a **constructor** that may carry values of other types.

In Haskell, a `data` declaration creates a new type and names its constructors. The simplest kind lists constructors that carry nothing, and each is a value of the new type:

```haskell
data CoinFlip = Heads | Tails
data Bool = True | False   -- how Haskell's own Bool is defined
```

Constructors can also carry **associated values**. Each such constructor is then a function from its fields to the type (e.g., `CoolTo :: Int -> ThermostatSetting`), and a constructor with no fields is a plain value. In general, a declaration has the shape of a grammar rule:

```
data <TypeName>
  = <Constructor> <Type> … <Type>
  | <Constructor> <Type> … <Type>
  …
```

Values are built by applying constructors and taken apart by [[Pattern Matching]], with one case per constructor. A type whose fields include the type itself is a [[Recursive Data Type]].

More generally, a type built this way is called algebraic because of how it combines other types. A choice between constructors is a **sum**: a value is one constructor *or* another. The values a constructor carries form a **product**: a value has one field *and* another. Counting values shows why: if `A` has 2 values and `B` has 3, a type that holds either an `A` or a `B` has $2 + 3$ values, and a pair of an `A` and a `B` has $2 \times 3$. A type whose constructors carry nothing is an **enumeration**, and a tuple (e.g., `(Bool, Double)`) is an anonymous product. Many other languages have the same idea under other names (e.g., Rust's `enum`, Swift's `enum` with associated values, and OCaml's variant types).

# Example

A thermostat setting is off, cooling to a temperature, heating to a temperature, or out of service with a message:

```haskell
data ThermostatSetting
  = Off
  | CoolTo Int
  | HeatTo Int
  | OutOfService String
  deriving (Show, Eq)

isRunning :: Int -> ThermostatSetting -> Bool
isRunning _ Off              = False
isRunning _ (OutOfService _) = False
isRunning temp (CoolTo t)    = temp > t
isRunning temp (HeatTo t)    = temp < t
```

`CoolTo 20` and `OutOfService "Under repair"` are both values of type `ThermostatSetting`. Each equation of `isRunning` matches one constructor and binds its associated value.

# Connections

- [[Pattern Matching]]: how a function takes an algebraic data type apart, one case per constructor
- [[Recursive Data Type]]: an algebraic data type that refers to itself
- [[Expression Problem]]: why defining a type by its alternatives organizes a program differently from classes
- [[Type Class]]: `deriving` adds a type to type classes like `Show` and `Eq`
- [[Concrete and Abstract Syntax]]: algebraic data types are how Haskell represents a language's programs as data
- [[Option Type]]: `Maybe`, a standard algebraic data type with two constructors
- [[Context-Free Grammar]]: a `data` declaration has the same shape as a grammar rule
- [[Curry-Howard Correspondence]]: products and sums correspond to logical "and" and "or"
- [[Church Encoding]]: the same data represented with functions alone

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

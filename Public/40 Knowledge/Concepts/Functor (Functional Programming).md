---
type: concept
created: 2026-11-15
updated: 2026-11-21
aliases:
  - Functor
  - fmap
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **functor** is a type of container, or context, that a function can be mapped over: applying a function to every value inside while keeping the structure the same.

Mapping isn't special to lists. Code that adds 1 to every element of a list, to the value inside a `Maybe` (if there is one), or to every node of a tree has the same shape each time: take the structure apart, apply the function to each value, and rebuild the structure. Each can be refactored into a helper that takes the function as a parameter (see [[Abstraction]]), and the helpers differ only in which structure they rebuild. Haskell names that pattern with a [[Type Class|type class]], `Functor`, whose one operation is `fmap`:

```haskell
fmap :: Functor f => (a -> b) -> f a -> f b
```

It reads "for any functor `f`, `fmap` turns a function from `a` to `b` into a function from `f a` to `f b`." Here `f` stands for a type constructor (e.g., `Maybe`, lists, or `Tree`), not a full type, so `f a` is "an `f` of `a`s." Lists and `Maybe` are built-in functors, and [[Higher-Order Function|`map`]] is just `fmap` specialized to lists. Any new parameterized data type can become a functor by defining `fmap` in an instance, or by deriving it with the `DeriveFunctor` language extension.

With functors, code that maps a function can be written once for every structure. A type constraint says the function works for any functor (e.g., `(Functor f, Show a) => f a -> f String`).

More generally, an `fmap` instance should obey two **functor laws**, which Haskell can't check: mapping the identity function changes nothing (`fmap id == id`), and mapping two functions one after the other is the same as mapping their composition (`fmap (g . f) == fmap g . fmap f`). The name comes from category theory, where a functor maps between categories. Other languages have the same idea under other names (e.g., `map` on Rust's `Option` and on Java's `Optional` and streams).

# Example

The same three functions, once for `Maybe` and once for trees, collapse to `fmap`:

```haskell
data Tree a = Empty | Branch a (Tree a) (Tree a)

instance Functor Tree where
  fmap _ Empty                 = Empty
  fmap f (Branch v left right) = Branch (f v) (fmap f left) (fmap f right)

incrementFunctor :: (Functor f, Num a) => f a -> f a
incrementFunctor = fmap (1 +)

showFunctor :: (Functor f, Show a) => f a -> f String
showFunctor = fmap show

incrementFunctor (Just 41)                    -- Just 42
incrementFunctor Nothing                      -- Nothing
incrementFunctor [1, 2, 3]                    -- [2, 3, 4]
showFunctor (Branch 1 Empty (Branch 2 Empty Empty))
  -- Branch "1" Empty (Branch "2" Empty Empty)
```

# Connections

- [[Higher-Order Function]]: map, the list case that functors generalize to any structure
- [[Type Class]]: `Functor` is a type class whose members are type constructors
- [[Parametric Polymorphism]]: a functor is a parameterized type, like `Maybe a` or `Tree a`
- [[Monad (Functional Programming)]]: a functor that can also sequence computations
- [[Abstraction]]: functors are what's left after abstracting the structure out of mapping functions

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

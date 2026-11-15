---
type: concept
created: 2026-11-15
updated: 2026-11-15
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **recursive data type** is a type whose definition refers to itself, so a value can contain smaller values of the same type.

Every useful recursive type has at least one alternative that doesn't refer to the type, a **base case**, so that values can be finite. A list is either empty, or an element followed by another list. A binary tree is either a leaf, or a node with two smaller trees. As [[Algebraic Data Type|algebraic data types]], these are declared like any other, with the type name appearing among a constructor's fields.

Functions over a recursive type follow its shape. Each constructor gets a case, and each recursive field gets a recursive call, so a function over lists has an empty case and a non-empty case, and a function over trees recurs on both subtrees. More generally, this pattern is called **structural recursion** (see [[Recursion]]), and it always terminates on finite values, since each call is on a smaller part.

# Example

A list of integers, built from scratch, and its length:

```haskell
data IntList = Empty | Cons Int IntList

intListLength :: IntList -> Int
intListLength Empty       = 0
intListLength (Cons _ xs) = 1 + intListLength xs
```

`Cons 10 (Cons 20 Empty)` is the list of 10 and 20, and its length is `1 + (1 + 0)`. Haskell's built-in lists have the same structure (see [[Cons List]]).

A binary tree of strings, with no empty trees:

```haskell
data StringBinaryTree
  = Leaf String
  | Node String StringBinaryTree StringBinaryTree

treeHeight :: StringBinaryTree -> Int
treeHeight (Leaf _)            = 0
treeHeight (Node _ left right) = 1 + max (treeHeight left) (treeHeight right)

tree7 = Node "i" (Leaf "c")
          (Node "h" (Node "g" (Leaf "a") (Leaf "b"))
                    (Node "f" (Leaf "d") (Leaf "e")))
```

```mermaid
flowchart TD
    i --> c
    i --> h
    h --> g
    h --> f
    g --> a
    g --> b
    f --> d
    f --> e
```

`treeHeight tree7` is `3`, the longest path from `i` down to a leaf.

# Connections

- [[Algebraic Data Type]]: recursive types are algebraic data types that mention themselves
- [[Recursion]]: functions over recursive types are recursive in the same places
- [[Cons List]]: the recursive type built into Haskell and most functional languages
- [[Map (Higher-Order Function)]]: mapping works over any recursive structure, not just lists (e.g., applying a function at every node of a tree)
- [[Concrete and Abstract Syntax]]: an abstract syntax tree is a recursive data type, with expressions inside expressions

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

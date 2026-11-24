---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Left-Recursive Grammar
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A grammar rule is **left-recursive** when a non-terminal's alternative starts with that same non-terminal (e.g., `Expr ::= Expr + Expr`).

Left recursion breaks a [[Recursive-Descent Parser|recursive-descent parser]]. The function for `Expr` tries the alternative `Expr + Expr`, and the first thing it does is call the function for `Expr`, on the same input, without consuming anything. That call does the same, so the parser recurs forever and diverges.

The fix is to rewrite the grammar so every alternative starts with something that consumes input, while describing the same language. For arithmetic, the left operand becomes a new non-terminal (e.g., `Factor`) for the pieces that can't contain a bare operator: numbers and parenthesized expressions. There's a general algorithm for removing left recursion from any grammar.

Rewriting changes how operators group. Replacing `Expr + Expr` with `Factor + Expr` makes the recursion go to the right, so `1 - 2 - 3` parses as `1 - (2 - 3)`: every operator becomes right-associative, which is wrong for subtraction and division. Getting left associativity back takes another rewrite, where a helper non-terminal handles a chain of operators that ends in $\varepsilon$ (see the [[#Restoring Precedence and Associativity|example]]).

More generally, left recursion is only a problem for top-down parsers. Bottom-up parsers (e.g., LR parsers, which many parser generators build) handle left-recursive rules directly, and even prefer them. Hand-written parsers often avoid the grammar rewrite by parsing a chain of operators with a loop, or a fold over a list, that builds the tree from the left.

# Examples

## A Left-Recursive Grammar

Left-recursive, so a recursive-descent parser diverges:

```
Expr ::= Expr + Expr | Expr - Expr | Expr * Expr | Expr / Expr | number | ( Expr )
```

## Removing Left Recursion

Left recursion removed, but every operator has the same precedence and groups to the right:

```
Expr   ::= Factor + Expr | Factor - Expr | Factor * Expr | Factor / Expr | Factor
Factor ::= number | ( Expr )
```

## Restoring Precedence and Associativity

Precedence and left associativity restored, using $\varepsilon$ to end each chain:

```
Expr      ::= Term PlusMinus
PlusMinus ::= + Term PlusMinus | - Term PlusMinus | ε
Term      ::= Factor TimesDiv
TimesDiv  ::= * Factor TimesDiv | / Factor TimesDiv | ε
Factor    ::= number | ( Expr )
```

# Connections

- [[Recursive-Descent Parser]]: the kind of parser left recursion breaks
- [[Context-Free Grammar]]: rewriting a grammar without changing the language it describes
- [[Operator Precedence and Associativity]]: what the rewrite has to preserve

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

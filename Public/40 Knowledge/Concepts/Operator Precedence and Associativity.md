---
type: concept
created: 2026-11-11
updated: 2026-11-24
aliases:
  - Precedence
  - Associativity
  - Fixity Declaration
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Precedence** and **associativity** are the rules that decide how an expression with several operators is grouped.

An **operator** (e.g., `+`) is applied to **operands** (e.g., `1` and `2` in `1 + 2`), and each use of it is an **application**. An expression with several applications can be **ambiguous**: it could be grouped more than one way, with different results. Two rules **disambiguate** it, picking one grouping:

- **Precedence** settles applications of different operators. An operator with higher precedence is applied first, so `1 + 2 * 3` means `1 + (2 * 3)`, since `*` has higher precedence than `+`.
- **Associativity** settles repeated applications of operators with the same precedence. A **left-associative** operator groups from the left, so `1 - 2 - 3` means `(1 - 2) - 3`. A **right-associative** operator groups from the right, so `2 ^ 3 ^ 2` means `2 ^ (3 ^ 2)`. A **non-associative** operator can't be chained without parentheses (e.g., `1 < 2 < 3` is an error in Haskell).

Function application counts as an operator too. In Haskell, it has the highest precedence of all and is left-associative, so `show 4 ++ show 2` means `(show 4) ++ (show 2)`, and `max 100 42 + 1` means `(max 100 42) + 1`. Haskell also lets a program set the precedence and associativity of its own operators, with a **fixity declaration** (see [[Haskell Operators]]).

A parser gets precedence and associativity from the shape of its grammar (see [[Context-Free Grammar]]). Each precedence level becomes its own non-terminal, with the lowest level at the top: `Expr` handles `+` and `-` and is built from `Term`s, which handle `*` and `/` and are built from `Factor`s. A tighter-binding operator sits deeper, so it ends up lower in the tree and is applied first. The direction of each rule's recursion sets associativity. A rule that recurs on the left (e.g., `Expr ::= Expr + Term`) groups to the left, and one that recurs on the right (e.g., `Expr ::= Term + Expr`) groups to the right. So a grammar can state left associativity directly, with a left-recursive rule. A recursive-descent parser can't follow left recursion, though, so a grammar written for one recurs on the right and gets left associativity a different way: with a rule that handles a chain of operators, building the tree from the left (see [[Left Recursion]]).

# Examples

## Three Groupings of One Expression

`5 - 1 - 2 * 2` has three plausible groupings:

| Grouping | Value | Correct? |
|---|---|---|
| `(5 - 1) - (2 * 2)` | `0` | Yes: `*` first by precedence, then `-` from the left |
| `((5 - 1) - 2) * 2` | `4` | No: applies `*` last |
| `(5 - (1 - 2)) * 2` | `12` | No: applies `*` last and groups `-` from the right |

# Connections

- [[Currying]]: function application is left-associative and the function-type arrow is right-associative, and the two fit together
- [[Concrete and Abstract Syntax]]: precedence is a rule of concrete syntax, and an abstract syntax tree makes it unnecessary
- [[Context-Free Grammar]]: a grammar encodes precedence in its levels of non-terminals
- [[Left Recursion]]: removing it from a grammar changes how operators associate

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

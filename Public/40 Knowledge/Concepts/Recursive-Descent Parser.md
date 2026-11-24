---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Recursive Descent
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **recursive-descent parser** is a parser with one function for each non-terminal of the grammar, where each function calls the others as the grammar's rules do.

The goal is parser code that looks like the grammar, which makes it easier to read and debug (see [[Context-Free Grammar]]). Each alternative of a rule becomes a branch of its function, a non-terminal in the rule becomes a call, and a terminal becomes a check that the next token matches. Since rules refer to each other, and often to themselves, the functions are mutually recursive.

A parsing function has to track **state**: how much of the input it has consumed. A function that only answers "valid or not" (e.g., of type `[Token] -> Bool`) fails, because each check is handed the same tokens and nothing is ever consumed. So a parsing function returns a pair: its result, and the tokens it didn't use, which the next function continues from. The whole parse succeeds when the start symbol's function succeeds and no tokens are left over. A function that builds the abstract syntax tree returns the tree it built in place of a Boolean.

The grammar has to suit the technique. Recursive descent can't follow a left-recursive rule (see [[Left Recursion]]), and since each function tries one alternative's structure, the grammar's shape decides how operators group (see [[Operator Precedence and Associativity]]).

More generally, recursive descent is **top-down** parsing: it starts from the start symbol and works toward the tokens. A **predictive** recursive-descent parser picks an alternative by looking at the next token, without backtracking, which works for the class of grammars called LL(1). Parser generators usually build **bottom-up** parsers instead (e.g., LR parsers), which handle left recursion directly.

# Examples

## A Grammar with Precedence

The grammar, with precedence built in:

```
Expr   ::= Term + Expr   | Term - Expr   | Term
Term   ::= Factor * Term | Factor / Term | Factor
Factor ::= number | ( Expr )
```

## Parsing a Factor

A parsing function for `Factor`, which consumes tokens and builds part of the AST:

```haskell
factor :: [Token] -> (Exp, [Token])
factor (NumberToken n : rest) = (Num n, rest)
factor (LParenToken : rest) =
  case expr rest of
    (e, RParenToken : rest') -> (e, rest')
    _                        -> error "expected )"
factor _ = error "expected a number or ("
```

`factor` handles a number token directly, and for `( Expr )` it calls `expr` on the tokens after the parenthesis, then checks that a closing parenthesis comes next.

# Connections

- [[Context-Free Grammar]]: each non-terminal becomes a function
- [[Parsing]]: recursive descent is the from-scratch way to write a parser
- [[Left Recursion]]: the grammar shape recursive descent can't handle
- [[Recursion]]: the parser's functions call each other as the grammar's rules do
- [[Parser Combinator]]: a library approach that keeps the grammar's shape and hides the state

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

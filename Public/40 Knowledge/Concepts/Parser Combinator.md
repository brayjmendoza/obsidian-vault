---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Parsing Library
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **parser combinator** is a higher-order function that takes parsers and returns a new parser, so that a whole parser can be built from small ones the way a grammar is built from rules.

A **parser** here is a function from input to a result and the remaining input. Small parsers recognize one thing (e.g., a digit, a letter, or a given symbol). Combinators build bigger ones:

| Combinator | Means | Grammar equivalent |
|---|---|---|
| Sequence (`p1 <&&> p2`) | Parse `p1`, then `p2` on what's left | `A B` |
| Alternative (<code>p1 &lt;&#124;&#124;&gt; p2</code>) | Try `p1`, and if it fails, try `p2` on the same input | <code>A &#124; B</code> |
| `many p` | Parse `p` zero or more times | `A*` |
| `some p` | Parse `p` one or more times | `A+` |
| `skipws p` | Skip any whitespace, then parse `p` | |

A combinator handles the state (i.e., how much input has been consumed), so code that uses one never threads the remaining input by hand. The result is a parser that looks like its grammar. Order matters in alternatives: since `many p` is defined as "one `p` then more, or else succeed without consuming anything," putting the always-succeeding parser first would make it stop immediately.

The parser's type evolves as the library grows:

1. `String -> Bool`: success or failure, but no state, so nothing is consumed.
2. `String -> (Bool, String)`: success and the remaining input.
3. `String -> (String, String)`: a result, but there's no obvious result for a failure.
4. `String -> Maybe (String, String)`: failure is `Nothing`, success is `Just` a result and the rest (see [[Option Type]]).
5. `Parser a = String -> Maybe (a, String)`: a result of any type, so a parser can return an `Exp` and build the AST (see [[Parametric Polymorphism]]).

Parser combinators are [[Abstraction|abstraction]] at work: they can be used without knowing how they work. That same abstraction is what makes them hard at first. Implementing a combinator feels like imperative programming, with sequential updates to the state, while using one feels like functional programming, trusting that it just works. Testing small pieces separately makes them easier to debug.

The sequencing combinators all share one shape: run the first parser, fail if it fails, and otherwise pass its result and the remaining input to "the next thing." Capturing that shape as one operator, **bind** (`>>=`), makes the parser a [[Monad (Functional Programming)|monad]]. Then every sequencing combinator is a short `do` block, and the whole library rests on a small basis: `parse` to run a parser, `get` for the next character, `return` to succeed without consuming input, `pfail` to fail, the alternative `<|>`, and `>>=`. Everything else (e.g., `<+>`, `many`, `skipws`, and `number`) is built from those, so only the basis touches the parser's state directly.

More generally, parser combinator libraries exist for many languages (e.g., Haskell's Parsec and Megaparsec, and Rust's nom). To use Haskell's own `>>=` and `do` notation, the parser has to be a `newtype` rather than a type synonym, with instances of `Functor`, `Applicative`, and `Monad`.

# Example

The arithmetic grammar, and the parser written with combinators:

```
Expr   ::= Factor + Expr | Factor - Expr | Factor * Expr | Factor / Expr | Factor
Factor ::= number | ( Expr )
```

```haskell
expr =  (factor <&&> sym '+' <&&> expr)
    <||> (factor <&&> sym '-' <&&> expr)
    <||> (factor <&&> sym '*' <&&> expr)
    <||> (factor <&&> sym '/' <&&> expr)
    <||> factor

factor =  number
      <||> (sym '(' <&&> expr <&&> sym ')')
```

Sequence and alternative, for parsers of type `String -> (Bool, String)`:

```haskell
(p1 <&&> p2) s = case p1 s of
  (True, s') -> p2 s'        -- continue from where p1 stopped
  (False, _) -> (False, s)   -- fail without consuming anything

(p1 <||> p2) s = case p1 s of
  (True, s') -> (True, s')
  (False, _) -> p2 s         -- try p2 on the original input

many p = (p <&&> many p) <||> psucceed
some p = p <&&> many p
```

With results, sequencing passes both results on, and two variants keep just one (e.g., to drop a parenthesis and keep the expression inside):

```haskell
(<+>)  :: Parser a -> Parser b -> Parser (a, b)   -- keep both results
(<-+>) :: Parser a -> Parser b -> Parser b        -- keep the second
(<+->) :: Parser a -> Parser b -> Parser a        -- keep the first
```

The same combinator, before and after bind:

```haskell
(<+>) :: Parser a -> Parser b -> Parser (a, b)

-- by hand: thread the state through each step
(p1 <+> p2) s = case p1 s of
  Nothing          -> Nothing
  Just (result1, s') -> case p2 s' of
    Nothing             -> Nothing
    Just (result2, s'') -> Just ((result1, result2), s'')

-- with bind, in do notation
p1 <+> p2 = do
  result1 <- p1
  result2 <- p2
  return (result1, result2)
```

# Connections

- [[Higher-Order Function]]: combinators take parsers, which are functions, and return parsers
- [[Recursive-Descent Parser]]: what a combinator parser is underneath, with the state handled for it
- [[Context-Free Grammar]]: the parser mirrors the grammar's sequences and alternatives
- [[Option Type]]: how a parser reports failure
- [[Parametric Polymorphism]]: `Parser a` works for results of any type
- [[Abstraction]]: combinators abstract the repeated state-handling of hand-written parsers
- [[Monad (Functional Programming)]]: a parser is a monad, so bind and `do` notation sequence parsers

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

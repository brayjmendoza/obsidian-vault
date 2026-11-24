---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Expression Substitution
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
**Substitution** replaces every occurrence of a variable in an expression with another expression, written $e[x \mapsto e']$: "$e$ with $x$ replaced by $e'$."

Substitution is how function application can be defined: applying a function means substituting the argument for the parameter in the body, then evaluating the result. Substitution itself does no evaluation. It only rewrites:

$$
\begin{aligned}
(x + 1)[x \mapsto 5] &= 5 + 1 \\
(z \cdot z + 7)[z \mapsto 2] &= 2 \cdot 2 + 7 \\
(x + y + z)[y \mapsto x / 3] &= x + (x / 3) + z
\end{aligned}
$$

It's defined by recursion on the expression, one case per kind of expression:

- **A number:** nothing to replace, so it stays the same (e.g., $10[x \mapsto 5] = 10$).
- **The variable being replaced:** becomes the new expression (e.g., $x[x \mapsto 5] = 5$).
- **A different variable:** stays the same (e.g., $x[y \mapsto 1 + 2] = x$).
- **A compound expression:** substitute in each part, and rebuild (e.g., $(x + 3/x)[x \mapsto 12] = 12 + 3/12$).
- **A function definition:** substitute in its body.

The last case hides two problems, which this version sets aside by assuming names never clash. If the function's own parameter has the same name as the variable being replaced (e.g., replacing $x$ inside a function of $x$), the inner $x$ refers to the parameter and shouldn't be replaced. And a function's body can mention a variable that isn't its parameter (e.g., $y$ in a function of $x$), which refers to something outside the function.

More generally, the inner function **binds** its parameter, so occurrences of that name inside it are **bound**, and substitution must stop there. The second danger is **variable capture**: substituting an expression that mentions a variable $y$ into a function whose parameter is also $y$ changes what $y$ refers to. **Capture-avoiding substitution** fixes this by renaming the parameter first. Both problems lead to [[Scope]] and to evaluation with [[Environment (Programming Languages)|environments]], which avoid substitution altogether.

# Examples

## Substitution in Haskell

An implementation in Haskell, where `substitute e' (Var v) e` computes $e[v \mapsto e']$:

```haskell
substitute :: Exp -> Exp -> Exp -> Exp
substitute _  (Var v) (Num n)               = Num n
substitute e' (Var v) (Var w)               = if v == w then e' else Var w
substitute e' var     (BinOp left op right) =
  BinOp (substitute e' var left) op (substitute e' var right)
substitute e' var     (FuncDef v body)      = FuncDef v (substitute e' var body)
substitute _  _       _                     = error "bad substitution"
```

## Applying Plus One

Applying the "plus one" function to 5:

| Step | Expression |
|---|---|
| Start | `Apply (FuncDef "x" (BinOp (Var "x") PlusOp (Num 1))) (Num 5)` |
| Substitute `Num 5` for `x` in the body | `BinOp (Num 5) PlusOp (Num 1)` |
| Evaluate | `Num 6` |

# Connections

- [[Interpreter]]: uses substitution to apply functions
- [[Evaluation Strategy]]: whether the argument is evaluated before it's substituted
- [[Scope]]: which binding a variable refers to, which substitution has to respect
- [[Referential Transparency]]: replacing a name by its expression is only safe without side effects
- [[Environment (Programming Languages)]]: an alternative that records bindings instead of rewriting the body
- [[Beta Reduction]]: substitution as the lambda calculus's rule of computation
- [[Free and Bound Variables]]: the distinction substitution has to respect

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

---
type: reference
created: 2026-11-16
updated: 2026-11-24
topic: programming-languages
---
**Arith** is the small language that [[Programming Languages (HMC CS131)]] implements in Haskell, one feature at a time. It starts as arithmetic on numbers and grows variables, functions, and local bindings. Concept notes use it as their running example, and this note holds the whole language in one place.

An Arith program goes through three stages, each written in Haskell:

1. **Tokenize:** text like `"1 + 2 * 3"` becomes a list of tokens (see [[Lexical Analysis]]).
2. **Parse:** the tokens become an abstract syntax tree, a value of type `Exp` (see [[Parsing]] and [[Concrete and Abstract Syntax]]).
3. **Evaluate:** `eval` computes the tree's value (see [[Interpreter]]).

# How the Language Grows

Each feature adds constructors to `Exp` and cases to `eval`:

| Stage | Adds to `Exp` | What changes in `eval` | Explained in |
|---|---|---|---|
| Arithmetic | `Num`, `BinOp` | Returns a `Double` | [[Interpreter]] |
| Variables | `Var` | Looks a variable up in a list of pairs | [[Interpreter]] |
| Functions | `FuncDef`, `Apply` | Returns an `Exp`, since a function is a value but not a number. Applying a function substitutes the argument into the body | [[Substitution]], [[Evaluation Strategy]], [[Currying]] |
| Local bindings | `Let` | Rewrites `Let` into a function application | [[Syntactic Sugar]] |
| Environments | (nothing) | Takes an environment of variable values instead of substituting | [[Environment (Programming Languages)]] |
| Closures | `Closure` | A function's value saves the environment it was defined in | [[Closure (Programming Languages)]] |

# Abstract Syntax

The first version has only numbers and binary operations:

```haskell
data Op  = PlusOp | MinusOp | TimesOp | DivOp
  deriving (Show, Eq)

data Exp = Num Double | BinOp Exp Op Exp
  deriving (Show, Eq)

eval :: Exp -> Double
eval (Num x)                    = x
eval (BinOp left PlusOp right)  = eval left + eval right
eval (BinOp left MinusOp right) = eval left - eval right
eval (BinOp left TimesOp right) = eval left * eval right
eval (BinOp left DivOp right)   = eval left / eval right

eval (BinOp (Num 1) PlusOp (BinOp (Num 2) TimesOp (Num 3)))   -- 7.0, the value of 1 + 2 * 3
```

# The Full Interpreter

The last version, with every feature, environments, and closures:

```haskell
type VarName = String
type Env = [(VarName, Exp)]   -- each variable paired with its value

data Exp
  = Num Double
  | BinOp Exp Op Exp
  | Var VarName
  | FuncDef VarName Exp       -- parameter, body
  | Apply Exp Exp             -- function, argument
  | Let VarName Exp Exp       -- variable, bound expression, body
  | Closure Env VarName Exp   -- saved environment, parameter, body
  deriving (Show, Eq)

eval :: Env -> Exp -> Exp
eval _   (Num x)               = Num x
eval env (BinOp left op right) = evalOp (eval env left) op (eval env right)
eval env (Var v)               = envLookup v env
eval env (FuncDef v body)      = Closure env v body
eval env (Apply fexp arg)      =
  let Closure closureEnv v body = eval env fexp
      argval                    = eval env arg
  in eval (envInsert v argval closureEnv) body
eval env (Let v e body)        = eval env (Apply (FuncDef v body) e)
eval _   c@(Closure _ _ _)     = c

evalOp :: Exp -> Op -> Exp -> Exp
evalOp (Num x) PlusOp  (Num y) = Num (x + y)
evalOp (Num x) MinusOp (Num y) = Num (x - y)
evalOp (Num x) TimesOp (Num y) = Num (x * y)
evalOp (Num x) DivOp   (Num y) = Num (x / y)
evalOp _       _       _       = error "arithmetic on a non-number"
```

`envLookup` and `envInsert` are in [[Environment (Programming Languages)#The Environment as a List|Environment]].

Running a program that binds a function to a name and calls it:

```haskell
-- let double = (fun x -> x * 2) in double 21
eval [] (Let "double" (FuncDef "x" (BinOp (Var "x") TimesOp (Num 2)))
          (Apply (Var "double") (Num 21)))
-- Num 42.0
```

# Front End

- **Tokens:** `Token` and `tokenize` are in [[Lexical Analysis#A Tokenizer for Arith|Lexical Analysis]].
- **Grammar:** the grammar for arithmetic expressions is in [[Context-Free Grammar#A Grammar for Arithmetic|Context-Free Grammar]], and a version with precedence built in is in [[Recursive-Descent Parser#A Grammar with Precedence|Recursive-Descent Parser]].
- **Parsers:** a hand-written parser is in [[Recursive-Descent Parser]], and one built from combinators is in [[Parser Combinator]].
- **Printing:** a `Show` instance that prints `Exp` in prefix notation is in [[Type Class#A Show Instance for Arith|Type Class]].

# Related

- [[Lambda Calculus]]: Arith's `FuncDef` and `Apply` are lambda abstraction and application

---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Evaluator
  - eval
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
An **interpreter** is a program that takes another program, represented as abstract syntax, and computes its value directly.

An interpreter's core is an **evaluation function**, `eval`, that traverses the abstract syntax tree (see [[Concrete and Abstract Syntax]]). For example, with the grammar for expressions (see [[Context-Free Grammar#A Grammar for Arithmetic|Context-Free Grammar]]), the `eval` function would have one case per kind of expression, matched with [[Pattern Matching|pattern matching]]: a number evaluates to itself, and an operation evaluates its operands recursively and then combines the results. Writing `eval` defines a language's [[Syntax and Semantics|semantics]]: the function says what every expression means. [[Arith]], a small language of arithmetic expressions, is built this way, with both its abstract syntax and its semantics written in Haskell.

When developing the Arith language, we implement one feature at a time. Each feature requires a new constructor and a new case in `eval`:

1. **Arithmetic:** numbers and binary operators. `eval` returns a `Double`.
2. **Variables:** a `Symbol` constructor, and a dictionary of pairs from symbols to expressions. Evaluating a symbol looks it up and evaluates what it's bound to.
3. **Functions:** `FuncDef` holds a parameter name and a body, and `Apply` holds a function and an argument. Functions have no names, and they're values: evaluating a `FuncDef` returns it unchanged. Applying one substitutes the argument for the parameter in the body and evaluates the result (see [[Substitution]]).
4. **Local bindings:** `Let` holds a variable, an expression, and a body, and its meaning is defined by applying a function (see [[Syntactic Sugar]]).
5. **Environments:** instead of substituting, `eval` takes a map from variables to values and looks variables up as it reaches them (see [[Environment (Programming Languages)]]).
6. **Closures:** evaluating a function saves the environment it was defined in, which gives static scope and lets curried functions keep their earlier arguments (see [[Closure (Programming Languages)]]).

Adding functions changes `eval`'s result type from `Double` to `Exp`, so that evaluation stays in the world of expressions. A function is a value, but it isn't a number, so the result has to be able to hold one. A function of two arguments is a function whose body is another function, applied one argument at a time (see [[Currying]]). So `eval` on an `Apply` first evaluates the function part, which may itself be an `Apply`, until it reaches a `FuncDef`.

More generally, an interpreter written in one language for another is a **definitional interpreter**. The language being implemented (here, Arith) is the **object language**, and the language the interpreter is written in (here, Haskell) is the **metalanguage**. The other main way to implement a language is a **compiler**, which translates a program into another language (e.g., machine code) to run later, instead of computing its value itself.

# Examples

## Arith with Functions

Arith with functions (with `Eq` derived, which the comparison `v == w` in substitution needs):

```haskell
data Op = PlusOp | MinusOp | TimesOp | DivOp
  deriving (Show, Eq)

type VarName = String

data Exp
  = Var VarName
  | Num Double
  | BinOp Exp Op Exp
  | FuncDef VarName Exp   -- parameter, body
  | Apply Exp Exp         -- function, argument
  deriving (Show, Eq)

eval :: Exp -> Exp
eval (Num x)               = Num x
eval (BinOp left op right) = evalOp (eval left) op (eval right)
eval (FuncDef v body)      = FuncDef v body          -- functions are values
eval (Apply fexp arg)      =
  let FuncDef v body = eval fexp                   -- fexp may itself be an Apply
  in eval (substitute arg (Var v) body)

evalOp :: Exp -> Op -> Exp -> Exp
evalOp (Num x) PlusOp  (Num y) = Num (x + y)
evalOp (Num x) MinusOp (Num y) = Num (x - y)
evalOp (Num x) TimesOp (Num y) = Num (x * y)
evalOp (Num x) DivOp   (Num y) = Num (x / y)
```

## A Two-Argument Function

Adding with a two-argument function:

```haskell
eval (Apply (Apply (FuncDef "x" (FuncDef "y" (BinOp (Var "x") PlusOp (Var "y")))) (Num 10)) (Num 100))
-- the inner Apply gives FuncDef "y" (BinOp (Num 10) PlusOp (Var "y"))
-- applying that to Num 100 gives BinOp (Num 10) PlusOp (Num 100), which evaluates to Num 110
```

# Connections

- [[Concrete and Abstract Syntax]]: an interpreter takes code as data, working on the tree rather than the text
- [[Syntax and Semantics]]: the evaluation function defines the semantics
- [[Substitution]]: how this interpreter applies a function
- [[Evaluation Strategy]]: whether the argument is evaluated before it's substituted
- [[Currying]]: multi-argument functions as nested one-argument functions
- [[Syntactic Sugar]]: new syntax given meaning by rewriting it into existing syntax
- [[Environment (Programming Languages)]] and [[Closure (Programming Languages)]]: how the evaluator replaces substitution, and keeps static scope while doing it
- [[Parsing]]: the front end that produces the abstract syntax an interpreter evaluates
- [[Separate Compilation]]: the alternative to interpreting, which translates a program into an executable first

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

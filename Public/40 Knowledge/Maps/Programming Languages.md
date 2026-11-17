---
type: map
created: 2026-11-11
updated: 2026-11-16
field: computer-science
---
↑ [[Computer Science]]

+ [ ] Go over all of the PL's notes and give feedback to Claude🔺 
+ [ ] Start `quiz-me` skill by having Claude quiz you on all these concepts and determine `confidence`
# Functions

1. [[Pattern Matching]] — defining a function by cases, taking values apart by their shape
2. [[Recursion]] — functions that call themselves on smaller inputs, in place of loops
3. [[Partial Function]] — functions with no result for some inputs, like the head of an empty list
4. [[Currying]] — every function takes one argument, so a multi-argument function returns a function
5. [[Higher-Order Function]] — functions that take or return functions, like map and filter on lists
6. [[Function Composition]] — chaining two functions into one
7. [[Point-Free Style]] — defining functions by composition and partial application, without naming arguments

# Functional Programming

1. [[Functional Programming]] — computing by evaluating expressions instead of updating state
2. [[Abstraction]] — turning repeated code into a parameterized expression, the move every later idea builds on
3. [[Referential Transparency]] — what purity guarantees: an expression can be replaced by its result
4. [[Lazy Evaluation]] — evaluating only what's needed, made safe by referential transparency

# Names and Scope

1. [[Name Binding]] — names bound to expressions once, instead of assigned and reassigned
2. [[Scope]] — where a binding is visible, and how nested scopes resolve a name
3. [[Static and Dynamic Scope]] — whether a function's free variables use the bindings at its definition or at its call

# Types

1. [[Type (Programming Languages)]] — how data is interpreted, and what can be done with it
2. [[Type System]] — the rules for how types combine, and what counts as a type error
3. [[Static and Dynamic Typing]] — whether type errors are caught before a program runs or while it runs
4. [[Typing Rule]] — a type system written as inference rules, with a type environment
5. [[Curry-Howard Correspondence]] — typing rules as logic: programs are proofs, and types are propositions
6. [[Type Inference]] — static type checking without writing every type
7. [[Parametric Polymorphism]] — one definition for every type, written with type variables
8. [[Type Class]] — families of types that share operations, each with its own implementation
9. [[Option Type]] — a value or no value, so a missing result is part of the type
10. [[Subtyping]] — using a value of one type where another is expected
11. [[Covariance and Contravariance (Type Systems)]] — how subtyping carries over to pairs, lists, and functions
12. [[Top and Bottom Types]] — the types above and below every other, and the lattice between them

# Data Types

1. [[Algebraic Data Type]] — defining a type by its alternatives, each a constructor that may carry values
2. [[Recursive Data Type]] — a type that contains smaller values of itself, like lists and trees
3. [[Expression Problem]] — organizing code by data or by operation, and what each makes easy to change

# Syntax and Semantics

1. [[Syntax and Semantics]] — what a programmer may write, and what it means
2. [[Expressions and Statements]] — computations that produce values, and ones performed for their effects
3. [[Concrete and Abstract Syntax]] — the text a programmer writes, and the tree it stands for
4. [[Operator Precedence and Associativity]] — how concrete syntax groups an expression with several operators, function application included

# Functional Abstractions

1. [[Functor (Functional Programming)]] — structures a function can be mapped over, generalizing map
2. [[Monad (Functional Programming)]] — computations chained with bind, for failure, parsing, and input and output

# Parsing

1. [[Parsing]] — turning program text into an abstract syntax tree, or reporting a syntax error
2. [[Lexical Analysis]] — splitting text into tokens before parsing
3. [[Context-Free Grammar]] — the rules that specify which programs are valid
4. [[Recursive-Descent Parser]] — one function per grammar rule, consuming tokens as it goes
5. [[Left Recursion]] — a grammar shape recursive descent can't follow, and rewriting it away
6. [[Parser Combinator]] — building parsers from smaller parsers with higher-order functions

# Interpreters

1. [[Interpreter]] — evaluating abstract syntax directly, which defines a language's semantics
2. [[Substitution]] — replacing a variable with an expression, the way function application is first defined
3. [[Evaluation Strategy]] — whether an argument is evaluated before or after it's passed in
4. [[Syntactic Sugar]] — new syntax whose meaning is defined by rewriting it into existing syntax, like `let`
5. [[Environment (Programming Languages)]] — remembering bindings instead of substituting them
6. [[Closure (Programming Languages)]] — a function packaged with the environment it was defined in


# Lambda Calculus

1. [[Lambda Calculus]] — computation with nothing but anonymous functions, and where every later language sits on the ladder of abstraction
2. [[Free and Bound Variables]] — which function definition, if any, each variable refers to
3. [[Beta Reduction]] — applying a function by substitution, and normal forms
4. [[Church Encoding]] — Booleans, pairs, lists, numbers, and sets as functions
5. [[Russell's Paradox]] — the set of sets that don't contain themselves, as a lambda expression with no normal form
6. [[Fixed-Point Combinator]] — recursion without names, by finding a function's fixed point


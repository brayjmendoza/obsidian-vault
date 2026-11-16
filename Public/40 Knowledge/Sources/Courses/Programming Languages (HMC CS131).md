---
type: course
created: 2026-11-11
updated: 2026-11-15
authors:
  - Ben Wiedermann
year: 2024
fields:
  - computer-science
status: read
---
# Summary

Harvey Mudd College's CS 131, Programming Languages, studies how programming languages are designed and implemented. It uses Haskell both as a language to learn and as the language for implementing others. Its modules cover Haskell and functional programming, interpreters, parsing, functional abstractions, type systems, and lambda calculus. The course has no textbook: its material is the lecture slides and the instructors' summary of each lecture.

The course's running theme is [[Abstraction]]. It starts with functions as parameterized expressions and builds up to functions that take and return other functions. Its Haskell syntax is collected in [[GHCi]], [[Haskell Basics]], and [[Haskell Operators]].

# Key Ideas

## Module 2: Haskell and Functional Programming

- [[Functional Programming]] computes by evaluating expressions, not by updating state, and Haskell is purely functional: evaluation is the only way computation proceeds.
- [[Abstraction]] turns repeated code into a parameterized expression, and a function is its simplest form.
- A [[Name Binding|binding]] associates a name with an expression, at most once per [[Scope]], so every Haskell variable is a constant.
- [[Pattern Matching]] defines a function by cases, tried from top to bottom.
- Haskell is statically typed (see [[Static and Dynamic Typing]]) and uses [[Type Inference]], so type annotations are optional but recommended.
- [[Referential Transparency]] lets an expression be replaced by its result, which makes [[Lazy Evaluation]] safe.
- [[Operator Precedence and Associativity]] decide how an expression is grouped. In Haskell, operators and two-argument functions are interchangeable, and function application binds tightest.
- Every Haskell function takes one argument (see [[Currying]]), so every multi-argument function is a [[Higher-Order Function|higher-order function]].
- [[Function Composition]] and [[Point-Free Style]] build functions out of other functions.

## Module 3: Haskell Data Types

- A data type (in general, an [[Algebraic Data Type|algebraic data type]]) is defined by its alternatives. Each constructor may carry associated values and is itself a function to the type.
- A [[Recursive Data Type]] refers to itself, like lists and binary trees, and functions over it recur wherever the type does (see [[Recursion]]).
- A list is empty, or an element consed onto another list, the standard example of a [[Recursive Data Type|recursive data type]].
- [[Pattern Matching]] takes data apart by its shape, in function equations, `case` expressions, and bindings. A match that misses a case fails at run time (in general, it makes a [[Partial Function|partial function]]).
- Type variables and parameterized types let one definition work for every type (in general, [[Parametric Polymorphism|parametric polymorphism]]), and [[Type Class|type classes]] group types that share operations like `(==)` and `show`.
- Recurring patterns in list functions abstract into [[Map (Higher-Order Function)|map]] and [[Filter (Higher-Order Function)|filter]].
- Data types are not classes: functional code groups behavior by operation, and object-oriented code groups it by data (in general, the tradeoff between them is the [[Expression Problem|expression problem]]).

## Module 4: Interpreting Programs

- Code is data: programs can take other programs as input (see [[Code as Data]]).
- An expression computes a value, and a statement is performed for its effect (see [[Expressions and Statements]]).
- [[Syntax and Semantics|Syntax]] is what the programmer writes, and semantics is what it means.
- Concrete syntax is the text, and abstract syntax is the tree it stands for, with parsing and pretty printing between them (see [[Concrete and Abstract Syntax]]). Precedence and parentheses belong to concrete syntax.
- An `eval` function over abstract syntax defines the semantics of Arith, a language of arithmetic expressions, which grows variables and then functions (in general, an [[Interpreter|interpreter]]).
- Applying a function substitutes the argument for the parameter in the body, written $e[x \mapsto e']$ (see [[Substitution]]).
- Evaluating the argument before substituting it is call by value, and substituting it unevaluated is call by name (in general, an [[Evaluation Strategy|evaluation strategy]]).

## Module 5: Environments, Closures, and Scope

- A `let` expression is function application in disguise, so Arith adds `Let` as new abstract syntax with its semantics defined by existing semantics (in general, [[Syntactic Sugar|syntactic sugar]]).
- Substitution costs $O(N^2)$ work for a function of $N$ parameters, so the evaluator saves an environment of variables and values instead (see [[Environment (Programming Languages)]]). With constant-time lookups, evaluation is $O(N)$.
- Evaluating a function's body in the caller's environment gives dynamic scope, while static scope uses the bindings where the function was defined (see [[Static and Dynamic Scope]]).
- Evaluating a function definition must save its environment in a closure (see [[Closure (Programming Languages)]]). Without one, curried functions lose their earlier arguments.

## Module 6: Parsing

- A parser checks concrete syntax for errors and builds the AST (see [[Parsing]]). It can be written by hand, with a library, by a parser generator, or by a parser synthesizer.
- Tokenizing splits text into tokens such as reserved words, literals, and operators (in general, [[Lexical Analysis|lexical analysis]]).
- A grammar specifies valid programs with production rules, terminals, and non-terminals (in general, a [[Context-Free Grammar|context-free grammar]]).
- A recursive-descent parser has one function per non-terminal, and each returns its result with the unconsumed input (see [[Recursive-Descent Parser]]).
- Left recursion makes a recursive-descent parser diverge, and removing it takes care to keep [[Operator Precedence and Associativity|precedence and left associativity]] (see [[Left Recursion]]).
- Parser combinators like `<&&>`, `<||>`, and `many` build a parser that looks like its grammar (see [[Parser Combinator]]). With `Parser a = String -> Maybe (a, String)`, parsers can build ASTs.
- Parameterized data types like `Tree a` abstract over a type (see [[Parametric Polymorphism]]), and `Maybe` marks a value that might be missing (in general, an [[Option Type|option type]]).

## Module 7: Functional Abstractions

- Typeclasses can be implemented by hand with `instance`, and a type constraint like `Num a =>` limits a type variable to a typeclass's members (see [[Type Class]]).
- Mapping over lists, `Maybe`, and trees follows one pattern, which the `Functor` typeclass captures as `fmap` (in general, a [[Functor (Functional Programming)|functor]]).
- Chaining functions that return `Maybe` repeats the same pattern matching, which the bind operator `>>=` of the `Monad` typeclass captures (in general, a [[Monad (Functional Programming)|monad]]).
- `do` notation is syntactic sugar for `>>=`, and `IO` is a monad, which is how Haskell performs input and output.
- Every sequencing parser combinator passes a successful result to "the next thing," so bind becomes the core of a smaller parser library (see [[Parser Combinator]]).

## Module 8: Type Systems

- The same bits mean different things depending on their type, and a type is an abstraction, a set of values and operations, and a representation (see [[Type (Programming Languages)]]).
- A type system is a system of rules that governs types, and a well-typed program has no type conflicts (see [[Type System]]).
- Typing rules are written like natural deduction, with a type environment $\Gamma$ in judgments like $\Gamma \vdash e :: t$, and showing a program is well-typed means writing a proof (see [[Typing Rule]]).
- A proof is a program, and the formula it proves is the program's type (in general, the [[Curry-Howard Correspondence|Curry–Howard correspondence]]).
- A subtype can be substituted wherever its supertype is expected (see [[Subtyping]]). Pairs and lists keep the order of subtyping, but a function's argument reverses it (in general, [[Covariance and Contravariance (Type Systems)|covariance and contravariance]]).
- Any is a supertype of every type and None a subtype of every type, and a type lattice draws the relationships between (in general, [[Top and Bottom Types|top and bottom types]]).

## Module 9: Lambda Calculus

- Church's lambda calculus and Turing's machines both answered Hilbert's question of whether everything can be computed: no. The lambda calculus sits at the top of a ladder of abstraction, above even pure functional languages (see [[Lambda Calculus]]).
- Lambda calculus has three kinds of expression: variables, applications, and lambda abstractions. Variables are bound or free, and expressions are closed or open (see [[Free and Bound Variables]]).
- β-reduction applies a function by substitution, an expression that can't be reduced further is in normal form, and some expressions have none (see [[Beta Reduction]]). α-equivalent expressions differ only in the names of bound variables.
- Booleans, logic, pairs, lists, numbers, and sets can all be encoded as functions (in general, [[Church Encoding|Church encodings]]).
- Encoding sets as functions turns Russell's paradox into an expression with no normal form (see [[Russell's Paradox]]).
- The Y combinator repeats a function forever, which gives anonymous functions recursion by finding a fixed point (in general, a [[Fixed-Point Combinator|fixed-point combinator]]).

# Open Questions


## Quotes

> "Abstraction is the essence of CS 131." (Functional Programming, slide 15)

> "All Haskell functions take only one argument!" (Functions = Values, slide 27)

> "Where there is a pattern, there is an opportunity to perform abstraction." (Lists, slide 14)

> "This is not a Haskell class. Haskell is the vehicle!" (Lambda Calculus, slide 21)

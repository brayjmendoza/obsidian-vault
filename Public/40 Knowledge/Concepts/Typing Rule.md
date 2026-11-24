---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Typing Judgment
  - Type Environment
  - Type Derivation
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A **typing rule** is an inference rule stating when an expression has a given type: if the premises above the line hold, the conclusion below it does.

Typing rules are written in the style of natural deduction from logic. Each rule has zero or more **premises** above a line and one **conclusion** below it. A rule with no premises is a base case (e.g., any number literal $n$ has type `int`). Showing that a program is well-typed means building a **derivation**: a tree of rules whose conclusion is the program's type, with every premise proved by another rule. Writing one is writing a proof.

A rule for a variable needs to know the variable's type, so rules carry a **type environment**, written $\Gamma$, which maps variables to types the way an evaluator's [[Environment (Programming Languages)|environment]] maps them to values. A **typing judgment** $\Gamma \vdash e :: t$ reads "the type environment $\Gamma$ entails that $e$ has type $t$." The turnstile $\vdash$ comes from Gottlob Frege's logic. $\Gamma, x :: t$ is $\Gamma$ extended with $x$ having type $t$, and a judgment with nothing before $\vdash$ uses the empty environment.

Each kind of expression gets one rule, and rules pass $\Gamma$ to their premises, just as an evaluator passes its environment to recursive calls. A rule that binds a variable (e.g., `let`, a function, or a `case` on a list) extends $\Gamma$ for the part of the expression where that variable is in scope.

The rules for a small language with integers, Booleans, pairs, lists, `let`, and annotated anonymous functions:

$$
\frac{}{\Gamma \vdash n :: \text{int}}
\qquad
\frac{}{\Gamma \vdash \text{true} :: \text{bool}}
\qquad
\frac{\text{var} \in \text{dom}(\Gamma)}{\Gamma \vdash \text{var} :: \Gamma(\text{var})}
$$

$$
\frac{\Gamma \vdash e_1 :: \text{int} \quad \Gamma \vdash e_2 :: \text{int}}{\Gamma \vdash e_1 + e_2 :: \text{int}}
\qquad
\frac{\Gamma \vdash e_1 :: \text{int} \quad \Gamma \vdash e_2 :: \text{int}}{\Gamma \vdash e_1 < e_2 :: \text{bool}}
$$

$$
\frac{\Gamma \vdash e_1 :: \text{bool} \quad \Gamma \vdash e_2 :: t \quad \Gamma \vdash e_3 :: t}{\Gamma \vdash \text{if } e_1 \text{ then } e_2 \text{ else } e_3 :: t}
\qquad
\frac{\Gamma \vdash e_1 :: t_1 \quad \Gamma, \text{var} :: t_1 \vdash e_2 :: t_2}{\Gamma \vdash \text{let var} = e_1 \text{ in } e_2 :: t_2}
$$

$$
\frac{\Gamma, \text{var} :: t_1 \vdash e :: t_2}{\Gamma \vdash (\backslash \text{var} :: t_1 \to e) :: t_1 \to t_2}
\qquad
\frac{\Gamma \vdash e_1 :: t_2 \to t \quad \Gamma \vdash e_2 :: t_2}{\Gamma \vdash e_1 \; e_2 :: t}
$$

$$
\frac{\Gamma \vdash e_1 :: t_1 \quad \Gamma \vdash e_2 :: t_2}{\Gamma \vdash \langle e_1, e_2 \rangle :: (t_1, t_2)}
\qquad
\frac{\Gamma \vdash e :: (t_1, t_2)}{\Gamma \vdash \text{fst } e :: t_1}
\qquad
\frac{\Gamma \vdash e :: (t_1, t_2)}{\Gamma \vdash \text{snd } e :: t_2}
$$

$$
\frac{}{\Gamma \vdash (\text{nil} :: t) :: [t]}
\qquad
\frac{\Gamma \vdash e_1 :: t \quad \Gamma \vdash e_2 :: [t]}{\Gamma \vdash e_1 : e_2 :: [t]}
$$

$$
\frac{\Gamma \vdash e_1 :: [t_1] \quad \Gamma \vdash e_2 :: t_2 \quad \Gamma, \text{var}_1 :: t_1, \text{var}_2 :: [t_1] \vdash e_3 :: t_2}{\Gamma \vdash (\text{case } e_1 \text{ of nil} \Rightarrow e_2 \mid \text{var}_1 : \text{var}_2 \Rightarrow e_3) :: t_2}
$$

(`false` has a rule like `true`'s.) The language's grammar requires annotations where a type can't be read off the expression: on an anonymous function's parameter, and on `nil`, so an empty list's element type is known.

More generally, this style of presenting a type system comes from the study of the typed lambda calculus, and the same derivations are what a type checker builds as it works. A type system is **sound** when well-typed programs can't go wrong at run time in the ways the types rule out, often stated as "progress and preservation." Checking a derivation is mechanical, while finding one without annotations is [[Type Inference|type inference]].

# Examples

## A Derivation for Let

A derivation of $y :: \text{bool} \vdash \text{let } x = 5 \text{ in } x + 1 :: \text{int}$, using the rules for `let`, `+`, variables, and numbers:

$$
\dfrac{
  y :: \text{bool} \vdash 5 :: \text{int}
  \qquad
  \dfrac{
    \dfrac{x \in \{x, y\}}{y :: \text{bool}, x :: \text{int} \vdash x :: \text{int}}
    \qquad
    y :: \text{bool}, x :: \text{int} \vdash 1 :: \text{int}
  }{y :: \text{bool}, x :: \text{int} \vdash x + 1 :: \text{int}}
}{y :: \text{bool} \vdash \text{let } x = 5 \text{ in } x + 1 :: \text{int}}
$$

The `let` rule extends the environment with $x :: \text{int}$, since the bound expression `5` is an `int`, and the body is checked in the extended environment.

# Connections

- [[Type System]]: typing rules are how a type system is specified
- [[Environment (Programming Languages)]]: a type environment maps variables to types the way a value environment maps them to values
- [[Curry-Howard Correspondence]]: why typing derivations are proofs in a deeper sense
- [[Subtyping]]: one more rule, letting a value of a subtype stand in for its supertype
- [[Type Inference]]: finding a derivation without type annotations
- [[Context-Free Grammar]]: the grammar of types and expressions the rules are written over
- [[Lambda Calculus]]: typing rules like these come from the typed lambda calculus

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

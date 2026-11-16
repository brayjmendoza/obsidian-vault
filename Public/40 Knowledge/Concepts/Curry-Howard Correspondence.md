---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Curry–Howard Correspondence
  - Propositions as Types
  - Proofs as Programs
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
The **Curry–Howard correspondence** is the deep connection between logic and programming: a proof is a program, and the formula it proves is the program's type.

Typing rules look like the inference rules of natural deduction, with premises above a line and a conclusion below (see [[Typing Rule]]). The resemblance isn't a coincidence. The rule for applying a function, from $e_1 :: t_2 \to t$ and $e_2 :: t_2$ conclude $e_1 \, e_2 :: t$, has the same shape as modus ponens, from $A \to B$ and $A$ conclude $B$. A function type $A \to B$ corresponds to the implication "$A$ implies $B$," and a function of that type is a proof of it: given a proof of $A$, it produces a proof of $B$.

More generally, the correspondence extends across logic and type theory. Under it, a pair type $(A, B)$ corresponds to "$A$ and $B$," a sum type (e.g., Haskell's `Either A B`) to "$A$ or $B$," and an empty type to falsehood. Evaluating a program corresponds to simplifying a proof. It's named for Haskell Curry and William Howard, and it's the basis of proof assistants like Coq (now Rocq), Agda, and Lean, where proving a theorem means writing a program of the theorem's type. Note that typing derivations are proofs too, but of a different statement: a derivation proves "this program has this type," while Curry–Howard reads the program itself as the proof.

# Example

Function application next to modus ponens:

$$
\frac{\Gamma \vdash e_1 :: t_2 \to t \qquad \Gamma \vdash e_2 :: t_2}{\Gamma \vdash e_1 \; e_2 :: t}
\qquad\qquad
\frac{A \to B \qquad A}{B}
$$

A Haskell function of type `(a -> b) -> a -> b` is a proof that "if $a$ implies $b$, and $a$ holds, then $b$ holds":

```haskell
modusPonens :: (a -> b) -> a -> b
modusPonens f x = f x
```

The type is the proposition, and the definition is its proof. Read each value as evidence:

- **`f :: a -> b` is a proof that $a$ implies $b$.** A function of that type turns any value of type `a` into a value of type `b`, just as a proof of an implication turns any proof of $a$ into a proof of $b$.
- **`x :: a` is a proof of $a$.** Having a value of a type counts as having proved the proposition the type stands for.
- **`f x :: b` is the conclusion.** Applying `f` to `x` produces a value of type `b`, which is a proof of $b$. That one application is the modus ponens step.

So writing a body that type-checks is building the proof, and the type checker accepting it is checking the proof. A proposition with no proof is a type with no program. Nothing of type `a -> b` can be written for arbitrary `a` and `b`, which matches the fact that "$a$ implies $b$" isn't true in general.

One caution for Haskell: a definition that never finishes (e.g., `loop = loop`) can be given any type, so as a logic, Haskell can "prove" anything. Proof assistants built on the correspondence require every program to terminate, which rules this out.

# Connections

- [[Typing Rule]]: typing rules have the form of logical inference rules
- [[Currying]]: also named for Haskell Curry, whose work on combinatory logic led to the correspondence
- [[Type System]]: under the correspondence, a type system is a logic
- [[Lambda Calculus]]: typed lambda calculi are where the correspondence was first stated

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

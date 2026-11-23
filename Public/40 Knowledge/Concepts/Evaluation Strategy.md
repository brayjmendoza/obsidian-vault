---
type: concept
created: 2026-11-15
updated: 2026-11-23
aliases:
  - Call by Value
  - Call by Name
  - Call by Reference
  - Pass by Value
  - Pass by Reference
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An **evaluation strategy** decides when a function's argument is evaluated and what the function receives: in **call by value**, the argument's value, computed before the call; in **call by name**, the unevaluated argument, evaluated only where the body uses it; and in **call by reference**, the caller's variable itself.

In an interpreter that applies functions by [[Substitution|substitution]], the difference is one line:

- **Call by name:** substitute the unevaluated argument for the parameter, then evaluate the body.
- **Call by value:** evaluate the argument first, then substitute its value for the parameter, then evaluate the body.

In most cases, the two give the same result, but they can cost different amounts of work:

| Situation | Call by name | Call by value |
|---|---|---|
| The argument is expensive, and the parameter appears many times | Evaluates it once per use: more work and space | Evaluates it once |
| The argument is expensive, or never finishes, and the parameter is unused | Never evaluates it | Evaluates it anyway: wasted work, or no result at all |

C++ uses call by value by default, and offers call by reference through [[Reference (Programming Languages)|reference]] parameters:

- **Pass by value** (e.g., `void f(Cow c)`): the parameter is copy-initialized from the argument (see [[Initialization (Programming Languages)]]), so the function works on its own copy. Changes to the copy don't reach the caller, and copying a large object costs time and memory.
- **Pass by reference** (e.g., `void f(Cow& c)`): the parameter is another name for the caller's variable. Nothing is copied, and changes reach the caller, which also lets a function give back several results through its reference parameters.
- **Pass by `const` reference** (e.g., `void f(const Cow& c)`): nothing is copied, and the function can't change the argument (see [[Const-Correctness]]). It's the usual way to pass a large object a function only reads.

More generally, the strategies give different results for when evaluating the argument either fails or never finishes but the function itself doesn't actually use the problematic argument: call by name returns a result, and call by value doesn't. With side effects, they can also differ in what happens and how often. Most languages use call by value (e.g., C, Java, and Python). Java and Python pass objects as hidden pointers by value, sometimes called **call by sharing**: a function can change the object it's given, but not which object the caller's variable refers to. Haskell uses **call by need**, which is [[Lazy Evaluation|lazy evaluation]]: call by name, plus remembering an argument's value once it's computed, so it's evaluated at most once.

# Example

The two versions of `eval` for function application, from [[Arith]]'s interpreter:

```haskell
-- Call by name: substitute the unevaluated argument
eval (Apply (FuncDef v body) arg) =
  eval (substitute arg (Var v) body)

-- Call by value: evaluate the argument, then substitute
eval (Apply (FuncDef v body) arg) =
  let val = eval arg
  in eval (substitute val (Var v) body)
```

In C++, `spotTransplant` moves one cow's spots to another, but with value parameters it changes only its copies:

```c++
void spotTransplant(Cow donor, Cow recipient) {
    recipient.setNumSpots(donor.getNumSpots() + recipient.getNumSpots());
    donor.setNumSpots(0);
}

Cow buttercup{1, 3};   // Cow(numSpots, age)
Cow flopsy{2, 13};
spotTransplant(flopsy, buttercup);
std::cout << buttercup.getNumSpots() << " " << flopsy.getNumSpots();   // 1 2
```

This prints `1 2`: `donor` and `recipient` were copies, destroyed when the function returned. With reference parameters, `void spotTransplant(Cow& donor, Cow& recipient)`, they're other names for `flopsy` and `buttercup`, so it prints `3 0`.

# Connections

- [[Lazy Evaluation]]: Haskell's strategy, call by name with sharing
- [[Substitution]]: the step both strategies share
- [[Interpreter]]: where the choice of strategy is made
- [[Reference (Programming Languages)]]: what C++'s call by reference passes
- [[Const-Correctness]]: pass by `const` reference avoids a copy without allowing changes
- [[Beta Reduction]]: the same choice of order, in the lambda calculus, decides whether `((λy . pig) Ω)` ends

# Sources

- [[Programming Languages (HMC CS131)]]
- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

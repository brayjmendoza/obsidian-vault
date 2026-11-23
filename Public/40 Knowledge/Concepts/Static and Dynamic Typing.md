---
type: concept
created: 2026-11-11
updated: 2026-11-23
aliases:
  - Static Typing
  - Dynamic Typing
  - Type Checking
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-21
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A language is **statically typed** when it checks a program for type errors before running it, and **dynamically typed** when it checks them as the program runs.

A **type error** is an operation applied to a value of the wrong type (e.g., adding a number to a string). A program with no type errors is **type-safe**, and to **type-check** a program is to determine whether it has any. The distinction between the two kinds of language rests on two more terms:

- **Static:** a property of a program that is, or can be, determined without running it.
- **Dynamic:** a property that is determined by running the program.

| | Statically typed | Dynamically typed |
|---|---|---|
| Who checks | Usually a compiler, before the program runs | Usually an interpreter, as the program runs |
| A type error | Stops the program from compiling, so it never runs | Can crash the program partway through |

More generally, statically typed languages include Haskell, Java, and Rust, and dynamically typed ones include Python, JavaScript, and Racket. Static typing catches mistakes earlier and in code paths a test might never reach. Dynamic typing accepts some correct programs a static checker would reject, and it asks less of the programmer up front.

A **type annotation** is information the programmer writes about a type (e.g., `successor :: Integer -> Integer`, read "`successor` has type `Integer -> Integer`"). Static typing doesn't require annotations everywhere: a language with [[Type Inference]] works most of them out itself.

# Example

Haskell rejects a list of mixed types before evaluating anything, since every element of a list must have the same type:

```
ghci> [True, True, 'a']
<interactive>:27:14: error:
    • Couldn't match expected type ‘Bool’ with actual type ‘Char’
    • In the expression: 'a'
      In the expression: [True, True, 'a']
```

Python accepts the same list, and a type error shows up only when a line runs:

```python
items = [True, True, 'a']  # fine
total = 1 + 'a'            # TypeError, raised only when this line runs
```

# Connections

- [[Type Inference]]: how Haskell stays statically typed without annotations everywhere
- [[Partial Function]]: a well-typed program can still fail at run time when a function has no result for its argument
- [[Type System]]: the rules being checked, whenever the checking happens
- [[Typing Rule]]: how static type checking is specified precisely
- [[Undefined Behavior]]: what C++ gives instead of a run-time error for the mistakes it doesn't check
- [[Type Conversion]]: a statically typed language decides at compile time where values are converted

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]

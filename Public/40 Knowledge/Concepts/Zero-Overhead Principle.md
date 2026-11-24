---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Zero-Cost Abstraction
  - What You Don't Use, You Don't Pay For
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
The **zero-overhead principle** is a rule for designing a language: a feature costs nothing, in time or space, to a program that doesn't use it, and a program that does use it couldn't do the same thing any better by hand.

The principle has two halves:

1. **What you don't use, you don't pay for.** Adding a feature must not make existing programs, which don't use it, any larger or slower.
2. **What you do use, you couldn't hand-code any better.** The code a compiler generates for a feature must be as good as what a programmer could write without it.

The principle comes from C++'s design goals. Bjarne Stroustrup created C++ to analyze the performance of the UNIX operating system, so he wanted a language that was fast and gave the programmer close control of the machine. He also built it as an extension of C, so that C programmers would adopt it: almost every C program is also a C++ program, and its C++ version must be just as fast and use just as little memory. Every feature C++ adds has to leave that true.

A consequence is that C++ doesn't check whether a program follows its rules while it runs, since every check would cost time in programs that follow them. A program that breaks a rule has [[Undefined Behavior|undefined behavior]] instead of an error message. This goes with a second design principle, sometimes called **power to the people**: C++ trusts the programmer and gives them a high level of control, including the control to make mistakes the language won't catch.

More generally, Stroustrup states the principle in *The Design and Evolution of C++* (1994), and C++ features built on it, such as templates and inline functions, are often called **zero-cost abstractions**. Rust adopts the same principle. Most languages make the opposite trade: Java and Python, for instance, check array bounds on every access, so a mistake gives an error instead of undefined behavior, at a cost every program pays.

# Example

For illustration (an example not from the source), indexing an array in C++ compiles to a single memory access, with no check that the index is in bounds. A bounds check would be a comparison on every access, paid by every program, even one whose indices are always correct. A programmer who wants the check can write it, or use a library function that includes it (e.g., `std::vector`'s `at`), and pays for it only there.

# Connections

- [[Undefined Behavior]]: the cost of leaving rule-breaking unchecked
- [[Abstraction]]: the principle asks that an abstraction add no cost over the code it abstracts
- [[Static and Dynamic Typing]]: checks done before a program runs cost nothing at run time, which is why C++ does its type checking statically
- [[Array (Data Structure)]]: C++ doesn't check array indices, so indexing costs one memory access
- [[Dynamic Dispatch]]: C++ makes virtual calls opt-in, so classes without them don't pay for them

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

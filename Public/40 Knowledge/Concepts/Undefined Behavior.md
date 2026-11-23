---
type: concept
created: 2026-11-23
updated: 2026-11-23
aliases:
  - Indeterminate Value
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Undefined behavior** is what a program does when it breaks a rule that the language's definition places on programs but that no one is required to check: the language says nothing about what happens next, so anything may.

C++ has many such rules. A program must not read past the end of an array, follow a pointer that doesn't point to a valid object, or use a variable's value before giving it one. A program that breaks one of them isn't rejected by the compiler and isn't stopped while it runs, because checking would cost time or space in every program, including the ones that follow the rules (see [[Zero-Overhead Principle]]). Instead, the language places the burden on the programmer, and a program that breaks a rule has no meaning at all.

Undefined behavior is hard to find for three reasons:

- **It can look correct.** A program that breaks a rule may run exactly as intended, on one machine or for one input.
- **It can change without warning.** The same program may behave differently with another compiler, another optimization setting, or another machine.
- **Its effects can appear far from the cause.** A write past the end of an array can corrupt an unrelated variable, and the failure shows up only when that variable is used.

Compilers and other tools can warn about some rule-breaking code, but they aren't required to, and they can't catch all of it.

A related idea is the **indeterminate value**: the value of a variable that was created without being given one (e.g., `int x;` in C++, see [[Initialization (Programming Languages)]]). Its contents are whatever bits were already in that memory, which can differ between runs and machines. Using an indeterminate value is undefined behavior for most types, and for a `bool` it can even be neither `true` nor `false`.

More generally, undefined behavior is a feature of C and C++ above all, and it's what lets their compilers optimize aggressively: a compiler may assume no rule is ever broken (e.g., that a loop's index never overflows) and generate code that's only correct under that assumption. It differs from **unspecified behavior**, where the language allows a few outcomes and an implementation picks one (e.g., the order in which a function's arguments are evaluated), and from **implementation-defined behavior**, where the implementation picks and documents the outcome (e.g., the size of an `int`). Languages like Java and Python define what happens in these situations instead, usually by raising an error, and pay for the checks at run time. Rust allows undefined behavior only inside code marked `unsafe`.

# Example

A linear search with an off-by-one mistake (an example not from the source) compares `x` against one element too many. When `i` equals `arrSize`, `arr[i]` reads past the end of the array:

```c++
bool lookUp(float x, const float* arr, size_t arrSize) {
    for (size_t i = 0; i <= arrSize; ++i) {   // should be i < arrSize
        if (arr[i] == x) {
            return true;
        }
    }
    return false;
}
```

The compiler accepts it, and it often returns the right answer, since the extra memory it reads usually just holds some other value. That's why the bug can go unnoticed: the program's behavior on the last comparison is undefined, so the same code can also return `true` for a value that isn't in the array, or crash.

# Connections

- [[Zero-Overhead Principle]]: why C++ leaves rule-breaking unchecked instead of reporting it
- [[Initialization (Programming Languages)]]: default-initialized variables hold indeterminate values
- [[Static and Dynamic Typing]]: some errors that undefined behavior covers in C++ are caught by checks in other languages, before or during a run
- [[Black-Box Testing]]: tests must never rely on undefined behavior, since its result means nothing
- [[Syntax and Semantics]]: a program with undefined behavior is syntactically valid but has no semantics
- [[Pointer (Programming Languages)]]: following an invalid, null, or past-the-end pointer
- [[Dynamic Memory Allocation]]: using memory after it's freed, or freeing it twice
- [[Segmentation Fault]]: the crash undefined behavior often, but not always, causes

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

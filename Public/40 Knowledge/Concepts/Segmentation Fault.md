---
type: concept
created: 2026-11-23
updated: 2026-11-23
aliases:
  - Segfault
  - Access Violation
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **segmentation fault** is the error the operating system raises when a program tries to access memory outside the regions it's been given, and it usually ends the program.

Each running program has its own set of memory regions it may use (e.g., its stack, its heap, and its code), and the hardware checks every access against them. An access outside them stops the program on the spot. In C++, a segmentation fault is the usual symptom of following a null pointer, a dangling pointer, or a pointer far past the end of an array (see [[Pointer (Programming Languages)]] and [[Dynamic Memory Allocation]]).

A segmentation fault is a symptom, not a guarantee. Those mistakes are [[Undefined Behavior|undefined behavior]], and a segmentation fault happens only when a bad access lands outside the program's memory. A pointer a little past the end of an array usually lands in memory the program owns, so the access succeeds and quietly reads or corrupts other data.

More generally, the name comes from **segmentation**, an older way of dividing memory into segments. Modern systems divide memory into pages instead, but the name stuck on Unix-like systems, where the signal is `SIGSEGV`. Windows calls the same error an **access violation**. A tool like Valgrind, or a compiler's address sanitizer, catches many bad accesses that don't segfault.

# Example

For illustration (an example not from the source), following a null pointer:

```c++
int* p = nullptr;
std::cout << *p;   // usually: Segmentation fault (core dumped)
```

Address zero is never part of a program's memory, so dereferencing `p` reliably faults in practice. The standard promises nothing, though: the program's behavior is undefined, so a compiler may even remove the read.

# Connections

- [[Undefined Behavior]]: a segmentation fault is one possible outcome of it
- [[Pointer (Programming Languages)]]: following a null or invalid pointer
- [[Dynamic Memory Allocation]]: dangling pointers into freed memory

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

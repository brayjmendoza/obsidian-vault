---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Stack
  - LIFO
  - Last In, First Out
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **stack** is a collection where items are added and removed at the same end, so the item removed is always the one added most recently: **last in, first out** (LIFO).

A stack's interface has three main operations: **push** adds an item to the top, **pop** removes the top item, and **top** (or **peek**) returns it without removing it. It's a linear data structure, keeping its items in an order, but only one item, the top, is ever reachable.

A stack is like an ideal plane boarding: the first passengers to board sit at the back, so they're the last to leave. Either a [[Dynamic Array|dynamic array]], pushing and popping at its end, or a [[Linked List|linked list]], pushing and popping at its front, gives every operation constant time (amortized constant time, for the array).

More generally, stacks are everywhere a computation must return to where it was: a program's **call stack** holds each active function call's stack frame (see [[Object Lifetime]]), undo histories are stacks, and checking that brackets match pushes each opening bracket and pops at each closing one. The term "first in, last out" (FILO) means the same as LIFO.

# Example

Matching brackets with a stack (an example not from the source): push each opening bracket, and at each closing bracket, pop and check that it's the matching kind.

| Input so far | Stack after (top on the right) |
|---|---|
| `(` | `(` |
| `([` | `( [` |
| `([]` | `(` |
| `([])` | empty |

The string is balanced, since every pop matched and the stack ends empty. For `([)]`, the `)` would pop `[`, a mismatch, so it's unbalanced. A stack fits because the most recently opened bracket must be the first one closed.

# Connections

- [[Queue (Abstract Data Type)]]: the first-in, first-out counterpart
- [[List (Abstract Data Type)]]: a stack is a list restricted to one end
- [[Abstract Data Type]]: a stack is defined by its operations, whatever stores it
- [[Dynamic Array]] and [[Linked List]]: the usual encodings
- [[Black-Box Testing]]: testing a stack through push, pop, and top alone

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - ADT
  - Interface
  - Encoding
  - Implementation
  - Representation Invariant
  - Contract
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An **abstract data type** is a data type defined by the operations it supports and what they promise, separately from how its data is stored and how the operations work.

A data structure is described at three levels:

- **Interface:** *what* the data structure supports, the set of operations available and what each does, without saying how. In C++, it's the public members of the class definition, in the header.
- **Encoding:** *how* the data is organized. It's the design decisions about what variables store the data, what bookkeeping values are needed (e.g., a count of items), what each variable means, and what relationships must always hold between them. In C++, it's the private members of the class definition.
- **Implementation:** the mechanisms that create and maintain the encoding so that it delivers what the interface promises. In C++, it's mostly the member functions' definitions, in the source file.

One interface can have many valid encodings, and one encoding many valid implementations. A list, for instance, can be encoded as an array or as a chain of linked nodes, and code that uses only the interface works with either.

At each level, the designer has to decide which promises it makes and which it doesn't. Together, these promises are the data structure's **contract** with its users:

| Level | Example promise |
|---|---|
| Interface | An operation takes constant time |
| Encoding | A relationship between members always holds (e.g., `size_ <= capacity_`) |
| Implementation | Running out of memory is handled gracefully, or the code is optimized for one processor |

A promise made at the encoding level, a relationship that must hold whenever no operation is in progress, is a **representation invariant**. Every operation may assume it on entry and must restore it before returning.

## Choosing a Data Structure

Interfaces fall into three broad categories, each good at something different:

| Category | Examples | Good at | Not good at |
|---|---|---|---|
| **Linear** | [[List (Abstract Data Type)\|List]], [[Stack (Abstract Data Type)\|stack]], and [[Queue (Abstract Data Type)\|queue]] | Keeping items in a particular order | Searching for a particular item |
| **Associative** | [[Set (Abstract Data Type)\|Set]], and [[Associative Array\|map]] | Searching for a particular item | Keeping track of order |
| **[[Priority Queue\|Priority queue]]** | A category of its own | Finding the smallest item (or the largest) | Searching, and keeping order, beyond repeatedly removing the smallest |

No data structure is best overall: each has different trade-offs, and the best one depends on the application. The more that's known about the data to be stored (e.g., that keys arrive in random order, or that recent items are looked up most), the easier it is to pick the best structure. For small problems, the choice may make no noticeable difference, so extra work to optimize isn't always worth it.

More generally, the idea comes from Barbara Liskov and Stephen Zilles, who introduced abstract data types in 1974, and from David Parnas's principle of **information hiding** (1972): hide each design decision that's likely to change behind an interface. "Encoding" is a less common word for what's usually called the **representation**. Java and Go state interfaces as types of their own, separate from any class that implements them, and Haskell does much the same with [[Type Class|type classes]].

# Examples

## A Resizable List

For illustration (an example not from the source), a resizable list of `int`s might have this interface:

| Operation | Promise |
|---|---|
| `push_back(x)` | Adds `x` at the end, in amortized constant time |
| `size()` | Returns how many items there are |
| `operator[](i)` | Returns item `i`, for `i < size()` |

One encoding is a heap array `values_` with `capacity_` slots, of which the first `size_` hold the list, with the invariant `size_ <= capacity_`. Another is a linked chain of nodes. A user of `push_back` can't tell which is in use: only the interface's promises are visible, so either encoding, and any implementation of it that keeps the promises, is correct.

# Connections

- [[Class (Programming Languages)]]: public members give the interface, and private members the encoding
- [[Abstraction]]: an interface abstracts away its encoding and implementation
- [[Black-Box Testing]]: tests check only the interface's promises, so they work for any encoding
- [[Type Class]]: Haskell's way to state an interface many types can implement
- [[Expression Problem]]: what an interface makes easy and hard to extend
- [[Asymptotic Analysis]]: how an interface states the cost of its operations
- [[Inheritance (Object-Oriented Programming)]]: an interface class states an interface as a C++ type
- [[Iterator]]: a container's interface for visiting its items

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

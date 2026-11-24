---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - List
  - Sequence (Abstract Data Type)
  - Linear Data Structure
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **list** is a collection that stores items in a linear order and allows access, insertion, and removal at any position.

A list is the most general **linear data structure**, a collection that keeps its items in a particular order. Stacks, queues, steques, and deques are lists restricted to their ends (see [[Stack (Abstract Data Type)]] and [[Queue (Abstract Data Type)]]). Linear data structures are good at keeping things in order, but not always good at searching for a particular item: finding one means checking items in turn.

Every linear data structure is encoded by one of two kinds of list, whose costs are opposite:

| Operation | [[Dynamic Array]] (array-backed list) | [[Linked List]] |
|---|---|---|
| Reach the $i$th item | $\Theta(1)$ | $\Theta(i)$ |
| Add or remove at the end | $\Theta(1)$ amortized | $\Theta(1)$, with a pointer to the last node (and, to remove, a doubly linked list) |
| Add or remove at the front | $\Theta(n)$ | $\Theta(1)$ |
| Add or remove at a known position | $\Theta(n)$, shifting the items after it | $\Theta(1)$ |
| Search for an item | $\Theta(n)$ | $\Theta(n)$ |

Neither is best: which to use depends on which operations the program needs most (see [[Abstract Data Type]]).

More generally, Python's `list` and Java's `List` interface are lists in this sense. In functional languages, "list" usually means an immutable singly linked list, built from an empty list and an item consed onto another list (see [[Recursive Data Type]]).

# Examples

## A Playlist and a Leaderboard

For illustration (an example not from the source), a playlist that's played in order, with songs inserted wherever the listener drags them, needs insertion at a known position more than reaching a song by number. A linked list does each insertion in constant time, while a dynamic array would shift every later song. A leaderboard read by rank ("show the 10th score") needs the reverse, so a dynamic array suits it.

# Connections

- [[Dynamic Array]] and [[Linked List]]: the two encodings, with opposite costs
- [[Stack (Abstract Data Type)]] and [[Queue (Abstract Data Type)]]: lists restricted to their ends
- [[Associative Array]]: the associative counterpart, good at search rather than order
- [[Iterator]]: how code walks a list without knowing its encoding

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Queue
  - FIFO
  - First In, First Out
  - Deque
  - Double-Ended Queue
  - Steque
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **queue** is a collection where items are added at one end, the back, and removed from the other, the front, so the item removed is always the one that's waited longest: **first in, first out** (FIFO).

A queue's main operations are **enqueue**, which adds an item at the back, and **dequeue**, which removes the item at the front. It's like the line at a bank: the first customer in line is served first.

Two variants relax which ends allow what:

| Structure | Add at | Remove from | Like |
|---|---|---|---|
| [[Stack (Abstract Data Type)\|Stack]] | One end | The same end | Plane boarding: first on, last off |
| **Queue** | The back | The front | A bank line |
| **Steque** (stack-ended queue) | Either end | The front only | A grocery store's milk fridge: stocked from the back, and customers take from the front, or put a carton back there |
| **Deque** (double-ended queue) | Either end | Either end | A freight train: cars attach and detach at either end, never the middle |

All are linear data structures. A [[Linked List|linked list]] with pointers to both ends gives a queue constant-time operations, and a doubly linked list does the same for a deque. A [[Dynamic Array|dynamic array]] can too, if it treats its array as a ring, wrapping around from the last slot to the first, so removing at the front doesn't shift every item.

More generally, queues order work that should be handled in arrival order, like print jobs, requests to a server, and the frontier of a breadth-first search. When items should leave by importance rather than arrival, the structure is a **[[Priority Queue|priority queue]]**. C++'s standard library provides `std::queue` and `std::deque`, and Python's `collections.deque` is a deque.

# Examples

## Enqueuing and Dequeuing

For illustration (an example not from the source), enqueuing `A`, `B`, and `C`, then dequeuing twice:

| Operation | Queue after (front on the left) | Returns |
|---|---|---|
| enqueue `A` | `A` | |
| enqueue `B` | `A B` | |
| enqueue `C` | `A B C` | |
| dequeue | `B C` | `A` |
| dequeue | `C` | `B` |

Items leave in the order they arrived. A stack given the same operations would return `C` first, then `B`.

# Connections

- [[Stack (Abstract Data Type)]]: the last-in, first-out counterpart
- [[List (Abstract Data Type)]]: a queue is a list restricted to its two ends
- [[Linked List]]: the simplest encoding with constant-time operations at both ends
- [[Abstract Data Type]]: each variant is a different interface over the same kind of data
- [[Priority Queue]]: items leave by key instead of by arrival

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

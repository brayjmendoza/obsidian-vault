---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Priority Queue (Abstract Data Type)
  - Ordered Key
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **priority queue** is a collection in which every item has a key, its priority, and the item removed next is always the one with the smallest key (or, if set up the other way, the largest).

Keys must be **ordered keys**, comparable with `<`, most commonly numbers. Whether lower or higher values count as more important is a choice of the design. A priority queue's main operations:

| Operation | Does |
|---|---|
| **INSERT** | Adds a new item with a given key |
| **GET-MIN** | Returns the item with the smallest key. Items with equal keys come out in no particular order |
| **POP-MIN** | Removes the item with the smallest key |
| **CHANGE-PRIORITY** | Changes the key of an item already in the queue, and reorders it accordingly |

A priority queue is a category of its own among abstract data types (see [[Abstract Data Type#Choosing a Data Structure|Choosing a Data Structure]]). It's good at finding the minimum, and only that: it isn't good at searching for a particular item, and it doesn't keep items in an order, beyond the order in which repeated POP-MINs remove them. Its most common encoding is a [[Binary Heap|binary heap]], which does INSERT, POP-MIN, and CHANGE-PRIORITY in $O(\log n)$ time and GET-MIN in $\Theta(1)$.

Priority queues serve algorithms that repeatedly take the most urgent thing next, such as finding shortest paths in a graph (Dijkstra's algorithm, which uses CHANGE-PRIORITY to lower a distance) and building Huffman codes for data compression (which repeatedly combines the two least frequent symbols).

More generally, a [[Queue (Abstract Data Type)|queue]] is the special case where priority is arrival time, and a [[Stack (Abstract Data Type)|stack]] is the case where it's the reverse of arrival time. Operating systems schedule processes with priority queues, and simulations keep pending events in one, ordered by time. C++'s `std::priority_queue` is a max-heap by default, and Python's `heapq` module keeps a min-heap in a list.

# Examples

## Order of Removal

Three items inserted with keys 5, 3, and 10 come out in order of key, not of insertion:

```c++
PriorityQueue pq;
pq.insert("First", 5);    // item, key
pq.insert("Second", 3);
pq.insert("Third", 10);

for (size_t i = 0; i < 3; ++i) {
    std::cout << pq.getMin() << " ";
    pq.popMin();
}
```

This prints `Second First Third`. `"Second"` has the smallest key, 3, so it's the minimum though it was inserted second. A plain queue would have printed `First Second Third`.

# Connections

- [[Binary Heap]]: the most common encoding
- [[Queue (Abstract Data Type)]]: a priority queue ordered by arrival time
- [[Abstract Data Type]]: a priority queue is defined by its operations, whatever stores it
- [[Heap Sort]]: sorting by inserting everything and popping the minimum repeatedly

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

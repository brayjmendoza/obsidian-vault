---
type: map
created: 2026-11-23
updated: 2026-11-24
field: computer-science
---
↑ [[Computer Science]]

# Analysis of Algorithms

1. [[Asymptotic Analysis]] — how cost scales with input size, in $O$, $\Theta$, and $\Omega$
2. [[Best, Worst, and Expected Case]] — which inputs of a given size a bound describes
3. [[Amortized Analysis]] — bounding a whole sequence of operations, so rare expensive ones are paid for by cheap ones

# Abstract Data Types

1. [[Abstract Data Type]] — a type described by its interface, separately from its encoding and implementation

# Linear Data Structures

1. [[Array (Data Structure)]] — fixed-size, contiguous storage with constant-time indexing, the base most other structures build on
2. [[Dynamic Array]] — an array that grows by copying into a bigger one, so it can hold any number of items
3. [[Linked List]] — a chain of nodes, cheap to insert into and slow to index
4. [[Iterator]] — a position in a collection that steps through its items, whatever the storage
5. [[List (Abstract Data Type)]] — items in order, reachable at any position, encoded by either kind of list
6. [[Stack (Abstract Data Type)]] — last in, first out
7. [[Queue (Abstract Data Type)]] — first in, first out, and the steque and deque that relax it

# Associative Data Structures

1. [[Set (Abstract Data Type)]] — unique keys, for fast membership tests
2. [[Associative Array]] — unique keys with values, looked up by key

# Search Trees

1. [[Tree (Data Structure)]] — roots, leaves, subtrees, height, and binary trees
2. [[Binary Search Tree]] — a binary tree ordered for search, as fast as it is short
3. [[Tree Rotation]] — reshaping a BST in constant time without breaking its order
4. [[Randomized Binary Search Tree]] — random choices for an expected logarithmic height
5. [[Splay Tree]] — moving each used key to the root, for amortized logarithmic time
6. [[2-3-4 Tree]] — nodes of one to three keys, growing only at the root, so always balanced
7. [[Red-Black Tree]] — a 2-3-4 tree as a BST, for worst-case logarithmic time

# Priority Queues and Heaps

1. [[Priority Queue]] — always removing the item with the smallest key
2. [[Binary Heap]] — a complete tree ordered top to bottom, stored in an array
3. [[Heap Sort]] — sorting in place by repeatedly popping a max-heap's maximum

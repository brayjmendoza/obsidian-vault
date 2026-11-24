---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Doubly Linked List
  - Singly Linked List
  - Node (Data Structure)
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **linked list** stores a list as a chain of separately allocated **nodes**, each holding one item and a pointer to the next node, so the items needn't sit together in memory.

In a **singly linked list**, each node points only to the next node. In a **doubly linked list**, each node also points to the previous one, so the list can be walked in both directions. The list itself keeps a pointer to its first node, and often its last. Each node is allocated on its own (see [[Dynamic Memory Allocation]]), so the list grows one node at a time, with no capacity to run out of.

A linked list's strengths and weaknesses are the reverse of a [[Dynamic Array|dynamic array]]'s:

- **Inserting or removing at a known position is cheap.** It rewires a few pointers, whatever the list's length, and moves no other item.
- **Reaching an item by position is slow.** There's no index arithmetic: reaching the $i$th item means following $i$ pointers from the start.
- **Iterators stay valid.** Inserting moves no existing node, so every [[Iterator|iterator]] still refers to its item, and erasing invalidates only iterators at the erased item.

C++'s `std::list` is a doubly linked list. Its iterators are **bidirectional**: they can move forward with `++` and back with `--`, one node at a time, but can't jump to an arbitrary position as an array index can.

More generally, linked lists are a classic [[Recursive Data Type|recursive data type]]: a list is either empty or a node holding an item and the rest of the list, which is exactly how Haskell's lists are defined. On modern hardware, a linked list is often slower in practice than its costs suggest, since following pointers to nodes scattered across memory defeats the processor's caches, while a dynamic array's contiguous items suit them. So dynamic arrays are the usual default, and linked lists are kept for when insertions in the middle, or stable iterators, matter.

# Examples

## Inserting in the Middle

For illustration (an example not from the source), inserting into the middle of a `std::list` touches only the neighbors:

```c++
std::list<int> values{1, 2, 4};
auto i = values.begin();
++i; ++i;                 // i is at 4
values.insert(i, 3);      // values is now {1, 2, 3, 4}
std::cout << *i;          // still 4: i is still valid
```

`insert` puts the new node before `i`, linking it between the nodes holding `2` and `4`, and no other node moves. With a `std::vector`, the same insertion would shift `4` one slot over, and `i` would be invalid afterward.

# Connections

- [[Dynamic Array]]: the array-based way to store a list, with the opposite trade-offs
- [[Pointer (Programming Languages)]]: what links each node to the next
- [[Iterator]]: a linked list's iterators follow its links
- [[Recursive Data Type]]: a list is empty, or an item followed by a list
- [[Abstract Data Type]]: a list interface that either kind of list can encode
- [[List (Abstract Data Type)]]: the interface a linked list encodes
- [[Binary Search Tree]]: a BST built from sorted keys degenerates into a linked list

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

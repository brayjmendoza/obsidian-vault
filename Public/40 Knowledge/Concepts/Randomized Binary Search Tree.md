---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Randomized BST
  - Random Binary Search Tree
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **randomized binary search tree** keeps itself balanced by randomly choosing where along an insertion's path the new key ends up, so that the tree has the shape of one built from keys inserted in a random order.

## Why Random Order Works

A plain [[Binary Search Tree|BST]]'s shape depends on the order its keys were inserted in. Consider every possible order of inserting 31 keys, each equally likely:

- It's vanishingly unlikely to get a stick: a stick of $n$ keys arises from only $2^{n-1}$ of the $n!$ orders, so for 31 keys its probability is about $10^{-25}$.
- It's also very unlikely to get a perfectly balanced tree, with probability about $10^{-11}$ for 31 keys, though that's far likelier than a stick.
- It's likely to get a tree that's balanced *enough*. The average height is $8.174$, with a standard deviation of $1.302$, against the perfect height of $4$.

So random insertion order gives an expected height, and expected average depth, of $\Theta(\log n)$, the same order as a perfectly balanced tree. But real keys often arrive in an order that isn't random (e.g., already sorted), which builds a stick. A randomized BST moves the randomness into the insertion algorithm itself, which has the same effect as shuffling the keys before inserting them, without needing to know all the keys in advance.

## Insertion

In a randomly built tree of $N$ nodes, a newly inserted key would have been inserted first, and so be the root, with probability $\frac{1}{N + 1}$, since it's one of $N + 1$ keys. So insertion walks down from the root as usual, and at each node, whose subtree holds $N$ nodes:

- **With probability $\frac{1}{N + 1}$,** the new key becomes the root of this subtree, inserted there by **insert-at-root**: insert it as a leaf, then rotate it up to this position (see [[Tree Rotation#Moving a Node to the Root|Tree Rotation]]).
- **With probability $\frac{N}{N + 1}$,** continue into the left or right subtree, as a plain BST insert would.

Each node stores the size of its subtree, so the probability can be computed at every step.

## Cost

Lookup, insert, and delete are still $O(n)$: in the worst case, $\Theta(n)$. But the worst case is extremely unlikely, whatever order the keys arrive in, so the expected time, $O(\log n)$, is the less misleading description (see [[Best, Worst, and Expected Case]]). The cost is the extra space for each node's subtree size, and rotations during insertion and deletion. It's simpler to implement than the strictly balanced trees.

More generally, Conrado Martínez and Salvador Roura described randomized BSTs in 1998. A **treap** (Cecilia Aragon and Raimund Seidel, 1989) reaches the same distribution of shapes differently: each node gets a random priority, and the tree is kept as a heap by priority. Skip lists apply the same idea, randomness in place of balance rules, to linked lists.

# Examples

## Inserting into Three Nodes

Inserting into a subtree of $N = 3$ nodes: with probability $\frac{1}{4}$, the new key becomes the root of that subtree, by insert-at-root. Otherwise, with probability $\frac{3}{4}$, insertion moves into the child subtree where the key belongs, say one of $1$ node, and there the new key becomes its root with probability $\frac{1}{2}$, or else continues down. When the new key reaches an empty subtree, $N = 0$, and the probability is $\frac{1}{1} = 1$: it becomes a leaf, as in a plain BST.

# Connections

- [[Binary Search Tree]]: the structure being kept balanced
- [[Tree Rotation]]: insert-at-root moves the new key up by rotations
- [[Best, Worst, and Expected Case]]: why expected time is the honest measure here
- [[Splay Tree]] and [[Red-Black Tree]]: the amortized and worst-case alternatives

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

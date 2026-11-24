---
type: reference
created: 2026-11-24
updated: 2026-11-24
topic: algorithms
---
How plain, randomized, splay, and red-black binary search trees compare, for choosing between them. The trees themselves are explained in [[Binary Search Tree]], [[Randomized Binary Search Tree]], [[Splay Tree]], and [[Red-Black Tree]].

# Single Operations and Sequences

$n$ is the tree's size, and $m$ the number of operations.

| | Plain BST | Splay tree | Red-black tree |
|---|---|---|---|
| Best insert, tree of size $n$ | Child of root: $\Theta(1)$ | Child of root: $\Theta(1)$ | $\Theta(\log n)$ |
| Worst insert, tree of size $n$ | Bottom of a stick: $\Theta(n)$ | Bottom of a stick: $\Theta(n)$ | $\Theta(\log n)$ |
| Best lookup, tree of size $n$ | Key at root: $\Theta(1)$ | Key at root: $\Theta(1)$ | Key at root: $\Theta(1)$ |
| Worst lookup, tree of size $n$ | Bottom of a stick: $\Theta(n)$ | Bottom of a stick: $\Theta(n)$ | $\Theta(\log n)$ |
| Best $m$ inserts into an empty tree | Balanced: $\Theta(m \log m)$ | Sorted order: $\Theta(m)$ | $\Theta(m \log m)$ |
| Worst $m$ inserts into an empty tree | Sorted order: $\Theta(m^2)$ | $\Theta(m \log m)$ | $\Theta(m \log m)$ |
| Best $m$ lookups, tree of size $m$ | All at root: $\Theta(m)$ | Same key repeatedly: $\Theta(m)$ | All at root: $\Theta(m)$ |
| Worst $m$ lookups, tree of size $m$ | Bottom of a stick: $\Theta(m^2)$ | $\Theta(m \log m)$ | All in leaves: $\Theta(m \log m)$ |

# Balanced Trees Side by Side

| | Randomized BST | Red-black tree | Splay tree |
|---|---|---|---|
| Overall | Expected $\Theta(\log n)$ | Worst-case $\Theta(\log n)$ | Amortized $\Theta(\log n)$ |
| Height | Expected $\Theta(\log n)$: untidy, but balanced enough | Worst-case $\Theta(\log n)$: very well balanced | $O(n)$: can become a stick, but operations tend to rebalance it |
| Best lookup | $O(1)$ | $O(1)$ | $O(1)$ |
| Best insert or delete | $O(1)$ | $\Theta(\log n)$ | $O(1)$ |
| Worst single operation | $\Theta(n)$, but implausible | $\Theta(\log n)$ | $\Theta(n)$, and easily triggered |
| Worst $m$ operations | $\Theta(m^2)$, but implausible | $\Theta(m \log m)$ | $\Theta(m \log m)$ |
| Inserting $n$ keys in sorted order | Expected $\Theta(n \log n)$, with a better constant than usual | $\Theta(n \log n)$ | $\Theta(n)$, with balancing deferred |
| Locality | No promises | No promises | Recently used keys are cheap |
| Extra space per node | Subtree size (an integer) | Color (a boolean) | None |
| Extra time | Rotations on insert and delete | Rotations on insert and delete | Rotations on insert, delete, and lookup |
| Implementation | Pretty simple | Often considered complex | Medium |

# Choosing

- **Need a guarantee for every operation** (e.g., real-time code): red-black tree.
- **Recently used keys are likely to be used again:** splay tree.
- **Want simple code and good typical behavior:** randomized BST.
- **Keys are known to arrive in random order:** a plain BST is enough.

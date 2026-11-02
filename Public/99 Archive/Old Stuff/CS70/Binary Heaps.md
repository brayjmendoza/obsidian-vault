The most common encoding of [[Priority Queue|priority queues]]

A **binary heap** is a **binary tree** such that
1. **Structure Property:** The tree is **complete**
    - Every level except (possibly) the last is full
    - The last level is filled in from left to right
2. **Order Property:** There are two kinds of heaps: **min-heaps** (which have the smallest element at the top) and **max-heaps** (which have the largest)
    - In a _min-heap_, the value in every node is at least as small as _all_ of its children
    - In a _max-heap_, the value in every node is at least as big as _all_ of its children
- **Note:** Each subtree is also a binary heap

#### Example Heap
![[binaryHeap.png]]
+ Note that left/right is not relevant to how data is organized, but rather above/below

## Representing a Heap
Though we visualize heaps as a binary tree, we usually encode them as an array
+ Binary heaps are *complete trees*, meaning there are no gaps
+ A level-order traversal tell us how to order the nodes as an array
![[HeapAsArray.png]]

In general, the node at index $i$ has its
+ Left children at index $2i + 1$
+ Right children at index $2i + 2$
+ Parent at index $\lfloor(i-1)/2\rfloor$ (where $\lfloor x \rfloor$ is the floor function)

## Insert
To insert a new value into the heap:
+ Insert at the end of the last layer of the tree 
	+ This is the next available spot in the array
- Swap with the parent until the parent has a smaller priority (for a min-heap)
	- Larger priority for a max-heap

+ Complexity: $O(\log{n})$

## Pop-Min
To pop the minimum value off a (min)-heap
1. Replace the root (index 0) with the last element in the heap (index $n - 1$).
	+ Note that the root index is the smallest value in a min-heap
	+ Swapping with the last element maintains completeness
		+ If we only swapped with the smallest child, we would get a hole in the tree (breaking the structure property)
2. Swap it with its smallest child until it has a smaller key than both children.
	+ Maintains the order property

+ Complexity: $O(\log{n})$
## Heapify
Turns an array with pre-existing items into a binary heap

The algorithm (pseudocode):
```
for (i = n − 1; i ≥ 0; −−i)
    SINK-DOWN(i)
```
+ We start at the end of the array and sink every element down 
	+ `SINK-DOWN` moves the item to its correct position in the array (as a heap)
		+ This correct position will be at a lower index 

+ Complexity: $\Theta(n)$

## Heap Sort
We can use heap operations for a sorting algorithm

Pseudocode (for an array `arr` with `n` items):
```
HEAP-SORT(arr) algorithm:
    MAX-HEAPIFY(arr)        // Turn the array into a max-heap
    for (i = 1; i ≤ n; ++i)
        x = GET-MAX(arr)    // Remember this is a max heap
        POP-MAX(arr)
        arr[n − i] = x      // This spot is no longer part of the heap
```
+ At the end, the array that used to hold the heap will be filled with the numbers in sorted order (smallest to largest)
+ [Heap Sort Visualizer](https://www.cs.usfca.edu/~galles/visualization/HeapSort.html)

**Complexity:**
+ `MAX-HEAPIFY` takes $\Theta(n)$ time
+ $n$ calls to `POP-MAX` $O(\log{n})$ time but each call makes the heap smaller
+ Overall complexity: $O(n\log{n})$
	+ Best case $\Theta(n)$ when all items are equal
	+ Otherwise always takes $\Theta(n\log{n})$ time

## Summary
- **Binary heap**
    - A binary tree such that
        - The tree is **complete** (every level is full except the bottom, which is filled from left to right);
        - The key in any node is the largest/smallest in its subtree.
    - Usually encoded as an array rather than as a tree.
        - The array contains the items in level order.
    - Complexities (for a min-heap):
        - GET-MIN: $\Theta(1)$
        - POP-MIN: $O(\log{n})$
        - INSERT: $O(\log{n})$
        - HEAPIFY: $\Theta(n)$
            - (Turn an array in arbitrary order into a heap)
        - For a max-heap, replace MIN with MAX
- **HEAPSORT**
    - A sorting algorithm that uses heap operations!
        - Essentially, MAX-HEAPIFY then POP-MAX every item.
    - Sorts an array of arbitrary numbers in $O(n\log{n})$ time.
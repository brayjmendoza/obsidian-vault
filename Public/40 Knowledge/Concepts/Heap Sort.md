---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Heapsort
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Heap sort** sorts an array by turning it into a max-heap, then repeatedly moving the largest remaining item to the end of the array.

It uses [[Binary Heap|binary heap]] operations on the array itself, with no extra storage:

1. **MAX-HEAPIFY** the array, so it's a max-heap with the largest item at index $0$.
2. Then, $n$ times: take the maximum (GET-MAX), remove it from the heap (POP-MAX), and put it in the slot the heap just gave up at the end of the array. On the $i$th pass, that's index $n - i$.

Each POP-MAX shrinks the heap by one item, freeing the last slot of the heap's part of the array, which is exactly where the item just removed belongs. So the array is divided into a heap at the front and a sorted part at the back, and when the heap is empty, the whole array holds the items in order, smallest to largest.

```
HEAP-SORT(arr):
    MAX-HEAPIFY(arr)
    for (i = 1; i ≤ n; ++i)
        x = GET-MAX(arr)
        POP-MAX(arr)
        arr[n − i] = x      // this slot is no longer part of the heap
```

**Cost:** MAX-HEAPIFY takes $\Theta(n)$, and the $n$ POP-MAXes take $O(\log n)$ each, though the heap shrinks as they go. So heap sort takes $O(n \log n)$. In general, it takes $\Theta(n \log n)$. The exception is when all the items are equal: then no sift moves anything, and it takes $\Theta(n)$.

More generally, heap sort is one of the standard $O(n \log n)$ comparison sorts, beside merge sort and quicksort, and no comparison sort can do better in the worst case. Its strengths are a worst case of $O(n \log n)$, which quicksort lacks, and sorting in place, which merge sort doesn't. Its weaknesses are that it isn't **stable**, so equal items can change their relative order, and that it jumps around the array, which caches handle poorly, so quicksort is usually faster in practice. C++'s `std::sort` falls back on heap sort when quicksort recurses too deeply, an approach called introsort.

# Example

For illustration (an example not from the source), sorting `[3, 1, 2]`:

| Step | Array | Heap part |
|---|---|---|
| MAX-HEAPIFY | `[3, 1, 2]` | All three (already a max-heap) |
| Pop `3` into index 2 | `[2, 1, 3]` | `[2, 1]` |
| Pop `2` into index 1 | `[1, 2, 3]` | `[1]` |
| Pop `1` into index 0 | `[1, 2, 3]` | Empty |

Each pass takes the largest item left in the heap and puts it just after the heap's end, so the sorted part grows from the back. Popping `3` moved the last item, `2`, to the root, where it was already larger than its child `1`, so no sift was needed.

# Connections

- [[Binary Heap]]: heapify and pop-max, the operations heap sort uses
- [[Priority Queue]]: sorting by popping a priority queue's items in order
- [[Asymptotic Analysis]]: the $\Theta(n \log n)$ bound, and the $\Theta(n)$ best case

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

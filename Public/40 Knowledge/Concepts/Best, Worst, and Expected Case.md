---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Best Case
  - Worst Case
  - Expected Case
  - Average Case
  - Expected Time
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An algorithm's **best case**, **worst case**, and **expected case** are its cost on the cheapest inputs of a given size, on the most expensive, and on average over a stated probability distribution of inputs.

Two inputs of the same size $n$ can cost very different amounts, so "the cost of an algorithm" for size $n$ isn't one function until a case is chosen. Each case is then analyzed with [[Asymptotic Analysis|asymptotic analysis]], and the three can fall in different orders of complexity:

- **Best case:** the least the algorithm can cost on any input of size $n$.
- **Worst case:** the most it can cost. It's a guarantee, and it's what an analysis gives unless it says otherwise.
- **Expected case:** the average cost, weighted by how likely each input is. It depends on an assumption about the inputs (e.g., that every position is equally likely), which the analysis must state.

When the cases differ, a single tight bound can't describe the algorithm. $O$ of the worst case still holds for every input, so it's the usual summary: the algorithm is never worse than that. A $\Theta$ bound describes the algorithm in all cases only when they agree.

When the worst case is possible but vanishingly unlikely, the expected case is the more honest description: quoting the worst case alone would mislead. A randomized algorithm makes this precise by taking the randomness into its own hands, so the expected cost holds for every input rather than depending on an assumption about inputs (e.g., a randomized binary search tree).

More generally, "average case" is the usual name for the expected case over a distribution of inputs, and "expected" is used more for the average over an algorithm's own random choices. A fourth measure, the cost of a whole sequence of operations, is [[Amortized Analysis|amortized]] cost, which, unlike an expected case, is a guarantee with no probability involved.

# Examples

## Linear Search

Linear search checks each element of an array in turn for a value `x`:

```cpp
bool lookUp(float x, const float* arr, size_t arrSize) {
    for (size_t i = 0; i < arrSize; ++i) {
        if (arr[i] == x) {
            return true;   // Found it!
        }
    }
    return false;          // compared x to everything
}
```

- **Best case:** `x` is the first element, so one comparison: $\Theta(1)$.
- **Worst case:** `x` is last or absent, so $n$ comparisons: $\Theta(n)$.
- **Expected case:** if `x` is in the array and equally likely to be at each position, the average number of comparisons is $\frac{1 + 2 + \cdots + n}{n} = \frac{n + 1}{2}$, which is $\Theta(n)$.

The best case is a different order from the other two, so linear search as a whole is $O(n)$: never worse than linear, sometimes better.

# Connections

- [[Asymptotic Analysis]]: the notation each case is stated in
- [[Amortized Analysis]]: a bound on a sequence of operations, rather than on one input
- [[Randomized Binary Search Tree]]: where the worst case is possible but implausible, so the expected case describes it

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: reference
created: 2026-11-24
updated: 2026-11-24
topic: algorithms
---
The common orders of complexity and the asymptotic notations, for quick lookup. What they mean and how they're defined is in [[Asymptotic Analysis]].

# Orders of Complexity

From slowest-growing to fastest:

| Order | Name | Example |
|---|---|---|
| $\Theta(1)$ | Constant | Indexing an array |
| $\Theta(\log n)$ | Logarithmic | Binary search |
| $\Theta(n)$ | Linear | Linear search |
| $\Theta(n \log n)$ | Linearithmic | Merge sort, [[Heap Sort\|heap sort]] |
| $\Theta(n^2)$ | Quadratic | Bubble sort |
| $\Theta(n^3)$ | Cubic | Multiplying two $n \times n$ matrices the usual way |
| $\Theta(n^k)$, for some $k$ | Polynomial | Any of the above |
| $\Theta(k^n)$, for some $k > 1$ | Exponential | Subset sum, by trying every subset |
| $\Theta(n!)$ | Factorial | The traveling salesperson problem, by trying every route |
| $\Theta(n^n)$ | Super-exponential | Listing every function from an $n$-element set to itself |

# The Asymptotic Family

| Notation | In words | Like | Limit of $f(n)/g(n)$ |
|---|---|---|---|
| $f(n) \in o(g(n))$ | $f$ is definitely better than $g$ | $x < y$ | $0$ |
| $f(n) \in O(g(n))$ | $f$ is no worse than $g$ | $x \le y$ | Finite |
| $f(n) \in \Theta(g(n))$ | $f$ is similar to $g$ | $x = y$ | Finite and positive |
| $f(n) \in \Omega(g(n))$ | $f$ is no better than $g$ | $x \ge y$ | Positive, or $\infty$ |
| $f(n) \in \omega(g(n))$ | $f$ is definitely worse than $g$ | $x > y$ | $\infty$ |

**Mnemonic:** Charlie Chaplin jumping over a puddle under the full moon. From top to bottom: little $o$ is the moon, a strict upper bound. Big $O$ is Charlie's head, an upper bound. $\Theta$ is his body, both an upper and a lower bound. $\Omega$ is his legs, a lower bound. Little $\omega$ is the puddle, a strict lower bound.

# Quick Rules

- **Drop constant factors:** $5n^2 \in \Theta(n^2)$.
- **Keep only the fastest-growing term:** $n^2 + 100n + 10^6 \in \Theta(n^2)$.
- **Log bases don't matter:** $\log_2 n$ and $\log_{10} n$ differ by a constant factor, so both are $\Theta(\log n)$.
- **$O$ is an upper bound only:** linear search is $O(n)$, and also $O(n^2)$, but the tighter bound says more.

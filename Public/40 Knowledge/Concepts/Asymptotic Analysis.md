---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Asymptotic Complexity
  - Big O Notation
  - Big Theta
  - Big Omega
  - Little o
  - Little omega
  - Order of Complexity
  - Time Complexity
fields:
  - computer-science
  - math
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Asymptotic analysis** asks how the cost of an algorithm *scales* as the size of its input grows toward infinity.

It isn't about how long an algorithm takes on a particular input, or how many times it performs some operation. Cost is a function of the input size $n$ (usually the length of the input), and the analysis compares how such functions grow. Two simplifications follow:

- **Constant factors don't matter.** $n$, $0.00001n$, and $99999n$ all scale linearly, and $n^2$ and $99999n^2$ both scale quadratically.
- **Small terms don't matter.** For very large $n$, $n^2 + 100n + 1000000$ behaves like $n^2$, and $2^n + 500n^{10} + 1234567$ behaves like $2^n$.

At its core, asymptotic analysis compares two cost functions $f$ and $g$ through the limit of their ratio:

$$\lim_{n \to \infty} \frac{f(n)}{g(n)}$$

If the limit is $\infty$, $f$ grows faster, or **dominates**. If it's $0$, $g$ dominates. If it's a positive constant, neither does: they grow at the same rate.

## The Asymptotic Family

Each notation names a **set of functions**, defined by how they grow compared to $g$. When the limit exists:

| Notation | Holds when | In words | Like |
|---|---|---|---|
| $f(n) \in o(g(n))$ | $\lim_{n \to \infty} f(n)/g(n) = 0$ | $f$ is definitely better than $g$ | $x < y$ |
| $f(n) \in O(g(n))$ | $\lim_{n \to \infty} f(n)/g(n) < \infty$ | $f$ is no worse than $g$ | $x \le y$ |
| $f(n) \in \Theta(g(n))$ | $0 < \lim_{n \to \infty} f(n)/g(n) < \infty$ | $f$ is similar to $g$ | $x = y$ |
| $f(n) \in \Omega(g(n))$ | $\lim_{n \to \infty} f(n)/g(n) > 0$ | $f$ is no better than $g$ | $x \ge y$ |
| $f(n) \in \omega(g(n))$ | $\lim_{n \to \infty} f(n)/g(n) = \infty$ | $f$ is definitely worse than $g$ | $x > y$ |

"Better" means lower cost, so slower growth. Read from top to bottom, the notations go from a strict upper bound ($o$), through an upper bound ($O$), a tight bound ($\Theta$), and a lower bound ($\Omega$), to a strict lower bound ($\omega$). Two facts relate them:

- $f(n) \in O(g(n))$ exactly when $g(n) \in \Omega(f(n))$.
- $f(n) \in \Theta(g(n))$ exactly when $f(n) \in O(g(n))$ and $f(n) \in \Omega(g(n))$.

The $\Theta$ sets for particular choices of $g$ are the **orders of complexity**, and they don't overlap: $\Theta(1)$ (constant), $\Theta(\log n)$ (logarithmic), $\Theta(n)$ (linear), $\Theta(n \log n)$ (linearithmic), $\Theta(n^2)$ (quadratic), and so on up through exponential $\Theta(k^n)$ and factorial $\Theta(n!)$ (see [[Orders of Complexity]]).

An algorithm's cost often depends on which input of size $n$ it gets, not just on $n$, so an analysis states which case it describes (see [[Best, Worst, and Expected Case]]). $O$ is then the natural way to describe an algorithm over all its cases: "linear search is $O(n)$" says it's never worse than linear, though it can be better.

More generally, the notation comes from mathematics: Paul Bachmann introduced $O$ in 1894, Edmund Landau popularized it along with $o$, and Donald Knuth introduced $\Omega$ and $\Theta$ in their modern sense in 1976. The limit definitions above need the limit to exist. The standard definitions use constants instead, and cover every case: $f(n) \in O(g(n))$ when there are constants $c > 0$ and $n_0$ such that $f(n) \le c \cdot g(n)$ for all $n \ge n_0$, and $\Omega$ reverses the inequality. Writing $f(n) = O(g(n))$, with an equals sign, is common, though $f$ is a member of a set rather than equal to one.

# Examples

## Comparing Orders with a Limit

To compare $f(n) = 3n^2 + 100n$ with $g(n) = n^2$:

$$\lim_{n \to \infty} \frac{3n^2 + 100n}{n^2} = \lim_{n \to \infty} \left(3 + \frac{100}{n}\right) = 3$$

The limit is a positive constant, so $f(n) \in \Theta(n^2)$, and so also $O(n^2)$ and $\Omega(n^2)$. Compared with $n^3$ instead, the limit is $0$, so $f(n) \in o(n^3)$ and $O(n^3)$, but not $\Theta(n^3)$. The constant $3$ and the term $100n$ made no difference to which order $f$ is in.

# Connections

- [[Best, Worst, and Expected Case]]: which inputs an asymptotic bound describes
- [[Amortized Analysis]]: bounding the total cost of a sequence of operations instead of each one
- [[Orders of Complexity]]: the common orders, with names and examples
- [[Abstract Data Type]]: an interface can promise an operation's asymptotic cost
- [[Heap Sort]]: an $O(n \log n)$ sort whose best case is $\Theta(n)$

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

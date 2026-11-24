---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Amortized Time
  - Amortized Cost
  - Aggregate Method
  - Banker's Method
  - Physicist's Method
  - Potential Method
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Amortized analysis** bounds the total cost of a sequence of operations: when operations have a stated **amortized time**, the total time of all the operations performed so far is at most the sum of their amortized times.

It suits data structures whose operations are usually cheap but occasionally expensive, like a [[Dynamic Array|dynamic array]] that now and then copies everything into a bigger array. Stating only the worst-case time of each operation would mislead, since it overemphasizes the rare expensive ones. Amortized time is a kind of average over the sequence, but unlike an [[Best, Worst, and Expected Case|expected case]], it involves no probability: it's a guarantee about every sequence.

What the guarantee covers is exact:

- **It bounds totals, from the very beginning.** After any number $m$ of operations starting from an empty structure, the total cost so far is at most the sum of their amortized costs.
- **It doesn't bound any single operation.** One operation can cost far more than its amortized time, as long as the cheap ones before it have paid for it. An operation with $\Theta(1)$ amortized time can still take $\Theta(n)$ time on its own.

Three methods prove amortized bounds:

- **Aggregate method:** work out the total time for $m$ operations, and divide by $m$. It's only practical when the operations are essentially all the same kind.
- **Banker's method:** treat time like money. Charge each externally visible operation (e.g., adding an item) a fixed price, more than its actual cost when it's cheap, and save the surplus as credit. Then show that the saved credit always pays for the expensive internal work (e.g., copying the array) when it comes.
- **Physicist's method:** treat time like energy. Define a **potential function** mapping each state of the data structure to a number, its stored "potential energy." Cheap operations raise the potential, expensive ones spend it, and the proof shows there's always enough potential for each operation.

More generally, Robert Tarjan formalized amortized analysis in 1985. The banker's and physicist's methods are usually called the **accounting method** and the **potential method**. In the potential method, an operation's amortized cost is its actual cost plus the change in potential it causes, and if the potential starts at zero and never goes negative, the amortized costs bound the actual total. Splay trees and hash tables that resize are standard examples, besides dynamic arrays.

# Examples

## Doubling a Dynamic Array

A dynamic array doubles its capacity whenever it's full, at sizes 1, 2, 4, 8, and so on. Adding an item to the end costs $\Theta(1)$ when there's room, and $\Theta(n)$ when the array must be copied.

By the aggregate method, start from empty and add $m$ items. Each addition does $1$ unit of work to place its item, $m$ in all. The copies happen at sizes $1, 2, 4, \ldots$, up to at most $m$, and copy that many items each time, so they copy at most

$$1 + 2 + 4 + \cdots + 2^{\lfloor \log_2 m \rfloor} < 2m$$

items. The total is under $m + 2m = 3m$, which is $\Theta(m)$, so each addition is $\Theta(1)$ amortized time, though the occasional addition that copies takes $\Theta(n)$ on its own. Growing by a fixed amount instead of doubling breaks this: the copies then add up to $\Theta(m^2)$ (see the [[Dynamic Array#Growing by a Fixed Amount|example in Dynamic Array]]).

# Connections

- [[Dynamic Array]]: the standard case, with constant amortized time to add at the end
- [[Asymptotic Analysis]]: amortized bounds are stated in the same notation
- [[Best, Worst, and Expected Case]]: per-operation cases, which amortized analysis looks past
- [[Splay Tree]]: $O(\log n)$ amortized time per operation, though one operation can take $\Theta(n)$

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

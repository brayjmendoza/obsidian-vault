**Definition:** When operations have a specified _amortized time_, the total time of all the operations performed up until now is bounded by the sum of the amortized times of the individual operations

Amortized time is kind of like an "average" time
+ There is a specified *maximum* (e.g. by a certain point, only $m$ operations could have happened)
+ Note that at any specific point of time, more work cannot be down than the specified amortized time
	+ For constant amortized time, there is no point where we would end up doing $\Theta(n)$ work
	+ For $O(n)$ amortized time, we could do $\Theta(n)$ or $\Theta(1)$ work at a given step, but not $\Theta(n^2)$ or anything more

### Example: Array-backed List
Let's consider an array-backed list that resizes with every factor of 2 (i.e. when there are 1, 2, 4, 8, 16, etc. elements in the array).
+ In the best case (no resizing), we do $\Theta(1)$ work
+ In the worst case (resizing). we do $\Theta(n)$ work
+ After $m$ pushes, we will have done $\Theta(m) + \Theta(m) = \Theta(m)$  work
	+ $\Theta(1)$ for $m$ pushes and and additional $m$ inserts when resizing
+ Therefore, a single push is $\Theta(1)$ amortized time
	+ After $m$ pushes, we have done at most $\Theta(m)$ work
		+ Averages out to $\Theta(1)$ work per push or $\Theta(1)$ amortized time


# Ways to Prove Amortized Bounds
### Aggregate Method
Work out the time for 𝑚 operations and divide by 𝑚 
+ This approach is really only practical if all the operations are essentially the same
+ We can use other approaches when we have a mix of different operations to deal with

### Banker's Method
In this method we treat time like money, and assign a charge for each externally visible action (e.g. pushing to the back of an array-backed list)
+ We use this charge to set aside money to pay for internal operations (e.g. resizing)
+ The goal is to show that if we need to do many operations at some point in the future, we'll have to set aside enough money to pay for them

### Physicist's Method
In this method, we treat time like energy
+ We want to show that there's a *potential function* that maps situations to numbers representing the "potential energy" in that situation
+ Some operations use energy and some increase energy
	+ We can prove that there is always enough energy in the system to perform each operation

# Main Points
+ Amortized time is useful when we have a data structure where operations are usually quite cheap to perform, but _occasionally_ we need to do something expensive (like copying a large array)
	+ Just stating the worst-case time _per operation_ would be misleading (overemphasizes the rare expensive operations)
+ Amortized time promises that the worst-case time of a sequence of operations is bounded by the sum of the amortized times of the individual operations.
    - Only applies to the total time of the sequence of operations from the very beginning
    - Think of amortized time as an rare **upper bound**

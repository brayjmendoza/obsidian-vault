# Overview
**Asymptotic analysis** asks the question "How does the cost of the algorithm _scale_ as input sizes grow toward infinity?"
+ NOT about figuring out how much time the algorithm will take on a specific input
+ NOT about  how many occurrences of a particular operation it will perform


Only care about how costs *grow* not specific values (so we don't care about factors or coefficients)
- $n$, 0.00001$n$, and 99999$n$ all scale _linearly_
- $n^2$, 0.00001$n^2$, and 99999$n^2$ all scale _quadratically_


It's about _arbitrarily huge_ inputs, not specific input sizes (so we don't care about "small" terms)
- $n^2$+100$n$+1000000 $\approx$ $n^2$ for very large $n$
- $2^n$+500$n^{10}$+6000$n^5$+1234567 $\approx$ $2^n$ for very large $n$

Though technically $n$ could represent anything, it typically refers to the length of an input

At it's core, asymptotic analysis is a comparison of cost functions. To make this comparison, we focus on the quantity
 $\displaystyle \lim_{n\to\infty} \dfrac{f(n)}{g(n)}$ 
+ If the limit goes to $\infty$, then $f(n)$ dominates
+ If the limit goes to 0, then $g(n)$ dominates
+ If the limit ends up as a ratio (not 0 or $\infty$), then neither dominate

# Big $\Theta$
For a function $g(n)$, $\Theta(g(n))$ is a *set of functions* – all functions $f$ that grow at a similar rate as $g$ as $n\to\infty$.

Mathematically,
$\displaystyle f(n) \in \Theta(g(n)) \textrm{ if and only if } 0 <\lim_{n\to\infty} \dfrac{f(n)}{g(n)} < \infty$

## Orders of Complexity
$\Theta(g(n))$ is a *set of functions*. There are particular sets known as **orders of complexity** that are defined by different choices for $g(n)$
+ Note that these sets don't overlap

Some examples:
![[OrdersOfComplexity.png]]More examples [here](https://en.wikipedia.org/wiki/Time_complexity)

# Big $O$
For a function $g(n)$, $O(g(n))$ is a *set of functions* – all functions $f$ that grow more slowly or at a similar rate as $g$ as $n\to\infty$.

Mathematically, 
$\displaystyle f(n) \in O(g(n)) \textrm{ if and only if } \lim_{n\to\infty} \dfrac{f(n)}{g(n)} < \infty$

Whereas $f(n) \in\Theta(g(n))$ means "$f$ is similar to $g$", $f(n) \in O(g(n))$ means "$f$ is no worse than $g$"

In general Big $O$ tells us that a function is *no worse than* something. For example, it could be linear time, but in some cases it could be better

# Big $\Omega$
For a function $g(n)$, $\Omega(g(n))$ is a *set of functions* – all functions $f$ that grow faster than or at a similar rate as $g$ as $n\to\infty$.

Mathematically, 
$\displaystyle f(n) \in \Omega(g(n)) \textrm{ if and only if } \lim_{n\to\infty} \dfrac{f(n)}{g(n)} > \infty$

Whereas $f(n) \in\Omega(g(n))$ means "$f$ is no worse than $g$", $f(n) \in\Omega(g(n))$ means "$f$ is no better than $g$"

# Useful Facts
- If $f(n) \in O(g(n))$, then $g(n) \in\Omega(f(n))$ and vice versa
- If $f(n) \in O(g(n))$, and $f(n) \in\Omega(g(n))$, then $f(n)\in\Theta(g(n))$ and vice versa

# The Whole Asymptotic Family
![[AsympototicFamily.png]]

A handy mnemonic to remember the order of the different class is "Charlie Chaplin jumping over a puddle under the full moon":
![[charliechapman.png]]
In the Charlie Chaplin picture, the complexity symbols are ordered from top (strict upper bound) to bottom (strict lower bound):
- Little $o$, at the very top, is the full moon. It represents a strict upper bound on our function.
- Big $O$ is next. It's Charlie Chaplin's head, and represents a (not necessarily strict) upper bound on our function.
- Big $\Theta$ is Charlie's body, and represents an upper and lower bound on our function.
- Big $\Omega$ is Charlie's legs, and represents a (not necessarily strict) lower bound on our function.
- Little $\omega$ is at the bottom, as the puddle that Charlie is jumping over. It represents a strict lower bound on our function.
## Example: Linear Search
Given an array of `n` numbers, we want to determine if a given number `x` is in the array or not
```
bool lookUp(float x, float* arr, size_t arrSize) {
    for (size_t i = 0; i < arrSize; ++i) {
        if (arr[i] == x) {
            return true; // Found it!
        }
    }
    return false; // If we are here, we've compared x to everything in the array
}
```
+ Best-case complexity: $\Theta(1)$
+ Worst-case complexity: $\Theta(n)$
+ Expected-case complexity: $\Theta(n)$
	+ Assuming it's equally likely to find `x` in any location
	+ Doing the math, the expected number of numbers we check is $\dfrac{n+1}{2} \in \Theta(n)$

So,
+ Depending on the input it could have a completely different order of complexity
+ Big $O$ tells us that the complexity of linear search is *never worse than linear*
	+ Big $O$ tells us that linear search is at worse linear time (but it could be better in some cases)
	+ Big $\Theta$ tells us that no matter what it's always a given complexity

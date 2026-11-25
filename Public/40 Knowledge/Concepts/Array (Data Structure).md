---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Array
  - Primitive Array
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An **array** is a fixed number of values of one type, stored one after another in memory and reached by position.

A primitive array has four properties:

- **Contiguous:** its elements sit together in memory, with no gaps.
- **Ordered:** its elements have a clear order, so there's a first element and a forty-second.
- **Homogeneous:** every element has the same type.
- **Fixed-size:** once created, it can't change how many elements it holds.

Together these make indexing fast. Element $i$ is at the array's starting address plus $i$ times the size of one element, so reaching any element takes the same constant time, whatever $i$ is. In C++, `a[i]` and `*(a + i)` mean the same thing, and the array's name, used as a value, gives the address of its first element (see [[Pointer (Programming Languages)]]). Indices run from $0$ to $n - 1$. Nothing checks them: indexing outside that range is [[Undefined Behavior|undefined behavior]].

A local array lives on the stack, so the compiler must know its size: in C++, the size must be a compile-time constant, like a literal or a `constexpr` variable. An array whose size is known only at run time goes on the heap (see [[Dynamic Memory Allocation]]). Either way, its size is fixed once it's made. To grow, a program allocates a bigger array and copies the elements over, which is what a resizable list does behind the scenes.

More generally, most languages build their resizable lists on arrays (e.g., C++'s `std::vector`, Java's `ArrayList`, and Python's `list`), and many check every index, raising an error instead of reading past the end. Contiguity also makes arrays fast in practice: scanning one reads memory in order, which is what processor caches are built for.

# Examples

## Declaring and Initializing Arrays

```cpp
int values[42];                   // 42 ints, indeterminate values
int oneTwoThree[3] = {1, 2, 3};
int fourFiveSix[3]{4, 5, 6};
int a[5]{1, 2};                   // {1, 2, 0, 0, 0}: the rest are zeroed

size_t n = 3;
int bad[n];                       // error: n isn't a compile-time constant
constexpr size_t N = 3;
int good[N];                      // fine
```

With braces, any elements without a value are zero-initialized, so `a` holds `{1, 2, 0, 0, 0}`, and an array of pointers given `{}` holds null pointers. `bad` fails because a stack array's size must be known when the program is compiled, and `n` is an ordinary variable, whose value exists only once the program runs. `good` works because `constexpr` promises `N` is known at compile time and never changes.

# Connections

- [[Pointer (Programming Languages)]]: an array's name decays to a pointer, and pointer arithmetic moves through it
- [[Dynamic Memory Allocation]]: arrays whose size is chosen at run time
- [[Object Lifetime]]: each element goes through every phase, in order
- [[Undefined Behavior]]: indexing outside the array
- [[Dynamic Array]]: an array that grows, by copying into a bigger one
- [[Asymptotic Analysis]]: indexing an array takes $\Theta(1)$ time, whatever the index
- [[Binary Heap]]: a tree stored in an array, with children found by index arithmetic

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

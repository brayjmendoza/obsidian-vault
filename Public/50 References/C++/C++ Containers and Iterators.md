---
type: reference
created: 2026-11-24
updated: 2026-11-24
topic: c++
---
`std::vector`, `std::list`, and how to iterate over them. The ideas are in [[Dynamic Array]], [[Linked List]], and [[Iterator]].

# `std::vector`

A [[Dynamic Array|dynamic array]]. Needs `#include <vector>`.

| Code | Gives |
|---|---|
| `std::vector<double> v;` | An empty vector |
| `std::vector<double> v(100);` | 100 elements, all `0.0` |
| `std::vector<int> v{42, 54, 7};` | Three elements: 42, 54, and 7 |

| Member function | Does |
|---|---|
| `size()` | How many elements it holds |
| `capacity()` | How many fit in the array underneath before it must grow |
| `reserve(n)` | Makes room for at least `n` elements now |
| `shrink_to_fit()` | Gives back the spare capacity |
| `push_back(x)` | Adds `x` at the end, growing if needed (amortized constant time) |
| `pop_back()` | Removes the last element, without returning it |
| `front()`, `back()` | References to the first and last elements (e.g., `v.back() = 7.3;`) |
| `v[i]` | Element `i`, unchecked |
| `at(i)` | Element `i`, checked: throws `std::out_of_range` if `i >= size()` |
| `insert(iter, x)` | Inserts `x` before `iter`, shifting the rest |
| `erase(iter)` | Removes the element at `iter`, returning an iterator to the next one |
| `begin()`, `end()` | Iterators to the first element and past the end |
| `swap(other)` | Swaps the contents of two vectors, in constant time |

Pushing a value of another type uses the usual promotions and conversions (see [[Type Conversion]]).

# `std::list`

A doubly [[Linked List|linked list]]. Needs `#include <list>`. Created like a vector, with `push_back`, `pop_back`, `front`, `back`, `insert`, and `erase`, plus:

| Member function | Does |
|---|---|
| `push_front(x)`, `pop_front()` | Adds or removes at the front, in constant time |

No `[]` or `capacity()`: reach elements by walking an iterator, which can move forward (`++`) or back (`--`) one node at a time.

# Iterating

| Loop | Use when |
|---|---|
| `for (double x : v)` | Reading each element, as a copy |
| `for (const auto& x : v)` | Reading each element without copying it |
| `for (double& x : v)` | Changing each element in place |
| `for (auto i = v.begin(); i != v.end(); ++i)` | You need the iterator itself (e.g., to `erase`) |

The range-based `for` loop is shorthand for the iterator loop (see [[Syntactic Sugar]]).

| Iterator | `*i` gives |
|---|---|
| `std::vector<double>::iterator` | A reference you can read and write |
| `std::vector<double>::const_iterator` | A `const` reference, read-only |

# Iterator Rules

- Never `*` or `++` the past-the-end iterator, and never `--` the first.
- Never compare iterators from different containers.
- After `i = c.erase(i);`, `i` is at the element after the erased one.

| Operation | Invalidates, for `std::vector` | Invalidates, for `std::list` |
|---|---|---|
| Growing past capacity | Every iterator | Nothing |
| `insert` | Iterators at or after the position (all of them if it grows) | Nothing |
| `erase` | Iterators at or after the position | Iterators at the erased element |
| Destroying the container | Every iterator | Every iterator |

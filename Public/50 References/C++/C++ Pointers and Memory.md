---
type: reference
created: 2026-11-23
updated: 2026-11-23
topic: c++
---
C++ syntax for arrays, pointers, references, and the heap. The ideas behind them are in [[Array (Data Structure)]], [[Pointer (Programming Languages)]], [[Reference (Programming Languages)]], and [[Dynamic Memory Allocation]].

# `*` and `&`

Both symbols mean one thing in a type and another in a value:

| Symbol | In a type | In a value |
|---|---|---|
| `&` | Reference to (used a lot), as in `int& r = x;` | Address-of (rarely needed), as in `&x` |
| `*` | Pointer to, as in `int* p = &x;` | Indirection: the object at an address, as in `*p` |

`*&x` is `x`. To reach a member through a pointer, write `p->name_`, which means `(*p).name_`.

# Arrays

| Code | Does |
|---|---|
| `int values[42];` | 42 `int`s with indeterminate values |
| `int v[3] = {1, 2, 3};` or `int v[3]{1, 2, 3};` | Three `int`s with given values |
| `int a[5]{1, 2};` | `{1, 2, 0, 0, 0}`: missing values are zeroed |
| `Elephant* herd[10]{};` | Ten null pointers |
| `int values[];` | Error: the size is required |
| `int values[n];` | Error, unless `n` is `constexpr` |
| `a[i]` or `*(a + i)` | Element `i`, with no bounds check |
| `std::begin(a)`, `std::end(a)` | Pointers to the first element and past the end |

# Pointers

| Code | Does |
|---|---|
| `float* p = &x;` | `p` points to `x` |
| `float* p = nullptr;` | `p` points nowhere, on purpose |
| `if (p != nullptr)` | Checks before following `p` |
| `p + i`, `++p` | Moves `p` by `i` elements, or by one |
| `p < q`, `p != q` | Compares positions in the same array |

Where `const` goes in a pointer type is in [[Reading C++ Declarations]].

Loop over a range with a pointer to the start and a past-the-end pointer:

```c++
for (const float* p = first; p != pastEnd; ++p) {
    std::cout << *p << std::endl;
}
```

Never dereference the past-the-end pointer, and remember that `first == pastEnd` means the range is empty.

# References

| Code | Does |
|---|---|
| `int& r = x;` | `r` is another name for `x`, for good |
| `const int& r = x;` | `r` can read `x` but not change it |
| `void f(Cow& c)` | `f` can change the caller's `Cow` |
| `void f(const Cow& c)` | `f` reads the caller's `Cow` without copying it |
| `void f(Cow c)` | `f` gets its own copy |

A non-`const` reference can't refer to a `const` variable or to a temporary (e.g., `x + y`).

# The Heap

| Code | Does |
|---|---|
| `int* p = new int{42};` | Puts an `int` holding 42 on the heap |
| `delete p;` | Destroys and frees it. `p` still holds the old address |
| `int* a = new int[n];` | An array of `n` `int`s, where `n` can be any variable |
| `delete[] a;` | Destroys and frees the whole array |

- **One `delete` for every `new`,** and `delete[]` for every `new[]`. Never mix them.
- **Set a deleted pointer to `nullptr`** if it's still in use, so it doesn't dangle.
- **Check with Valgrind** (`valgrind ./prog`) for leaks and bad memory accesses.

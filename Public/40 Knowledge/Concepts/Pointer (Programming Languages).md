---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Pointer
  - Null Pointer
  - Dereference
  - Indirection
  - Pointer Arithmetic
  - Past-the-End Pointer
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **pointer** is a value that holds the memory address of an object, so the object can be reached through it.

In C++, a pointer's type says what it points to: `float* start` declares `start` as a pointer to a `float`, a memory address where a `float` will be found. Two operators move between objects and their addresses:

- **Address-of** (`&x`): gives a pointer to `x`, its address.
- **Indirection**, or **dereferencing** (`*p`): gives the object that `p` points to, which can be read or assigned to (e.g., `*p = 7.8;`).

The two cancel out: `*&x` is `x`. The same symbols mean something else in a type: there, `*` means "pointer to," and `&` means "reference to" (see [[Reference (Programming Languages)]]). To reach a member of an object through a pointer, `p->name_` is shorthand for `(*p).name_`.

A pointer is a primitive type, so it has three properties that follow from that:

- **A default-initialized pointer is invalid.** It holds an indeterminate address, and following it is [[Undefined Behavior|undefined behavior]] (see [[Initialization (Programming Languages)]]).
- **Destroying a pointer does nothing to what it points to.** The pointer's [[Object Lifetime|lifetime]] and its target's are independent.
- **A pointer can point nowhere on purpose.** The special value `nullptr` means "not a valid address," and a pointer holding it is a **null pointer**. It gives code something to check before following a pointer, and following one is undefined behavior, which in practice usually crashes the program with a [[Segmentation Fault|segmentation fault]].

## Pointer Arithmetic

Since an [[Array (Data Structure)|array]]'s elements sit next to each other in memory, adding an integer to a pointer into an array moves it that many elements, not bytes. An array's name **decays** to a pointer to its first element, so for an array `vals` of $N$ elements:

- `vals + 0` points to the first element, and `*(vals + i)` is the same as `vals[i]`.
- `vals + N - 1` points to the last element.
- `vals + N` is the **past-the-end pointer**, just beyond the last element. It's valid to compute and compare with, but not to dereference.

A pair of pointers, one to the first element and one past the end, describes a whole range without knowing its length: a loop starts at the first and stops when it reaches the second. This makes a pointer the simplest kind of iterator.

Pointers also save copying. To reorder large objects, a program can sort an array of pointers to them instead, so each swap moves an address rather than a whole object.

More generally, a pointer is an explicit **indirection**, and most languages hide it: in Java and Python, every variable that holds an object holds a hidden pointer to it, with no address-of operator and no arithmetic, and following `null` or `None` raises an error instead of causing undefined behavior. Tony Hoare, who added the null reference to ALGOL W in 1965, later called it his "billion-dollar mistake." Many newer languages (e.g., Rust, Swift, and Kotlin) make a possibly missing value part of its type instead (see [[Option Type]]).

# Examples

## Normalizing an Array

`normalize` scales an array's values so the largest becomes `newmax`, given a pointer to the first value and a past-the-end pointer:

```c++
void normalize(float newmax, float* firstValPtr, float* pastEndPtr) {
    float maxval = *firstValPtr;
    for (float* p = firstValPtr; p < pastEndPtr; ++p) {
        if (*p > maxval) {
            maxval = *p;
        }
    }
    for (float* q = firstValPtr; q < pastEndPtr; ++q) {
        *q = *q / maxval * newmax;
    }
}

normalize(height, vals, vals + TEMPERATURE_SAMPLE_COUNT);
```

It has a bug: for an empty range, `firstValPtr` equals `pastEndPtr`, so the first line dereferences a past-the-end pointer, which is undefined behavior. A range of one element is fine, since `firstValPtr` then points to that element. (If every value is zero, dividing by `maxval` is a separate problem.)

# Connections

- [[Reference (Programming Languages)]]: another name for an object, which unlike a pointer can't be null or point elsewhere
- [[Array (Data Structure)]]: why pointer arithmetic works, and what past-the-end means
- [[Dynamic Memory Allocation]]: `new` returns a pointer, the only way to reach a heap object
- [[Const-Correctness]]: a pointer to `const` can read its target but not change it
- [[Undefined Behavior]]: following an invalid, null, or past-the-end pointer
- [[Option Type]]: making "no value" explicit in the type, instead of a null pointer
- [[Iterator]]: a pointer into an array is the simplest iterator

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Iterators
  - Iterator Invalidation
  - Past-the-End Iterator
  - const_iterator
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An **iterator** is an object that represents the location of one item in a collection, and can be moved to visit and access every item in turn.

Every iterator, in any language, supports four abstract operations:

- **BEGIN(*data*):** start an iterator at the first item of *data*.
- **NEXT(*iter*):** move the iterator forward to the next item.
- **FETCH(*iter*):** access the item the iterator is at.
- **IS-DONE(*iter*):** tell whether the iterator has passed the last item.

So code that uses only an iterator can walk through an array, a linked list, or a tree alike, without knowing how the collection is stored: the iterator is the collection's interface for traversal (see [[Abstract Data Type]]).

In C++, an iterator is any type that supports this loop:

```cpp
for (auto i = c.begin(); i != c.end(); ++i) {
    ... *i ...
}
```

`c.begin()` gives an iterator at the first item, `++i` moves it to the next, `*i` gives a reference to the item it's at, and `i != c.end()` checks whether it has run off the end. `end()` gives a **past-the-end** iterator, one step beyond the last item, that marks where to stop, so a container `c` is empty exactly when `c.begin() == c.end()`. Iterators usually support `==` and `->` too. A [[Pointer (Programming Languages)|pointer]] into an array is the simplest iterator, but most iterators aren't pointers: an iterator for a linked list or a tree has to follow links between nodes.

An iterator that only reads is a separate type, not a `const` one. A `const` iterator couldn't move, since `++` changes it. So containers provide a second iterator class, `const_iterator`, whose `*` gives a `const` reference to the item, and `auto` picks it when the container is `const`.

## Iterator Rules

Breaking any of these is [[Undefined Behavior|undefined behavior]]:

- Don't use `*` or `++` on a past-the-end iterator.
- Don't use `--` on an iterator at the beginning: there's no before-the-beginning.
- Don't compare iterators from different containers.
- Don't do anything with an invalid iterator except destroy it or assign it a new value.

An iterator becomes **invalid** when using it could no longer reach the item it referred to. Destroying a container invalidates all its iterators, and erasing an item invalidates every iterator at that item. Whether other changes invalidate iterators depends on how the container stores its items:

- **Array-backed containers** (e.g., `std::vector`): growing past the array's capacity moves every item to a new array, invalidating every iterator. Inserting or erasing an item shifts the items after it, invalidating iterators from that position on.
- **Linked containers** (e.g., `std::list`): inserting leaves every iterator valid, since no existing node moves, and erasing invalidates only iterators at the erased item.

So an interface must say which operations invalidate iterators, and documentation warns of it.

More generally, other languages build iteration into their loops: Python's `for` calls `iter` and `next` and stops at a `StopIteration` exception, and Java's `Iterator` has `hasNext` and `next`. C++'s pair-of-iterators style, from Alexander Stepanov's Standard Template Library, lets algorithms like `std::sort` and `std::find` work on any container's range. C++ also has categories of iterator by what they can do: a **forward** iterator only moves ahead, a **bidirectional** iterator can also move back with `--`, and a **random-access** iterator can jump any distance, as a pointer can.

# Examples

## Erasing while Iterating

Erasing items while iterating needs care, since `erase` invalidates the iterator passed to it. In the C++ standard library, `erase` returns an iterator to the item after the erased one, so a loop continues from there:

```cpp
std::list<int> values{1, 2, 3, 4};
for (auto i = values.begin(); i != values.end(); ) {
    if (*i % 2 == 0) {
        i = values.erase(i);   // i was invalidated; continue from the next item
    } else {
        ++i;
    }
}
// values is now {1, 3}
```

Writing `values.erase(i); ++i;` instead would apply `++` to an invalid iterator, which is undefined behavior.

# Connections

- [[Pointer (Programming Languages)]]: the simplest iterator, and the model for C++'s
- [[Abstract Data Type]]: an iterator is a container's interface for traversal
- [[Linked List]]: iterators that follow links, and stay valid through insertions
- [[Dynamic Array]]: iterators that resizing invalidates
- [[Syntactic Sugar]]: C++'s range-based `for` is sugar for an iterator loop
- [[Undefined Behavior]]: what breaking an iterator rule causes

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

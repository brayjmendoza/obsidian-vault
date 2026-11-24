---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Multiset (Abstract Data Type)
  - Bag (Abstract Data Type)
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **set** is a collection of unique keys, not necessarily in any order, supporting insertion, lookup, and removal of any key.

Lookup answers whether a key is in the set. Inserting a key that's already there changes nothing, since each key appears at most once. A **multiset**, or **bag**, is a set that allows duplicate keys, and so can also say how many times a key appears.

A set is an [[Associative Array|associative data structure]], like a map with keys but no values, and is encoded the same ways: with a [[Binary Search Tree|binary search tree]], which keeps keys in order, or a hash table, which doesn't.

More generally, the abstract data type follows the mathematical set, where membership is all that matters, and many languages add operations like union and intersection. Python's `set`, Java's `Set` interface, and C++'s `std::set` (a balanced binary search tree) and `std::unordered_set` (a hash table) all implement it, and C++ has `std::multiset` for multisets.

# Example

For illustration (an example not from the source), counting the distinct words in a text:

```python
words = "the cat saw the dog".split()
distinct = set(words)
print(len(distinct))   # 4: the, cat, saw, dog
```

Adding `"the"` a second time changed nothing, so the set holds four words. A multiset of the same words would hold five, with `"the"` counted twice.

# Connections

- [[Associative Array]]: a map is a set whose keys carry values
- [[List (Abstract Data Type)]]: a list keeps duplicates and order, where a set keeps neither
- [[Abstract Data Type]]: a set is defined by insert, lookup, and remove
- [[Binary Search Tree]]: the usual ordered encoding

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

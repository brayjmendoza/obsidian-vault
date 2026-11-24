---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Map (Abstract Data Type)
  - Dictionary (Abstract Data Type)
  - Multimap
  - Associative Container
  - Symbol Table
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An **associative array**, or **map**, is a collection that associates unique keys with values, so a value can be looked up by its key.

A map supports looking up the value associated with a key, inserting a key and value, and removing a key with its value. Keys are unique, but values needn't be: two keys can map to the same value. A **multimap** allows duplicate keys too, each with its own value.

Maps are **associative data structures**, as are sets (see [[Set (Abstract Data Type)]]). They're good at searching for a particular item, by its key, but not always good at keeping track of the order of things: a map promises nothing about the order of its keys unless its interface says so. That's the reverse of a linear data structure (see [[List (Abstract Data Type)]]).

Associative data structures are usually encoded with **[[Binary Search Tree|binary search trees]]**, which keep keys in sorted order and find one in time proportional to the tree's height, or with **hash tables**, which find one in constant expected time but keep no order.

More generally, every major language provides maps: Python's `dict`, Java's `Map` interface (with `HashMap` and `TreeMap`), and C++'s `std::map` (a balanced binary search tree) and `std::unordered_map` (a hash table). In compilers, a map from names to what they mean is a **symbol table**, much like an interpreter's environment (see [[Environment (Programming Languages)]]).

# Example

For illustration (an example not from the source), a phone book in Python, a `dict`:

```python
phone = {"Ada": "555-0101", "Grace": "555-0102"}
phone["Alan"] = "555-0103"   # insert
print(phone["Grace"])        # lookup: 555-0102
del phone["Ada"]             # remove
```

Each operation goes straight to the key it names, with no scan through the other entries. Inserting `"Grace"` again would replace her number rather than add a second entry, since keys are unique.

# Connections

- [[Set (Abstract Data Type)]]: the other associative structure, keys without values
- [[List (Abstract Data Type)]]: the linear counterpart, good at order rather than search
- [[Environment (Programming Languages)]]: a map from variable names to values
- [[Abstract Data Type]]: a map is defined by lookup, insert, and remove, whatever stores it
- [[Binary Search Tree]]: an ordered encoding, with lookup in time proportional to its height
- [[Red-Black Tree]]: what most standard libraries' ordered maps use

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

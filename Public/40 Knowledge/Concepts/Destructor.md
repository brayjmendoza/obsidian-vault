---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Destructors
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **destructor** is a special member function that runs automatically when an object of a class is destroyed, to clean up what the object holds.

Destruction is the fourth phase of an object's lifetime (see [[Object Lifetime]]), and for an object of class type it runs the destructor. In C++, a destructor is named for its class with a tilde (e.g., `~Cow()`), and takes no arguments. It runs whenever an object is destroyed, whether at the end of a block, by `delete`, or as part of destroying a larger object that contains it.

If a class doesn't declare a destructor, the compiler synthesizes one, which destroys each member variable. Writing `~Cow() = default;` asks for it explicitly. A destructor could be declared `= delete`, but that's a mistake: every object is destroyed at some point, so an object of such a class could hardly be used.

The synthesized destructor destroys only the members themselves. A member that's a pointer to heap memory is just a primitive value, so destroying it leaves its target in place (see [[Pointer (Programming Languages)]]). So a class that allocates heap memory must write its own destructor and `delete` that memory there, or every object leaks it (see [[Dynamic Memory Allocation]]). The destructor is how a class carries out [[Ownership (Memory Management)|ownership]]: the object owns its heap memory, and its destruction frees it.

More generally, deleting what an object owns in its destructor is the heart of the C++ idiom RAII, and the **rule of three** says a class that needs a custom destructor almost always needs a custom copy constructor and assignment operator too, since copying would otherwise create two owners of the same memory (see [[Deep and Shallow Copy]]). Languages with garbage collection have no destructors in this sense: Java's finalizers and Python's `__del__` run at no guaranteed time, so those languages release resources like files with explicit constructs instead (e.g., Python's `with`).

# Examples

## A Barn's Destructor

A `Barn` holds an array of pointers to cows, `residentCows_`, with the array and every cow on the heap. Its destructor deletes each cow, then the array:

```c++
Barn::~Barn() {
    for (size_t i = 0; i < cowCount_; ++i) {
        delete residentCows_[i];
    }
    delete[] residentCows_;
}
```

The order matters: the cows are reached through the array, so the array must still exist while they're deleted. With the synthesized destructor instead, destroying a `Barn` would destroy only the pointer `residentCows_` and the two counts, leaking the array and every cow.

# Connections

- [[Constructor (Object-Oriented Programming)]]: the counterpart that starts an object's lifetime
- [[Object Lifetime]]: destruction is its fourth phase
- [[Ownership (Memory Management)]]: an owner deletes what it owns in its destructor
- [[Dynamic Memory Allocation]]: what a destructor must free, since the synthesized one doesn't
- [[Deep and Shallow Copy]]: a class with a custom destructor needs custom copying too

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

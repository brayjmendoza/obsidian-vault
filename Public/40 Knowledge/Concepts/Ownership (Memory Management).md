---
type: concept
created: 2026-11-23
updated: 2026-11-23
aliases:
  - Ownership
  - Principle of Ownership
  - RAII
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
The **principle of ownership** says that every object on the heap has a single **owner**, responsible for its lifetime: for creating it and, above all, for destroying it.

Heap memory isn't freed automatically (see [[Dynamic Memory Allocation]]), so a program must decide, for every object it allocates, which piece of code will delete it. When nobody does, the object leaks. When two pieces of code each think they're responsible, the second deletes memory the first already freed, and any pointer the first left behind dangles. Giving each object exactly one owner answers the question once: the owner deletes it, and everything else may use it but never deletes it.

An owner is usually an object whose [[Object Lifetime|lifetime]] is managed automatically, such as a local variable or a class instance that holds pointers to heap memory. When the owner is destroyed, it deletes what it owns, so the heap object's lifetime ends with its owner's. Copying an owner needs care: copying only its pointers would leave two owners of the same heap objects, which breaks the principle.

More generally, tying a resource's release to an owner's destruction is the C++ idiom called **RAII** ("resource acquisition is initialization"), and it applies to any resource that must be released, such as files and locks, not just memory. The standard library's smart pointers encode ownership in types: a `std::unique_ptr` is a sole owner that deletes its object when destroyed, and `std::shared_ptr` allows shared ownership, deleting the object when its last owner goes. Rust builds ownership into the language itself, so the compiler rejects code that would leak, dangle, or delete twice.

# Example

For illustration (an example not from the source), a `Barn` owns the heap array of cows it allocates, and nothing else deletes it:

```c++
void visit() {
    Barn barn{10};   // barn's constructor allocates its array of cows with new[]
    barn.addCow(Cow{3, 12});
    // ...
}                    // barn is destroyed here, and deletes the array it owns
```

The array lives exactly as long as `barn`, a local variable, though the array itself is on the heap. Code that borrows a pointer to one of the cows may use it while `barn` exists, but must never delete it: only the owner does.

# Connections

- [[Dynamic Memory Allocation]]: the leaks, dangling pointers, and double deletes ownership prevents
- [[Object Lifetime]]: an owned object's lifetime ends with its owner's
- [[Pointer (Programming Languages)]]: other code reaches an owned object through pointers that don't own it
- [[Destructor]]: where an owner deletes what it owns
- [[Deep and Shallow Copy]]: copying an owner must copy what it owns, or create two owners

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

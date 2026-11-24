---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Heap Memory
  - Dynamic Allocation
  - Memory Leak
  - Dangling Pointer
  - Double Delete
  - Double Free
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Dynamic memory allocation** gets memory for an object while a program runs, from a region called the **heap**, and keeps it until the program explicitly gives it back.

Memory for a local variable is allocated and deallocated automatically, when its function begins and ends (see [[Object Lifetime]]). That ties the variable to its function, and its size must be known at compile time. Heap memory has neither limit: the program decides at run time how much to allocate and when, and an object on the heap outlives the function that created it.

In C++, `new` allocates on the heap:

1. It **allocates** space on the heap for an object of the given type.
2. It **initializes** that object as specified.
3. It **returns** a [[Pointer (Programming Languages)|pointer]] to the object, the only way to reach it.

So `int* p = new int{42};` puts an `int` holding 42 on the heap, and the pointer `p`, a local variable, on the stack. `delete p` does the reverse: it destroys the object `p` points to and deallocates its memory. Arrays use `new int[n]` and `delete[]`, and since the size is chosen at run time, `n` doesn't need to be a compile-time constant. Every `new` needs exactly one matching `delete`.

Three mistakes come from getting that wrong:

- **Memory leak:** losing every pointer to a heap object before deleting it. The memory can't be reached or freed, and stays occupied until the program ends.
- **Dangling pointer:** a pointer to memory that's been deallocated. `delete` changes nothing about the pointer it's given, so afterward the pointer still holds the old address. Following it is [[Undefined Behavior|undefined behavior]], and the bug is hard to find, since the old data may stay in place, and look correct, until the memory is reused.
- **Double delete:** deleting the same memory twice, through a dangling pointer. It usually crashes the program.

The usual guard against all three is to give every heap object one clear owner (see [[Ownership (Memory Management)]]).

More generally, C does the same with the functions `malloc` and `free`, which allocate bytes rather than objects. Modern C++ rarely calls `delete` directly: **smart pointers** like `std::unique_ptr` delete their object when they're destroyed. Languages with **garbage collection**, like Java, Python, and Haskell, have no `delete`: they find objects nothing points to and reclaim them automatically, which rules out dangling pointers and double deletes at some cost in time and memory. The heap of memory allocation is unrelated to the heap data structure (see [[Binary Heap]]).

# Example

A program reads elephants until the user stops, storing them in a heap array that grows when it fills up:

```c++
Elephant* elephants = new Elephant[elephantCapacity];
// ...
if (numElephants > elephantCapacity) {
    // We ran out of space, so make a bigger array
    Elephant* newElephants = new Elephant[elephantCapacity + ELEPHANTS_TO_ADD];
    for (size_t i = 0; i < elephantCapacity; ++i) {
        newElephants[i] = elephants[i];
    }
    delete[] elephants;          // done with the old array
    elephants = newElephants;    // now use the new one
    elephantCapacity += ELEPHANTS_TO_ADD;
}
// ...
delete[] elephants;              // at the end of main
```

The number of elephants isn't known until the program runs, so the array must be on the heap. Each `new[]` is matched by a `delete[]`: the old array is deleted once its elements are copied, and the last one at the end. Leaving out the first `delete[]` would leak every array but the last, since `elephants` is then pointed elsewhere and nothing points to the old one.

# Connections

- [[Object Lifetime]]: automatic and static allocation, and the phases `new` and `delete` perform
- [[Pointer (Programming Languages)]]: what `new` returns, and what dangles after `delete`
- [[Ownership (Memory Management)]]: who is responsible for each `delete`
- [[Array (Data Structure)]]: a heap array's size can be chosen at run time
- [[Undefined Behavior]]: following a dangling pointer, or deleting twice
- [[Destructor]]: where a class deletes the heap memory it allocated
- [[Dynamic Array]]: growing by allocating a bigger array and deleting the old one

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

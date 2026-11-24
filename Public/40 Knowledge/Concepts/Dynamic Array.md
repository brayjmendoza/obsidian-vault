---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Resizable Array
  - Array-Backed List
  - Growable Array
  - Vector (Data Structure)
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **dynamic array** is a list stored in a fixed-size [[Array (Data Structure)|array]] on the heap, which it replaces with a bigger array when it runs out of room, so it can hold any number of items.

A dynamic array tracks two numbers:

- **Size:** how many items it holds.
- **Capacity:** how many items the array underneath can hold.

The first *size* slots of the array hold the items, in order, and the rest are spare, so the invariant `size <= capacity` always holds. Adding an item at the end uses a spare slot when there is one. When there isn't, the dynamic array allocates a larger array, copies every item over, deletes the old array, and then adds the item (see [[Dynamic Memory Allocation]]). Making the new array larger than needed leaves spare slots, so many more items can be added before the next copy.

Since the items are still in one contiguous array, a dynamic array keeps an array's strengths: reaching any item by its index takes constant time. Adding or removing at the end is usually cheap too. Inserting or removing anywhere else shifts every item after that position by one slot.

C++'s `std::vector` is a dynamic array. Besides its size, it reports its `capacity()`, and two member functions manage capacity directly: `reserve(n)` makes room for at least `n` items at once, avoiding repeated copies when the final size is known, and `shrink_to_fit()` gives back the spare space once the vector won't grow any more. Copying everything to a new array moves the items, so growing invalidates every [[Iterator|iterator]] into the vector.

How much to grow matters. Growing by a constant factor, such as doubling the capacity at sizes 1, 2, 4, 8, and so on, makes adding an item at the end take $\Theta(1)$ amortized time: an occasional addition copies the whole array, in $\Theta(n)$ time, but the total over any sequence of $m$ additions is $\Theta(m)$ (see [[Amortized Analysis]]). Growing by a fixed number of slots instead makes $m$ additions take $\Theta(m^2)$ time in all.

More generally, every major language has one: Java's `ArrayList` and Python's `list` are dynamic arrays. Languages differ in the growth factor they use, often 2 or 1.5: a smaller factor wastes less space, at the cost of copying more often.

# Example

A program reads elephants until the user stops, so it can't know in advance how many to store. The source grows its heap array by a fixed two slots whenever it fills:

```c++
if (numElephants > elephantCapacity) {
    Elephant* newElephants = new Elephant[elephantCapacity + ELEPHANTS_TO_ADD];
    for (size_t i = 0; i < elephantCapacity; ++i) {
        newElephants[i] = elephants[i];
    }
    delete[] elephants;
    elephants = newElephants;
    elephantCapacity += ELEPHANTS_TO_ADD;
}
```

This is a hand-written dynamic array, with `elephantCapacity` as its capacity and `numElephants` as its size. With `ELEPHANTS_TO_ADD` fixed at 2, it copies every elephant on every second addition, so $n$ elephants take about $n^2/4$ copies in all. Doubling `elephantCapacity` instead would copy each elephant only a constant number of times on average, as `std::vector` does.

# Connections

- [[Array (Data Structure)]]: the fixed-size storage underneath
- [[Linked List]]: the other way to store a list, with different costs
- [[Dynamic Memory Allocation]]: allocating the new array and deleting the old one
- [[Iterator]]: growing invalidates every iterator
- [[Amortized Analysis]]: why doubling gives constant amortized time per addition
- [[List (Abstract Data Type)]]: the interface a dynamic array encodes
- [[Abstract Data Type]]: a list interface that a dynamic array or a linked list can encode

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

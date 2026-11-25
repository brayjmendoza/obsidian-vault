---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Deep Copy
  - Shallow Copy
  - Assignment Operator
  - Copy Assignment
  - Copy-and-Swap Idiom
  - Rule of Three
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **shallow copy** of an object copies its members as they are, so a pointer in the copy points to the same data as the original's, and a **deep copy** copies the data those pointers lead to as well, so the two objects share nothing.

C++ copies an object in two situations:

- **Copy construction** initializes a brand-new object as a copy of an existing one (e.g., `Sheep dolly{fluffy};`, or passing an object by value). It runs the copy constructor (see [[Constructor (Object-Oriented Programming)]]).
- **Assignment** changes an existing object to be the same as another existing object (e.g., `sabor = siri;`). It runs the **assignment operator**, a member function named `operator=`.

For both, the compiler synthesizes a version that copies each member, unless the class writes its own or forbids copying with `= delete`. For a member that's a pointer to heap memory, copying the member copies only the address, so the synthesized versions make shallow copies: the original and the copy point to the same heap data. That breaks [[Ownership (Memory Management)|ownership]], since both objects now think they own it. Changing the data through one changes it for the other, and when both are destroyed, each one's [[Destructor|destructor]] deletes the same memory, a double delete. A class that owns heap memory must write its own copy constructor and assignment operator to make deep copies.

The assignment operator has more to do than the copy constructor, since its object already holds data:

1. **Check for self-assignment.** For `x = x`, `this == &other`, and the next step would delete the very data to be copied. So if the two are the same object, there's nothing to do.
2. **Clean up the old data,** as the destructor would.
3. **Copy the new data,** as the copy constructor would.
4. **Return `*this`,** a reference to the object, so assignments can be chained (e.g., `x = y = z`).

Steps 2 and 3 repeat the destructor and copy constructor. The **copy-and-swap idiom** removes the repetition: the assignment operator takes its argument by value, so the copy constructor makes a deep copy of it. Then it swaps every member with that copy. The object now holds the new data, and the copy holds the old, which its destructor deletes when the function returns. Self-assignment needs no special case: it swaps with a copy.

More generally, the **rule of three** says that a class needing any one of a custom destructor, copy constructor, or assignment operator almost always needs all three, since all come from owning a resource. C++11's move operations extend it to the rule of five. Languages where variables hold hidden pointers to objects, like Java and Python, never copy objects on assignment: `a = b` makes `a` refer to the same object, and a copy must be asked for (e.g., Python's `copy.copy` for a shallow copy and `copy.deepcopy` for a deep one).

# Examples

## Copying a Barn

A `Barn`'s members are its capacity, its count of cows, and `residentCows_`, a heap array of pointers to cows on the heap. Its copy constructor makes a deep copy, a new array and a new copy of every cow:

```cpp
Barn::Barn(const Barn& other)
    : cowCapacity_{other.cowCapacity_},
      cowCount_{other.cowCount_},
      residentCows_{new Cow*[cowCapacity_]}
{
    for (size_t i = 0; i < other.cowCount_; ++i) {
        residentCows_[i] = new Cow{*other.residentCows_[i]};   // copy each Cow
    }
}
```

## Copy-and-Swap Assignment

With the copy constructor and destructor written, copy-and-swap gives the assignment operator:

```cpp
Barn& Barn::operator=(Barn other) {    // other is a deep copy of the right-hand side
    std::swap(cowCapacity_, other.cowCapacity_);
    std::swap(cowCount_, other.cowCount_);
    std::swap(residentCows_, other.residentCows_);
    return *this;
}                                      // other, now holding the old cows, is destroyed
```

After `barnA = barnB;`, `barnA` holds its own copies of `barnB`'s cows. Its old cows went to `other` in the swap and were deleted by `other`'s destructor at the end of the function.

# Connections

- [[Constructor (Object-Oriented Programming)]]: the copy constructor, which makes new objects as copies
- [[Destructor]]: what frees the data, and what double-deletes after a shallow copy
- [[Ownership (Memory Management)]]: a shallow copy creates two owners of the same memory
- [[Dynamic Memory Allocation]]: the heap memory a deep copy duplicates
- [[Evaluation Strategy]]: passing by value runs the copy constructor, which copy-and-swap relies on
- [[Reference (Programming Languages)]]: `operator=` returns a reference to its object

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

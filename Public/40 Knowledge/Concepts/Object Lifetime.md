---
type: concept
created: 2026-11-23
updated: 2026-11-23
aliases:
  - Lifetime
  - Storage Duration
  - Automatic Allocation
  - Static Allocation
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
An object's **lifetime** is the span of a program's run during which the object exists, from when memory is set aside for it to when that memory is given back.

Every object, whether a primitive value like an `int` or an instance of a class, goes through five phases, in order:

1. **Allocation:** memory is acquired for the object.
2. **Initialization:** the object is put into a usable starting state (see [[Initialization (Programming Languages)]]).
3. **Use:** the object is read, changed, printed, passed to functions, and so on.
4. **Destruction:** the object is cleaned up, which for a class can mean running code that releases what the object holds.
5. **Deallocation:** the object's memory is given back, to be reused.

Allocation and initialization each happen exactly once, and in a correct program, so do destruction and deallocation. Where an object's memory comes from decides when the phases happen. C++ has three kinds of allocation:

| Allocation | Memory | Lifetime |
|---|---|---|
| **Automatic** | The stack: each function call gets a region of memory, its **stack frame**, for its local variables | Tied to the function call and its blocks, so it's handled automatically |
| **Static** | Set aside before the program starts | The whole run of the program (e.g., a `static` data member, of which there's one for the whole program) |
| **Dynamic** | The heap, a region of memory used on request | From when the program asks for it to when it gives it back, decided while the program runs (see [[Dynamic Memory Allocation]]) |

For a local variable, which is allocated automatically, the phases happen at fixed points in the code:

| Phase | When it happens |
|---|---|
| Allocation | The opening `{` of the function, for every local variable in it |
| Initialization | The variable's declaration |
| Use | Between initialization and destruction |
| Destruction | The closing `}` of the block that declares it, after which its name can't be used |
| Deallocation | The closing `}` of the function |

A few cases follow from these rules:

- **Arrays:** an array of $N$ elements goes through each phase $N$ times, once per element, in order.
- **References:** nothing happens for a reference, which is another name for an object that already exists (see [[Reference (Programming Languages)]]).
- **Data members:** an object's data members follow the object. They're allocated, initialized, used, destroyed, and deallocated along with it, and they're destroyed in the reverse of the order the class declares them.
- **Return values:** a function's result is an object too. The caller allocates space for it in its own stack frame and tells the called function where it is, the called function initializes it (usually at `return`), and the caller later destroys and deallocates it. So every function call that returns a value initializes a new object.

More generally, the C++ standard calls these kinds of allocation **storage durations** (automatic, static, dynamic, and thread), and its model is simpler than the one above in one respect: compilers usually set up a function's whole stack frame at once, but a local variable's lifetime officially begins at its declaration. Languages with garbage collection, like Java and Python, separate the phases: an object's memory is reclaimed some time after nothing can refer to it, rather than at a point in the code.

# Example

For illustration (an example not from the source), each phase of `x` and `y` happens at a brace or a declaration:

```c++
void f() {           // x and y allocated
    int x = 1;       // x initialized
    {
        int y = x;   // y initialized; x used
        x = y + 1;   // x and y used
    }                // y destroyed
    printMoos(x);    // x used
}                    // x destroyed; x and y deallocated
```

`y` is destroyed at the inner `}`, since that block declares it, but its memory is deallocated only at the function's `}`, along with `x`'s. Between the two, `y`'s memory is still the function's, but there's no object in it.

# Connections

- [[Initialization (Programming Languages)]]: the second phase, and what a default-initialized variable holds
- [[Dynamic Memory Allocation]]: objects whose allocation and deallocation the program controls
- [[Scope]]: a local variable's name is usable from its declaration to the end of its block, which is also when it's destroyed
- [[Ownership (Memory Management)]]: who is responsible for ending a heap object's lifetime
- [[Lvalues and Rvalues]]: temporaries, unnamed objects whose lifetime is one line of code
- [[Constructor (Object-Oriented Programming)]]: what initialization runs for an object of class type
- [[Destructor]]: what destruction runs for an object of class type

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

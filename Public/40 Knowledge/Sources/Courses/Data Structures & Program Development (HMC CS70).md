---
type: course
created: 2026-11-23
updated: 2026-11-24
authors:
  - Melissa O'Neill
year: 2023
fields:
  - computer-science
status: read
---
# Summary

Harvey Mudd College's CS 70, Data Structures and Program Development, teaches C++ and uses it to build and analyze data structures. It starts with the language and how C++ programs are built, then covers memory (arrays, pointers, references, and the heap), classes, and generic programming. Its second half analyzes algorithms with asymptotic and amortized complexity and studies lists, search trees, and heaps. The material ingested here is a set of notes taken during the course. They have no lecture numbering, so they're split into seven units by topic, in the course's order.

The course's C++ syntax is collected in `50 References/C++/`, starting with [[C++ Basics]] and [[Compiling C++]].

# Key Ideas

## Unit 1: C++ Basics and Compilation

- C++ was designed so that a feature costs nothing to a program that doesn't use it (see [[Zero-Overhead Principle]]), so it doesn't check whether a program follows its rules.
- A program that breaks C++'s rules has [[Undefined Behavior|undefined behavior]]: it may run correctly, crash, or do anything else, and the compiler needn't warn.
- A variable declared without a starting value is default-initialized and holds an indeterminate value, while giving it one copy-initializes it (see [[Initialization (Programming Languages)]]). Parameters and return values are copy-initialized too.
- `auto` lets the compiler work out a variable's type from its initializer (in general, [[Type Inference|type inference]]).
- A promotion moves a value to a type of the same kind whose range includes the original's, so it never loses information, and any other numeric change is a conversion, which can (in general, [[Type Conversion|widening and narrowing conversions]]).
- A `float` has 24 significand bits and a `double` has 53, so converting a large integer to a `float` can round it (see [[Floating-Point Arithmetic]]).
- A namespace (in general, a [[Namespace (Programming Languages)|namespace]]) collects names so they can't clash, and `::` reaches into it. `using namespace` belongs in source files, never headers.
- A C++ program is built in four stages, preprocessing, compilation, assembly, and linking, and each source file is compiled separately (see [[Separate Compilation]]).
- A function can be called from a file that only declares it, with its definition in another file, and headers hold these declarations (see [[Declaration and Definition]]). Include guards stop a header's definitions from appearing twice.
- A Makefile's rules say which targets depend on which prerequisites, and `make` reruns only the commands whose prerequisites have changed (in general, [[Build Automation|build automation]]).
- Tests use only a class's public interface, never rely on undefined behavior, and assume nothing an interface doesn't promise (in general, [[Black-Box Testing|black-box testing]]).

## Unit 2: Memory

- An array is contiguous, ordered, homogeneous, and fixed-size, and a stack array's size must be a compile-time constant (see [[Array (Data Structure)]]).
- A pointer holds a memory address: `&` takes an object's address, and `*` follows a pointer to its object (see [[Pointer (Programming Languages)]]). Following an invalid, null, or past-the-end pointer is undefined behavior.
- An array's name decays to a pointer to its first element, so a pointer to the start and a past-the-end pointer describe a range, and pointer arithmetic moves through it.
- A reference is another name for an existing object and never changes its referent (see [[Reference (Programming Languages)]]).
- Passing by value copies an argument into the parameter, while passing by reference lets a function change the caller's variable or avoid a copy (in general, [[Evaluation Strategy|call by value and call by reference]]).
- `const` restricts access through one name only, and can be added but never removed (in general, [[Const-Correctness|const-correctness]]).
- Every object goes through allocation, initialization, use, destruction, and deallocation, and for a local variable each happens at a brace or its declaration (see [[Object Lifetime]]). Allocation is static, automatic (on the stack), or dynamic (on the heap).
- A function's result is initialized in space its caller allocated, and an unnamed result lives in a temporary until the end of its line (see [[Lvalues and Rvalues]]).
- `new` allocates and initializes an object on the heap and returns a pointer to it, and `delete` destroys and frees it (see [[Dynamic Memory Allocation]]). Getting them wrong causes memory leaks, dangling pointers, and double deletes.
- Every heap object should have a single owner responsible for deleting it (in general, the principle of [[Ownership (Memory Management)|ownership]]).
- A segmentation fault is the operating system stopping a program that touched memory outside its own (see [[Segmentation Fault]]).

## Unit 3: Classes

- A class bundles member variables with member functions, its public members are what other code may use, and its private members only it can touch (see [[Class (Programming Languages)]]). A `struct` is a class whose members are public by default.
- A data structure is described by its interface (what it does), its encoding (how its data is organized, and what must always hold), and its implementation (how its operations work), each with its own promises (in general, an [[Abstract Data Type|abstract data type]]).
- Constructors initialize new objects, and member initialization lists initialize members before the constructor's body runs (see [[Constructor (Object-Oriented Programming)]]). The default and copy constructors are synthesized when a class doesn't write them, the default one only if it declares no constructors.
- A [[Destructor|destructor]] runs when an object is destroyed, and a class that allocates heap memory deletes it there.
- `const` member functions promise not to change their object, and they're the only ones a `const` object can call (see [[Const-Correctness]]).
- `this` points to the object a member function was called on, and `static` members belong to the class rather than to any object (see [[Class (Programming Languages)]]).
- The synthesized copy constructor and assignment operator copy pointers, not what they point to, so a class that owns heap memory writes its own to make deep copies (see [[Deep and Shallow Copy]]). Copy-and-swap builds the assignment operator from the copy constructor and destructor.
- A one-argument constructor converts values into a class, a type-cast operator converts out of it, and `explicit` stops either from happening automatically (see [[Type Conversion]]).

## Unit 4: Generic Programming and Polymorphism

- A function is polymorphic if a parameter accepts arguments of more than one type, and C++ has three kinds: subtype, parametric, and ad hoc (see [[Polymorphism (Computer Science)]]).
- Function and class templates take types as parameters, and the compiler generates code for each type used (in general, [[Parametric Polymorphism|parametric polymorphism]]). A template's definition goes in a header, since it can't be compiled on its own.
- Overloading gives several functions one name, and C++ picks among them by the arguments' types, preferring exact matches, then promotions, then conversions (see [[Function Overloading]]). Operators are overloadable functions too, which is how `<<` prints every type.
- A derived class is a subtype of its base class (see [[Inheritance (Object-Oriented Programming)]] and [[Subtyping]]). A pure virtual function makes its class abstract, and a class of only pure virtual functions is an interface.
- A `virtual` member function is chosen by the object's actual type at run time, and `override` marks a derived class's version (in general, [[Dynamic Dispatch|dynamic dispatch]]).
- An iterator marks one item's place in a collection, and supports begin, next, fetch, and is-done (see [[Iterator]]). Its rules, like never dereferencing past-the-end, prevent undefined behavior, and changing a container can invalidate its iterators.
- The range-based `for` loop is shorthand for a loop over iterators (in general, [[Syntactic Sugar|syntactic sugar]]).
- `std::vector` is a dynamic array, with a size and a capacity it grows when full (in general, a [[Dynamic Array|dynamic array]]), and `std::list` is a doubly [[Linked List|linked list]].

## Unit 5: Asymptotic and Amortized Analysis

- Asymptotic analysis asks how an algorithm's cost scales as its input grows, ignoring constant factors and smaller terms, and compares cost functions by the limit of their ratio (see [[Asymptotic Analysis]]).
- $O$, $\Theta$, and $\Omega$ are sets of functions that grow no faster than, as fast as, and no slower than a given function, and little $o$ and $\omega$ are their strict versions.
- The orders of complexity, from constant and logarithmic up to exponential and factorial, are $\Theta$ sets that don't overlap (see [[Orders of Complexity]]).
- An algorithm can have different best, worst, and expected costs, as linear search does: $\Theta(1)$, $\Theta(n)$, and $\Theta(n)$ (see [[Best, Worst, and Expected Case]]).
- Amortized time bounds the total cost of a sequence of operations from the start, not each operation, so pushing onto an array-backed list that doubles when full is $\Theta(1)$ amortized (see [[Amortized Analysis]] and [[Dynamic Array]]). The aggregate, banker's, and physicist's methods prove such bounds.
- Stacks, queues, steques, deques, and lists are linear data structures, encoded with array-backed or linked lists (see [[Stack (Abstract Data Type)]], [[Queue (Abstract Data Type)]], and [[List (Abstract Data Type)]]).
- Sets, maps, multisets, and multimaps are associative data structures, encoded with binary search trees or hash tables (see [[Set (Abstract Data Type)]] and [[Associative Array]]).
- No data structure is best: linear structures keep order, associative ones search, and priority queues find the minimum, so the choice depends on the application (see [[Abstract Data Type#Choosing a Data Structure|Choosing a Data Structure]]).

## Unit 6: Search Trees

- A tree has a root, parents and children, leaves, and subtrees, and its height is the longest path from the root to a leaf, $-1$ for the empty tree (see [[Tree (Data Structure)]]). A binary tree is empty, or a node with a left and a right subtree.
- In a binary search tree, every key is greater than those in its left subtree and less than those in its right, so lookup is binary search, and an in-order traversal visits keys in sorted order (see [[Binary Search Tree]]). Its operations take time proportional to its height, from $\Theta(\log n)$ when balanced to $\Theta(n)$ for a stick.
- A rotation raises a child into its parent's place in constant time, keeping the keys in order, and every balancing strategy uses rotations (see [[Tree Rotation]]).
- A randomized BST makes each new key the root of the subtree it's entering with probability $rac{1}{N+1}$, which simulates inserting keys in random order and gives expected $\Theta(\log n)$ height (see [[Randomized Binary Search Tree]]).
- A splay tree moves every inserted or found key to the root with double rotations, taking advantage of temporal locality, for $O(\log n)$ amortized time (see [[Splay Tree]]).
- A 2-3-4 tree has 2-, 3-, and 4-nodes, splits 4-nodes by promoting their middle key, and stays perfectly balanced (see [[2-3-4 Tree]]).
- A red-black tree is a binarized 2-3-4 tree, with red nodes marking keys that share a 2-3-4 node, and it guarantees $O(\log n)$ time in the worst case (see [[Red-Black Tree]]).
- The trees trade off expected, amortized, and worst-case guarantees against extra space, extra rotations, locality, and how hard they are to implement (see [[Search Tree Comparison]]).

## Unit 7: Heaps and Priority Queues

- A priority queue gives each item an ordered key, and always removes the item with the smallest key next (see [[Priority Queue]]). It supports insert, get-min, pop-min, and change-priority, and serves algorithms like shortest paths and Huffman coding.
- A binary heap is a complete binary tree in which every node's key is no larger than its children's, the most common encoding of a priority queue (see [[Binary Heap]]).
- A heap is stored as an array in level order, where node $i$'s children are at $2i + 1$ and $2i + 2$ and its parent at $\lfloor (i - 1)/2 \rfloor$.
- Insert adds at the end and swaps upward, and pop-min moves the last item to the root and swaps it down with its smaller child, each in $O(\log n)$. Heapify builds a heap from an arbitrary array in $\Theta(n)$.
- Heap sort max-heapifies an array, then pops the maximum into the slot each pop frees at the end, sorting in place in $O(n \log n)$ (see [[Heap Sort]]).

# Open Questions

- 

# Quotes


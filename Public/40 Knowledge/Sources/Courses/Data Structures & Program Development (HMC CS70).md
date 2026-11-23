---
type: course
created: 2026-11-23
updated: 2026-11-23
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

# Open Questions

- 

# Quotes


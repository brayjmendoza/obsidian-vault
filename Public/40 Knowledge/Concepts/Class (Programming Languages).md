---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Class
  - Object
  - Instance
  - Member Variable
  - Data Member
  - Member Function
  - Method
  - Access Control
  - Struct
  - this Pointer
  - Static Member
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **class** defines a new type by bundling data with the functions that operate on it, and an **object**, or **instance**, is a value of that type.

Each object stores its own copy of the class's data, its **member variables** (or **data members**), and the class's **member functions** operate on whichever object they're called on, written with dot notation (e.g., `bessie.moo(1)` calls `moo` on the object `bessie`). Inside a member function, the class's members can be referred to by name, since they're in scope throughout the class.

A class controls who can reach its members:

- **`public`** members can be used by any code. Together they form the class's interface, what other code may do with its objects.
- **`private`** members can be used only by the class's own member functions. They hold the details other code shouldn't depend on.

Since access levels are part of the class's definition, they appear only where the class is defined, in its header, not with the member functions' definitions. This split between what a class offers and how it does it is what makes a class an [[Abstract Data Type|abstract data type]].

Three more features complete the picture:

- **`this`:** every non-`static` member function receives, implicitly, a pointer to the object it was called on, named `this`. So `name_` inside a member function means `this->name_`, and `*this` is the object itself. In a `const` member function, `this` is a pointer to a `const` object (see [[Const-Correctness]]).
- **`static` members** belong to the class, not to any object: there's exactly one, shared by every instance, reached as `Cow::MAX_LEGS` rather than through an object. A member function that doesn't need `this` can be `static`.
- **`struct`:** a `struct` is a class whose members are public by default, where a `class`'s are private by default. Otherwise the two keywords are interchangeable. By convention, a `struct` is "just the data," a few public members that outside code works on, as in C, where a `struct` has no member functions or private data at all. A `class` takes care of itself, keeping its data private behind member functions.

More generally, classes are the core of **object-oriented programming**, and Java and Python use different words for the same things: a **method** is a member function, a **field** or **instance variable** is a member variable, and creating an object, which C++ calls **construction**, is **instantiation**. Python has no access control enforced by the language, only the convention that a name starting with an underscore is private. The distinction between grouping behavior by data, as classes do, and by operation, as functions over data types do, is the [[Expression Problem|expression problem]].

# Examples

## A Cow Class

A `Cow` knows how many spots it has and how old it is, and can moo. Its definition goes in `cow.hpp`:

```cpp
class Cow {
 public:
    Cow(int numSpots, int age);
    Cow() = delete;                  // no Cow without spots and an age

    void moo(int numMoos) const;
    int getNumSpots() const;         // accessors
    int getAge() const;
    void setNumSpots(int numSpots);  // mutators
    void setAge(int age);

 private:
    int numSpots_;                   // each Cow has its own
    int age_;
};                                   // note the semicolon
```

Its member functions are defined in `cow.cpp`, each name qualified with `Cow::` so the compiler knows which class it belongs to (see [[Namespace (Programming Languages)]]):

```cpp
void Cow::setAge(int age) {
    age_ = age;
}
```

Code that uses a `Cow` can call its public member functions but can't touch `age_` directly: `bessie.setAge(4)` compiles, and `bessie.age_ = 4` doesn't, since `age_` is private.

# Connections

- [[Constructor (Object-Oriented Programming)]]: how a class's objects are initialized
- [[Destructor]]: how they're cleaned up
- [[Abstract Data Type]]: a class's public members are an interface, and its private ones an encoding
- [[Const-Correctness]]: `const` member functions promise not to change their object
- [[Algebraic Data Type]]: the functional way to define a new type, by its alternatives instead of by bundled data and functions
- [[Expression Problem]]: classes make new kinds of data easy to add, and new operations hard
- [[Inheritance (Object-Oriented Programming)]]: defining a class as an extension of another

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

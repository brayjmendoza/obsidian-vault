---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Inheritance
  - Base Class
  - Derived Class
  - Superclass
  - Subclass
  - Abstract Class
  - Pure Virtual Function
  - Interface Class
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Inheritance** defines a new class as an extension of an existing one: the new class, the **derived class**, gets the members of the existing one, the **base class**, and can add its own or replace the base class's behavior.

In C++, a class `Student` derived from `Person` is everything a `Person` is, and possibly more. So `Student` is a [[Subtyping|subtype]] of `Person`: every `Student` can also be seen as a `Person`, but not every `Person` is a `Student`. Any function that wants a `Person`, by pointer or by reference, can be given a `Student` and still work. This is how C++ provides subtype polymorphism (see [[Polymorphism (Computer Science)]]). Java and Python call the two classes the **superclass** and **subclass**.

A derived class can **override** a member function of its base class, giving its own implementation. Which implementation a call runs, the base class's or the derived class's, depends on whether the function is virtual (see [[Dynamic Dispatch]]).

## Abstract Classes

Sometimes a base class can say what its derived classes must do, but not how. A **pure virtual** member function is declared in the base class with `= 0` and has no implementation there:

```c++
virtual void speak() const = 0;
```

A class with at least one pure virtual function is an **abstract class**. No object of it can be made, only objects of classes derived from it, and every derived class that's meant to have objects (a **concrete** class) must override each pure virtual function with an implementation.

If a base class has no data members and every member function is pure virtual, it's an **interface class**: it specifies *what* its derived classes can do, without saying anything about *how*. That's the interface of an [[Abstract Data Type|abstract data type]], written as a type that code can depend on.

More generally, inheritance mixes two things: reusing a base class's code, and declaring a subtype. Many designers now prefer **composition**, building a class from objects of other classes, for reuse, and keep inheritance for genuine "is a" relationships. The **Liskov substitution principle** states when a derived class is a proper subtype: wherever the base class works, the derived class must too. Java separates the two uses of abstract classes, with `interface` types that a class can implement many of and classes it can inherit from only one of. C++ allows a class to have several base classes, **multiple inheritance**.

# Example

For illustration (an example not from the source), an abstract `Animal` and two concrete classes derived from it:

```c++
class Animal {
 public:
    virtual void speak() const = 0;   // pure virtual: Animal is abstract
    virtual ~Animal() = default;
};

class Cow : public Animal {
 public:
    void speak() const override { std::cout << "Moo" << std::endl; }
};

class Sheep : public Animal {
 public:
    void speak() const override { std::cout << "Baa" << std::endl; }
};

void chorus(const Animal& a) {
    a.speak();
}

chorus(Cow{});      // Moo
chorus(Sheep{});    // Baa
// Animal a;        // error: Animal is abstract
```

`chorus` is written for `Animal`, but since `Cow` and `Sheep` are subtypes of `Animal`, it accepts both, and each speaks in its own way. No `Animal` itself can be created, since `speak` has no implementation in it.

# Connections

- [[Subtyping]]: a derived class is a subtype of its base class
- [[Dynamic Dispatch]]: how a call through a base class reaches a derived class's override
- [[Polymorphism (Computer Science)]]: inheritance gives subtype polymorphism
- [[Abstract Data Type]]: an interface class states an interface as a type
- [[Class (Programming Languages)]]: what is inherited
- [[Expression Problem]]: inheritance makes new kinds of data easy to add, and new operations hard

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

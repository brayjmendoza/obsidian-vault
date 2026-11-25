---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Virtual Function
  - Virtual Member Function
  - Late Binding
  - Static Dispatch
  - Method Overriding
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Dynamic dispatch** chooses which implementation of a member function to run from the actual type of the object at run time, rather than from the declared type of the variable that refers to it.

With [[Inheritance (Object-Oriented Programming)|inheritance]], a variable's declared type and its object's actual type can differ: a reference of type `Animal&` can refer to a `Cow`. If `Cow` overrides a member function of `Animal`, a call through that reference could mean either version. The declared type is known when the program is compiled, so choosing by it is **static dispatch**. The actual type may be known only when the program runs, so choosing by it is **dynamic dispatch**.

By default, C++ uses static dispatch. Dynamic dispatch is opt-in:

- **`virtual`:** a member function declared `virtual` in the base class is dispatched dynamically. Once a function is virtual in a base class, it's virtual in every class derived from it.
- **`override`:** when a derived class overrides a virtual function, its declaration should say `override`. Then the compiler checks that a virtual function with that signature really exists in a base class, and rejects the declaration if not, which catches misspelled names and mismatched parameters.

Dynamic dispatch happens only through pointers and references. Passing a `Cow` by value to a parameter of type `Animal` copies just its `Animal` part, so the copy really is an `Animal`, and its actual type matches the declared one.

More generally, C++ makes dynamic dispatch opt-in because it has a cost: each call looks up the right function at run time, usually in a per-class table of function pointers (a **vtable**), and can't be inlined. That fits the [[Zero-Overhead Principle|zero-overhead principle]]: a class that doesn't use `virtual` doesn't pay for it. Java and Python dispatch every method call dynamically by default, and Java's `final` opts a method out. Since the code a call runs is decided late, at run time, dynamic dispatch is also called **late binding**.

# Examples

## Virtual and Non-Virtual Calls

For illustration (an example not from the source):

```cpp
class Animal {
 public:
    void describe() const { std::cout << "an animal" << std::endl; }    // not virtual
    virtual void speak() const { std::cout << "..." << std::endl; }
};

class Cow : public Animal {
 public:
    void describe() const { std::cout << "a cow" << std::endl; }        // hides, doesn't override
    void speak() const override { std::cout << "Moo" << std::endl; }
};

Cow bessie;
Animal& a = bessie;
a.speak();       // Moo: virtual, so the actual type, Cow, decides
a.describe();    // an animal: not virtual, so the declared type, Animal, decides
```

Both calls go through the same reference to the same `Cow`. `speak` is virtual, so it runs `Cow`'s version. `describe` isn't, so the compiler picks `Animal`'s version from the declared type of `a`, and writing `override` on `Cow::describe` would be a compile error.

# Connections

- [[Inheritance (Object-Oriented Programming)]]: where declared and actual types come apart
- [[Polymorphism (Computer Science)]]: dynamic dispatch makes subtype polymorphism dynamic, unlike templates and overloading
- [[Static and Dynamic Typing]]: the same static-versus-dynamic distinction, applied to choosing code rather than checking types
- [[Zero-Overhead Principle]]: why C++ makes dynamic dispatch opt-in
- [[Function Overloading]]: chosen statically, from argument types, where virtual calls are chosen dynamically

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: reference
created: 2026-11-24
updated: 2026-11-24
topic: c++
---
C++ syntax for derived classes, virtual functions, and abstract classes. The ideas are in [[Inheritance (Object-Oriented Programming)]] and [[Dynamic Dispatch]].

# Syntax

```c++
class Animal {
 public:
    virtual void speak() const = 0;        // pure virtual: Animal is abstract
    virtual void eat();                    // virtual, with a default implementation
    virtual ~Animal() = default;           // virtual destructor
};

class Cow : public Animal {                // Cow is derived from Animal
 public:
    void speak() const override;           // overrides Animal::speak
};
```

| Keyword | Means |
|---|---|
| `class Cow : public Animal` | `Cow` is derived from `Animal`, and its public members stay public |
| `virtual` | Calls are dispatched on the object's actual type. Write it in the base class |
| `override` | Overrides a virtual function. A compile error if no base class function matches |
| `= 0` | Pure virtual: no implementation here, and the class is abstract |

# Rules

- **Mark `override` on every override,** so a typo becomes a compile error rather than a new, unrelated function.
- **Give a base class a virtual destructor** if derived objects may be deleted through a base class pointer. Otherwise only the base part is destroyed.
- **Call through pointers or references.** Passing a derived object by value to a base class parameter copies only its base part, and the call isn't dispatched to the derived class.
- **Abstract classes can't be created,** only pointed to or referred to (e.g., `Animal a;` is an error, and `Animal& a = bessie;` is fine).
- **An interface class** has no data members and only pure virtual functions.

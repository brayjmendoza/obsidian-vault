---
type: reference
created: 2026-11-23
updated: 2026-11-23
topic: c++
---
C++ syntax for writing a class: where each part goes, constructors, destructors, copying, `static` members, and conversions. The ideas are in [[Class (Programming Languages)]], [[Constructor (Object-Oriented Programming)]], [[Destructor]], [[Deep and Shallow Copy]], and [[Abstract Data Type]].

| Java and Python | C++ |
|---|---|
| Class | `class` or `struct` |
| Object, instance | Object of class type, instance of class `X` |
| Instantiation | Construction |
| Field, instance variable | Member variable, data member |
| Method | Member function |
| Superclass | Base class |
| Subclass | Derived class |

# Files

| File | Holds |
|---|---|
| `cow.hpp` | The class definition, with an include guard: member declarations, under `public:` and `private:` |
| `cow.cpp` | `#include "cow.hpp"`, then each member function's definition, named `Cow::` |
| Any file using `Cow` | `#include "cow.hpp"` |

```c++
// cow.hpp
#ifndef COW_HPP_INCLUDED
#define COW_HPP_INCLUDED

class Cow {
 public:
    Cow(int numSpots, int age);
    void moo(int numMoos) const;
    int getAge() const;
    void setAge(int age);

 private:
    int numSpots_;
    int age_;
};   // the semicolon is required

#endif  // COW_HPP_INCLUDED
```

```c++
// cow.cpp
#include "cow.hpp"

int Cow::getAge() const {   // const in both the .hpp and the .cpp
    return age_;
}
```

- **Member variables end in `_`** (e.g., `age_`), by convention.
- **`public:` and `private:` appear only in the header.**
- **Make every member function `const` that can be.** A `const` object can only call `const` member functions (see [[Const-Correctness]]).
- **Use `name_`, not `this->name_`,** inside member functions. `this` is there if you need the object itself (e.g., `return *this;`).

# Special Member Functions

| Declaration | Is | If you don't write it |
|---|---|---|
| `Cow(int numSpots, int age);` | A parameterized constructor | None |
| `Cow();` | The default constructor | Synthesized only if the class declares no constructors |
| `Cow(const Cow& other);` | The copy constructor | Synthesized: copies each member |
| `Cow& operator=(const Cow& other);` | The assignment operator | Synthesized: assigns each member |
| `~Cow();` | The destructor | Synthesized: destroys each member |

Add `= default` to ask for the synthesized version, or `= delete` to forbid it (e.g., `Cow() = delete;`). Never delete the destructor.

**A class that owns heap memory writes all three of its copy constructor, assignment operator, and destructor** (see [[Deep and Shallow Copy]]).

## Initialization Lists

```c++
Cow::Cow(int numSpots, int age)
    : numSpots_{numSpots},
      age_{age}
{
    // body runs after every member is initialized
}
```

List members in the order the class declares them: that's the order they're initialized in anyway.

## Assignment Operator

Copy-and-swap, given a working copy constructor and destructor:

```c++
Barn& Barn::operator=(Barn other) {
    std::swap(cowCapacity_, other.cowCapacity_);
    std::swap(cowCount_, other.cowCount_);
    std::swap(residentCows_, other.residentCows_);
    return *this;
}
```

Written by hand instead: check `if (this == &other) return *this;`, delete the old data, copy the new, and `return *this;`.

## Creating Objects

| Code | Runs |
|---|---|
| `Cow bessie{3, 12};` or `Cow bessie(3, 12);` | The parameterized constructor. Braces refuse lossy conversions of the arguments |
| `Sheep mead;` or `Sheep mead{};` | The default constructor |
| `Sheep herd[10];` | The default constructor, ten times |
| `Sheep dolly{fluffy};` or `Sheep dolly = fluffy;` | The copy constructor |
| `dolly = fluffy;` (both already exist) | The assignment operator |

# Static Members

```c++
class Cow {
    static constexpr int MAX_LEGS = 4;   // a compile-time constant: declared and defined here
    static size_t totalCowsEver;         // declared here; define it in cow.cpp
    static void openCowWikipediaPage();  // no Cow needed to call it
};

size_t Cow::totalCowsEver = 0;           // in cow.cpp, without the word static
```

Use them as `Cow::MAX_LEGS`, not through an object. Write `static` only in the class definition.

# Conversions

| Declaration | Allows |
|---|---|
| `FuzzyBool(bool b);` | `bool` $\to$ `FuzzyBool` automatically (e.g., `makeDinner(true)`) |
| `explicit FuzzyBool(bool b);` | Only when asked for, as in `FuzzyBool{true}` |
| `operator bool() const;` | `FuzzyBool` $\to$ `bool` automatically |
| `explicit operator bool() const;` | Only when asked for, as in `bool(fb)`, or in a condition like `if (fb)` |

Mark one-argument constructors `explicit` unless the automatic conversion is really wanted (see [[Type Conversion]]).

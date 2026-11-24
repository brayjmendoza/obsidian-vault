---
type: reference
created: 2026-11-24
updated: 2026-11-24
topic: c++
---
C++ syntax for function and class templates, and where their code goes. The idea is in [[Parametric Polymorphism]].

# Function Templates

```c++
template <typename T>
void printVal(const T& x) {
    std::cout << x << std::endl;
}

template <typename Iter, typename Value>
void fill(Iter start, Iter pastEnd, const Value& value) {
    for (Iter i = start; i != pastEnd; ++i) {
        *i = value;
    }
}
```

- **`template <typename T>`** makes `T` a template parameter, a type filled in at each use.
- **The compiler works out `T`** from the arguments (e.g., `printVal(42)` uses `T = int`), or you can give it (e.g., `printVal<double>(42)`).
- **Take parameters by `const T&`,** since `T` might be a large object.
- **An unsuitable type is a compile error,** reported where the template uses an operation the type lacks (e.g., `<<` for a type that can't be printed).

# Class Templates

```c++
template <typename F, typename S>
class Pair {
 public:
    Pair(const F& first, const S& second);
    const F& getFirst() const;
    void setFirst(const F& f);
 private:
    F first_;
    S second_;
};
```

Every member function defined outside the class repeats the template line, and names the class with its parameters:

```c++
template <typename F, typename S>
Pair<F, S>::Pair(const F& first, const S& second)
    : first_{first}, second_{second} {
}

template <typename F, typename S>
const F& Pair<F, S>::getFirst() const {
    return first_;
}
```

There's no class called `Pair`, only `Pair<int, int>`, `Pair<std::string, bool>`, and so on. `Pair myPair;` is an error.

# Where Template Code Goes

The compiler can only generate code for a template once it knows `T`, so a template's definition must be visible in every file that uses it. It can't go in its own `.cpp` file.

| File | Holds |
|---|---|
| `pair.hpp` | The declarations, with an include guard, and at the end `#include "pair-private.hpp"` |
| `pair-private.hpp` | The definitions of every member function |
| Any file using `Pair` | `#include "pair.hpp"` |

# Templates and Overloads

When a template and ordinary functions share a name:

| Call | Chosen |
|---|---|
| An ordinary function matches as well as the template | The ordinary function |
| The template matches exactly, and an ordinary function would need a conversion | The template |

```c++
template <typename T> void print(const T& val);   // "templated print"
void print(int val);                              // "int print"
void print(double val);                           // "double print"

print(42);       // int print
print(3.1415);   // double print
print("Hello");  // templated print: a string literal is neither an int nor a double
```

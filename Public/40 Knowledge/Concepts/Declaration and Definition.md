---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Declaration
  - Definition
  - Forward Declaration
  - One Definition Rule
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **declaration** introduces a name and says what kind of thing it is, and a **definition** is a declaration that also supplies the thing itself: a function's body, or the storage and starting value of a variable.

A declaration tells the compiler enough to check code that uses the name. For a function, that's its name, parameter types, and return type, written with a semicolon in place of the body:

```cpp
void printMoos(int numMoos);
```

A declaration made before the definition, so that code can use the name first, is a **forward declaration**. In C++, a name must be declared before it's used, so forward declarations are how a function calls another that's defined later in the file, and how a file calls a function defined in another file (see [[Separate Compilation]]). The definition can be anywhere, as long as the linker finds exactly one.

A name may be declared many times but defined only once, which is C++'s **one definition rule**. Including the same header twice in one file breaks the rule when the header contains a definition, as a constant does: the file ends up with two definitions of the same name, and compilation fails. Headers guard against this with **include guards**, preprocessor lines that skip the header's contents if the file has already included it (see [[Compiling C++]]).

More generally, the distinction matters most in languages compiled one file at a time, like C, C++, and Objective-C, where a file has to know a function's type without seeing its body. Many languages blur it: in Python, `def` both declares and defines a function, at the moment it runs. Haskell and Java let code use a name defined later in the same file or class, so they need no forward declarations. The one definition rule's general form is that a name is bound once per scope (see [[Name Binding]]).

# Examples

## A Header Included Twice

`pi.hpp` defines a constant, and `tau.hpp` includes `pi.hpp` to define another:

```cpp
// pi.hpp
constexpr double PI = 3.1415926535897932;

// tau.hpp
#include "pi.hpp"
constexpr double TAU = 2 * PI;
```

A file that includes both gets `pi.hpp`'s contents twice, once directly and once through `tau.hpp`:

```cpp
// circles.cpp
#include "pi.hpp"
#include "tau.hpp"     // includes pi.hpp again: PI is defined twice

double circumference(double radius) {
    return TAU * radius;
}
```

Preprocessing pastes in both copies, so `circles.cpp` defines `PI` twice and fails to compile. An include guard in `pi.hpp` makes the second copy empty.

# Connections

- [[Separate Compilation]]: declarations let one file use what another defines, and the linker joins them
- [[Name Binding]]: a definition binds a name, at most once per scope
- [[Scope]]: a declaration makes a name visible from that point to the end of its scope
- [[Type Inference]]: a declaration states a name's type, which inference would otherwise work out

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: reference
created: 2026-11-23
updated: 2026-11-24
topic: c++
---
The syntax for a first C++ program: functions, console input and output, variables, and namespaces. Types are in [[C++ Types]], and building a program is in [[Compiling C++]].

# Functions

A function states its return type and each parameter's type:

```cpp
bool isPrime(int n) {
    if (n < 2) {
        return false;
    }
    // Try dividing by all numbers from 2 to sqrt(n).
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            return false;
        }
    }
    // If we get here, we didn't find a factor, so n is prime.
    return true;
}
```

The loop runs while `i * i <= n`, so it tries every divisor up to $\sqrt{n}$, including $\sqrt{n}$ itself when $n$ is a perfect square (e.g., $9 = 3 \times 3$).

A function can be declared before it's defined, with a semicolon in place of its body (see [[Declaration and Definition]]).

# Console Input and Output

```cpp
#include <iostream>
#include <string>

std::cout << "What is your name? ";
std::string name;
std::cin >> name;
std::cout << "Hello, " << name << "!" << std::endl;
```

| Name | Does | Needs |
|---|---|---|
| `std::cout << x` | Writes `x` to the console ("character output") | `#include <iostream>` |
| `std::cin >> x` | Reads the next word from the console into `x` ("character input") | `#include <iostream>` |
| `std::endl` | Ends the line | `#include <iostream>` |
| `std::getline(std::cin, s)` | Reads a whole line into the string `s` | `#include <string>` |
| `std::string` | A string of characters | `#include <string>` |

`>>` stops at whitespace, so `std::cin >> name` reads one word. Use `std::getline` for a whole line.

# Variables

Every variable has a type, a name, a value, and a location in memory. The type must be written, or inferred with `auto` (see [[Type Inference]]):

```cpp
int x = 3;   // an int with the value 3
int y;       // an int with an indeterminate value: give it one before using it
```

`int y;` doesn't set `y` to zero. It holds whatever bits were in its memory, and reading it is undefined behavior (see [[Initialization (Programming Languages)]]). Always give a starting value.

## Qualifiers

| Qualifier | Means | Example |
|---|---|---|
| `constexpr` | Known at compile time, and never changes | `constexpr size_t SIZE = 42;` |
| `const` | Read-only, but its value can be computed at run time | `const int total = a + b;` |
| `&` (in a type) | A reference: another name for an existing variable | `int& z = x;` |

Use `constexpr` for anything the compiler needs to know, like an array's size. Pointers, references, and arrays are in [[C++ Pointers and Memory]].

# Namespaces

`::` is the scope-resolution operator: `place::name` means the `name` inside `place` (e.g., `Cow::moo` is the `moo` inside the class `Cow`). Everything in the standard library is in the namespace `std` (see [[Namespace (Programming Languages)]]).

- **`using namespace std;`** at the top of a file lets you write `cout` for `std::cout`, at the risk of name clashes.
- **Fine in a `.cpp` file.** Its effect stays in that file.
- **Never in a `.hpp` file.** A header is pasted into every file that includes it, so the `using` would spread to code that didn't ask for it.

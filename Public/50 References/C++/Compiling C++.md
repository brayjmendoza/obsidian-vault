---
type: reference
created: 2026-11-23
updated: 2026-11-23
topic: c++
---
Commands and file conventions for building a C++ program from several files with `clang++`. Why the steps exist is in [[Separate Compilation]], and automating them is in [[Makefiles]].

# Commands

| Command | Does |
|---|---|
| `clang++ -c file.cpp` | Preprocesses, compiles, and assembles `file.cpp` into the object file `file.o` |
| `clang++ -o prog a.o b.o` | Links object files into the executable `prog` |
| `clang++ -o prog a.cpp b.cpp` | Does both steps at once |
| `./prog` | Runs the executable |

Common flags:

| Flag | Does |
|---|---|
| `-std=c++17` | Compiles with the C++17 standard |
| `-g` | Keeps debugging information |
| `-Wall -Wextra` | Turns on most warnings |
| `-pedantic` | Warns about anything that isn't standard C++ |

`g++` takes the same commands and flags.

# Header and Source Files

- **`.hpp` files** hold declarations, and **`.cpp` files** hold definitions (see [[Declaration and Definition]]).
- **Headers aren't compiled.** Only `.cpp` files are, and each one includes the headers it needs.
- **Include your own headers with quotes,** as in `#include "cow.hpp"`, and standard ones with angle brackets, as in `#include <iostream>`.
- **A `.cpp` file includes its own `.hpp` file,** so the compiler checks that the definitions match the declarations.
- **Changing a header** means recompiling every `.cpp` file that includes it.
- **A forward declaration** (e.g., `void printMoos(int numMoos);`) is enough to call a function defined in another file. In practice, put it in that file's header instead.

# Include Guards

Every header starts and ends with an include guard, so including it twice in one file doesn't define things twice:

```c++
#ifndef PI_HPP_INCLUDED
#define PI_HPP_INCLUDED

constexpr double PI = 3.1415926535897932;

#endif  // PI_HPP_INCLUDED
```

The first time the header is included, `PI_HPP_INCLUDED` isn't defined yet, so `#ifndef` ("if not defined") keeps everything up to `#endif`, and `#define` defines it. Any later time, it's already defined, so the preprocessor skips the whole header. Name the guard after its file, so that each header's guard is different.

# Preprocessor Macros

`#define MACRO_NAME replacement text` tells the preprocessor to replace every `MACRO_NAME`, as a whole word, with `replacement text` before compiling. With no replacement text (as in an include guard), it just marks the name as defined. Macro names are in all caps by convention.

| Directive | Does |
|---|---|
| `#include "file"` | Pastes in the contents of `file` |
| `#define NAME text` | Replaces `NAME` with `text` from here on |
| `#ifndef NAME` … `#endif` | Keeps the lines between only if `NAME` isn't defined |
| `#ifdef NAME` … `#endif` | Keeps the lines between only if `NAME` is defined |
| `#if condition` … `#endif` | Keeps the lines between only if `condition` is true |

# Tools and Tips

- **Start with the first compiler error.** Later errors are often caused by the first, and fixing it can make them go away.
- **Valgrind** finds memory errors, like reading freed memory or leaking it, by running your program and watching every memory access.
- **cpplint** checks that code follows Google's C++ style guide.

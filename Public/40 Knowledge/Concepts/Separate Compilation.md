---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Compilation Stages
  - Linking
  - Object File
  - Header File
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Separate compilation** builds a program from several source files by compiling each file on its own into an **object file**, then **linking** the object files together into one executable.

Turning C++ source into an executable takes four stages:

| Stage | Does | Input | Output |
|---|---|---|---|
| Preprocessing | Carries out the lines starting with `#` (e.g., pasting in the contents of each `#include`d file) | A source file (`.cpp`) and the headers it includes (`.hpp`) | One big file of C++ source (`.ii`) |
| Compilation | Checks the code and translates it into assembly language | Preprocessed source | Assembly (`.s`), for a processor such as AMD64 or ARM64 |
| Assembly | Translates the assembly language into machine code | Assembly | An object file (`.o`) |
| Linking | Joins object files and libraries into a program the computer can run | Object files and libraries (`.o`, `.a`, and `.so`) | An executable |

The first three stages work on one source file at a time, and only linking sees the whole program. Compilation is where most errors are reported: it checks syntax, makes sure each name is used within its [[Scope|scope]], and handles types, which also tells it how much memory each variable needs.

Because compilation sees only one file, a file can call a function defined in another file only if it first declares that function: it states the function's name and type, and the linker finds the definition later (see [[Declaration and Definition]]). Writing these declarations in every file that needs them would repeat them, so they go in a **header file** instead, which each file that needs them includes. A header holds declarations, and its own source file holds the definitions. A header is never compiled on its own: it's pasted into each source file that includes it. So a change to a header means recompiling every source file that includes it, which is the kind of bookkeeping [[Build Automation|build automation]] handles.

Separate compilation pays off in two ways. Changing one source file means recompiling only that file and relinking, not recompiling the whole program, and a program's parts can be written and compiled by different people.

More generally, most compiled languages separate compiling from linking, though not always with C++'s four visible stages: Java compiles each class to its own `.class` file and links them while the program runs, and Rust compiles a whole crate at once. C and C++ headers are textual inclusion, which is why a large header slows down every file that includes it. C++20's modules replace them with compiled interfaces that each file imports instead of pasting in.

# Examples

## Compiling Two Files

`cowchat.cpp` calls `printMoos`, which is defined in `printmoos.cpp`. Compiled alone, `cowchat.cpp` fails, since the compiler has never seen `printMoos`. A declaration of it fixes that:

```cpp
// cowchat.cpp
#include <iostream>
#include <string>

void printMoos(int numMoos);   // declared here, defined in printmoos.cpp

int main() {
    std::string userIn;
    do {
        std::cout << std::endl << "> ";
        std::getline(std::cin, userIn);
        printMoos(1 + userIn.size() % 2);   // 1 or 2 moos
    } while (std::cin.good() && userIn != "");
    return 0;
}
```

Each file is compiled to an object file, and the two are linked:

```
clang++ -c cowchat.cpp        # cowchat.o
clang++ -c printmoos.cpp      # printmoos.o
clang++ -o cowchat cowchat.o printmoos.o
```

`cowchat.o` contains a call to `printMoos` with no code for it. Linking matches that call to the definition in `printmoos.o`. In practice, the declaration goes in `printmoos.hpp`, which `cowchat.cpp` includes (see [[Compiling C++]]).

# Connections

- [[Declaration and Definition]]: what lets one file use a function another file defines
- [[Build Automation]]: recompiling only the files a change affects
- [[Interpreter]]: the alternative to compiling, which runs a program's abstract syntax directly
- [[Static and Dynamic Typing]]: compilation is where C++'s type errors are caught

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: reference
created: 2026-11-23
updated: 2026-11-23
topic: c++
---
Make's syntax for building a C++ program. Running `make` in a folder reads its `Makefile` and runs the commands needed to bring the first target up to date, skipping any whose target is already newer than its prerequisites (see [[Build Automation]]).

# Rules

```make
target: prerequisites
	commands
```

"If any of these prerequisites change, then this target needs to be updated by running these commands." **Each command line must start with a literal tab**, not spaces, or Make reports a "missing separator" error.

A Makefile for an executable built from two files:

```make
generateSegfault: generateSegfault.o helloSayer.o
	clang++ -o generateSegfault -g -std=c++17 -pedantic -Wall -Wextra generateSegfault.o helloSayer.o

generateSegfault.o: generateSegfault.cpp helloSayer.hpp
	clang++ -c -g -std=c++17 -pedantic -Wall -Wextra generateSegfault.cpp

helloSayer.o: helloSayer.cpp helloSayer.hpp
	clang++ -c -g -std=c++17 -pedantic -Wall -Wextra helloSayer.cpp
```

An object file's prerequisites are its `.cpp` file and every header it includes, so changing a header recompiles everything that uses it.

| Command | Does |
|---|---|
| `make` | Brings the first target in the Makefile up to date |
| `make target` | Brings `target` up to date |

# Phony Targets

A phony target names a task instead of a file. Declare it with `.PHONY`, so a file that happens to share its name doesn't stop it from running:

```make
.PHONY: all clean

all: generateSegfault

clean:
	rm -rf *.o generateSegfault
```

- **`all`** lists every executable as a prerequisite and runs no commands. Put it first, so a bare `make` builds everything.
- **`clean`** deletes everything the build generated (i.e., object files and executables).

# Variables

`NAME = some text` defines a variable, and `$(NAME)` is replaced by `some text` wherever it appears. Use them so a change, like switching to `g++`, happens in one place:

| Variable | Holds, by convention |
|---|---|
| `CXX` | The C++ compiler (e.g., `clang++`) |
| `CXXFLAGS` | The compiler's flags (see [[Compiling C++]]) |

Make also sets these in every rule:

| Variable | Is |
|---|---|
| `$@` | The target |
| `$<` | The first prerequisite |
| `$^` | All the prerequisites |

The same Makefile with variables:

```make
CXX = clang++
CXXFLAGS = -g -std=c++17 -pedantic -Wall -Wextra

.PHONY: all clean

all: generateSegfault

generateSegfault: generateSegfault.o helloSayer.o
	$(CXX) -o $@ $(CXXFLAGS) $^

generateSegfault.o: generateSegfault.cpp helloSayer.hpp
	$(CXX) -c $(CXXFLAGS) $<

helloSayer.o: helloSayer.cpp helloSayer.hpp
	$(CXX) -c $(CXXFLAGS) $<

clean:
	rm -rf *.o generateSegfault
```

`$<` is the `.cpp` file, since it's listed first, so the headers after it are prerequisites without being passed to the compiler.

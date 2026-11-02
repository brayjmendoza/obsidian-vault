+ The Makefile is a configuration file that contains shell commands specifically for compilation. When we run `make` in the CLI, it looks for `Makefile` and runs the appropriate commands.
	+ `make` is a command we can use to compile our code
		+ Detects when changes have not been made and skips unnecessary commands for recompilation
		+ Operates recursively, if we try to make an executable where one of the source code files are changed, it will recompile that file
+ We specify rules in the Makefile
	+ "if any of these \<prerequisites> change, then \<target> needs to be updated by running one or more \<commands>."

## General Format
```
<target>: <prerequisites>
	<commands>
```
**Note:** There <u>must</u> be a literal tab character before the commands (spaces won't work)
##### Example:
```
generateSegfault: generateSegfault.o helloSayer.o
    clang++ -o generateSegfault -g -std=c++17 -pedantic -Wall -Wextra generateSegfault.o helloSayer.o

generateSegfault.o: generateSegfault.cpp helloSayer.hpp
        clang++ -c -g -std=c++17 -pedantic -Wall -Wextra generateSegfault.cpp

helloSayer.o: helloSayer.cpp helloSayer.hpp
    clang++ -c -g -std=c++17 -pedantic -Wall -Wextra helloSayer.cpp
```

## Phony Targets
Phony targets aren't actually names of files (unlike usual targets), but rather a name for a recipe to be executed when making a explicit request. 

There are two major phony targets:
+ `clean`
	+ Gets rid of all generated files (i.e. `.o` files and executables)
	+ Example (where `generateSegfault` is our main exectuable)
		+ `rm -rf *.o generateSegfault`
+ `all`
	+ Has all relevant programs as prerequisites, but runs no commands itself 
	+ Ensures all prerequisites (of the main executable) are up to date 
		+ Doesn’t do anything else 
	+  It is idiomatic for `all` to be the _first_ target in a Makefile, so that running `make` will bring all executables up to date.
		+ `make` implicitly runs the first rule in the Makefile
	+ Example (where `generateSegfault` is our main exectuable)
		+ `all: generateSegfault

## Macros (reduce redundancy)
Makefiles can be redundant. For example, if we wanted to change our compiler from `clang++` to `g++` we would have to change it for every rule. We use macros to address this

In general, the following is a macro:
> `VARIABLE=some text`

Now, `$(VARIABLE)` will be replaced by `some text` anywhere in the Makefile
##### Example:
```
CXX = clang++
CXXFLAGS = -g -std=c++17 -pedantic -Wall -Wextra

generateSegfault: generateSegfault.o helloSayer.o
    $(CXX) -o generateSegfault $(CXXFLAGS) generateSegfault.o helloSayer.o

generateSegfault.o: generateSegfault.cpp helloSayer.hpp
        $(CXX) -c $(CXXFLAGS) generateSegfault.cpp

helloSayer.o: helloSayer.cpp helloSayer.hpp
    $(CXX) -c $(CXXFLAGS) helloSayer.cpp

clean:
    rm -rf *.o generateSegfault
```
+ `CXX` is the macro for the compiler
+ `CXXFLAGS` is the macro for compiler options

### Special Macros
`make` predefines some macros based on targets and prerequisites:
+ `$@`: The target
+ `$<`: The first prerequisite
+ `$^`: All of the prerequisites
+ [More special macros](https://users.cs.duke.edu/~ola/courses/programming/Makefiles/node7.html#SECTION00016000000000000000)
##### Example:
```
CXX = clang++
CXXFLAGS = -g -std=c++17 -pedantic -Wall -Wextra

generateSegfault: generateSegfault.o helloSayer.o
    $(CXX) -o $@ $(CXXFLAGS) $^

generateSegfault.o: generateSegfault.cpp helloSayer.hpp
        $(CXX) -c $(CXXFLAGS) $<

helloSayer.o: helloSayer.cpp helloSayer.hpp
    $(CXX) -c $(CXXFLAGS) $<

clean:
    rm -rf *.o generateSegfault
```
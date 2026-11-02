## Stages
1. Preprocessing
    - Deals with preprocessor directives (commands to the preprocessor) to make one big file of C++ source code
	    - These are lines of code that start with `#`
		    - e.g. `#include`s
    - Input: Source File
        - Written in C++ (`.cpp` or `.hpp` files)
    - Output: Edited C++ source code
        - "One big file" where the contents of included files are pasted in
2. Compilation
    - Figures out what the program is trying to do and writes assembly code
    - Input: Preprocessor Output
        - Edited C++ Source or `.ii` files
    - Output: Assembly language
3. Assembly
    - Turns the machine instructions into an object file
    - Input: Assembly Language
        - AMD64 or ARM64 code, or `.s` files
    - Output: an object file
4. Linking
    - Gathers together all `.o` files as well as the C++ standard library to make an executable the computer can actually run
    - Input: Object File(s) & Libraries
        - `.o`,`.a`, and `.so` files
    - Output: an executable


## Responsibilities
- Checking syntax
- Handling variable names
    - Making sure everything is in the right scope
- Handling types
    - To figure out how much memory needs to be allocated

Any issues here will cause compilation errors!
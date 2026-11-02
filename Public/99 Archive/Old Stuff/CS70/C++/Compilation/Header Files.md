Header files only contain declaration statements. These files are then included in source files for compilation to avoid errors as a result of missing declarations. 

Header files *are not* compiled, they are simply included in source files.
If a header file is changed, then you have to recompile all sources files that include it.

**Notes:**
- Header files have the file extension `.hpp`, while source files have the file extension `.cpp`
- When including `.hpp` files, use quotes not angled brackets. (e.g. `#include "file.hpp"`)
- It's best practice for a `.cpp` file to include it's own `.hpp` file to prevent errors as a result of calling functions before they are declared (within their own `.cpp` file)

## Multiple Declarations Error
When `#include`'ing files, you may unintentionally declare a variable multiple times, causing a compilation error
##### Example: 
`pi.hpp`
```
constexpr double PI = 3.1415926535897932;
```

`tau.hpp`
```
#include "pi.hpp"

constexpr double TAU = 2*PI;
```

`circles.cpp`
```
#include "pi.hpp"
#include "tau.hpp"

double circumference(double radius) {
    return TAU * radius;
}

double area(double radius) {
    return PI * radius * radius;
}
```
In `circles.cpp`, `PI` gets declared twice

## Include Guards
Used to prevent multiple declarations as a result of `#include`'ing multiple files
### Example with Include Guard:
`pi.hpp`
```
#ifndef CONSTANTS_HPP_INCLUDED
#define CONSTANTS_HPP_INCLUDED

constexpr double PI = 3.14159265358979;

#endif
```
Here, `pi.hpp` uses preprocessor directives/macros to prevent `PI` from being defined if it has already been defined (which could happen from including a file that already defined it)
#### Explanation:
```
#ifndef CONSTANTS_HPP_INCLUDED`

...stuff...

#endif
```
`#if`, `#ifdef`, `#ifndef` are conditional preprocessor directives that run `...stuff...` if the given condition is met

+ `#ifndef` - if not defined
	+ `...stuff...` will run if `CONSTANTS_HPP_INCLUDED` is not defined, otherwise it won't
	+ For header files, `...stuff...` are declarations, so if `CONSTANTS_HPP_INCLUDED` is not defined, then all of the declarations will be made

`#define CONSTANTS_HPP_INCLUDED`
+ Replaces `CONSTANTS_HPP_INCLUDED` with nothing (empty string) if it is found in the file
	+ For the include guard, we use this to define `CONSTANTS_HPP_INCLUDED` so if this file is `#include`d multiple times, it won't make multiple declarations

##### Preprocessor Macros - More in Depth
`#define` `MACRO_NAME` _`replacement text`_ creates a _text-substitution macro_ for the preprocessor.
- Essentially, a search-and-replace instruction that looks for `MACRO_NAME` (as a distinct word, not a string) in the file and replaces it with _`replacement text`_ before compilation
- `MACRO_NAME` is in all caps by convention
	- Preprocessor macros are by convention in all caps
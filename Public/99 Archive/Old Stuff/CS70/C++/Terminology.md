**Undefined behavior:**  Anything could happen in the code
**Indeterminate Values:** A value that is unspecified
+ The value is usually whatever leftover bits are already in the memory

## Terms for Allocating Memory
- **Static allocation** 
	- Memory that is allocated for the entire duration of the program (e.g., a `static` data member in a class—there isn't a separate one for each object of that class, there is exactly one for the entire program)
- **Automatic allocation** 
	- Memory allocated on the stack (because it is allocated/deallocated automatically when functions begin/end)
- **Dynamic allocation:** 
	- Memory allocated on the heap (because the allocation is "dynamically" determined at runtime as opposed to compile time)

## Classes
![[JavaPythonToC++.png]]
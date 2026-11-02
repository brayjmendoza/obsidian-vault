There are five phases of an object's lifetime:
+ **Allocation:** Acquire memory for the object
+ **Initialization:** Get the object into a useable starting state
+ **Use:** Access the object (for printing, passing to a function, changing its value, etc.)
+ **Destruction:** Clean up the memory for the object
+ **Deallocation:** Give the object's memory back

### General Rules:
+ A program starts at the `main` function
+ Allocation
	+ When <u>reaching the opening curly brace of a function</u>, all local variables for that function are allocated
	+ Stuff can only be allocated **once**
+ Initialization
	+ When you <u>reach a variable declaration</u>, that variable is initialized
	+ Stuff can only be initialized **once**
+ Use
	+ When <u>a variable's value changes</u> the value in the memory is overwritten with the new value
	+ Examples:
		+ `int y = x; // y is being initialized, but x is being used!`
		+ `printMoos(x);  // Another use of x`
		+ `x = 5; // the value 5 is copied into the memory                     // representing x`
	+ More info on [[Object Use|use for objects (from classes)
+ Destruction
	+ When you <u>reach a closing curly brace</u>, all variables declared in the block being closed are destroyed
		+ The variable names can no longer be used in the program
	+ A well-formed program (no memory errors) should only be destroyed **once**
	+ More info on [[Destructors|destruction for objects]]
+ Deallocation
	+ When you <u>reach the closing curly brace of a function</u>, all local variables in that function are deallocated
		+ All memory that was allocated for the function is now free memory that can be reallocated for future functions
	+ A well-formed program (no memory errors) should only be deallocated **once**

### Additional Notes
+ For an array of length $N$, all of the 5 phases happen $N$ times, once for each element of the array (in order)
+ For references, nothing extra happens, since they are just aliases to something that already exists
+ For data members of an object, they go through the lifetime as the object they exist in goes through it
	+ Space is allocated for them when memory for the object is allocated
	+ They are initialized when an object is initialized
	+ They are used as the object is used
	+ They are destroyed when the object is destroyed (in reverse order from what they're declared in the class definition)
	+ They are deallocated when the object is deallocated
### Summary
![[ObjectLifetime.png]]
Variables/function with a pointer type hold the memory address for the variable/function

**Example:**
> `float* start = vals;`
+ Here, `start` is a *pointer to a float*
+ Alternatively, `start` is a memory address for a location in memory where we will find a float

## Default-Initialized Pointers
+ Pointers are a primitive type, so if not initialized, it will be indeterminate
+ Default-initialized pointers are *invalid*
	+ You can't (shouldn't) apply `*` on it because you don't know what would happen
	+ Following an invalid pointer leads to undefined behavior

### Additional Notes
+ `*` in a type means the type is a pointer, while `*` in a value is the [[Memory Operators|indirection operator]]
+ Pointers are a primitive type
	+ When a pointer variable is destroyed, nothing (observable) happens


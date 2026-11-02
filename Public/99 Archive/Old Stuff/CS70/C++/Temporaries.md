Whenever C++ invokes a function/operator that returns a value, or directly invokes a constructor, if the resulting value is not put directly into a known memory location (e.g. a named variable), it gets stored as a *temporary* value.
+ This value is a short-lived unnamed variable that exists only for the duration of that line of code

**For example**, for a function `passByRef` that takes in an `int`:
```
passByRef(x+y)
```
can be modeled as 
```
{
    int _temp1 = x+y;
    passByRef(_temp1);
}
```

## How Functions Return Result Values
The last example shows that at most one function call happens at a time, and intermediate results are stored in hidden temporary variables
+ Thus, *every function call that returns a value is actually initializing a new object in memory* (running a constructor to make an instance of a class or copy initializing a primitive type)

For a function call that returns a value:
- The _caller_ will have _allocated space_ somewhere in its stack frame to store the result
- Behind the scenes, the caller tells the called function (a.k.a. “the callee”) where that space is
- The _called function_ then _initializes_ that space (usually when it `return`s)
- The _caller_ is responsible for _destroying_ the result and eventually _deallocating_ it

So, `return` is actually initializing an object in the caller
+ `return val` copy initializes an object
+ `return {}` causes the object to be default initialized
+ `return {arg1, arg2, arg3, ...}` can be used to call a specific constructor

## Additional Terminology:
- An **lvalue** can be thought of something like a variable that has an associated memory _**L**ocation_.
- An **rvalue** can be thought of as a “result” value, or a _tempo**R**ary_ value.
	
	- We may see **lvalue** or **rvalue** in error messages when trying to get the memory address of a temporary (e.g. `int* p = &(x + y);`)
	- These can also be thought of as left/hand right side (e.g. `x = y + z`)
		- Left hand side needs to be something that has location in memory so we can write it a new value
		- Right hand side is the result of an expression
# Primitive Types
We can initialize primitive types with an explicit value, or let it be default initialized (have an indeterminate value)
### Default Initialization
```
// Default-initialize x -- danger indeterminate (possibly weird) int // value!
int x;

// Default-initialize y -- danger indeterminate (possibly weird) float // value!
float f;

// Default-initialize b -- DANGER indeterminate (possibly INVALID)   // bool value!!!
bool b;
```
### Copy Initialization (initialize with explicit value)
```
int x = 5;     // Copy-initialize x with 5   -- Looks like assignment                 //                               but isn't
float f{4.2};  // Copy-initialize y with 4.2 -- Alternative brace-                    //                               based syntax
```
During copy initialization, the given value is *copied* into the memory representing the variable
##### Example (with a function):
```
float myFun(int x, float f) {
    return x + f;
}

float result = myFun(5, 4.2);
```
+ The parameters `x` and `f` in `myFun` are copy initialized with the values of the arguments (`5` and `4.2` in this example)
+ `result` is copy initialized from the return value `x + f`
+ The same is true for parameters and return values that are objects

### The `auto` Keyword
If you declare a variable with `auto`, then it will have the type of whatever variable it's initialized with
+ The variable <u>cannot</u> change type during runtime
+ Compiler will figure out variable type at compile time

+ `auto` can declutter code
	+ Example: pointers in for loops that use begin/past-the-end pointers
+ Use sparingly (`auto` is not always good for readability)

#### General Rules:
+ Use `auto` when it improves readability, such as when the type is
	+ Complicated
	+ Genuinely doesn't matter
	+ Clear from context
+ Avoid using `auto` when the type is
	+ Simple and known
	+ Important for understanding the code
	+ Unclear from the context
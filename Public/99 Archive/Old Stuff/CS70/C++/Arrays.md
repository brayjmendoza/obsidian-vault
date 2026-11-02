## Fundamental Properties of Primitive Arrays
All arrays are contiguous, ordered, homogenous, fixed-size storage
+ **Contiguous**
	+ The items in the array are all together in memory with no gaps
+ **Ordered**
	+ The elements in an array have a clear order to them
	+ We know which one is "first" and which one is "forty-second"
+ **Homogenous**
	+ The elements of an array all have to be the same *type*
+ **Fixed-Size**
	+ Once we create an array, we can't change the number of things it can hold

## Declaring Arrays
Similar to declaring a single value, but we include a size
> `int values[42];`
+ Creates an array of integers called values with 42 int's

A size must be specified!
> `int values[];`
+ This will cause a compilation error

Since arrays are fixed-size if we use variables to declare the size they have to be `constexpr`
> `size_t numberOfValues = 3;`
>`int myArray[numberOfValues];`
+ This is a compilation error (a `size_t` could change, messing up the array)

Instead,
> `constexpr size_t numberOfValues = 3;`
> `int myArray[numberOfValues];`
+ Will work because `constexpr` tells the compiler that the variable should be known at compile time and does not change during runtime
	+ Otherwise, an error would be generated

You can also initialize values:
> `int oneTwoThree[3] = {1,2,3};`
> `int fourFiveSix[3]{4,5,6};`
+ Both are valid

## Accessing Arrays
+ Can use the indirection operator `*`
+ Can use brackets `[i]` where `i` is the index
+ You could "access" indices outside the bounds of the array, but this causes undefined behavior

## Memory
+ Allocation
	+ A slot of memory is allocated for each element in the array
	+ As a whole, the `n` number of elements for the array appear next to each other (contiguous) in memory
	+ Arrays are fixed-size so the compiler knows how much space to allocate on the stack
+ Value of `a` where `a` is an array
	+ You would get the memory address of the first item of the array

## Dynamically Allocated Arrays
Since heap memory is allocated whenever we want, we can use a non-`constexpr` variable for the array size
#### Example: Asking for Array Size from User Input
```
size_t numElements;
cin >> numElements;
int* arr = new int[numElements];
```
Since `arr` is initialized on the heap, it's okay that `numElements` is not a compile-time constant
+ The address that's returned from `int* arr = new int[numElements];` is the first element of the array, so you can index as usual
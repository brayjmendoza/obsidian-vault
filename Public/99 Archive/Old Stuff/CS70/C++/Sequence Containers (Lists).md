C++ provides different data structures for lists

## `std::vector`
A vector is a dynamically-sized array that uses dynamic allocation
#### Syntax
> `std::vector<double> values;`
+ Creates a vector of doubles called `values`
+ Has size 0

> `std::vector<double> values(100);`
+ Creates a vector of doubles called `values`
+ Has size 100, all values set to `0.0`

> `std::vector<int> favorites{42, 54, 7};`
+ Creates a vector of ints called `favorites`
+ Has size 3, with values `42`, `54`, and `7`
+ The curly braces `{}` are used to provide initial values for the elements

The `std::vector` is a generic, meaning you can create a `std::vector` of any type
+ The type of the vector is specified in the angled brackets `<...>`
#### Member Functions for the Size of a Vector
The `std::vector` knows what size it is (we don't have to specify a size ahead of time)
+ `size()` - returns how many elements are stored in the vector
+ `capacity()` - returns the size of the primitive array used behind-the-scenes for this vector
	+ To avoid having to resize often, a resized vector uses a larger array behind-the-scenes so that multiple empty spaces will have to be filled before needing to resize again
+ `reserve(n)` - tell the compiler to set aside a specific capacity
	+ Use if we know that an array has to be a certain size
	+ Reduces the need to resize and copy
+ `shrink_to_fit()` - throw away spare space in the vector
	+ Use if we know an array won't grow any further
#### Adding, Removing, and Getting Elements
+ `push_back(e)` - adds a new element `e` to the end of the vector
	+ Adds to the array's size
	+ May reallocated and move all contents of the array to a new array if there isn't enough capacity in the underlying primitive away
	+ If you try to push a different type, [[Promotion and Conversion]] rules will be used
		+ Compiler error if promotion/conversion can't occur
+ `pop_back()` - removes the end element
	+ <u>Does not</u> return the removed element
+ `insert` - insert an element into an array wherever is specified
+ `erase` - get rid of an element at a specified spot in the array

+ `.back()` - return the back element
+ `.front()` - return the front element
	+ Both `.back()` and `.front()` return a reference to the element which we can modify
		+ `values.back() = 7.3` changes the last element to `7.3`
+ `operator[]` - access elements (like in an array)
	+ `values[3]` accesses the fourth element of the array (element at index 3)

#### More Member Functions
+ `begin()` - return a pointer to the first element in the array
+ `end()` - return a past-the-end pointer
+ `swap` - swap the contents of two vectors (in constant time)


# `std::list`
+ A doubly linked list
+ Is generic (just like vector)
	+ Has the same syntax as `std::vector`
+ Supports [[Iterators|iterators]] and uses them to traverse through the list
	+ More specifically, a bidirectional iterator
		+ Can only go forward or backward (and not an arbitrary point in the list)
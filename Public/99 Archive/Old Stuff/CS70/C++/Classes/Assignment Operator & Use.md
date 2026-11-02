The way an instance of class can be used is defined by the class's *interface*

During use you can:
+ Access and use public member variables
+ Call public member functions
+ Make copies using a copy constructor
+ Pass it as an argument to a function

# Assignment Operator
Changes one existing instance of class to look exactly like another existing instance of the class.

The assignment operator for classes is a member function
> `operator=(const Cow& other);`
+ Similar to default and copy constructors, either we write it, the compiler writes it, or we specify we don't want one at all
	+ `operator=(const Cow& other);` - we will write it
	+ `operator=(const Cow& other) = default;` - the compiler writes it
		+ Goes through each data member in the class and sets the new object to the `other` object's data members
			+ `other` is on the right side of the equal sign
	+ `operator=(const Cow& other) = delete;` - no one writes it

### Example:
```
Leopard sabor{40};      // Sets sabor's spots_ = 40
Leopard siri{42};       // Sets siri's spots_ = 42

sabor = siri;           // Assign siri to sabor
```
`sabor = siri` implicitly calls the assignment operator
+ Note that this is the same syntax used for [[Constructors|copy constructing]]

**Remember:**
+ The **copy constructor** is used to *initialize a brand-new object*, making it a copy of an existing object.
+ The **assignment operator** is used to _change_ an _existing object_, making it the same as another existing object.

### Writing our Own Assignment Operator
We usually want to write our own assignment operator when we have to deal with memory allocated on the [[The Heap|heap]].
+ The synthesized constructor will create a **shallow copy**, which violates the [[Design & Programming Principles|ownership principle]].

With the assignment operator, we want to overwrite an object with another object's data. So, for objects with stuff on the heap, we will first have to destroy the existing data, and then allocate new memory for the new data that we're copying from the other object
```
void Barn::operator=(const Barn& other) {
	// check for self assignment
	// If this == &other, then these Barns are at the same address!
    if (this == &other) { 
        return *this;
    }
    
    // First clean up memory currently in use (code from the destructor)
    for (Cow**p = residentCows_; p < residentCows_ + cowCount_; ++p) {
        delete *p;
    }
    delete[] residentCows_;

    // Now set up memory for the new data (code adapted from copy constructor)
    cowCapacity_ = other.cowCapacity_;
    cowCount_ = 0;
    residentCows_ = new Cow*[cowCapacity_];

    for (size_t i = 0; i < other.cowCount_; ++i) {
        // Fetch pointer to the Cow we want to copy from the array
        Cow* otherCowPtr = other.residentCows_[i];
        // Make a copy.
        addCow(*otherCowPtr);
    }

	return *this;
}
```
This is an example of an assignment operator for the `Barn` class, where `residentCows_` are stored on the heap.

##### `return *this`
The C++ standard requires assignment operators to support the chain assignments
(e.g. `x = y = z = 3`)
+ Thus, the assignment operator has to return a reference to a `Barn`
	+ The return type will be `Barn&`, and we just have to return the current object
		+ `*this` returns the current object because [[The this Pointer|this]] is a pointer to the current object
##### Note on self-assignment
To support functionality like `x = x`, we have to put the first `if` statement there. Otherwise, we will destroy stuff on the heap, then try to use the deallocated memory to reassign – this would break things horribly!
+ So, if we're doing self-assignment, we can simply return `*this` (the current object)

#### Copy and Swap Idiom
The previous code had some code duplication. We can use `std::swap` to make the function cleaner
```
Barn& Barn::operator=(Barn other) {
    // Copy-and-swap idiom
    std::swap(cowCapacity_, other.cowCapacity_);
    std::swap(cowCount_, other.cowCount_);
    std::swap(residentCows_, other.residentCows_);
    return *this;
}
```
Does the same as the previous code. Here's how it works
+ For the parameter, we use `Barn other`, so we are duplicating the `Barn` on the right-hand side
	+ We pass `other` by value rather than constant reference in `swap`
+ With `swap` we swap all the data members between the current object's data members and `other`s data members
	+ All of the old data ends up in `other`, all of the new data is now in the current object
+ Since `other` was a copy (and not a reference), when the function ends `other` is destroyed (along with all of the old data we don't want)
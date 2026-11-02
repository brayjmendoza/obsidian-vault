`static` members are properties of the class and not individual instances of the class
+ They are shared across all instances of a class
+ We only specify if a member is `static` in the header file
### Example:
```
// cow.hpp

class Cow {
    ...
    // Static compile-time constants, declaration AND definition
    static constexpr int MAX_LEGS = 4;  

    // Static variables and functions; declaration only 
    // (needs def in .cpp file)
    static size_t totalCowsEver;          
    static void openCowWikipediaPage();   // function that doesn't                                               // require a cow
    ...
};
```
+ Compile-time constants (`MAX_LEGS` in this example) only need to be given in the class definition (in header file)
+ Variables and constants are declared in the header file, but still need to be defined in the source file

### Using `static` Members
We use the scope resolution operator `::` to access `static` members
> `Cow::MAX_LEGS` 

NOT
> `bessie.MAX_LEGS` where bessie is a `Cow`

## Additional Notes
+ There is exactly *one* copy of a `static` member and all instances of a class share it (no matter how many instances there are)
+ If a member function doesn't need a `this` object, it can be declared as `static`
	+ Notes that `this` is passed around in normal member functions so they could have access to this instance's member variables/functions
+ We only put `static` when declaring the function in the class definition (`.hpp` file)
	+ We don't need to say `static` again in the implementation (`.cpp` file)
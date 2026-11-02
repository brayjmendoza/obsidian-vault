A *constructor* is used to create an instance (i.e. object) of a class
+ Constructors initialize objects
+ It's main job is to **initialize the member variables** of the object being constructed

## Parameterized Constructors
Constructors that have parameters. These must be explicitly invoked
#### Example:
```
class Cow {
  public:
    // parameterized constructor
    Cow(int numSpots, int age);
...
}

int main() {
	// explicit invocations of the parameterized constructor
    Cow bessie{3, 12};
    const Cow mabel{1, 2};
```


## Default Constructors
The **default constructor** is the constructor with no parameters.
In the class definition, we would write it as:
> `Sheep();`

It can be invoked explicitly:
> `Sheep mead{}`

Or it can be invoked implicitly with default initialization. The default constructor is used for default initialization:
> `Sheep mead;`
+ This is not uninitialized, null, none, indeterminate, etc.

> `Sheep herd[10];` 
+ Creates an array of `Sheep` objects, each of which are created with the default constructor

**Every class has a default constructor, even if you don't define one**
+ If not defined, the compiler creates a default constructor that initializes the member variables as shown in the class definition
	+ If member variables were not initialized in the class definition
		+ Primitive types (`int`, `double`, etc.) would be indeterminate
		+ Objects would be initialized with their default constructors
	+ We can explicitly tell the compiler to create the constructor with `default`
		+ `Sheep() = default;`

**`delete`** keyword
+ If we <u>do not</u> want a default constructor, we use `delete`
```c++
class Cow {
 public:
    // tells C++ that the Cow class should not have a default              // constructor
    Cow() = delete;

	// other constructors...

    ...
```
+ Attempting to create a Cow here with the default constructor would result in a compile error


## Copy Constructors
The **copy constructor** is a parameterized constructor that takes a `const` reference to an object of the same class.
+ It is used for [[Initialization|copy initialization]] of objects.
+ These constructors initialize new objects to be just like the one that's passed in
+ **Note:** We need to define what it means to make a copy of class because that determines what it means for objects to be passed in as parameters and returned from functions

Like default constructors, if we don't write a copy constructor, the compiler will synthesize one for us.
+ The synthesized copy constructor will copy initialize all member variables using the member variables of the object passed in 
+ We can explicitly tell the compiler to synthesize a copy constructor with `default`
	+ `Cow(const Cow& other) = default;`
+ If we don't want a copy constructor, we can use `delete`
	+ `Cow(const Cow& other) = delete;`
	+ This is very similar to the [[Assignment Operator & Use|assignment operator]]
### Example:
> `Cow(const Cow& other);
+ This constructor would be used to create new `Cows` that behave the same as the `Cow` that is passed in
#### Implementation:
```c++
Cow::Cow(const Cow& other) :
    age_{other.age_},
    numSpots_{other.numSpots_} {
    // Nothing else to do
}
```

### Shallow & Deep Copies
If we use the synthesized copy constructor for instances of classes that have stuff on the heap, we will end up with a **shallow copy**
+ The synthesized constructor copies over member variables, so the variables that store pointers to the heap will store the same pointer
	+ Thus, both the original and the copy will point to the same data in the heap, meaning that the share that data (this is a shallow copy)
		+ Violates the [[Design & Programming Principles|principle of ownership]]

We fix this issue with a **deep copy**, which requires us to write our own copy constructor
+ Goes through and makes copies of all the heap memory, so that we'll have truly separate instances of classes

##### Example: Barn
```c++
Barn::Barn(const Barn& other) :
    cowCapacity_{other.cowCapacity_},
    cowCount_{other.cowCount_},
    residentCows_{new Cow*[cowCapacity_]}
{
    for (size_t i = 0; i < other.cowCount_; ++i) {
        // Fetch pointer to the Cow we want to copy from their array
        Cow* otherCowPtr = other.residentCows_[i];
        // Make a copy.
        Cow* duplicateCowPtr = new Cow{*otherCowPtr};
        // Store it in our array.
        residentCows_[i] = duplicateCowPtr;
    }
}
```
A `Barn`'s member variables are the maximum number of `Cow`s it can hold (`cowCapacity_`), the current number of `Cow`s in the barn (`cowCount_`) and an array (`residentCows_`) of pointers (on the heap) to `Cow`s (also on the heap)
+ This copy constructor we made makes a **deep copy**
+ We could also leverage member functions already defined (e.g. `addCow()`) when copying (if applicable)

## Constructing Objects
#### Curly Brace Initialization
Both of the following are valid ways to use a constructor to create objects
```c++
Cow bessie{3, 12};
const Cow mabel{1, 2};
```
and
```c++
Cow bessie(3, 12);
const Cow mabel(1, 2);
```

However, the curly braces `{}` are stricter
+ C++ usually performs both conversions and promotions on arguments passed in parentheses
+ Curly braces only allow for promotions, NOT conversions (where data can be lost)

For copy initialization, you could use `=` or `{}`
```c++
// both Sheep are copy initialized
Sheep dolly{fluffy};   // dolly is initialized to be a copy of fluffy,
Sheep denise = dolly;  // denise is a copy of dolly
```

## Member Initialization Lists
+ When initializing an object, all of its member variables need to be initialized
+ We can refer to member variables inside the body of a constructor
+ However, we cannot use a variable until it's initialized
+ So, we must initialize member variables before entering the body of a constructor
	+ This is done with **member initialization lists.**
#### Example:
```
Cow::Cow(int numSpots, int age)
    : numSpots_{numSpots},
      age_{age}
{
    cout << "Made a cow with " << numSpots_ << " spots!" << endl;
}
```
+ `numSpots_` and `age_` are member variables for the `Cow` class
+ The member initialization starts at the colon after the function header and ends at the opening curly brace of the function 
	+ This list initializes all of the member variables (before the constructor body!)
		+ These are not initialized in the constructor body, because then they would be destroyed at the closing curly brace of the constructor
	+ Having the member initialization list here makes the scope span the entire class (not just the body of the constructor)
### Rules
+ **Ordering:** member variables must be initialized in the same order they are declared in the class definition
+ **Missing Variables:** If a member variable doesn't appear in the member initialization list, it will be initialized as specified in the class definition
### Additional Notes
+ You can invoke another constructor in the member initialization list
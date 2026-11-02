# Member Variables
Each object of class stores its own data (that defines it's properties). These data are known as *data members* or *member variables* (these terms are interchangeable).

We can refer to member variables in member functions by name. All member variables exist in the scope of the entire class.
##### Example:
```
void Cow::setAge(int age) {
    age_ = age;
}
```
This sets the age of the Cow. `age_` is the member variable for the Cow.
### Conventions
+ Member variables names always end with an underscore `_`
	+ E.g. `age_` for the age of a Cow in a Cow class

# Member Functions
Member functions are the functions that belong to a class. Each instance of a class has functions. (e.g. a `Cow` named `bessie` has the function `setAge`)

### Defining Member Functions
All member functions use the **scope-resolution operator** `::` in the function definition. This tells the compiler that we are defining a function inside our class
##### Example: moo
```
void Cow::moo(int numMoos) const {
    for (int i = 0; i < numMoos; ++i) {
        cout << "Moo! ";
    }
    cout << endl;
}
```
`Cow::moo` means that we are defining the function `moo` within the `Cow` class.
+ Without `::` we would be defining a function `moo` with no relationship to `Cow`

### Calling Member Functions
We use **dot notation to call member functions**
> `bessie.moo(1);`

Calls the `moo` member function with `bessie`, an instance of the class `Cow`

### const Member Functions
A `const` member function makes a promise to not change anything about the object it's called on
+ To tell C++ that a member function is `const`, you say so at the <u>end</u> of it's declaration
+ The object itself is considered `const` for `const` member functions (which means its member variables are considered `const`)
+ The `const` keyword appears in the declaration (must be in both `.hpp` and `.cpp` files)
+ If a class has no `const` member functions, then `const` instances of that class will not work
	+ So in general, **any member function that can be `const` should be `const`**
##### Uses
+ **Automated Correctness Checking:** if you don't intend a member function to change member variables, making it `const` allows the compiler to check that
+ **Interface Contract:** Anyone using the class knows they can call `const` member functions and not have member variables be changed
+ **`const` Objects:** If an object is declared as `const`, then it can only use `const` member functions
	+ `const` objects cannot have their member variables changed
##### Example:
```
int main() {
    Cow bessie{3, 12};
    const Cow mabel{1, 2};

    bessie.moo(1);
    mabel.moo(2);
    bessie.setAge(4);

    // This line wouldn't work!
    // mabel.setAge(2);

    return 0;
}
```
## Function Example
```
bool isPrime(int n) {
    if (n < 2) {
        return false;
    }
    // Try dividing by all numbers from 2 to sqrt(n).
    for (int i = 2; i*i < n; ++i) {
        if (n % i == 0) {
            return false;
        }
    }
    // If we get here, we didn't find a factor, so n is prime.
    return true;
}

```

## Printing to Console & User Input
```
#include <iostream>
#include <string>

std::cout << "Hello World";
std::cout << "What is your name? "
std::string name;
std::cin >> name;
std::cout << "Hello, " << name << "!" << std::endl;
```
The `include` statements are necessary for input and output (`iostream`) and for using strings (`string`)
+ `std` stands for standard
+ `cout` stands for character output, and the `<<` operator essentially outputs a given string
+ `cin` stands for character input, and the `>>` operator stores the (user) input from the console into a given variable (`name` in this case)
	+ Note that `>>` only reads the next "word"

## Declaring Variables
In C++, every variable has a type, name, value, and a location in memory
##### Example: 
> `int x = 3;`

Declares `x` as an integer and assigns it a value of `3`
Note that types have to be specified!

##### Example: Implicit Starting Value
> `int x;`

`x` now holds an *indeterminate* value (there is no default value)
+ This *indeterminate* value could be different between machines
	+ Could cause hard to catch bugs
+ It's good practice to explicitly assign starting values instead!

### Qualifiers
+ `constexpr`
	+ The variable is known at compile time (not run time) and can never be changed
+ `const`
	+ The variable is <u>read-only</u>
	+ Does not have to be known at compile time
	+ Can be used with [[const References|references]]
+ `&`
	+ The variable is a [[Definition & Additional Notes|reference]]

## Operators
+ Scope-Resolution operator `::`
	+ Tells the compiler how things are related
	+ Used as `someplace::something`, which essentially means `something` is inside of `someplace`
		+ Example: `Cow::moo` means "the `moo` function/variable inside of class `Cow`"
		+ `someplace` is known as a *namespace*

## Namespaces
A *namespace* is a collection of functions and variables whose purpose is to be a named collection
+ We can use namespaces to avoid double-declaration errors
	+ e.g. our classes `Cow` and `Pig` both have a function called `setAge`
		+ Without the namespace, we would just have two `setAge` functions (which is a double declaration error)
+ `std` - the namespace that contains all standard library code

+ `using namespace std` 
	+ If we put this at the top of our file, then we don't have to say `std::` every time when using functions/variables from `std`
	+ However, we would have to now be careful of name collisions
	+ Can put in `.cpp` files, but DO NOT put in `.hpp` files because then it would be included in `.cpp` files and people might not want that

## For loops that use Iterators
In general, a for loop that utilizes an iterator is written as follows:
```
for (auto p = values.begin(); p != values.end(); ++p) {
    ... *p ...
}
```

We can hide the iterator by rewriting it as this instead (does the same thing):
```
for (double v : values) {
    ... v ...
}
```
+ Note that `double` was used as example (in general, this has to be the desired type)
	+ `double&` would be used if we want to change values in the data structure we're iterating through

#### How it Works
When we write
```
for (TYPE var : thing) {
    ... var ...
}
```

C++ turns it into
```
{
    auto _past_end = std::end(thing);
    for (auto _i = std::begin(thing); _i != _past_end; ++_i) {
        TYPE var = *i;
        ... var ...
    }
}
```
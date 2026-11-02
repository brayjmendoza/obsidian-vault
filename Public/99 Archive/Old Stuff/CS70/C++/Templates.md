## Function Templates

Consider a function fill that fills a list with a value `val`
```c++
void fill(list<double>::iterator startingPoint, list<double>::iterator pastTheEnd, double val) {
    for (list<double>::iterator iter = startingPoint; iter != pastTheEnd; ++iter) {
        *iter = val;
    }
}
```
Note that this only works for lists of doubles. If we wanted to use this for lists of ints, we would need another function for ints.
+ Simply copying and pasting this function and changing `double` to `int` is a possible, but causes too much code duplicatino

A ***function template*** is essentially a recipe for generating a function
+ We can use a use a variable to generalize types

**Example**
```c++
template <typename T>
void printVal(const T& x) {
    std::cout << x << std::endl;
}
```
+ A function that prints the value `x` for any type `T`
	+ `T` is a <u>template parameter</u> (in this case it holds a type)
+ Usually, we would have to specify a type for `x`, restricting the function to only print out arguments of the correct type
+ Function templates allow us to generalize this type
	+ The compiler fills in the variable `T` and generates the necessary functions for our code to run correctly
		+ Now we don't need duplicate code!
	+ If we try to use a type `T` that is incompatible with the function, we get a compiler error
+ Note that we passed the argument in by reference
	+ Some types may be for large objects
	+ Passing by reference allows us to avoid accidentally copying large objects


We can use function templates to generalize our `fill()` function from above too:
```c++
template <typename Iter, typename Value>
void fill(Iter start, Iter pastEnd, Value value) {
    for (Iter iter = start; iter != pastEnd; ++iter) {
        *iter = value;
    }
}
```
+ Now we can fill lists of any type with values of any type with one function!

#### Compilation issues
Consider `printVal` again
```c++
template <typename T>
void printVal(T x) {
    cout << x << endl;
}
```
On it's own, the compiler can't compile this function because it can't translate it to machine readable code
+ The compiler doesn't know what `T` is, and there is no machine-readable code for an arbitrary type (only actual, concrete types)
+ This function can only compile if it's with code that uses it
	+ Then the compiler knows how to fill in the template for what it's used for

**Templates must be compiled along with the code that use them.**
+ Thus, we can't compile templates in their own source (`.cpp`) file
+ We have to `#include` the function template *definition* in any file that uses it
	+ We do this with an `.hpp`  file that declares the template (like we've done with declaring functions in classes)
	+ And an `.hpp` file that defines the template (instead of `.cpp` like usual)
##### Example:
`main.cpp` – a source file that uses the template
```c++
#include "printval.hpp"

int main() {
    printVal(42);
    printVal("Moo");
}
```

`printval.hpp` – a header file that _declares_ the template
```c++ 
#ifndef PRINTVAL_HPP_INCLUDED
#define PRINTVAL_HPP_INCLUDED

template <typename T>
void printVal(const T& x);

#include "printval-private.hpp"

#endif
```

`printval-private.hpp` – a file that _defines_ the template
```c++
#include <iostream>

template <typename T>
void printVal(const T& x)
{
    std::cout << x << std::endl;
}
```
+ Note that we `#include`d the implementation of the function template at the end of the `printval.hpp` file which declared the template
	+ The header that declares the template includes the file that defines the template


## Class Templates
Class templates are useful for data structures that might store different types of items (e.g. `std::vector`)

#### Example
Consider a simple class IntPair
```c++
class IntPair {
  public:
    IntPair(int f, int s);
    int getFirst() const;
    int getSecond() const;
    void setFirst(int f);
    void setSecond(int s);
  private:
    int first_;
    int second_;
};
```


We can convert this into a class template to generalize the types for a Pair. If we wanted a pair like IntPair, we would say `Pair<int, int>`. We could do Pairs with different types too like `Pair<std::string, bool>`

`pair.hpp` – declarations (include guard omitted)
```c++
template <typename F, typename S>
class Pair {
  public:
    Pair(const F& first, const S& second);
    const F& getFirst() const;
    const S& getSecond() const;
    void setFirst(const F& f);
    void setSecond(const S& s);
  private:
    F first_;
    S second_;
};

#include "pair-private.hpp"
```

`pair-private.hpp`– definitions
```c++
template <typename F, typename S>
Pair<F, S>::Pair(const F& first, const S& second) :
    first_{first},
    second_{second} {
}

template <typename F, typename S>
const F& Pair<F, S>::getFirst() const {
    return first_;
}

template <typename F, typename S>
void Pair<F, S>::setFirst(const F& f) {
    first_ = f;
}
```
+ Note that every member function definition needs to have the same template preamble as the class itself (i.e. `template <typename F, typename S>`)
	+ This is because these are part of a class template, so these functions also need to be templates themselves
		+ Since these are templates we say `Pair<F, S>` instead of `Pair`

+ Note that since `Pair` is a class template, there's no actual class named Pair
	+ Instead the classes are `Pair<float, bool>`, `Pair<int, int>`, etc.
	+ If we said `Pair myPair;` we would get an error

## Overloading and Templates
Both overloading and template are ways to provide a family of functions with the same name
+ Overloading functions are prioritized over templated ones
+ Function templates are used over type promotions/conversions

**Example**
```c++
#include <iostream>
#include <string>

template <typename T>
void print(const T& val) {
    std::cout << "templated print: " << val << std::endl;
}

void print(int val) {
    std::cout << "int print: " << val << std::endl;
}

void print(double val) {
    std::cout << "double print: " << val << std::endl;
}

int main()
{
    print(42);
    print(3.1415);
    print("Hello");

    return 0;
}
```

This prints
```
int print: 42
double print: 3.1415
templated print: Hello
```

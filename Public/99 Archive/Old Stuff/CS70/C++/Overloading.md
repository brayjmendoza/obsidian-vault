**Overloading** is the idea that we can have more than one function with the same name
+ When defining functions with the same name, C++ uses *only* the <u>types of the arguments</u> to figure out which function to call

### Example:
We have two functions called `combine`:
```
int combine(double x, double y) {
    return (x+y)/2;
}

std::string combine(std::string x, std::string y) {
    x.append(" & ");
    x.append(y);
    return x;
}
```
If we write the following, C++ will call the write function!
```
cout << combine(3.142, 2.718) << endl
cout << combine("Chalk", "Cheese") << endl
```
+ If there isn't a perfect match, C++ will do [[Promotion and Conversion|promotions and conversions]] to try to find the right function

## Rules for Resolving Overloading
C++ finds the right function using the number of arguments and their types
- If there is a perfect match, it's found the right function and is done
- Otherwise, it produces a list of candidates based on the conversions/promotions it could perform.
- If, out of that list of candidates, there is an overloaded function that is
    - Better than all the others for some arguments (i.e., fewer conversions); _and_,
    - No worse than any of the others for the remaining arguments, then
        - That function is the one that is used.
- Otherwise, the best choice is still ambiguous, and the compiler throws an error.

## Overloading Operators
We can introduce new meanings to C++'s operators (e.g. `+`, `/`, `=`, `++`, `*`, etc.) with overloading

#### Example `<<` operator
Consider the following
```
cout << 42 << 'x' << 3.14;
```
This is equivalent to
```
((cout << 42) << 'x') << 3.14;
```
Which is equivalent to
```
{
    std::ostream& _temp1 = cout << 42;
    std::ostream& _temp2 = _temp1 << 'x';
    _temp2 << 3.14;
}
```
By convention, all these `<<` operators return a reference to their left-hand argument, so our code is also equivalent to saying
```
cout << 42;         // calls operator<<(std::ostream, int)
cout << 'x';        // calls operator<<(std::ostream, char)
cout << 3.14;       // calls operator<<(std::ostream, double)
```
+ So, our "print 3 values" code was actually calling 3 different functions!
+ This mechanism is *extensible*, allowing us to define `operator<<` for our own types
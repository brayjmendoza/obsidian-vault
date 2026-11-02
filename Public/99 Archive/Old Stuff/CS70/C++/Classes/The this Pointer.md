`this` is a pointer to the instance of an object.
+ When you call a member function, `this` is implicitly passed in so the program knows what instance it was called on
+ `*this` would give the actual object that a member function was called on

## Type
The type for `this` for a class `Elephant` is
+ `const Elephant* this` for `const` member functions
+ `Elephant* this` for non-`const` member functions

## Example
Consider the following function (where `name_` is a public member variable)
```
void printElephant(const Elephant* ePtr) {
    cout << "Elephant named " << ePtr->name_ << endl;
}
```
This is a global function and is called with `printElephant(&charlie);`, where we pass in a memory address.

Alternatively, we can take advantage of `this`
```
void Elephant::print() const {
    cout << "Elephant named " << name_ << endl;
}
```
This is a member function and is called with `charlie.print();` where `this` is implicitly passed in
+ Instead of writing `name_`, we could have written `this->name_`
	+ That being said, just use `name_` (`this` is extra stuff that's unnecessary)
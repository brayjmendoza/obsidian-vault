In C++, [[Polymorphism|subtype polymorphism]] is used by creating _base classes_ and _derived classes_
+ These are like super- and sub-classes
+ For example, consider a class `Person` which has a subclass `Student`
	+ In C++ we would say `Student` is a class derived from `Person`

## Dynamic Dispatch
_Dynamic dispatch_ is when we figure out which implementation of a member function to call based on the actual type of the object at <u>runtime</u>, rather than the declared type of the variable.
+ e.g. the variable could be type `Animal` when compiled, but type `Cow` at runtime

By default, C++ classes do _not_ use dynamic dispatch.
- If you want to use dynamic dispatch, put the keyword `virtual` in front of a member function in the class definition
- If a member function is declared virtual in a base class, then it's virtual for all of its derived classes.
- When writing a derived class, use the `override` keyword for `virtual`member functions whenever you override the implementation for that class in a derived class
	- If you say `override` for a member function that _wasn't_ declared `virtual` in the base class, you'll get a compiler error

## Pure Virtual Member Functions
A _pure virtual function_ is one where we declare it in the base class, but the base class _doesn't implement_ that function
+ All (concrete) derived classes _must_ override it and provide their own implementation
+ This makes the base class an _abstract class_, 
	+ We can't make any objects of this base class
	+ We can only make objects that derive from it

**Syntax:**
> `virtual void speak() const = 0;`
+ The `= 0;` means "make this function pure virtual"

## Abstract Classes as Interfaces
If a base class has no data members *and* all member functions are declared as pure virtual, then it's an **interface class**
+ These classes specify _what_ the class needs to be able to do, without saying anything about _how_
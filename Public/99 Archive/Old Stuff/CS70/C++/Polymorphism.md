+ **Polymorphism** means "many forms/types"
+ A function is **polymorphic** if it has at least one parameter that accepts arguments of more than one type

Three types of polymorphism in C++:
+ Subtype Polymorphism (inheritance).
+ Parametric Polymorphism (templates).
+ Ad-Hoc Polymorphism (overloading).

## Subtype Polymorphism
 In C++, subtype polymorphism is used by creating _base classes_ and _derived classes_
+ This is [[Inheritance|inheritance]]
+ For example, consider a class `Person` which has a subclass `Student`
	+ In C++ we would say `Student` is a class derived from `Person`

+ When `Student` is derived from `Person`, then
	+ `Student` is a _subtype_ of `Person`
	+ "Subtype" is similar to "subset" 
		+ Every `Student` can also be seen as a `Person` (but not vice versa)
		+ E.g. we can say that `short` is a subtype of `int` and `float` is a subtype of `double`

+ Any function that wants a particular type can be given a subtype of that type and still work, e.g.
	+ A function that wants a `Person` can be given a `Student` 
	+ A function that wants a `double` can be given a `float`

## Parametric Polymorphism
Consider the following function template:
```c++
template <typename T>
const T& max(const T& x, const T& y) {
    if (x > y) {
        return x;
    } else {
        return y;
    }
}
```
+ `max()` takes arguments of many types because of the type <u>parameter</u> `T`
+ People would often say `max()` is **generic** instead of calling it parametric polymorphism
+ Since instantiations of `max` are made at compile time, this polymorphism can be described as *static*

## Ad-Hoc Polymorphism
We could instead define specific `max()` functions for particular types (i.e. a `max()` for `int`s and one for `double`s)
+ This is [[Overloading|overloading]]!
+ This kind of polymorphism is much less expansive than templates (a.k.a. genericity or parametric polymorphism) 
	+ Only works for the specific types we've defined it for. So it's called _ad hoc_ polymorphism.
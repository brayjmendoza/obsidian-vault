Classes can provide type conversion

## Conversion *Into* a Class
C++ considers **single-argument constructors** as a way to automatically convert a value into that type
#### Example
Consider a class `FuzzyBool` that supports the idea of Yes/No/Maybe
```c++
class FuzzyBool {
    // ...
    FuzzyBool(bool preciseBool);
    // ...
};
```
with the following member function
```c++
void makeDinner(FuzzyBool opinion) {
    if (opinion.positiveEnough()) {
        // make the dinner
    } else {
        // wait
    }
}
```

All of the following would successfully call the member function
> `FuzzyBool wantDinner{true};
> `makeDinner(wantDinner);`
> `makeDinner(FuzzyBool{true});`
> `makeDinner(true);`
+ The last one works despite passing in a boolean instead of a `FuzzyBool`
	+ With the single-argument constructor, C++ will implicitly create a temporary `FuzzyBool` and automatically convert `true`

+ Automatic conversion occurs with arguments taken in by copy or by constant reference
	+ Does NOT work with arguments passed by non-const reference

## Conversion *Out of* a Class
What if we want to turn `FuzzyBool`s into normal `bool`s?
+ We can define a *type-cast operator* in `FuzzyBool`

**Type-cast operator** -  a special member function (a type-conversion operator) whose name matches the name of the type you want to be able to convert to

#### Example
**Declaration:**
```c++
class FuzzyBool {
    // ...
    operator bool();
    // ...
};
```

**Definition:**
```c++
FuzzyBool::operator bool() {
    return state_ != NO;
};
```
+ The return type is already in the function's name

## Avoiding Type Conversion
The `explicit` keyword will ensure that a conversion constructor or type-cast operator is only used when you explicitly ask for it
#### Example: explicit constructor
Here, `FuzzyBool` instead has an `explicit` single-argument constructor
```c++
class FuzzyBool {
    // ...
    explicit FuzzyBool(bool preciseBool);
    // ...
};
```

Now, this works
> `makeDinner(FuzzyBool{true});

But this doesn't
> `makeDinner(true);

#### Example: explicit type-cast operator
An explicit type-cast operator will only be called if we explicitly ask for the conversion
```c++
class FuzzyBool {
    // ...
    explicit operator bool();
    // ...
};
```

Here, this works
> `bool doit = bool(myFuzzyBool);

But this doesn't
> `bool doit = myFuzzyBool;`


## Type Conversion Limits
+ A compiler will only perform conversion once
	+ It won't do a “chain” of conversions.
+ A compiler will only perform conversion for parameters to a function
	+ You can't apply conversion to a value that you're calling a member function on
---
type: concept
created: 2026-11-24
updated: 2026-11-24
aliases:
  - Overloading
  - Ad Hoc Polymorphism
  - Operator Overloading
  - Overload Resolution
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-24
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Overloading** gives several functions the same name, and the language chooses which one a call means from the number and types of its arguments.

In C++, two `combine` functions can coexist, one taking two `double`s and one taking two strings, and `combine(3.142, 2.718)` calls the first while `combine("Chalk", "Cheese")` calls the second. Only the parameters distinguish overloads: two functions that differ only in their return type can't share a name.

Choosing the function is **overload resolution**, done at compile time:

1. If one candidate matches the arguments' types exactly, it's chosen.
2. Otherwise, the compiler lists the candidates it could call by promoting or converting arguments (see [[Type Conversion]]).
3. A candidate is chosen if it's better than every other for at least one argument (e.g., needing a promotion where another needs a conversion), and no worse for the rest.
4. If no candidate is best, the call is ambiguous, and compilation fails.

When an overload and a function template could both handle a call, an equally good ordinary function wins over the template. But a template that matches exactly is preferred to an ordinary function that needs a conversion (see [[Parametric Polymorphism]]).

## Operator Overloading

C++'s operators are functions too, named `operator` followed by the symbol (e.g., `operator+` or `operator<<`), so they can be overloaded to give an operator a meaning for a new type. Output is the standard example: `cout << 42 << 'x' << 3.14` groups as `((cout << 42) << 'x') << 3.14`, and each `<<` is a separate call, chosen by the type of its right-hand argument. By convention, each returns a reference to its left-hand stream, so the next `<<` writes to the same stream (see [[Lvalues and Rvalues]]). Since overloading is open-ended, a class can define its own `operator<<` and be printed the same way. The assignment operator, `operator=`, is overloaded the same way (see [[Deep and Shallow Copy]]).

More generally, overloading is a form of **ad hoc polymorphism** (see [[Polymorphism (Computer Science)]]): the name works only for the types someone wrote a definition for. Java overloads methods by parameter types much as C++ does, but doesn't let programs overload operators. Python has no overloading by parameter type, since its functions don't declare types, though classes can define operators through special methods like `__add__`. Haskell has no overloading as such: a [[Type Class|type class]] gives a family of types one shared name for an operation, with an implementation per type, so `==` and `+` work across types in a more structured way.

# Examples

## Combining Numbers and Strings

```cpp
int combine(double x, double y) {
    return (x + y) / 2;
}

std::string combine(std::string x, std::string y) {
    x.append(" & ");
    x.append(y);
    return x;
}

std::cout << combine(3.142, 2.718) << std::endl;      // 2
std::cout << combine("Chalk", "Cheese") << std::endl; // Chalk & Cheese
```

The first call matches the `double` version exactly. The second passes two string literals, which aren't `std::string`s but convert to them, and can't convert to `double`, so the string version is the only candidate. The first prints `2`, not `2.93`, because that `combine` returns an `int`, so its average is converted and truncated.

# Connections

- [[Polymorphism (Computer Science)]]: overloading is ad hoc polymorphism
- [[Type Conversion]]: the promotions and conversions overload resolution weighs
- [[Parametric Polymorphism]]: templates, which overloads are ranked against
- [[Type Class]]: Haskell's alternative to overloading
- [[Lvalues and Rvalues]]: a chain of `<<` calls passes its stream along as a reference

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

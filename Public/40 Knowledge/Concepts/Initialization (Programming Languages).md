---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Initialization
  - Default Initialization
  - Copy Initialization
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Initialization** gives a newly created variable its first value, as distinct from **assignment**, which replaces the value of a variable that already has one.

In C++, every variable has a type, a name, a value, and a location in memory, and initialization happens once, when the variable is created. A variable of a primitive type (e.g., `int`, `float`, `bool`, or a pointer) can be initialized in two ways:

- **Default initialization:** no starting value is given (e.g., `int x;`). For a primitive type, the variable then holds an **indeterminate value**, whatever bits were already in its memory, and using it is [[Undefined Behavior|undefined behavior]]. There is no default value like zero, and the leftover bits can differ between runs and machines, which makes the resulting bugs hard to catch. So it's good practice to always give a starting value.
- **Copy initialization:** a starting value is given, and it's copied into the variable's memory, written with `=` (e.g., `int x = 5;`) or braces (e.g., `float f{4.2};`). Though `int x = 5;` looks like an assignment, it isn't one: no earlier value of `x` exists to replace.

Copy initialization happens in more places than declarations. When a function is called, each parameter is copy-initialized from its argument, and the function's result is copy-initialized from the expression it returns. This holds for objects as well as primitive values, which is why copying an object, for an argument or a result, is something a class defines.

More generally, languages differ in whether a variable can exist without a value. Java gives fields a default value (e.g., `0` or `null`) and rejects a local variable read before it's assigned, and Rust rejects any variable used before it's initialized, so neither has indeterminate values. In a pure functional language like Haskell, there's no assignment at all: a name is bound to its expression once, and binding is the only kind of initialization (see [[Name Binding]]). C++ also offers **value initialization** with empty braces (e.g., `int x{};`), which sets a primitive variable to zero.

# Examples

## Initializing in a Function Call

Function calls copy-initialize both their parameters and their result:

```c++
float myFun(int x, float f) {
    return x + f;
}

float result = myFun(5, 4.2);
```

The parameters `x` and `f` are initialized with copies of the arguments, `5` and `4.2`. `myFun` computes `x + f`, and `result` is initialized with a copy of that value, about $9.2$. Nothing here is assigned: each of the three variables gets its first and only value when it's created.

# Connections

- [[Undefined Behavior]]: using a default-initialized primitive variable
- [[Name Binding]]: the functional counterpart, where a name gets its value once and never another
- [[Type Inference]]: C++'s `auto` takes a variable's type from its initializer
- [[Type Conversion]]: brace initialization refuses conversions that could lose information, and `=` allows them
- [[Object Lifetime]]: initialization is the second of an object's five phases
- [[Evaluation Strategy]]: pass by value copy-initializes a parameter, and pass by reference doesn't copy at all
- [[Constructor (Object-Oriented Programming)]]: how an object of class type is default- or copy-initialized

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

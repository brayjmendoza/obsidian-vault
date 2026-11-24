---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Promotion
  - Conversion
  - Widening Conversion
  - Narrowing Conversion
  - Type Coercion
  - Type Cast
  - Conversion Constructor
  - Type-Cast Operator
  - explicit
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **type conversion** turns a value of one type into a value of another type that represents it, such as an integer into a floating-point number.

Arithmetic in C++ starts from one rule: an operation on two values of the same numeric type gives that type (e.g., an `int` plus an `int` is an `int`). When the types differ, or when a value is passed where another type is expected, C++ converts a value first. Numeric conversions come in two kinds, depending on whether information can be lost:

- **Promotion:** a move to a type of the same kind (i.e., integer to integer, or floating point to floating point) whose range includes every value of the original type. A promotion can never lose information. Adding an `int` to a `long`, on a machine where `long` is the larger type, promotes the `int` to a `long` first, and the sum is a `long`. An `unsigned int` promotes to a `long` too, as long as `long` is larger, since then its whole range fits.
- **Conversion:** any other move between numeric types. A conversion can lose information, since the new type may not hold every value of the old one.

From those definitions, a few cases follow:

| Change | Kind |
|---|---|
| Integer to floating point | Always a conversion, since the kinds differ |
| To a smaller type of the same kind (e.g., `int` $\to$ `short`, or `double` $\to$ `float`) | A conversion |
| Signed to unsigned | Always a conversion, since negative values have no unsigned equivalent |
| Unsigned to signed | A conversion, unless the signed type is larger (e.g., `unsigned int` $\to$ `long`, on a machine where `long` is larger) |

C++ performs both kinds automatically, for instance when an argument's type differs from its parameter's. A conversion can also be requested explicitly by writing the type like a function: `int(dollar)` converts `dollar` to an `int`. Brace initialization (e.g., `int x{y}`) refuses conversions that could lose information, while initializing with `=` or parentheses allows them (see [[Initialization (Programming Languages)]]).

A class can take part in conversions too, in both directions:

- **Into the class:** C++ treats a constructor with a single parameter as a way to convert a value of the parameter's type into the class (see [[Constructor (Object-Oriented Programming)]]). Where a `FuzzyBool` is expected, a `bool` is accepted, and C++ builds a temporary `FuzzyBool` from it. This works for parameters taken by value or by `const` reference, but not by non-`const` reference, which can't refer to a temporary (see [[Lvalues and Rvalues]]).
- **Out of the class:** a **type-cast operator** is a member function named for the type it converts to (e.g., `operator bool()`), and its return type is already in its name.

Marking either one `explicit` means it's used only when a conversion is asked for (e.g., `FuzzyBool{true}` or `bool(fb)`), never automatically. Automatic conversions have limits: in one implicit conversion, C++ applies at most one of these user-defined conversions, not a chain of them, and it never converts the object a member function is called on.

More generally, an automatic conversion is called a **coercion**, or an **implicit conversion**, and a requested one is a **cast**. What this note calls a promotion is usually called a **widening conversion**, and a conversion that can lose information is a **narrowing conversion**. The C++ standard itself uses "promotion" more narrowly, for converting small integer types to `int` and `float` to `double`, and what it forbids in brace initialization is exactly narrowing. Languages differ in how much they coerce: Java widens automatically but requires a cast to narrow, and Haskell never converts numbers implicitly, so mixing an `Int` with a `Double` needs an explicit function like `fromIntegral`.

# Example

A `float` has 24 bits of precision, too few to hold every 10-digit integer. Converting a `long` to a `float` and back rounds the value to the nearest one a `float` can represent:

```c++
long worldPop = 7960583250;     // assumes a 64-bit long
std::cout << worldPop << std::endl                  // 7960583250
          << float(worldPop) << std::endl           // 7.96058e+09
          << long(float(worldPop)) << std::endl;    // 7960583168
```

The round trip loses 82: near 8 billion, consecutive `float` values are 512 apart, so 7,960,583,250 rounds to the nearest multiple of 512, 7,960,583,168. Integer to floating point is always a conversion, and this is the information it can lose (see [[Floating-Point Arithmetic]]).

A promotion, by contrast, changes the type and keeps the value:

```c++
signed char dollar = 36;
std::cout << dollar << " " << int(dollar);   // prints "$ 36"
```

Printed as a `char`, the value is the character with code 36, a dollar sign. Promoted to an `int`, the same value prints as a number.

A class conversion lets `makeDinner`, which takes a `FuzzyBool`, accept a plain `bool`:

```c++
class FuzzyBool {
 public:
    FuzzyBool(bool preciseBool);   // converts bool into FuzzyBool
    // ...
};

void makeDinner(FuzzyBool opinion);

makeDinner(FuzzyBool{true});   // explicit
makeDinner(true);              // a temporary FuzzyBool is built from true
```

Declared `explicit FuzzyBool(bool preciseBool);`, the constructor allows only the first call, and the second fails to compile.

# Connections

- [[Floating-Point Arithmetic]]: why integer-to-float conversions round
- [[Type (Programming Languages)]]: a conversion reinterprets a value in another type's representation
- [[Subtyping]]: another way a value of one type is used where another is expected, without changing its representation
- [[Static and Dynamic Typing]]: a statically typed language decides at compile time where conversions happen
- [[Initialization (Programming Languages)]]: brace initialization refuses narrowing conversions
- [[Constructor (Object-Oriented Programming)]]: a one-parameter constructor converts values into its class
- [[Function Overloading]]: overload resolution ranks candidates by the promotions and conversions they need

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

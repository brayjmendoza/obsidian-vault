---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Constructor
  - Default Constructor
  - Parameterized Constructor
  - Copy Constructor
  - Member Initialization List
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **constructor** is a special member function that initializes a new object of a class, and its main job is to initialize the object's member variables.

A constructor has the class's name and no return type. Creating an object runs one, chosen by its arguments, as part of the object's initialization (see [[Object Lifetime]]). C++ distinguishes three kinds:

- **Parameterized constructor:** takes arguments, and runs when they're given (e.g., `Cow bessie{3, 12};`).
- **Default constructor:** takes none, and runs for default initialization (e.g., `Sheep mead;`, or each element of `Sheep herd[10];`). For a class, default initialization isn't indeterminate: it means running this constructor.
- **Copy constructor:** takes a `const` reference to an object of the same class, and makes the new object a copy of it. It runs for copy initialization, which includes passing an object by value and returning one, so the copy constructor defines what those mean for the class.

The compiler writes, or **synthesizes**, some constructors itself. If a class declares no constructors at all, the compiler synthesizes a default constructor, which initializes each member as the class definition says, or with its own default initialization if it says nothing: members of class type get their default constructors, and primitive members get indeterminate values. Declaring any constructor stops this, so a class with only a parameterized constructor has no default constructor. Unless the class declares one, the compiler also synthesizes a copy constructor, which copy-initializes each member from the other object's. Writing `= default` asks for the synthesized version explicitly, and `= delete` forbids the constructor, so code that would use it doesn't compile.

## Member Initialization Lists

A member variable must be initialized before it's used, and by the time a constructor's body runs, every member already has been. So members are initialized in a **member initialization list**, between the parameter list's closing parenthesis, after a colon, and the body's opening brace. A member missing from the list is initialized as the class definition specifies, or default-initialized. The list can also call another constructor of the same class to do the work.

Members are always initialized in the order the class declares them, whatever order the list gives. So the list should follow the declaration order: compilers warn when it doesn't, since a member initialized from another member that comes later in the class would read an uninitialized value.

More generally, nearly every object-oriented language has constructors: Java's look like C++'s, and Python's `__init__` plays the same role. Few separate initialization from the constructor's body as C++ does, since their members can't be indeterminate. The constructors of an [[Algebraic Data Type|algebraic data type]] are different: they build values from their fields and run no code.

# Examples

## A Parameterized Constructor

`Cow`'s parameterized constructor initializes both members in its initialization list, then prints:

```cpp
Cow::Cow(int numSpots, int age)
    : numSpots_{numSpots},
      age_{age}
{
    std::cout << "Made a cow with " << numSpots_ << " spots!" << std::endl;
}
```

## A Copy Constructor

`Cow`'s copy constructor copies each member from `other`, in the order the class declares them (`numSpots_`, then `age_`):

```cpp
Cow::Cow(const Cow& other)
    : numSpots_{other.numSpots_},
      age_{other.age_}
{
    // Nothing else to do
}
```

This is exactly what the synthesized copy constructor would do, so `Cow(const Cow& other) = default;` would serve as well. Writing one by hand matters when copying each member isn't enough, as when a member is a pointer to heap memory (see [[Deep and Shallow Copy]]).

# Connections

- [[Initialization (Programming Languages)]]: default and copy initialization, which run the default and copy constructors
- [[Destructor]]: the constructor's counterpart at the end of an object's lifetime
- [[Deep and Shallow Copy]]: when the synthesized copy constructor isn't enough
- [[Class (Programming Languages)]]: what a constructor initializes
- [[Type Conversion]]: a constructor with one parameter also converts values into the class

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: concept
created: 2026-11-15
updated: 2026-11-24
aliases:
  - Parameterized Type
  - Type Variable
  - Generics
  - Template (C++)
  - Function Template
  - Class Template
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Parametric polymorphism** lets one definition work for values of every type, by writing its type with **type variables** that stand for any type.

In Haskell, a type variable is a lowercase name like `a` or `b` in a type. Asking GHCi for the type of `(:)` shows one: `a -> [a] -> [a]`. Each use of the function fills `a` in with a real type, and within one type, the same variable must be filled in consistently: the element on the left of `:` and the elements of the list on the right must match. A list type is itself a **parameterized type**: `[a]`, "list of `a`," becomes a concrete type when `a` is filled in (e.g., `[Integer]` or `[Char]`). A data type can take a type parameter too (e.g., `data List a = Empty | Cons a (List a)`).

C++ provides parametric polymorphism through **templates**. A **function template** is a recipe for generating functions: `template <typename T>` before a definition makes `T` a template parameter, a type that each use fills in. A **class template** does the same for a class, so `std::vector<int>` and `std::vector<std::string>` are two classes generated from one template, and there's no class called plain `std::vector`. Templates replace copying a function and changing its types by hand, which would duplicate code. The compiler generates code for each type a template is used with, when the program is compiled, so this polymorphism is static, and a type that lacks an operation the template uses is a compile error (see [[Polymorphism (Computer Science)]]). Since no code can be generated until `T` is known, a template's whole definition must be visible wherever it's used, so it goes in a header, not a separately compiled source file (see [[Separate Compilation]]).

More generally, a **polymorphic** definition is one that works with more than one type, and in parametric polymorphism it works with all of them the same way: the code never inspects which type it was given, so one definition serves every type. As the name suggests, a parametrically polymorphic definition takes types as parameters: its type variables are parameters, filled in with an actual type at each use, just as a function's parameters are filled in with values. Many languages offer the same idea as **generics** (e.g., Java's `List<T>` and Rust's `Vec<T>`). It differs from the polymorphism a [[Type Class]] provides, where a function's behavior depends on the type.

# Examples

## Types of List Functions

The types of some list functions (newer versions of GHCi add constraints to a few, e.g., `HasCallStack` on `head`):

| Function | Type                        | Reads as                                                            |
| -------- | --------------------------- | ------------------------------------------------------------------- |
| `(:)`    | `a -> [a] -> [a]`           | An element and a list of the same type give a list of that type     |
| `(++)`   | `[a] -> [a] -> [a]`         | Two lists of the same type give a list of that type                 |
| `head`   | `[a] -> a`                  | A list of any type gives one of its elements                        |
| `take`   | `Int -> [a] -> [a]`         | A count and a list give a list of the same type                     |
| `map`    | `(a -> b) -> [a] -> [b]`    | A function from `a` to `b` turns a list of `a`s into a list of `b`s |
| `filter` | `(a -> Bool) -> [a] -> [a]` | A predicate on `a`s selects from a list of `a`s                     |

`3 : [17, 10, 5]` fills `a` with a number, and `'h' : "ello"` fills it with `Char`. `True : "ello"` is a type error, since `a` can't be both `Bool` and `Char`.

## Generalizing a List Type

A list of integers, generalized to a list of anything:

```haskell
data IntList = Empty | Cons Int IntList
data List a  = Empty | Cons a (List a)
```

## A Fill Template in C++

In C++, `fill` sets every item in a range to one value. Written for lists of `double`s, it works only for them:

```c++
void fill(std::list<double>::iterator start, std::list<double>::iterator pastEnd, double val);
```

As a template over the iterator type and the value type, one definition serves every container and element type:

```c++
template <typename Iter, typename Value>
void fill(Iter start, Iter pastEnd, const Value& value) {
    for (Iter i = start; i != pastEnd; ++i) {
        *i = value;
    }
}
```

Calling it with two `std::list<double>::iterator`s and a `double` fills in `Iter` and `Value`, and the compiler generates that version. Called with pointers into an `int` array, it generates another.

# Connections

- [[Type Class]]: the other kind of polymorphism, where one name has a different implementation for each type
- [[Type Inference]]: Haskell infers the most general polymorphic type a definition allows
- [[Recursive Data Type]]: Haskell's lists, `[a]`, are the standard parameterized recursive type
- [[Higher-Order Function]]: `map` is polymorphic in two type variables at once
- [[Option Type]]: `Maybe a`, a parameterized type for values that might be missing
- [[Parser Combinator]]: `Parser a`, a parser whose result can be any type
- [[Functor (Functional Programming)]]: a type class over parameterized types, like `Maybe` and `Tree`
- [[Covariance and Contravariance (Type Systems)]]: how generic types relate when their parameters are subtypes
- [[Polymorphism (Computer Science)]]: parametric polymorphism is one of three kinds, beside subtyping and overloading
- [[Function Overloading]]: one name with a definition per type, ranked against templates
- [[Iterator]]: templates over iterator types make algorithms work on any container

# Sources

- [[Programming Languages (HMC CS131)]]
- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: reference
created: 2026-11-23
updated: 2026-11-24
topic: c++
url: https://www.doxygen.nl/
---
How to comment C++ code: interface comments in headers, written with Doxygen tags, and implementation comments in source files.

# Interface Comments

Interface comments say *what* a class or function does, never how. They go in the `.hpp` file, and a reader should never need the `.cpp` file to understand them. Doxygen turns them into documentation, using these tags:

| Tag | Holds | Required |
|---|---|---|
| `\brief` | A one-line description | For every function and class |
| `\param <name>` | What one parameter means | For every parameter |
| `\returns` | What the function returns | For every function that doesn't return `void` |
| `\warning` | Dangers: requirements on parameters, or iterators the function invalidates | Whenever there are any. There may be several, each over several lines |
| `\note` | Anything else worth knowing (e.g., an odd edge case, or the asymptotic running time) | No. There may be several |
| `\class <name>` | The class being described | For every class |

A function:

```cpp
/**
 * \brief               Returns the quotient of two numbers
 * \param numerator     The number being divided
 * \param denominator   The number to divide by
 * \returns             The result of numerator divided by denominator
 * \warning             denominator cannot be equal to zero
 */
double divide(double numerator, double denominator);
```

A class:

```cpp
/**
 * \class Sheep
 * \brief A simple sheep implementation with a hat
 */
class Sheep {
```

# Implementation Comments

Implementation comments say *how* and *why* the code works. They go in the `.cpp` file, next to the code they describe.

- **Comment every idea, not every line.** Too many comments clutter the code and distract from what it means.
- **Skip lines whose purpose is obvious.**
- **Comment each nontrivial function, loop, and `if`/`else`.** A loop's comment goes before it and says what it does. When every case of an `if` is complicated, say what each case does.
- **Explain why, don't translate.** A comment that restates the C++ in English adds nothing.

A comment that translates the code:

```cpp
// Run a for loop with i starting at one, and increase i by one
// every time as long as i is less than vec.size()
for (size_t i = 1; i < vec.size(); ++i) {
```

A comment that explains it:

```cpp
// We need to print the first element of vec separately to avoid
// putting a comma before it (as long as vec is not empty)
if (!vec.empty()) {
    std::cout << vec[0];
}

// Print the remaining elements of vec separated by commas
for (size_t i = 1; i < vec.size(); ++i) {
    std::cout << "," << vec[i];
}
```

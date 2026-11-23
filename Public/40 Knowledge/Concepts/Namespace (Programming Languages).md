---
type: concept
created: 2026-11-23
updated: 2026-11-23
aliases:
  - Namespace
  - Scope Resolution
  - Qualified Name
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **namespace** is a named collection of names, such as functions, variables, and types, so that the same name can be used in different collections without the two clashing.

Without namespaces, every name in a program shares one space, and two definitions with the same name conflict (see [[Declaration and Definition]]). Putting each definition inside a namespace gives it a longer, **qualified name**: in C++, `someplace::something` means "the `something` inside `someplace`," and `::` is the **scope-resolution operator**. So two classes `Cow` and `Pig` can each have a member function `setAge`, since one is `Cow::setAge` and the other is `Pig::setAge`. A class acts as a namespace for its members in this way, and the C++ standard library puts all of its names in the namespace `std` (e.g., `std::cout`).

Writing every qualified name in full is long, so C++ can bring a namespace's names into the current scope: after `using namespace std;`, `cout` means `std::cout`. That brings back the risk of clashes the namespace prevented, since every name in `std` is now visible unqualified. So `using namespace` is acceptable in a `.cpp` file, whose scope is that one file, but never in a header: a header is pasted into every file that includes it (see [[Separate Compilation]]), so its `using` would apply in files whose authors didn't choose it.

More generally, nearly every language has some form of namespace, though not always by that name: Python's modules, Java's packages, and Haskell's modules all qualify names (e.g., `math.sqrt` in Python, or `Data.Map.lookup` in Haskell), and each has its own way to import names unqualified, with the same trade-off. A namespace is a kind of [[Scope|scope]] with a name, so code outside it can refer to what's inside.

# Example

For illustration (an example not from the source), two libraries both define `print`. Each in its own namespace, they can live in one program:

```c++
namespace barn {
    void print();
}

namespace zoo {
    void print();
}

int main() {
    barn::print();   // the print inside barn
    zoo::print();    // the print inside zoo
}
```

Writing `using namespace barn;` and `using namespace zoo;` before `main` would make a plain `print()` ambiguous: both namespaces now supply a `print` in the same scope, and the compiler can't choose between them.

# Connections

- [[Scope]]: a namespace is a named scope, and qualified names reach into it from outside
- [[Name Binding]]: within one namespace, each name is bound once
- [[Declaration and Definition]]: the clashes namespaces prevent are duplicate definitions of one name

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

---
type: reference
created: 2026-11-23
updated: 2026-11-23
topic: c++
---
How to read a C++ type that mixes pointers (`*`), references (`&`), arrays (`[N]`), functions, and `const`. Read inside out, starting from the variable's name. What pointers and references are is in [[Pointer (Programming Languages)]] and [[Reference (Programming Languages)]].

# Simple Rule

For types without parentheses:

1. Read the variable's name.
2. Read to the right until the end of the declaration (or an `=`).
3. Jump back to the name.
4. Read right to left until the start of the declaration.

| Declaration | Reading |
|---|---|
| `int* a[5];` | `a` is an array of 5 pointers to `int`s |
| `const float* p;` | `p` is a pointer to a `float` that's `const`: the `float` can't change through `p` |
| `float* const p;` | `p` is a `const` pointer to a `float`: `p` can't point elsewhere |
| `const float* const p;` | `p` is a `const` pointer to a `const` `float`: neither can change |
| `const int* const* b[3];` | `b` is an array of 3 pointers to `const` pointers to `const` `int`s |

`const` applies to what's on its left, or to what's on its right when nothing is on its left. That's why `const float*` and `float const*` mean the same thing.

# Rule with Parentheses

Parentheses group a declaration, which is how you get a pointer to an array or to a function:

1. Start at the name, or where the name would be if it's left out.
2. Read outward, respecting parentheses. When you can go either way, read to the right first.
3. When you reach the edge of a parenthesized group, treat the whole group as a new starting point and continue from step 2.

| Declaration | Reading |
|---|---|
| `int (* const x)[10];` | `x` is a `const` pointer to an array of 10 `int`s |
| `double (*(*(* const x)[10])[20])(short*, string);` | `x` is a `const` pointer to an array of 10 pointers to arrays of 20 pointers to functions that take a pointer to `short` and a `string` and return a `double` |

Without the parentheses, `int* const x[10];` is instead an array of 10 `const` pointers to `int`s, since `[10]` on the right is read first.

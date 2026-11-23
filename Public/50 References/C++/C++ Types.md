---
type: reference
created: 2026-11-23
updated: 2026-11-23
topic: c++
---
C++'s built-in numeric types and which to use. How values move between them is in [[Type Conversion]], and how to read a type built from pointers, arrays, and `const` is in [[Reading C++ Declarations]].

# Integer Types

The standard fixes only minimum sizes, so a machine may make any of these larger:

| Type | Minimum bits | Minimum bytes | Use for |
|---|---|---|---|
| `char` | 8 | 1 | Characters, as characters |
| `short int` | 16 | 2 | |
| `int` | 16 | 2 | An integer from the user or input data, and the default otherwise |
| `long int` | 32 | 4 | |
| `long long int` | 64 | 8 | |

Whatever the sizes, `sizeof(char)` $\le$ `sizeof(short)` $\le$ `sizeof(int)` $\le$ `sizeof(long)` $\le$ `sizeof(long long)`. You can drop the `int` from `short int`, `long int`, and `long long int` (e.g., `long x = 256;`).

## Signed and Unsigned

- **`signed`** (the default, except for `char`): half the possible values are negative, and the other half are zero or positive.
- **`unsigned`:** every value is zero or positive, so the largest value is about twice as large.
- **Prefer signed types.** Mixing signed and unsigned values converts the signed one to unsigned, which turns a negative number into a huge positive one (see [[Type Conversion]]).

## Other Integer Types

| Type | Is | Needs | Use for |
|---|---|---|---|
| `bool` | `true` or `false` (size unspecified) | | Conditions |
| `size_t` | Unsigned, just big enough for the size of any object | `#include <cstddef>` | Counting things you store, and array indices |
| `ptrdiff_t` | Signed, big enough for the difference between two positions | `#include <cstddef>` | Offsets, which can be negative |
| `int8_t`, `int16_t`, `int32_t`, `int64_t` | Signed, exactly 8, 16, 32, or 64 bits | `#include <cstdint>` | When the exact size matters |
| `uint8_t`, `uint16_t`, `uint32_t`, `uint64_t` | Unsigned, exactly 8, 16, 32, or 64 bits | `#include <cstdint>` | When the exact size matters |

# Floating-Point Types

On nearly every machine (see [[Floating-Point Arithmetic]]):

| Type | Total bits | Significand bits | Exponent bits | Decimal digits |
|---|---|---|---|---|
| `float` | 32 | 24 | 8 | About 7 |
| `double` | 64 | 53 | 11 | About 16 |

The standard only promises `sizeof(float)` $\le$ `sizeof(double)` $\le$ `sizeof(long double)`. Use `double` for non-integer data where scientific notation would make sense.

# Conversions at a Glance

The rules behind these are in [[Type Conversion]].

| Change | Can lose information? |
|---|---|
| To a larger type of the same kind (e.g., `short` $\to$ `int`, or `float` $\to$ `double`) | No: it's a promotion |
| Integer $\to$ floating point | Yes, for large values |
| To a smaller type (e.g., `int` $\to$ `short`, or `double` $\to$ `float`) | Yes |
| Signed $\to$ unsigned | Yes, for negative values |
| Unsigned $\to$ a larger signed type (e.g., `unsigned int` $\to$ `long`, if `long` is larger) | No: it's a promotion |

- **Same-type arithmetic stays in that type:** an `int` plus an `int` is an `int`, so `7 / 2` is `3`.
- **Explicit conversion:** write the type like a function, as in `int(dollar)` or `double(count)`.
- **Braces refuse lossy conversions:** `int x{3.7};` doesn't compile, while `int x = 3.7;` quietly gives `3`.

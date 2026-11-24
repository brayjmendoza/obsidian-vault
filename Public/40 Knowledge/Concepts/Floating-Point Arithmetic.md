---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Floating-Point Number
  - Floating Point
  - IEEE 754
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
A **floating-point number** represents a real number in a fixed number of bits as a **significand** times a power of two, $m \times 2^e$, the binary form of scientific notation.

The significand $m$ holds the number's digits, and the **exponent** $e$ says where the binary point goes, so the point "floats." A fixed number of bits goes to each:

| C++ type | Total bits | Significand bits | Exponent bits |
|---|---|---|---|
| `float` | 32 | 24 | 8 |
| `double` | 64 | 53 | 11 |

The significand's bits set the **precision**, how many significant digits a number keeps: 24 bits is about 7 decimal digits, and 53 bits is about 16. The exponent's bits set the **range**, how large or small a number can be. C++ only promises that `sizeof(float)` $\le$ `sizeof(double)` $\le$ `sizeof(long double)`, but nearly every machine uses the sizes in the table. A `double` suits non-integer data where scientific notation would be natural (e.g., measurements).

Since the significand has a fixed number of bits, only some real numbers can be represented exactly, and the rest are rounded to the nearest one that can. Representable numbers are densest near zero and spread out as they grow, since the same number of significand bits covers each power of two: between $2^{32}$ and $2^{33}$, consecutive `float` values are $2^{32-23} = 512$ apart. So converting a large integer to a `float` can change its value (see [[Type Conversion#Rounding a Long to a Float|Type Conversion]]).

More generally, nearly all hardware follows the IEEE 754 standard (1985), which fixes these formats. It stores one sign bit and leaves the significand's leading 1 implicit, which is how a `float` gets 24 bits of precision from 23 stored bits ($1 + 8 + 23 = 32$), and a `double` gets 53 from 52 ($1 + 11 + 52 = 64$). It also defines special values: positive and negative infinity, and NaN ("not a number," the result of operations like $0/0$). Rounding makes floating-point arithmetic differ from real arithmetic: addition isn't associative, and familiar decimals like $0.1$ have no exact binary form.

# Examples

## Adding 0.1 and 0.2

For comparison, in Python, whose `float` is a 64-bit `double`, $0.1$ and $0.2$ are each rounded, and so is their sum:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

Neither $0.1$ nor $0.2$ has a finite binary expansion, just as $1/3$ has no finite decimal one. Each is stored as the nearest `double`, and the rounding errors in the sum don't cancel, so it lands on a different `double` from the one nearest $0.3$. That's why floating-point values are compared within a tolerance instead of with `==`.

# Connections

- [[Type Conversion]]: converting an integer to floating point can round it
- [[Type (Programming Languages)]]: the same 32 bits read as an integer or a `float` mean different numbers

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]

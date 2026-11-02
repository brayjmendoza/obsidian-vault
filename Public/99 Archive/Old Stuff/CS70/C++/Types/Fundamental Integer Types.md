+ `char`
	+ Minimum Size (Bits): 8
	+ Minimum Size (Bytes): 1
	+ Use when working with characters as characters
+ `short int`
	+ Minimum Size (Bits): 16
	+ Minimum Size (Bytes): 2
+ `int`
	+ Minimum Size (Bits): 16
	+ Minimum Size (Bytes): 2
	+ Use when you have an integer from the user or input data
		+ Use if you otherwise wouldn't use other types of int's
+ `long int`
	+ Minimum Size (Bits): 32
	+ Minimum Size (Bytes): 4
+ `long long int`
	+ Minimum Size (Bits): 64
	+ Minimum Size (Bytes): 8

These are <u>minimums</u>. In general, computer systems can adopt larger values for as long as the following is true:
+ `sizeof(char)` $\leq$ `sizeof(short)` $\leq$ `sizeof(int)`$\leq$ `sizeof(long)` $\leq$ `sizeof(long long)`

**Note:** You can omit `int` for `short int` and `long int` when declaring these types (e.g. `long x = 256` is perfectly valid)

## Signed and Unsigned Integers
`signed` - Half of the bits for the number are used for negative values, the other half for non-negatives
+ Prefer signed types over unsigned types
`unsigned` - only includes non-negative numbers, so all bits for the number are used
+ Can have larger maximum values than signed numbers

## Other Integer Types
+ `bool`
	+ Can only store 0 or 1 (size is unspecified)
+ `size_t`
	+ An unsigned integer type with just enough bits to represent the *size* of any object
	+ Requires `#include <cstddef>`
	+ Use when you want to count how many of something you're storing, or for array indices
		+ Non-negative
		+ Use `ptrdiff_t` if you need negative values
+ `ptrdiff_t`
	+ A signed integer type with just enough bits to represent the difference between any two sizes (e.g. the offset of one thing compared to another)
	+ Requires `#include <cstddef>`

Each of the following require `#include <cstdint>`
+ `int8_t`
	+ A signed int guaranteed to be 8 bits
+ `int16_t`
	+ A signed int guaranteed to be 16 bits
+ `int32_t`
	+ A signed int guaranteed to be 32 bits
+ `int64_t`
	+ A signed int guaranteed to be 64 bits
+ `uint8_t`
	+ An unsigned int guaranteed to be 8 bits
+ `uint16_t
	+ An unsigned int guaranteed to be 16 bits
+ `uint32_t`
	+ An unsigned int guaranteed to be 32 bits
+ `uint64_t`
	+ An unsigned int guaranteed to be 64 bits

# Floating-Point Numbers
In general:
+ `sizeof(float)` $\leq$ `sizeof(double)` $\leq$ `sizeof(long double)`

+ `float`
	+ Total Bits: 32
	+ Significand Bits: 24
	+ Exponent Bits: 8
+ `double`
	+ Total Bits: 64
	+ Significand Bits: 43
	+ Exponent Bits: 11
	+ Use when you have non-integer numerical data where scientific notation would be appropriate
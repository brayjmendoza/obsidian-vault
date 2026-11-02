A type can be a mix of pointers, references, arrays, and `const`
+ Types can get very complicated

## Simplified Inside-Out Rule
When reading the type of a variable...
1. Read the name of the variable
2. Read to the right until you hit the end of the declaration (or any initialization)
3. Jump back to the name of the variable
4. Read from right-to-left until you hit the beginning of the declaration
#### Example (simple):
> `int* a[5];`
1. `a` is... (read the variable name)
2. `[5]` an array of 5... (read to the right)
3. `*` pointers to... (jump back to the name and read right to left)
4. `int` integers
So, `a` is an array of 5 pointers to integers.

#### Example (more complicated):
> `const int* const * b[3];`
1. `b` is... (read the variable name)
2. `[3]` an array of three... (read to the right)
3. `*` pointers to... (jump back to the name and read right to left)
4. `const` const...
5. `*` pointers...
6. `int` to integers...
7. `const` that are const
`b` is an array of three pointers to const pointers to integers that are const

## Generalized Inside-Out Rule for Complex Types
Imagine you want a single pointer to an array of ints. It would be written as follows:
> `int (* const x)[10];`

To read this type, do the following:
1. Start at the name of the variable
	+ Sometimes the name is omitted, if this is the case start where the name would otherwise be
2. Read outwards, respecting parenthetical grouping
	+ If you can read both to the right and left, read to the right first
3. If you're not done yet because you were in parentheses, consider the parenthesized group as a new starting point and continue from step 2
#### Example:
> `double (*(*(* const x)[10])[20])(short *, string);`
+ `x` is a `const` pointer to
	+ an array of ten pointers to
		+ an array of twenty pointers to
			+ a function that takes a pointer to `short` and a `string` and returns a double
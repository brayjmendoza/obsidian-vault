+ A pointer is a variable that stores a memory address as its value
	+ See [[Pointer Types]]
+ A pointer is a type of [[Iterators|iterator]]
## Past-the-End Pointers
Consider
> `float vals[TEMPERATURE_SAMPLE_COUNT];`
- `vals` _decays_ to a pointer to the first element of the array
- `vals + 0` also gives a pointer that points to the first element of the array
- `vals + TEMPERATURE_SAMPLE_COUNT - 1` gives a pointer that points to the last element of the array
- `vals + TEMPERATURE_SAMPLE_COUNT` gives a pointer that points to just beyond the last element of the array
	- This is the past-the-end pointer

#### Example: For Loop
We can use past-the-end pointers to specify how many times a loop should run
```
void normalize(float newmax, float* firstValPtr, float* pastEndPtr) {
    float maxval = *firstValPtr;
    for (float* p = firstValPtr; p < pastEndPtr; ++p) {
        if (*p > maxval) {
            maxval = *p;
        }
    }

    for (float* q = firstValPtr; q < pastEndPtr; ++q) {
        *q = *q / maxval * newmax;
    }
}
```
Here, we use `firstValPtr` to show where the array starts and `pastEndPtr` to show where it ends. This lets us loop through the entire array (despite not knowing its size)
+ There are a couple ways to call this function
	+ `normalize(height, vals, vals+TEMPERATURE_SAMPLE_COUNT);`
	+ `normalize(height, std::begin(vals), std::end(vals));`
+ ***There's a bug***
	+ If the array is length one, we would end up calling `*p` when `p` is a past-the-end pointer (resulting in undefined behavior)

## Const Pointers
Consider the example:
```
float max_value(float* firstValPtr, float* pastEndPtr) {
    float maxval = *firstValPtr;
    for (float* p = firstValPtr; p < pastEndPtr; ++p) {
        if (*p > maxval) {
            maxval = *p;
        }
    }
    return maxval;
}
```
This returns the max value of an array of floats
+ However, we would get an error if we pass in a `const` array of floats
+ This is because we evaluate `*p` which we *could* use to modify the array
	+ This is regardless of implementation because the compiler doesn't check what a function does, just *if* it could break something (in this case, change a `const` array)

We can fix this with `const` pointers by changing the function header:
> `float max_value(const float* firstValPtr, const float* pastEndPtr) {`
+ Now, the compiler knows `*` can't be used to modify the value in the pointer

**Note:** `const` pointers are similar to [[const References]]
+ You would read these rights right to left (as usual)
	+ "`firstValPtr` is a pointer to a `float` that's `const`"
		+ The `float` is `const`, not the pointer

#### Where we put `const` matters
We can have `const` pointers.
**Remember:** when reading types we read inside-out (right to left). This should clarify if `const` is making the pointer or the value read only.
+ `const float* firstValPtr` 
	+ The `float` that the pointer points to can't change
	+ It's a pointer to `const float`.
- `float* const firstValPtr`
	- The pointer itself can't change.
- `const float* const firstValPtr` says both
	- The pointer itself can't change
	- The `float` it points to can't change.

## Null Pointers
Pointers can store the special value `nullptr`, which means "not a valid address".
+ Such pointers are known as null pointers
+ Explicitly set pointers to point to *nothing*
	+ Easier to see if we accidentally follow a pointer that isn't initialized
	+ Gives us a value to compare to when needed
+ Following a null pointer is undefined behavior
	+ In practice, you'd usually get a [[Segmentation Fault|seg fault]]

#### 0/null Initializing an array
We can initialize an entire away with `nullptr` as follows:
+ `Elephant* elephants[10]{nullptr};`
OR
+ `Elephant* elephants[10]{};`

This is because of curly-brace initialization. 
+ For numeric types, if you use curly-brace initialization but don't give a value for everything, the rest of the array will be _0-initialized_.
	+ `int a[5]{1, 2};` gives the array `[1, 2, 0, 0, 0]`
+ For pointer types, curly-brace initialization gives `nullptr`'s instead
	+ So the above Elephant pointer array examples initialize an array of 10 null pointers

#### Example Function
```
void printAge(const Elephant* e) {
    if (e != nullptr) {
        cout << e->getAge() << endl;
    } else {
        cout << "No elephant here!" << endl;
    }
}
```
Prints the age of elephants stored as pointers in an array.
+ These elephants may be on the [[The Heap|heap]]
	+ Say we have an array of pointers to elephants that are all default initialized
	+ Elephants are stored on the heap, so we reassign the default initialized pointers whenever we want to "store" an elephant in the array
	+ Not all pointers may be assigned elephants, so these are set as `nullptr`
		+ Gives us a value to compare to so we don't get undefined behavior

## Using Pointers to Move Data Efficiently
**Consider the following code:**
```
// Perform an in-place sort on a range of Elephants
void sortElephantsByName(Elephant* start, Elephant* pastTheEnd);
```
Where somewhere we will have
```
Elephant temp = *p;
*p = *q
*q = temp;
```
**Note**: `p` and`q` are pointers to `Elephant`s
+ This in ***inefficient*** because we are copying and reassignment `Elephant` objects
	+ We are moving around large amounts of data!
	+ We can use pointers to "move" this data around more efficiently

**Revision: Use an array of `Elephant*` pointers to sort**
```
// Create the array of elephant pointers
Elephant* herdPtrs[HSIZE];
for (size_t i = 0; i < HSIZE; ++i) {
    herdPtrs[i] = herd + i;
}

// Sort
sortElephantPtrsByName(herdPtrs, herdPtrs+HSIZE);
```
+ Behind the scenes, the elephants stay put, and our array of pointers is reordered
	+ We can use this sorted array of pointers as our sorted array of elephants (with the help of `*`)
+ The parameter types are different for this function
	+ `sortElephantsByName(Elephant** start, Elephant** pastTheEnd);
	+ We have two `**` because we are passing in the starting pointer to an array of pointers
		+ In other words, `start` is a pointer to a pointer to an Elephant

## Pointers vs. References
+ Pointers are more general (than references)
+ Pointers have their own storage/memory
+ A pointer is a memory address (that we can access with `*`)
+ Pointers support math (like being added)
	+ Only really used for pointers in an array

## Additional Stuff
+ Consider a class with the member variable `name_` and a pointer `p` that pointers to an instance of the class
	+ We can access name as `(*p).name_` (assuming we have access)
	+ Alternatively, we can say `p->name_`
		+ This <u>arrow notation</u> is preferred
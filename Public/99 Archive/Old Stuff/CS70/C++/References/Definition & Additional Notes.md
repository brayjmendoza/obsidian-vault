A **reference** is another name for an existing piece of data
```
int x = 5;
int& z = x;
```
Here, `x` and `z` refer to the same value `5`. `z` is the reference, and `x` is the referent. `z` refers to the thin in memory as `x` does (same memory location and everything).

`&` means "reference to", so the second line says "z is a reference to an int" (we read types outwards from z)

#### Example:
```
int a = 2;
int& b = a;
int c = 31;
a = 8;
cout << a << " " << b;
b = c;
cout << " " << a << " " << b;
```
This outputs "8 8 31 31" because since `a` and `b` refer to the same thing, any change to `a` or `b` affects both `a` and `b`

**Key Idea:** A reference *never* changes its referent. Once it's initialized the reference and referent are interchangeable


## Additional Notes
- You can have references to references, they will just all refer to the same thing
```
int m = 7;
int& n = m;
int& o = n;
o = 3;
cout << m << " " << n << " " << o;
```
This will print out "3 3 3"
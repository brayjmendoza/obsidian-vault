We can add the `const` qualifier when declaring references to make it a *read-only* reference.
```
int a = 3;
const int& b = a;
++b;
cout << a << " " << b;
```
Here, we cannot use `b` to change the value in the memory address. However, we can use reassign a value to `a` (which changes the value for both `a` and `b`)

**Key Idea:** the `const` keyword affects access through *that name*, but it does not change access through any other names

**Important Rule:** You *cannot* make a non-`const` reference to a `const` variable
+ Otherwise we could easily get around the `const` qualify by making a reference
+ The same is true for making a non-`const` reference to a `const` reference (even if that `const` reference refers to a non-`const` variable)

### Example:
Valid code:
```
int c = 5;
int& d = c;

const int e = 10;
const int& f = e;

int g = 3;
const int& h = g;
```

Invalid code (causes a compilation error):
```
const int i = 9;
int& j = i; // Causes a compiler error!
```

### Applications
`const` references are useful when we don't want to make changes to things that we passing into functions by reference.
```
bool isJuvenile(const Elephant& e) {
    return e.age() >= 5 && e.age() < 10;
}

int main() {
    Elephant nelly{"Nelly", 17, false, true};
    cout << isJuvenile(nelly) << endl;
}
```
Here, we use we pass in parameters by reference to prevent unnecessary copy operations. We use `const` so that we can't change the `Elephant` we passed into `isJuvenile` while in the function (we don't want to accidentally change the `Elephant`).
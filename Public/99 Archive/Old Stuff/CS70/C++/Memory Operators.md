## Indirection Operator
`*` is the indirection operator, which gives the value at some memory address
+ This is also known as the deference operator

Let `x` be some memory address
+ `*x` would give the value stored at memory address `x`
##### Example: Array
```
float myArr[3]{1.2, 3.4, 5.6};
*myArr
```
+ `*myArr` evaluates to 1.2
	+ `myArr` returns the memory address of the first element in the array

If we were to then do
```
*myArr = 7.8;
```
Then, the first item of the array `myArr` will change to 7.8

We can use addition to access memory next to the address
> `*(myArr + 1)`
+ Gives the second item of an array
+ `myArr + 1` returns the memory address of the second item of the array

## Address-of Operator
`&` is the address-of operator
`&` takes a thing and gives you a pointer to it (i.e. the thing's memory address)
+ `&` and `*` cancel each other out
	+ `*&x == x`
#### Example
```
void printElephant(const Elephant* ePtr) {
    cout << "Elephant named " << ePtr->name_ << endl;
}

int main() {
    Elephant charlie{"Charlemagne", 19};

    printElephant(&charlie);
}
```
+ `&charlie` gives us a pointer so that we can use it in `printElephant`
	+ Better to just use [[Applications of References|references]]
	+ That being said, pointers are more versatile

## Additional Notes
+ Both `*` and `&` mean different things in a type and value context
![[MemoryOperators.png]]
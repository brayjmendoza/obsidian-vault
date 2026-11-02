The **heap** is a region of memory (separate from the stack) that is allocated and deallocated whenever we tell it to
+ Memory allocated to the heap during a function can persist even after that function returns

### The `new` Keyword
We use `new` to allocate stuff on the heap
> `int* p = new int{42}`
+ Allocates space on the heap for an integer
+ Initializes the integer with the value 42
+ The stack stores the pointer `p` to this integer on the heap
	+ We can access this integer with `*p`

In general, `new`
- **Allocates** space on the heap for the given type
- **Initializes** the data as specified
- **Returns** a _pointer_ to the new piece of data
- Used for [[Public/99 Archive/Old Stuff/CS70/C++/Terminology|dynamic allocation]]

### Memory Leaks
- A **memory leak** is when we have allocated memory on the heap and lost all pointers to that memory
	- We lose access to this memory, but it still occupying the memory on the system (until the program terminates)

### Dangling Pointers
+ Dangling pointers are pointers to deallocated memory
	+ Deallocated memory could be overwritten at some point
		+ Following a dangling pointer leads to undefined behavior
	+ Deallocated memory may not be overwritten right away
		+ Can make bugs hard to find

### Double Delete
+ When you use `delete` on a dangling pointer (or a pointer that points to deallocated memory)
	+ Is an issue because you are trying to deallocate memory that has already been deallocated
		+ Usually causes a crash

### The `delete` Keyword
Essentially the opposite of `new`
- Takes a pointer to something on the heap
- Destroys that thing
- Deallocates the memory at that address

Can be read as "delete the thing in memory at address \_\_\_\_\_\_\_\_\_\_"
+ You give it the address to be deallocated
+ **NOTE:** Nothing happens to the pointer that you give to `delete`
	+ After `delete`, the pointer points to deallocated memory!
		+ Can lead to undefined behavior

To delete arrays, use `delete[]` instead of `delete`
+ Tells the compiler to destroy & deallocate the entire array

To prevent memory leaks, there must be a `delete` for every `new`!

### Example: Elephant Parade
```
int main() {
    constexpr size_t ELEPHANTS_TO_ADD = 2;
    size_t elephantCapacity = ELEPHANTS_TO_ADD;
    Elephant* elephants = new Elephant[ELEPHANTS_TO_ADD];

    string anotherElephant = "y";
    size_t numElephants = 0;
    while (anotherElephant == "y") {
        ++numElephants;
        cout << "Please enter elephant " << numElephants << endl;

        string name;
        cout << "Name: ";
        cin >> name;

        int age;
        cout << "Age: ";
        cin >> age;

        Elephant el{name, age};

        if (numElephants > elephantCapacity) {
            // We ran out of space, so make a bigger array
            Elephant* newElephants = new Elephant[elephantCapacity + ELEPHANTS_TO_ADD];
            // Now copy the contents
            for (size_t i = 0; i < elephantCapacity; ++i) {
                newElephants[i] = elephants[i];
            }
            // We are done with the old array
            delete[] elephants;
            // Now start using the new array
            elephants = newElephants;
            elephantCapacity += ELEPHANTS_TO_ADD;
        }
        elephants[numElephants - 1] = el;

        cout << endl << "Another elephant (y/n)? ";
        cin >> anotherElephant;
        cout << endl;
    }

    // We'll just assume this works
    sortElephantsByName(elephants, elephants + numElephants);

    cout << "The elephants are parading!" << endl;

    for (size_t i = 0; i < numElephants; ++i) {
        cout << elephants[i].getName() << " (" << elephants[i].getAge() << ")" << endl;
    }

    delete[] elephants;
    return 0;
}
```
This makes a parade of elephants. It asks the user if they want an elephant. If yes, the program asks it to provide a name and age.
+ All of these elephants are assigned to the heap, so the user can specify an arbitrary number of elephants
	+ Since the elephants are on the heap, we don't have to allocate space for an elephant on the stack (which would be a lot since elephants are big)
		+ We only allocate space for an elephant when the user specifies
+ Dynamically-allocated arrays are used so the user can add as many elephants to the parade as they want.
+ Appropriate `delete` statements are used so we don't have memory leaks
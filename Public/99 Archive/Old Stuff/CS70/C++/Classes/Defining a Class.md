# Header File
Contains the **class definition**
+ Specifies the *interface* of the class
	+ How other pieces of code should interact with the class
+ Includes **declarations** of all member variables and functions of the class

### Example: Cow Class
`cow.hpp`
```
/*
 * \file cow.hpp
 * \author CS 70 Provided Code
 * \brief Interface definition for the Cow class.
 */

#ifndef COW_HPP_INCLUDED
#define COW_HPP_INCLUDED

#include <iostream>
#include <fstream>

/*
 * \class Cow
 * \brief Knows how many spots it has and how old it is. Can moo.
 */
class Cow {
 public:
    // We can only have a Cow if we know
    // how many spots it has and how old it is
    Cow(int numSpots, int age);
    Cow() = delete;

    // Moo the right number of times.
    void moo(int numMoos) const;

    // Accessor member functions
    int getNumSpots() const;
    int getAge() const;

    // Mutator member functions
    void setNumSpots(int numSpots);
    void setAge(int age);

 private:
    // Per-Cow data
    int numSpots_;
    int age_;
};

#endif  // ifndef COW_HPP_INCLUDED
```

All files that use the class need to `#include` the header file for the class
+ Tells the compiler that the class exists and the names and types of all member variables and functions

**NOTE** the semicolon `;` at the end of the class definition!
# Source File
Contains **member function definitions**
+ This is the file that gets compiled into a `.o` file before being linked to create an executable
+ Needs to `#include` the header file so it knows what member functions/variables exist and what it's defining
	+ Source file needs to know about class interface too!

### Example: Cow Class
`cow.cpp`
```
/*
 * \file cow.cpp
 * \author CS 70 Provided Code
 * \brief Implements the Cow class
 */

#include <cstddef>
#include <iostream>
#include "cow.hpp"

using namespace std;

Cow::Cow(int numSpots, int age)
    : numSpots_{numSpots},
      age_{age}
{
    cout << "Made a cow with " << numSpots_ << " spots!" << endl;
}

void Cow::moo(int numMoos) const {
    for (int i = 0; i < numMoos; ++i) {
        cout << "Moo! ";
    }
    cout << endl;
}

int Cow::getNumSpots() const {
    return numSpots_;
}

int Cow::getAge() const {
    return age_;
}

void Cow::setNumSpots(int numSpots) {
    numSpots_ = numSpots;
}

void Cow::setAge(int age) {
    age_ = age;
}
```

# Example main.cpp file for Cow Class
`main.cpp` - uses the Cow class
```
using namespace std;

int main() {
    Cow bessie{3, 12};
    const Cow mabel{1, 2};

    // This line wouldn't work!
    // Cow duke;

    bessie.moo(1);
    mabel.moo(2);
    bessie.setAge(4);

    // This line wouldn't work!
    // mabel.setAge(2);

    return 0;
}
```

## Private vs. Public
- `public` members can be accessed by any piece of code
- `private` members can only be accessed by code within the class itself

+ Access levels (e.g. `public` and `private`) are part of the class definition, not implementation, so we only see `public` and `private` in the header files, not the source files

# Additional Notes
+ We can think of classes as a collection of variables and functions
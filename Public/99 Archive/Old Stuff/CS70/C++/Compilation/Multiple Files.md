When compiling multiple files, you may get an error in the compilation stage because a certain file calls a function that only exists in a separate file.

**Example:**
`printmoos.cpp`:
```
#include <iostream>

// Prints the given number of "moos"
void printMoos(int numMoos) {
    std::cout << "Moo";
    for (int i = 1; i < numMoos; ++i) {
        std::cout << " moo";
    }
    std::cout << ".";
}
```
`cowchat.cpp`:
```
#include <iostream>
#include <string>

int main() {
    std::cout << "Chat with a cow!";
    std::string userIn;
    do {
        std::cout << std::endl  // New line
                  << "> ";      // The prompt
        std::getline(std::cin, userIn);
        int nMoos = 1 + userIn.size() % 2;
                     // ^-- Either 1 or 2 moos;
        printMoos(nMoos);
    } while (std::cin.good() && userIn != "");
    std::cout << "\n\nBye!\n";

    return 0;
}
```
When compiling `cowchat.cpp` we would get an error because `printMoos` is called, but it is not defined in the file (but rather in a separate file that the compiler doesn't know about)

To fix this, we add the following line at the top of the file (after the includes)
```
// This line declares the printMoos function.
// It ends in a ; instead of { } because the function definition is elsewhere.
void printMoos(int numMoos);
```
This is known as **forward declaration**.

Alternatively (and more commonly), we could use [[Header Files]]
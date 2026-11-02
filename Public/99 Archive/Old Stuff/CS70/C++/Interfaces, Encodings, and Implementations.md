# Interfaces
An **interface** is a set of operations that describes what a data structure supports.
+ Not concerned with how the operations are implemented/performed
+ In C++, the interface is described in the class definition (`.hpp` file)
	+ Specifically the public members

# Encodings
If the interface specifies *what*, then the **encoding** specifies *how*
+ Encodings consist of the design decisions on how data will be organized
	+ What structures/variables are needed to store data?
	+ Any bookkeeping values?
	+ What are the roles/meanings of certain variables? 
	+ What relationships must always hold between the pieces?
+ In C++, the encoding is expressed in the private members of class definitions

There can be multiple valid encodings

# Implementations
The **implementation** of a data structure provides the mechanisms that create and maintain the structures given by the encoding and the interface.
+ In C++, the implementation is primarily expressed in the member-function definitions for a class

There can be multiple valid implementations

# Specifying Rules
At each stage—the interface, the encoding, and the implementation—we need to pay attention to what promises we're making and what promises we're _not_ making
+ This set of promises is sometimes called the data structure's “contract” with its users

**Example:**
+ The _interface_ might specify a required asymptotic complexity for a given operation
- The _encoding_ might specify a required relationship between two data members (e.g., it is always the case that `size_ <= capacity_`)
- The _implementation_ might specify that it gracefully handles unexpected situations, such as running out of memory, or that it includes optimizations for a particular CPU

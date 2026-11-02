## Tags
+ `\brief`
	+ A one line description of what the function does. 
	+ **Must include this for every function**
+ `\param <parameter name>`
	+ Information on a particular parameter that the user will pass in
	+ **Must include one of these comments for every parameter**
+ `\returns`: 
	+ Describes what the function returns
	+ **Must include this for every function that does not return `void`**
+ `\warning`: 
	+ Warns of any potential dangers associated with the function
	+ Should include any requirements of the parameters or changes in iterator validity.
	+ Can include multiple `\warning` comments,
		+ Each can span multiple lines
+ `\note`
	+ Any additional information that we think the user should know
		+ e.g. a strange edge case or the asymptotic runtime. 
	+ Can include multiple `\note` comments, and each can span multiple lines.

These tags allow [doxygen](https://www.doxygen.nl/) to automatically generate documentation.

## Interface Comments
Describe what a class or function does.
+ Always in `.hpp` files
+ Assume that someone reading interface comments does not have to see our `.cpp` files to figure out what the class/function does
+ Only discuss behavior, not implementation
#### Example:
```
/**
 * \brief               Returns the quotient of two numbers
 * \param numerator     The number being divided
 * \param denominator   The number to divide by
 * \returns             The result of numerator divided by denominator
 * \warning             denominator cannot be equal to zero
 */
double divide(double numerator, double denominator);
```

#### Example (class):
Classes need another `\class <class name>` tag as follows:
```
/**
 * \class Sheep
 * \brief A simple sheep implementation with a hat
 */
class Sheep {
```

## Implementation Comments
Help someone understand *how* and *why* our code works.
+ Included in `.cpp` files right next to code they describe
#### Avoid Undercommenting
+ Use for nontrivial functions
+ At least one comment for each non trivial loop
	+ Goes before loop and describes what it does
+ At least one comment for all non trivial `if/else` blocks
	+ If every case is complicated enough, make a comment describing what each case does
+ Include comments for confusing/complicated code
#### Focus on Meaning & Purpose
+ Focus on broader meaning/purpose
	+ Ask *why* was our approach here necessary?
##### Example (poor):
```
// Example 1 (poor): Comments simply reiterate the C++ syntax
void printVector(const std::vector<int>& vec) {
  // Run this code if !vec.empty() evaluates to true
  if (!vec.empty()) {
    // Print vec[0] to std::cout
    std::cout << vec[0];
  }

  // Run a for loop with i starting at one, and increase i by one        // every time as
  // long as i is less than vec.size()
  for (size_t i = 1; i < vec.size(); ++i) {
    // Print a comma and the ith entry of vec to std::cout
    std::cout << "," << vec[i];
  }

  // Print std::endl to std::cout
  std::cout << std::endl;
}
```
The comments do not add much value and simply translate C++ to English
##### Example (good):
```
// Example 2 (better): Comments focus on broader meaning of the code
void printVector(const std::vector<int>& vec) {
  // We need to print the first element of vec seperately to avoid       // putting a
  // comma before it (as long as vec is not empty)
  if (!vec.empty()) {
    std::cout << vec[0];
  }

  // Print the remaining elements of vec seperated by commas
  for (size_t i = 1; i < vec.size(); ++i) {
    std::cout << "," << vec[i];
  }

  std::cout << std::endl;
}
```
The comments here explain *why*

#### Avoid Overcommenting
+ Too many comments can clutter code and district from the overall meaning
+ For C++, **do not comment every line of code**
+ Include a comment for every *idea*
+ Do not provide comments for lines of code whose function is immediately obvious
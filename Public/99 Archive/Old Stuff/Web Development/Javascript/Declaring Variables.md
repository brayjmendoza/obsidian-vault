There are four ways to declare variables in Javascript

#### Automatically
```
x = 5;
y = 6;
z = x + y;
```
Here, `x`, `y`, and `z` are undeclared, so they are automatically declared (just like Python)

However, it's considered good practice to always declare variables before use.
+ Undeclared variables automatically have global scope

### var
```
var x = 5;
var y = 6;
var z = x + y;
```
`var` was used in all JavaScript code before 2015.
`var` should only be used for code written for older browsers.
`var` variables have global scope.

### let
```
let x = 5;
let y = 6;
let z = x + y;
```
Any variables declared with `let` are variable and can be changed.
`let` variables have block scope.

Using a `let` variable before it's declared will result in a `ReferenceError`
```
carName = "Saab";
let carName = "Volvo";  // Error!
```

### const
```
const x = 5;
const y = 6;
const z = x + y;
```
Any variables declared with `const` are constant and cannot be changed.
`const` variables have block scope.

`const` variable **MUST** be assigned a value when declared
```
const PI;  // Error!
PI = 3.14159265359;
```

`const` defines a constant reference to a value (like in C++)
+ CAN'T reassign a constant value, array, or object
+ CAN change elements of a constant array or the properties of a constant object


### Difference Between `var`, `let`, and `const`
![[declaration-differences.png|675x100]]
+ Information on [[Scope]]
+ Redeclare refers to if you can redeclare a variable with the keyword
+ Reassign refers to if you can reassign a variable with the keyword
+ Information on [[Hoisting]]
+ Information on [[Binds this]]

### Overall points:
- Always declare variables
- Always use `const` if a value (or type) should not be changed
- Only use `let` if you can't use `const`
- Only use `var` if you MUST support old browsers
- It's good practice to declare all variables at the beginning of a script

### Additional Notes:
+ As usual, you can declare a variable without setting a value
+ You cannot re-declare a variable with `let` or `const`
+ You can redeclare variables with `let` or `const` if you are redeclaring in different blocks


### Identifiers
All variables are identified with unique names called <u>identifiers</u>.

**Rules:**
- Can contain letters, digits, underscores, and dollar signs
- Must begin with a letter, $, or _
- Case sensitive
- Reserved words (e.g. keywords) cannot be used as names

#### Other Features
You can declare multiple variables in one statement
```
let person = "John Doe", carName = "Volvo", price = 200;
```
Declares `person`, `carName`, and `price`.

This statement can span multiple lines
```
let person = "John Doe",
carName = "Volvo",
price = "200";
```


##### Source:
https://www.w3schools.com/js/js_variables.asp
https://www.w3schools.com/js/js_let.asp
https://www.w3schools.com/js/js_const.asp
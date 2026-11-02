There are different types of scope in JavaScript:
- Block Scope (as of 2015 with [ES6](https://www.geeksforgeeks.org/introduction-to-es6/))
- Global Scope
- Function (Local) Scope

### Block Scope
Variables declared within a `{ }` code block cannot be accessed form outside the block
```
{
  let x = 2;
}
// x can NOT be used here
```
Variables declared with `let` or `const` have block scope

Variables declared with `var` DO NOT have block scope
```
{
  var x = 2;
}
// x CAN be used here
```

### Function Scope
Variables declared within a function are local to that function
```
// code here can NOT use carName  
  
function myFunction() {  
  let carName = "Volvo";  
  // code here CAN use carName  
}  
  
// code here can NOT use carName
```
Local variables (like `carName`) have function scope as they can only be accessed from within the function
+ When within a function, `var`, `let`, and `const` all have function scope
	+ This makes `var` and `let` act pretty much the exact same
Function parameters act as local variables inside functions.

### Global Scope
The global scope is the entire JavaScript environment.
In HTML, the global scope is the window object.

When a variable is declared outside a function, it's a global variable
```
let carName = "Volvo";  
// code here can use carName  
  
function myFunction() {  
// code here can also use carName  
}
```
Anything declared with `var` will ALWAYS have global scope

If you assign values to variables that aren't declared, they are automatically global
```
myFunction();  
  
// code here can use carName  
  
function myFunction() {  
  carName = "Volvo";  
}
```


### Additional Notes
+ Objects and functions are also variables
+ In Strict Mode, undeclared variables are not automatically global

##### Sources:
https://www.w3schools.com/js/js_let.asp
https://www.w3schools.com/js/js_scope.asp
JavaScript's default behavior of moving declarations to the top of the current scope (to the top of current script or function).

### Declarations are Hoisted
Variables can be declared after being used because the declarations are *hoisted* to the top of the script

```
x = 5; // Assign 5 to x  
  
elem = document.getElementById("demo"); // Find an element  
elem.innerHTML = x;                     // Display x in the element  
  
var x; // Declare x
```
Does the same as this:
```
var x; // Declare x  
x = 5; // Assign 5 to x  
  
elem = document.getElementById("demo"); // Find an element  
elem.innerHTML = x;                     // Display x in the element
```
Since the `var x;` declaration is hoisted to the top of the script when run

###### Only <u>declarations</u> are hoisted NOT *initializations*
+ `var x;` is a declaration
+ `var x = 5;` is an initialization

Thus, this
```
var x = 5; // Initialize x  
var y = 7; // Initialize y  
  
elem = document.getElementById("demo"); // Find an element  
elem.innerHTML = x + " " + y;           // Display x and y
```
does not do the same as this
```
var x = 5; // Initialize x  
  
elem = document.getElementById("demo"); // Find an element  
elem.innerHTML = x + " " + y;           // Display x and y  
  
var y = 7; // Initialize y
```
because the initializations are not hoisted (unlike the declarations in the previous examples above)

**NOTE:** hoisted declarations (with var) get initialized as *undefined* 

Thus, in the last example, `var y` gets hoisted to the top, but not the `= 7` initialization part, so
`elem.innerHTML = x + " " + y;` evaluates to `5 undefined`

### let and const
`let` and `const` variables are hoisted, but not initialized (as undefined)
+ The code block is aware of the variable, but cannot be used until it has been declared
	+ The program know the variable exists, but until it is declared, the variable exists in a temporal dead zone where it cannot be used (without an error)
+ Using a `let` variable before declaration will result in a `ReferenceError`
+ Using a `const` variable before declaration is a syntax error
	+ Code just straight up won't run


### Function Hoisting
All functions are hoisted to the top, so you can use functions before they are declared.
```
myFunction(5);

function myFunction(y) {
  return y * y;
}
```
Will work fine
### Conclusion
Just declare all variables at the top!
Otherwise, because of hoisting, you may run into weird bugs

##### Sources:
https://www.w3schools.com/js/js_hoisting.asp
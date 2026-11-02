# Declarations
This is the syntax for a typical JavaScript function:
```
function functionName(parameters) {
	// code to be executed
}
```

#### Expressions
Functions can also be defined using an **expression** which is can be stored in a variable
```
const x = function (a, b) {return a * b};

let z = x(4, 3);   // z stores 12
```
These functions are *anonymous* functions (same as lambda functions in Python) since they do not have a name

Note that these functions end with a semicolon because it's part of an executable statement

#### The Function() Constructor
Functions can also be defined with a built-in JavaScript function constructor `Function()`
```
const myFunction = new Function("a", "b", "return a * b");
let x = myFunction(4, 3);
```
This is the same as
```
const myFunction = function (a, b) {return a * b};  
let x = myFunction(4, 3);
```

### Self-Invoking Functions
These functions are executed automatically without being called.
+ Function expressions self-invoke if the expression is followed by `()`
	+ You have to add parentheses around a function to indicate that it's a function expression
+ Function declarations cannot be self-invoked
	+ Functions with a name like the very first example at the top of this page
```
(function() {
	let x = "Hello!";
})();
```
This is an example of self-invoking function.

### Functions are Objects
They have properties and methods

 The `arguments.length` property returns number of arguments received when the function was invoked
```
function myFunction(a, b) {
	return arguments.length;
}

myFunction(3, 4) // returns 2
```

The `toString()` method returns the function as a string
```
function myFunction(a, b) {
	return a * b;
}

let text = myFunction.toString();
 // Returns "function myFunction(a, b) { return a * b; }"
```


### Arrow Functions
Allow for short syntax for writing function expressions
+ Does not need the `function` or `return` keywords nor curly brackets
```
var x = function(x, y) {
	return x * y;
}
```
is the same as
```
const x = (x, y) => x * y;
```
Note that using `const` is safer than `var` because function expressions never change
You can only omit `return` and the curly brackets if the function is a single statement

##### Sources:
https://www.w3schools.com/js/js_function_definition.asp
[Information on Parameters](https://www.w3schools.com/js/js_function_parameters.asp)

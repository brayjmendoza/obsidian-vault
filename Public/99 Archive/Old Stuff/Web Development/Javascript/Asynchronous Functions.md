**Asynchronous functions** are functions that run in *parallel* with other functions.

## Example: setTimeout()
```
setTimeout(myFunction, 3000);  
  
function myFunction() {  
  document.getElementById("demo").innerHTML = "I love You !!";  
}
```
Calls `myFunction` after 3000 milliseconds.
+ Here, `myFunction` is a callback function
	+ Callback functions - a function passed as an argument to another function
+ `myFunction` and `setTimeout`run in parallel

The following does the same thing:
```
setTimeout(function() { myFunction("I love You !!!"); }, 3000);
```


## Promise Object
Represents an operation that hasn't completed yet but is expected in to in the future.
+ Handles success or failure once operation is completed
+ An alternative to callbacks since callbacks are hard to use & debug
+ Links producing code and consuming code
	+ Producing code - code that can take some time 
	+ Consuming code - code that must wait for the result 
+ Contains both producing code and calls to the consuming code

##### General Syntax:
```
let myPromise = new Promise(function(myResolve, myReject) {  

	// "Producing Code" (asynchronous operations, may take some time)  
  
    myResolve(); // when successful  
    myReject();  // when error  
});  
  
// "Consuming Code" (Must wait for a fulfilled Promise)  
myPromise.then(  
    function(value) { /* code if successful */ },  
    function(error) { /* code if some error */ }  
);
```
The function inside the `Promise` constructer (`function(myResolve, myReject)`) is the *executor function*.
+ `myResolve` - a function that is called that handles success
+ `myReject` - a function that is called that handles failure
+ Within the executor function, some asynchronous operation (e.g. fetching data or reading a file) is typically performed
	+ `myResolve()` or `myReject()` is called depending on the outcome

`myPromise.then(...)` specifies how the result of a promise is handled. It takes in two callback functions
+ First callback - called if the promise is resolved (successful)
	+ For this example, the value passed into `myResolve()` in the promise constructor will serve as the argument to this callback
+ Second callback - called if the promise is rejected (failure)
	+ Here, the value passed into `myReject()` will be provided as the argument to the callback
+ Both callbacks are optional, so you can add callbacks for success or failure only

##### Example:
```
let myPromise = new Promise(function(myResolve, myReject) { 
	// Simulate an asynchronous operation 
	setTimeout(function() {
		let success = true; // Change to false to simulate an error 
		if (success) { 
			myResolve("Operation successful!"); 
		} else { 
			myReject("Operation failed.");
		}
	}, 1000); // 1 second delay 
}); 

myPromise.then( 
	// Logs "Operation successful!" if resolved 
	function(value) { console.log(value); },
	
	// Logs "Operation failed." if rejected ); 
	function(error) { console.log(error); } 
```
After one second, the promise is either resolved ("Operation successful!" is logged) or rejected ("Operation failed." is logged) based on the value of `success`.

##### Object Properties
Two properties: **state** and **result**. The value for result depends on state.
- State
	- "pending" - while a Promise object is working (during the asynchronous operation)
		- Result is undefined
	- "fulfilled" - when the Promise was successful
		- Result is a result value (`value` in the above example)
	- "rejected" - when the Promise failed
		- Result is an error object (`error` in the above example)


## Async/Await
`async` makes a function return a Promise
`await` makes a function wait for a Promise
#### Async Syntax:
```
async function myFunction() {
	return "Hello";
}
```
is the same as
```
function myFunction() {
	return Promise.resolve("Hello");
}
```
Note that when an async function returns a value, the value is wrapped in a resolved promise. So `return "Hello";` from the async function is equivalent to `return Promise.resolve("Hello");`

##### Example with `.then`
```
async function myFunction() {  
  return "Hello";  
}  
myFunction().then(  
  function(value) {myDisplayer(value);},  
  function(error) {myDisplayer(error);}  
);
```
Since the `myFunction` is `async`, it returns a promise. So, we can use `.then` with `myFunction` to specify what to do when the promise is successful or not.
+ Since `return "Hello"` is wrapped in a resolve promise, `"Hello"` is passed as the value for the first callback function
+ Note that the second callback function isn't necessary because the function will never fail 

#### Await Syntax:
`await` can only be used inside an `async` function
+ `await` makes the function pause execution and wait for a resolved promise before continuing
```
async function myDisplay() {  
  let myPromise = new Promise(function(resolve, reject) {  
    resolve("I love You !!");  
  });  
  document.getElementById("demo").innerHTML = await myPromise;  
}  
  
myDisplay();
```
+ This function is async, allowing `await` to be used. 
+ A promise is created, which is immediately resolved with the value `"I love You !!"`.
+ `await` pauses the function (so the lines after the promise is created are not executed) until the promise is resolved.
+ Once the promise is resolved, the function continues and the HTML content is updated with the resolved value (`"I love You !!"`)

`resolve` and `reject` are keywords that act as resolve/reject functions (same as `myResolve()` and `myReject()` from the above examples used explaining Promises)
Note: `reject` is not needed here since the promise is always resolved
```
async function myDisplay() {  
  let myPromise = new Promise(function(resolve) {  
    setTimeout(function() {resolve("I love You !!");}, 3000);  
  });  
  document.getElementById("demo").innerHTML = await myPromise;  
}  
  
myDisplay();
```
This function displays `"I love You !!"` after 3 seconds. It functions the same as the above example with `async` and `await`. Notice that `reject` is not used here.


### Sources:
https://www.w3schools.com/js/js_callback.asp
https://www.w3schools.com/js/js_asynchronous.asp
https://www.w3schools.com/js/js_promise.asp
https://www.w3schools.com/js/js_async.asp
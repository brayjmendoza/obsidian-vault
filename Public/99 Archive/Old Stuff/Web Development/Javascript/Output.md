There are multiple different ways to display data with Javascript:
+ `innerHTML`
+ `document.write()`
+ `window.alert()`
+ `console.log()`

### innerHTML
To access an HTML element, JavaScript can use the `document.getElementByID(id)` method.
+ `id` is an HTML attribute that defines an HTML element
+ `innerHTML`  defines the HTML content
```
<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = 5 + 6;
</script>
```
This makes the `"demo"` HTML element's content to be 11 (since 5 + 6 = 11)
+ `innerHTML` can also change properties of an HTML element
+ So, `innerHTML` is commonly used to display data in HTML

### document.write()
Writes whatever's in the parentheses to the HTML page
```
<p>Hello World!</p>

<script>
document.write(5 + 6);
</script>
```
This will output a webpage that shows Hello World! and 11.
+ ``document.write()`` should only be used for testing
+ DO NOT use `document.write()` after the HTML document is loaded
	+ All existing HTML be deleted and overwritten by whatever is in the statement

```
<h1>My First Web Page</h1>  
<p>My first paragraph.</p>  
  
<button type="button" onclick="document.write(5 + 6)">Try it</button>
```
When clicking the button, all HTML content will be overwritten with 11.

### window.alert()
Displays an alert box
```
<h1>Hello World!</h1>

<script>
window.alert(5 + 6);
</script>
```
This will create a pop up on the webpage that says 11.
The `window` keyword is not required
+ Simply saying `alert(5 + 6)` will do the same thing

### console.log()
Similar to a print statement, it will print contents to the console
```
<script>
console.log(5 + 6);
</script>
```
On a webpage, right click and click inspect. Here you will see a console tab. All `console.log()` statements will display data here. This example will display 11 to the console.

### Additional Notes:
+ There is no print object/method in JavaScript
+ `window.print()` will literally print the content of the current window

##### Sources:
https://www.w3schools.com/js/js_output.asp
https://www.w3schools.com/js/js_intro.asp
Used to exchange data with a web server behind the scenes
+ Makes it possible to update parts of a web page without reloading the whole page

## Syntax:
`variable = new XMLHttpRequest();` creates a new XMLHttpRequest object
+ All modern browsers have a built in XMLHttpRequest object

## Defining a Callback Function
Callback function is executed when the response to the XMLHttpRequest is ready

It is defined as follows:
```
xhttp.onload = function() {
	// What to do when the response is ready
}
```
where `xhttp` is an instance of the `XMLHttpRequest` object.

## Send a Request
Can send a request to a server with the `open()` and `send()` methods of the `XMLHttpRequest` object:
```
xhttp.open("GET", "ajax_info.txt");
xttp.send();
```
`open` - initializes a new request or re-initializes an existing one
+ First parameter - specifies the HTTP method to be used for the request
	+ `"GET"` means it's a request to retrieve data from the server
+ Second parameter - specifies the URL/path you want to fetch
	+ In this case, retrieves data from `ajax_info.txt`
`send` - sends the request to the server



### Source:
https://www.w3schools.com/js/js_ajax_http.asp - has more enough on XMLHttpRequest object methods and properties
+ Not a programming language
+ A technique for accessing web servers from a web page
+ Stands for Asynchronous JavaScript and XML
+ Uses a combination of
	+ A browser built-in `XMLHttpRequest` object (requests data from a web server)
	+ JavaScript and HTML DOM (Document Object Model) to display/use data

Allows you to:
+ Read data from a web server *after* the page has loaded
+ Update a web page *without* reloading the page
+ Send data to a web server in the background

## How AJAX Works
1. An event occurs in a web page (page is loaded, button is clicked, etc.)
2. An XMLHttpRequest object is created by JavaScript
3. The XMHttpRequest object sends a request to a web server
4. The server processes the request
5. The server sends a response back to the web page
6. The response is ready by JavaScript
7. Proper action (e.g. page update) is performed by JavaScript

NOTE: Modern browsers can use Fetch API instead (simpler version of the XMLHttpRequest object).

### Source:
https://www.w3schools.com/js/js_ajax_intro.asp
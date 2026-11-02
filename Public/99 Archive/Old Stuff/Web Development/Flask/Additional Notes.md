## Terminology:
*Registering* something means to associate it with an application instance so that it can be recognized and used by the Flask framework

## [HTTP Methods:](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)  
These are standardized request types that indicate the desired action to be performed on a resource identified by a URL

**Common methods:**
+ GET 
	+ Retrieves data from the server (default method when visiting a URL in browser)
+ POST  
	+ Used to send data to the server (e.g. submitting a form)
+ PUT  
	+ Used to update existing data on the server
+ DELETE  
	+ Used to delete data from the server

## Endpoints and URLs:
`url_for()` generates a URL to a view based on name and arguments

+ The *endpoint* is the name associated with a view
	+ By default it's the same name as the view function  

When using blueprints, the name of the blueprint is <u>prepended</u> to the view function name.

+ For a `login` function in an `auth` blueprint, the endpoint would be `auth.login` and the URL would end with `auth/login`

`add_url_rule()` changes how URL's are generated
Example: `add_url_rule('/', endpoint='index')`
+ Associates the endpoint name `'index'` with the URL `/`
+ `url_for('index')` will generate `/` instead of `/index`

## Deploying to Production
For information on deploying an application to a server, see 
[Deploy to Production from the Official Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/)
[Deploying to Production – Flask](https://flask.palletsprojects.com/en/3.0.x/deploying/)

Implements WSGI, which is the standard Python interface between applications and servers.
+ [WSGI](https://wsgi.readthedocs.io/en/latest/) is a specification that describes how a web server communicates with web applications and how web applications can be chained together to process one request

#### Functions:
`abort()` raises special exceptions that returns an HTTP code
+ Takes an optional message to show with the error, otherwise a default message is used
Example: `abort(404, f"Post id {id} doesn't exist.")`
+ Returns HTTP error code 404 along with the message `f"Post id {id} doesn't exist."


Sources:

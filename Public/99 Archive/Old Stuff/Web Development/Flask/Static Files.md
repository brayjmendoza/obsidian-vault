These are files that **will not** change. Essentially the opposite of a template

Flask automatically adds a `static` view. It's path is relative to the `flaskr/static` directory (Note that `flaskr` is the name of the package for the app).

Thus,  
> `url_for('static', filename='style.css')`

Returns the URL for the file `style.css`, which is located in the `static` directory since style.css is a static file

Note that `static` is an endpoint and so can be used with `url_for()` 

Static files are usually CSS or JavaScript files
[CSS Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)

#### Source: 
https://flask.palletsprojects.com/en/3.0.x/tutorial/static/
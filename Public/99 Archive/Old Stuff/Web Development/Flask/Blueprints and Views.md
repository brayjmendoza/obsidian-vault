A *view function* is the code you write to respond to requests to your application.
A *blueprint* is a way to organize a group of related views and other code.

+ Views registered with a blueprint, which is then registered with the application

# Initializing a Blueprint  
> `bp = Blueprint('auth', name, url_prefix='/auth')

This creates a `Blueprint`

+ First argument: name of the blueprint (`auth`)
+ Second argument: where the Blueprint is defined ( `__name__` )  
	+ Blueprints need to know where it's defined (like with application objects)
+ The `url_prefix` is prepended to all URL's associated with the blueprint

### Registration:
Blueprints must be registered with the application because it tells the application instance that the blueprint exists and all of the routes, templates, static files, etc. that it defines. 

Registering a blueprint integrates it into the application:
```
def create_app():
    app = ...

    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

return app
```
We can use the `register_blueprint()` method to register blueprints in the application factory.

# Example Blueprint: Authentication  
### Register View:
```
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'

        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
	            db.execute(
                    "INSERT INTO user (username, password) "
                    "VALUES (?, ?)",
                    (username, generate_password_hash(password)),

				)
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
                
        flash(error)

    return render_template('auth/register.html')
```

`@bp.route` associates the URL `/register` with this view function  

+ When a request is received to `/auth/register`, this function will be called and it's return value is the response
+ `methods` specifies what requests types the route can accept
	+ This function can only be called for GET and POST request types 
		+ "405 Method Not Allowed" error will be thrown otherwise

`request.method` determines the HTTP method used for the current request (e.g. GET or POST)

+ If the HTTP method (request type) is POST, then that means a user submitted the form 
	+ In this case, start validating the input  
	+ Otherwise, return the HTML template (contained in `auth/register.html` )
		+ This will happen after the input gets validated, or the HTTP method was GET 

`request.form` is a type of dict that maps keys and values from a form submission

+ Here, the user inputs their `username` and `password`, which we can then access using `request.form`
	+ The following if/elif block checks that `username` and `password` aren't empty 
	+ If both exist, insert new user data into database

`db.execute` performs a single SQL query
+ Allows `?` placeholders for user input  
	+ The following tuple replaces these `?` placeholders  
	- These values are automatically escaped to prevent an SQL injection attack
+ <u>Passwords should never be stored directly in a database</u> for security reasons 
	+ `generate_password_hash()` securely hashes the password and the hash is stored in the database  

`db.commit()` saves changes made in the database
+ `sqlite3.IntegrityError` would occur if the username already exists  

If `username` and `password` validation succeeds (and user is stored in database), they are redirected to the login page.
+ `url_for()` generates the URL for auth.login (the login view)
+ `redirect()` navigates client to the specified URL (in this case `url_for())` 

If validation fails, then error is shown to user

+ `flash()` stores messages that can be retrieved when rendering the template  
	- `error` will be stored, and then shown to the user when the HTML is rendered from `render_template()`

`render_template()` renders a template containing HTML (which the user sees)

### Login View:
The `login` view is similar to the `register` view
```
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()

            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
        
    return render_template('auth/login.html')
```

+ `fetchone()` returns one row from the query (`None` if no results returned)
+ `check_password_hash()` hashes the `password` the same way as the stored hash to securely compare them.
	+ Returns `True` if the hashes match
	+ `user['password']` is the hashed password stored in the database for user

`session` is essentially a dictionary that stores data across requests

+ Successful validation: the user's `id` is stored in a new session  
	+ Data is stored in a *cookie*, which tracks, personalizes, and saves information about a user's session (time spent on a website)
	+ The cookie is sent to the browser, which sends it back with subsequent requests 
	+ Flask *signs* the data for security

Now that the `id` is stored in `session`, whenever the user is logged in, their information can be loaded (and made available to other views) for new requests
```
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
```
Checks if a user id is stored in the `session` retrieves it 

`@bp.before_app_request` registers a function that runs before the view function for all URL's (i.e. when `register` is requested, `load_logged_in_user` will run before `register`)

User data is stored in `g.user`, which lasts the length of the request. Thus, the user's information is made available (when logged in) for all subsequent requests. We know the user is logged in because their ID is stored in the session.

### Logout View:
All we need to do to logout is remove the user id from the `session` , so that `load_logged_in_user` will store `None` in` g.user`
```
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
```
**Note** that `'index'` refers to the main page, or the view function for `@app.route('/')`

## Other Examples: 
#### Views with arguments  
Note: `login_required` is a decorator we created
```
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()

            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)

            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)
```
Here, we have a view for `update`, which allows a user to update a post they created. It takes in the argument `id` , which is the post id, so we know what post is to be updated.

The argument `id` corresponds to `<int:id>` in the route
+ Example URL: `/1/update`  
	+ `1` is the post id, and it will be passed into the `id` argument for this view
	+ `int:` tells Flask to ensure it's an int
		+ If this is not specified, id will instead be a string
+ When generating a URL, `url_for()` needs to be passed the id 
	+ `url_for('blog.update, id=post['id'])`
		+ Generates the URL for the update view, passing in `post['id']` for `id`

##### Sources:
https://flask.palletsprojects.com/en/3.0.x/tutorial/views/
https://flask.palletsprojects.com/en/3.0.x/tutorial/blog/
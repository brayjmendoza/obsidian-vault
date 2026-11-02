## Create/View Database Connection
```
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

return g.db
```
Opens a connection to the database and stores it in `g.db`. If a connection already exists, it reuses it (instead of creating another connection)

`if 'db' not in g` checks if the variable `db` exists for this `g` object 

`sqlite3.connect` establishes a connection to the database
+ First parameter (path-like) specifies what database to connect to
	+ `current_app` is a special object that points to the Flask application handling the sequence  
		+ Thus, `current_app.config['DATABASE']` returns the file pointed at by the `DATABASE` configuration key (which is where the database will exist)

+ `detect_types` controls whether/how data types that aren't natively supported by SQLite are handled
	+ `PARSE_DECLTYPES` says to look up a converter function using the declared types for each column (i.e. TIMESTAMP will be recognized and use the converter function that allows it to store a DateTime object)

`row_factory` controls how a row is fetched
+ If none, row is represented as a tuple  
+ `g.db.row_factory` refers to the `row_factory` that is attributed to the database connection stored in `g.db`
+ `sqlite3.Row` tells the connection to behave like a dictionary

## Close Database Connection
```
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```
Closes a connection to a database connection if it exists  

`g.pop('name', default = None)` gets and removes an attribute by name
+ First parameter is the attribute to be removed  
+ Second parameter is the value to return if the attribute doesn't exist

`db = g.pop('db', None)`, returns `g.db` and removes the attribute `db` from `g`. Returns `None` if `g.db` does not exist
+ `g.db` is stored in `db` if it exists  
+ `db` stores `None` if there was no database connection
+ `db` then used to close the connection (if it exists)
[Explanation for e=None](https://stackoverflow.com/questions/57455431/flask-official-tutorial-what-is-e-in-close-dbe-none)

## Running SQL in Python
```
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
```
Runs the SQL commands found in `schema.sql`  

`open_resource` opens a file relative to the location of the Flask application

```
with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
```
Opens the `schema.sql` file and aliases it as `f`
`f.read()` reads `schema.sql` (in binary)
`decode('utf8')` translates the binary into a string encoded by utf-8
`executescript` is used to execute multiple SQL statements from a single string

## Registering with the Application
```
def init_app(app):
        app.teardown_appcontext(close_db)
```
Registers the `close_db` and `init_db_command` functions with the application instance
+ For application factories, we don't have access to an application instance when developing, so we create a function that does the registration instead

`app.teardown_appcontext()` tells Flask to call the function after returning a response (at the end of a request)

To finish registration, run `init_app(app)` in the application factory function
```
def create_app():
    app = ...

    # existing code omitted

    from . import db
    db.init_app(app)

return app
```
where `init_app()` exists in the `db.py` file, which is in the same package 

### Notes:
+ SQLite database connections are stored as a `Connection` object 
	+ These are created when using `sqlite3.connect()`
+ By default, `current_app.open_resource()` opens a file in binary mode

##### Sources:
https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
https://docs.python.org/3/library/sqlite3.html  
and other Python documentation
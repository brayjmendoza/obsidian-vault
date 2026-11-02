Example from `Documents/Programming/flask_tutorial`
```
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
		pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    return app
```

`app = Flask(__name__, instance_relative_config = True)`
+ An instance of Flask, `__name__` is name of current Python module (file) 
	+ An instance of Flask is an *application* instance  
	+ Serves as the central registry for the application
		+ Manages routes, configurations, extensions, etc. 
	+ Defines routes, handles requests, and more
+ `instance_relative_config` tells the app that config files are relative to instance folder 
	+ Anything in instance folder cannot be committed to version control
		+ Good for configuration secrets and database file 

`app.config.from_mapping()` sets default configuration
+ `SECRET_KEY` used to keep data safe  
	+ Set to 'dev' for convenience when developing 
	+ Should be random when deploying (public use)
+ `DATABASE` is the path where database file is saved 
	+ Tutorial uses SQLite
	+ `app.instance_path`refers to the path that Flask uses for the instance folder 

`app.config.from_pyfile()` overrides default configuration
- `'config.py'` is the file used to override (in instance folder) 
	- Is the config for this specific instance  
	+ Can be used to set SECRET_KEY
	+ If `config.py` doesn't exist, `silent = True` tells Flask to silently ignore the error and continue
- `test_config` can be used instead of instance config
	- Provided by factory (developer)  
	- Used for testing

`@app.route(endpoint)`
+ Decorator that creates a connection between URL/endpoint to the following function

## Application Factories:
It's good practice to use an application factory when making apps. An application factory is a function that returns instances of the application. This allows us to test the app in different environments (e.g. testing environments). The example is an application factory because `create_app` returns `app`, which is an application instance 

##### Source: 
https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/
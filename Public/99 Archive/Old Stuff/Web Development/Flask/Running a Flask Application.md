First, ensure you are in top-level directory (i.e. `flask-tutorial`) that contains all packages, etc.

Next, be sure to activate the virtual environment
For macOS:
> `$ source .venv/bin/activate`

Note that `source` and `python -m `do the same thing (run the script specified by the path) 

Then, run the application with the `flask` command:
> `$ flask --app flaskr run --debug`

`--app` specifies where the application is (in this case, `flaskr` )
`--debug` runs in debug mode

#### Debug mode:
+ Shows interactive debugger when a page raises an exception
+ Restarts server when changes are made to the code

Example output after running command:
>`* Serving Flask app "flaskr"`
>`* Debug mode: on`
>`* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`
>`* Restarting with stat`
>`* Debugger is active!`
>`* Debugger PIN: nnn-nnn-nnn`

This shows that application is running on http://127.0.0.1:5000/
+ 5000 is the port  
+ If a program is already using port 5000, `OSERROR: [Errno 98]` or `OSError: [WinError 10013]` will occur  
+ Easy solution: use different port
	+ [Other solutions](https://flask.palletsprojects.com/en/3.0.x/server/#address-already-in-use)

#### Source:
https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/
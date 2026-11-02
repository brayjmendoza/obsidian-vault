+ Flask provides a test client that simulates a request to the application and returns the response data
	+ Use to create unit tests to check application functionality
## Fixtures
*Fixtures* are setup functions that each test function uses
**Note:** `@pytest.fixture` is a python decorator that specifies that the following function is a fixture
##### Examples:
```
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

	# create tables and insert data at temp path
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)
```
+ `tempfile.mkstemp()`
	+ Creates and opens a temporary file
	+ Returns the file descriptor and path for the temporary file
		+ `db_fd` is the file descriptor, `db_path` is the file path

+ `db_path` is used to override the `DATABASE`path (which has a default value given in the `create_app` function)
	+ `DATABASE` points to the temporary path instead of the instance folder
	+ Database tables/data are created/inserted at this temp path instead
	+ The temporary file is closed and removed after each test is over

+ `with app.app_context()`
	+ `app.app_context` creates and pushes an application context, making the current Flask application (`app`) instance active within the function, so we can use `init_db` and `get_db` without experiencing errors
	+ `with` ensures that the application context is correctly managed
		+ At the start of the block, `app.app_context` is called, ensuring resources are properly acquired
			+ Automatic setup
		+ At the end, the application is popped and resources are cleaned
			+ Automatic cleanup

+ `yield app`
	+ For pytest fixtures, code before `yield` is setup code for tests (which happens before a test is called), and code after `yield` is teardown code (which happens after a test is executed)
	+ When a test uses this fixture, it has access to `app`(because it is yielded)
		+ The yielded value is the provided resource for the test function
	+ **Note:** yielding a value is optional, it could yield nothing, just to indicate what is setup and teardown code

+ `os.close(db_fd)`
	+ Closes the file descriptor for the temporary database file created earlier
+ `os.unlink(db_path)`
	+ Deletes the temporary database file for cleanup after tests
	+ Ensures test environment doesn't leave behind unnecessary files

```
@pytest.fixture
def client(app):
    return app.test_client()
```
+ Uses the client to make requests (for tests) to the application without actually running the server
+ `app.test_client()` creates a test client for `app`
	+ Behaves like an actual client (e.g. web browser) that interacts with the Flask app
		+ Allows us to perform HTTP requests and get responses without running a live server

```
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```
+ Similar to `client`, `runner` can call registered Click commands
+ `app.test_cli_runner()`creates a test CLI runner for `app`
	+ Allows us to simulate running custom commands

## Test Examples
```
def test_config():
	assert not create_app().testing
	assert create_app({'TESTING: True'}).testing
```
+ Tests if the `'TESTING'` configuration is properly handled
+ `.testing` returns `True` if the `'TESTING'` configuration key is `True`
	+ Note that the default value for `'TESTING'` is `False`
#### Database Tests:
```
def test_get_close_db(app):
	# Test if each connection is the same
	with app.app_context():
		db = get_db()
		assert db is get_db()

	# Test if the connection is closed
	with pytest.raises(sqlite3.ProgrammingError) as e:
		db.execute('SELECT 1')

	assert 'closed' in str(e.value)
```
+ Tests if get_db returns the same connection each time it's called 
+ Also tests if the connection is closed after each application context
	+ `sqlite3.Progammming Error` - an exception that is typically raised when trying to operate on an SQLite database connection that has already been closed
	+ `pytest.raises` - checks whether a particular exception is raised when a block of code is run
		+ Use this in conjunction with `with` (i.e. we expect a `sqlite3.ProgammingError` when `db.execute('...')` is run)
		+ If the expected exception is raised, it's caught and is stored in `e`
		+ If the exception is not raised (or there is no exception at all), pytest will fail the test
			+ Note that `db` is cleared within the first `with` block

```
def test_init_db_command(runner, monkeypatch):
	class Recorder(object):
		called = False
	
	def fake_init_db():
		Recorder.called = True

	monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
	result = runner.invoke(args=['init-db'])
	assert 'Initialized' in result.output
	assert Recorder.called
```
Checks if the `init-db` command calls the `init_db` function and if there is the correct output message
+ `monkeypatch` - a fixture provided by `pytest`
	+ Allows us to modify/replace attributes, functions, or classes during a test
	+ Commonly used to temporarily replace parts of the application
		+ This test uses it to replace the `init_db` function with one that tells us that it's been called
+ The `Recorder` class
	+ Used to check if `fake_init_db` was called during the test
+ `fake_init_db`
	+ Simulates the `init_db` function by setting `Recorder.called` to `True`
		+ Indicates that `fake_init_db` was called
+ `monkekypatch.setattbr('flask.db.init_db', fake_init_db)`
	+ Uses `monkeypatch` to replace `init_db` with `fake_init_db` so that when the `init-db` command is invoked, it will call `fake_init_db` instead
+ `result = runner.invoke(args=['init-db'])`
	+ Uses the `runner` fixture to invoke the `init-db` command
	+ `result` contains the output and status of running the command
#### Authentication Tests:
```
@pytest.mark.parametrize(('username', 'password', 'message'), (
	('', '', b'Username is required.'),
	('a', '', b'Password is required.'),
	('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
	response = client.post(
		'/auth/register',
		data={'username': username, 'password': password}
	)
	assert message in response.data
```
Tests that the error messages are displayed properly given each error scenario when logging in 
+ `@pytest.mark.parameterize` is a `pytest` decorator that allows you to run the same test function with multiple sets of parameters
	+ Here, it's used for different combinations of `username`, `password`, and `message` (the expected error message)
+ `response.data` contains the body of the HTTP response `reponse` in bytes (which is why we use `b` strings in the decorator)

## Running the Tests
Extra configuration can be added to the `pyproject.toml` file to make running tests with coverage less verbose
```
[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
branch = true
source = ["flaskr"]
```
+ `[tool.pytest.ini_options`] configures options for `pytest`
	+ `testpaths` tells `pytest` where to look for test files
		+ `["tests"]` indicates that it should search for test files in the `tests` directory
+ `[tool.coverage.run]` configures options for `coverage.py`, a tool used to measure code coverage of tests
	+ `branch = true` enables branch coverage measurement
		+ Checks whether each possible branch (e.g. `if` and `else` conditions) in the application code has been executed during testing (not just whether each line has been executed)
	+ `source` tells `coverage.py` what code to include in the coverage report
		+ `["flaskr"]` indicates that coverage should be measured for code in the `flaskr` module

To run the tests, simply type `pytest` in the CLI from the root directory of the project
> `pytest`

To see a list of each test function (rather than dots), run
> `pytest -v`

To measure the code coverage of the tests, first run the following command to run `pytest` with `coverage` instead of directly
> `coverage run -m pytest`

Then, for a simple coverage report in the terminal, run
>`coverage report`

Alternatively, you could view an HTML report with
> `coverage html`
+ This generates a directory `htmlcov`, and the report can be found in `htmlcov/index.html`

## Additional Notes
```
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')
```
+ Reads the contents of the `data.sql` file (is a binary file)
	+ Decodes it to a UTF-8 string
		+ Stores the result in `_data_sql`
+ `os.path.dirname(__file__)`
	+ Returns the directory of the current script
	+ `__file__` is a special Python variable that contains the path to the current script
+ `os.path.join(..., 'data.sql')`
	+ Combines the directory path (from the above bullet point) with the filename `'data.sql'` to create a full file path to the `data.sql` file
		+ Allows the code to find `data.sql` regardless of OS conventions
+ `with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:`
	+ `with open(..., 'rb') as f:` opens the `data.sql` file in binary mode        (`'rb'` stands for "read binary")
		+ `with` ensures that the file is properly closed after it has been read, even if an error occurs.
    - `f` represents the open file object.

##### Source:
https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/
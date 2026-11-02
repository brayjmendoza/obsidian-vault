`g` stands for global 

`g` is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request.

Each instance of `g` only exists for the lifespan of a request. For each request, a new instance of `g` is created

`g` is thread safe within a single request. So, each thread handling a request has it's own isolated `g` object. For a new request, another *different* `g` object is initialized, so that data stored in `g` is not shared between requests
+ This all holds true for concurrent requests  
+ For two requests A and B, Flask handles both independently, and both A and B have their own independent g objects, which individually store different data

`g` can hold variables, called attributes, defined by `g.ATTRIBUTE_NAME`. For example, `g.num = 42`, stores the number 42 in `g` , which can then be accessed as `g.num` by functions throughout the request that `g` is responsible for.

### Example (from ChatGPT):
```
from flask import Flask, g

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        # replace with actual database connection function
        g.db = connect_to_database()
    return g.db

@app.route('/')
def index():
    db = get_db()  # get the database connection from g
    # Perform database operations...
    return 'Hello, World!'

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run()
```
#### Source:
https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
Click is a Python package used for creating commands. 
+ Declares commands through Python decorators
[Click Documentation](https://click.palletsprojects.com/en/8.1.x/)

**Example:**
```
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
```
`@click.command()` is the decorator used to make the following function (in this case, `init_db_command`) a command
+ `'init-db` is the name of the command when run in the terminal

`click.echo('Message')` displays a `'Message'` in the terminal when the command is run

**Running the Click Command:**
In the context of Flask, we need to register the command with the application. We can register the command like how we registered `close_db()` 

`app.cli.add_comand(command)` adds a new command `command` that can be called with the `flask` command.

After registering, The example command would be run as follows:
>`$ flask --app flaskr init-db`

If all goes well, it will output
>`Initialized the database.`


Source:
https://flask.palletsprojects.com/en/3.0.x/tutorial/database/ 
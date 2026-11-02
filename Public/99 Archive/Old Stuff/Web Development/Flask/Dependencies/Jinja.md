A template language that renders the pages your application serves

#### Properties:
Automatically *escapes* data rendered in HTML templates
+ This makes it safe to render user input, as characters that can mess with the HTML (like `<` and `>`) will be *escaped* with values so that the HTML is unaffected
	+ Example: `<a>` gets translated to `&lt;a&gt;` which when rendered will display `<a>` rather than being interpreted as an HTML tag

**Delimiters** used to distinguish Jinja syntax from static data (e.g. HTML) in the template
+ Anything between `{{` and `}}` will be evaluated and outputted to the final document
	+ Example: `{{ url_for(auth.login) }}` will return the URL for `auth.login`
+ `{%` and `%}` denotes a control flow statement (stuff like `if` and `for`)

#### Tags:
`{% block %}` tags specify sections that child templates fill in
+ Tells the template engine that a child template may override these placeholders
+ Will always be executed (even if in an `if` block that doesn't get rendered)
+ Example: `{%block title}{%endblock%}` is a block that will be overridden by a child template
	+ `title` is the name of the block

`{% extends base.html' %}` tells Jinja that this template should replace blocks from the `base.html` template
+ Appears at the top of a template file
+ This indicates a child template

Sources:
https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/
[Jinja Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)
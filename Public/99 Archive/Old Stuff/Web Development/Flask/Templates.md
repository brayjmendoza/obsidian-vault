Templates are files that contain static data and placeholders from dynamic data. Templates are rendered with specific data to produce a final document, which is what the user sees. 
Templates use [[Jinja]] to render

### Base Layout:
Pages in an application could have the same basic layout. Templates can be used to *extend* a base template (overriding specific sections) to avoid code repetition.

The base template is typically named `base.html`
```
<!DOCTYPE html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>

  <h1>Flaskr</h1>
  <ul>

    {% if g.user %}
      <li><span>{{ g.user['username'] }}</span>
      <li><a href="{{ url_for('auth.logout') }}">Log Out</a>

    {% else %}
      <li><a href="{{ url_for('auth.register') }}">Register</a>
      <li><a href="{{ url_for('auth.login') }}">Log In</a>

    {% endif %}
  </ul>

</nav>
<section class="content">

  <header>
    {% block header %}{% endblock %}

  </header>
  {% for message in get_flashed_messages() %}

    <div class="flash">{{ message }}</div>
  {% endfor %}
  {% block content %}{% endblock %}

</section>
```
**Note**: `g` and `url_for()` are automatically available in templates, so we can access data in `g` and take advantage of `url_for()` functionality

`get_flashed_messages()` returns all messages stored by `flash()` from the session. Thus, the `for` loop will display all error messages (since we have only been storing error messages in `flash()`)

#### Source: 
https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/
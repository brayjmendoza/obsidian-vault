```
<form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Register">
  </form>
```

#### Form Tag:
>`<form method="post">
- **`<form>`**: This element defines the start of an HTML form.
- **`method="post"`**: Specifies that the form will be submitted using the POST method. This means that the form data will be sent in the body of the HTTP request, which is more secure for sending sensitive information like passwords compared to the GET method.

#### Username Label and Input:
>`<label for="username">Username</label>
>`<input name="username" id="username" required>
- **`<label for="username">`**: Associates the label with the input field that has the `id="username"`. Clicking the label will focus the associated input field.
    - **`<input name="username" id="username" required>`**: Creates an input field for the username.
        - `name="username"`: The name attribute is used to reference the form data after submission.
        - `id="username"`: The id attribute uniquely identifies the input field and associates it with the label.
        - `required`: Specifies that this field must be filled out before submitting the form.

#### Password Label and Input:
>`<label for="password">Username</label>
>`<input type="password" name="password" id="username" required>
- **`<label for="password">`**: Associates the label with the input field that has the `id="password"`.
    - **`<input type="password" name="password" id="password" required>`**: Creates an input field for the password.
        - `type="password"`: Masks the input characters to ensure privacy.
        - `name="password"`: The name attribute is used to reference the form data after submission.
        - `id="password"`: The id attribute uniquely identifies the input field and associates it with the label.
        - `required`: Specifies that this field must be filled out before submitting the form.

#### Submit Button:
>`input type="submit" value="Register
+ **`<input type="submit">`**: Creates a submit button.
    - `value="Register"`: Sets the text displayed on the button to "Register".


Source: ChatGPT
## Run Development Server
> `python3 manage.py runserver`

## Make Database Model Changes
1.  Change your models (in `models.py`). 
2. Run [`python3 manage.py makemigrations`](https://docs.djangoproject.com/en/5.1/ref/django-admin/#django-admin-makemigrations) to create migrations for those changes
3. Run [`python3 manage.py migrate`](https://docs.djangoproject.com/en/5.1/ref/django-admin/#django-admin-migrate) to apply those changes to the database.

## Testing
#### Rules of Thumb:
1. Have a separate `TestClass` for each model or view
2. Have a separate test method for each set of conditions you want to test
3. Have test method names that describe their function

+ [Testing in Django](https://docs.djangoproject.com/en/5.1/topics/testing/)
+ [LiveServerTestCase](https://docs.djangoproject.com/en/5.1/topics/testing/tools/#django.test.LiveServerTestCase)
+ [Integration with coverage.py](https://docs.djangoproject.com/en/5.1/topics/testing/advanced/#topics-testing-code-coverage)

# Django & React
![[DjangoAndReact.png]]

## More Documentation
[How the Documentation Works](https://docs.djangoproject.com/en/5.1/intro/whatsnext/)
[Documentation Home Page](https://docs.djangoproject.com/en/5.1/topics/)
[How-To Guides](https://docs.djangoproject.com/en/5.1/howto/)
[Database API](https://docs.djangoproject.com/en/5.1/topics/db/queries/)
[Model Relations](https://docs.djangoproject.com/en/5.1/ref/models/relations/)
[Field Lookups via Database API](https://docs.djangoproject.com/en/5.1/topics/db/queries/#field-lookups-intro)
[URL Configurations](https://docs.djangoproject.com/en/5.1/topics/http/urls/)
[Templates](https://docs.djangoproject.com/en/5.1/topics/templates/)
[Request and Response Objects](https://docs.djangoproject.com/en/5.1/ref/request-response/)
[Generic Views](https://docs.djangoproject.com/en/5.1/topics/class-based-views/)
[Static Files Reference](https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/)
[Template Loading](https://docs.djangoproject.com/en/5.1/topics/templates/#template-loading)

## Extras
[Third-Party Packages List](https://djangopackages.org/)

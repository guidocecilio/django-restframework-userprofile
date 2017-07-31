# Public Profile

Public Profile is a Django REST Framework based API that demos how to extends
a default Django Auth User model with a Profile. In addition, the code also
includes a demo client that show how to consume the API from a Client Web
Application.

## Makefile

This project uses a Makefile for various tasks. Some of the available tasks
are listed below.

* `make setup`  - Setup the application (Creates venv, db, and loads fixtures)
* `make run`    - Run the server
* `make test`   - Run Unit Tests (using nose)
* `make lint`   - Get a pep8 compliance report about your code

## Backends
### Fixtures
The API comes with some data dumped by default that might be useful for testing
purpose.

Install fixtures by runnign the command:
```shell
$ python src/manage.py loaddata topics users
```

To backup your test fixtures use the following command:
```shell
$ python src/manage.py dumpdata auth.User --indent 4 > src/api/fixtures/users.json
$ python src/manage.py dumpdata api.topic --indent 4 > src/api/fixtures/topics.json
$ python src/manage.py dumpdata api.profile --indent 4 > src/api/fixtures/profiles.json
```

Then the API is exposed in your localhost through the port 8000
### Authentication
The API provides three default authentication. However, any Django REST
Framework supportes authentication can be added to the list of authentication
classes.

The top authentication class used by the API is the JWT

#### Security
Unlike some more typical uses of JWTs, this module only generates authentication
tokens that will verify the user who is requesting one of your DRF protected API
resources. The actual request parameters themselves are not included in the JWT
claims which means they are not signed and may be tampered with. You should only
expose your API endpoints over SSL/TLS to protect against content tampering and
certain kinds of replay attacks.

#### Using the API
You can easily test if the endpoint is working by doing the following in your
terminal, if you had a user created with the username admin and password
password123.

```shell
$ curl -X POST -d "username=admin&password=password123" http://localhost:8000/api-token-auth/
```

Alternatively, you can use all the content types supported by the Django REST
framework to obtain the auth token. For example:
```shell
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:8000/api-token-auth/
```

Now in order to access protected api urls you must include the Authorization:
JWT <your_token> header.
```shell
$ curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/
```

Visit [REST framework JWT Auth](http://getblimp.github.io/django-rest-framework-jwt/)
for a detailed explanation about Django REST Framework and JWT.


### Debug
#### Debugging unit test
To debug the unit test code, it is recommended to use the virtual environment
and the following command to append the conole output and allow the developer
to print data to the console output. e.g:
```shell
(.env) $ python src/manage.py test -s
```
## Clients

Client side applications are located within the `clients` folder in the root of
project. At the moment of this writing the available client application is the
`` but there will be even mobiles app for
consumption of __REST API__.

### Development
As all clients application are managed independently there should be a
__README.md__ file with instruction about how to use or extend the client
application.

### React Web Application
For more details about how to deploy or extend the web app please refer to the
__README.md__ file within client repository code.

[React User Profile](https://github.com/guidocecilio/react-userprofile)

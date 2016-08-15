#Eve-TokenAuth

## Introduction

Eve-TokenAuth is a way to add an auth layer on top of your existing eve app.

It is meant to be compatible with the awesome Satellizer project:

[Satellizer Github](https://github.com/sahat/satellizer/)

It follows this example: [Satellizer Python Server Example](https://github.com/sahat/satellizer/blob/master/examples/server/python/app.py)

## Usage

### Running the Example

To run the example, you will need to have a mongodb setup and change the settings.py to reflect your mongo server's
settings. A default.settings.py file is included.

It may require creating a user for the db as well:

``` 
db.addUser( { user: "user", pwd: "user", roles: [ "readWrite" ] } )
```

### Running the Tests
The tests currently setup a db according to the settings in testsettings.py. You will need to have a mongo server
running to run the tests.


### Using with your Eve App

This needs better docs. The gist is you:

1) Wrap your Eve with the Eve-TokenAuth Constructor:


    apiapp = Eve()
    evewta = EveWithTokenAuth(apiapp)


    This will create an accounts and a token endpoint.

2) Add Authentication to your Resource Configuration

    from eve_tokenauth.auth.token import TokenAuthentication
    ...
    books = {
        'authentication': TokenAuthentication(),
        ...
    }

3) Launch your app
4) Register an account

    curl -X POST -H "Content-Type: application/json" -d '{"first_name":"Navin R.","last_name":"Johnson","email":"a@a.net","password":"password","is_email_confirmed":true}' http://localhost:5000/api/v1/accounts
    
    curl -X POST -H "Content-Type: application/json" -d '{"username":"janreyho","password":"password","nickname":"李老师"}' http://localhost:5000/api/v1/teachers
5) Get a token with that account

    curl -X GET -H "Content-Type: application/json" -u "a@a.net:password" http://localhost:5000/api/v1/tokens
    
    curl -X GET -H "Content-Type: application/json" -u "janreyho:password" http://localhost:5000/api/v1/tokens
6) Use that token to hit your endpoint

    curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer ..." http://localhost:5000/api/v1/

### 添加学生和课程

    curl -H "Content-Type: application/json" -H "Authorization: Bearer ..." -d '{"username": "janreyho", "nickname": "janrey"}' http://127.0.0.1:5000/api/v1/students

    curl -H "Content-Type: application/json" -H "Authorization: Bearer ..." -d '{"teacherID": "57b177d89d7d9b5c12c30d4b", "studentID": "57b1a7359d7d9b6e61abef2c"}' http://localhost:5000/api/v1/courses

### Roadmap

- Rate Limit / Secure Registration Endpoint
- Store OAuth properly
- Document lol
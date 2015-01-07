#Eve-TokenAuth

## Introduction

Eve-TokenAuth is a way to add an auth layer on top of your existing eve app.

## Usage

### Running the Example

To run the example, you will need to have a mongodb setup and change the settings.py to reflect your mongo server's
settings.

It may require creating a user for the db as well:

``` 
db.addUser( { user: "user", pwd: "user", roles: [ "readWrite" ] } )
```

### Running the Tests
The tests currently setup a db according to the settings in testsettings.py. You will need to have a mongo server
running to run the tests.

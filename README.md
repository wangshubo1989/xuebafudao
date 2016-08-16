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
    
    curl -v -X POST -H "Content-Type: application/json" -d '{"username":"janreyho2","password":"password","nickname":"李老师"}' http://localhost:5000/fudaoapi/v1/teachers
5) Get a token with that account

    curl -v -X GET -H "Content-Type: application/json" -u "janreyho:password" http://localhost:5000/fudaoapi/v1/tokens
6) Use that token to hit your endpoint

    curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer ..." http://localhost:5000/fudaoapi/v1/

### 添加学生和课程

    curl -H "Content-Type: application/json" -H "Authorization: Bearer ..." -d '{"username": "janreyho", "nickname": "janrey"}' http://localhost:5000/fudaoapi/v1/students

    curl -H "Content-Type: application/json" -H "Authorization: Bearer ..." -d '{"teacherID": "janreyho", "studentID": "hejiayi"}' http://localhost:5000/fudaoapi/v1/courses

### api调用方法
    按lastname排序
    http http://eve-demo.herokuapp.com/people\?sort\=lastname
    http http://eve-demo.herokuapp.com/people?where=\{\"lastname\":\"Doe\"\}
    //引号需要转义
    http http://eve-demo.herokuapp.com/people?where={\"lastname\":\"Doe\"}
    //空格不能出现
    http http://eve-demo.herokuapp.com/people?where={\"location.city\":\"San%20Francisco\"}

    http http://eve-demo.herokuapp.com/people?where={\"_created\":\"Sun\,%2014%20Aug%202016%2012:20:35%20GMT\"}
    //按照时间查询
    http http://localhost:5000/fudaoapi/v1/courses?where={\"_created\":\"Tue\,%2016%20Aug%202016%2003:36:44%20GMT\"}
    //按照时间区间查找
    http http://localhost:5000/fudaoapi/v1/courses?where={"_created":{"$gte":"Tue, 16 Aug 2016 03:36:44 GMT"}}

    http http://localhost:5000/fudaoapi/v1/courses?where={\"_created\":{\"\$gte\":\"Tue\,%2016%20Aug%202016%2003:36:44%20GMT\"}}
[参照](https://github.com/nicolaiarocci/eve/issues/349)

### Roadmap

- Rate Limit / Secure Registration Endpoint
- Store OAuth properly
- Document lol
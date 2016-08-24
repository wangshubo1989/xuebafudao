

## Usage
    gunicorn -D -c deploy_config.py fudao:apiapp

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


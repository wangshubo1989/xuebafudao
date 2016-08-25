

## install
    yum install python-devel mysql-devel
    pip install -r requirements.txt --trusted-host mirrors.aliyun.com

## Usage
    gunicorn -D -c deploy_config.py fudao:apiapp

##辅导RESTAPI接口说明
http://192.168.0.2:5000/fudaoapi/v1/AAA         支持GET、POST操作
http://192.168.0.2:5000/fudaoapi/v1/AAA/BBB     支持GET、PUT、PATCH、DELETE操作
AAA：表示model名称。分别为：teachers、students、courses、courseProcess、token
BBB：表示某个model的一个具体实例的_id.

teachers、students、courses、courseProcess用token验证
token用用户名和密码验证

1) 注册账号
学生的账号注册和获取token都在学吧课堂移动端进行，可以用拿到token可以直接通过辅导后端的验证。

老师的账号注册：

    POST http://192.168.0.2:5000/fudaoapi/v1/teachers
    username和password必填。
老师获得token：

	GET http://localhost:5000/fudaoapi/v1/tokens

5) Get a token with that account

    curl -v -X GET -H "Content-Type: application/json" -u "janreyho:password" http://localhost:5000/fudaoapi/v1/tokens
6) Use that token to hit your endpoint

    curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer ..." http://localhost:5000/fudaoapi/v1/

### 添加学生和课程

    curl -H "Content-Type: application/json" -H "Authorization: Bearer ..." -d '{"username": "janreyho", "nickname": "janrey"}' http://localhost:5000/fudaoapi/v1/students

    curl -H "Content-Type: application/json" -H "Authorization: Bearer ..." -d '{"teacherID": "janreyho", "studentID": "hejiayi"}' http://localhost:5000/fudaoapi/v1/courses

### 查询课程
可以查询到course信息，内嵌了关联teacher、student、courseProcess的数据，避免多次请求
http://192.168.0.2:5000/fudaoapi/v1/courses?where={"teacherID":"57b70fe709f67b5c44b127af"}&embedded={"processID":1,"studentID":1,"teacherID":1}

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




## install
    yum install python-devel mysql-devel
    pip install -r requirements.txt --trusted-host mirrors.aliyun.com

## Usage
    gunicorn -D -c deploy_config.py fudao:apiapp
    
##model说明
[各model和demo](https://github.com/janreyho/xuebafudao/tree/mysql/doc/datamodel)分别为：teachers、students、courses、courseProcess（课程流程模型，包括体验课和系列课）、token。

* 字段说明：首字符为_的字段，为系统内部字段。
* _id:为模型的实例内部ID。
* _created：为模型实例的创建时间。
* _updated：为模型实例的修改时间。
* _etag：为模型实例的修改标记。
* 模型ID：比如：teacherID、studentID，processID等为关联ID，POST实例A时，需准确设置关联实例B的ID。

##辅导RESTAPI接口说明
http://192.168.0.2:5000/fudaoapi/v1/AAA         支持GET、POST操作

http://192.168.0.2:5000/fudaoapi/v1/AAA/BBB     支持GET、PUT、PATCH、DELETE操作

* AAA：表示model名称。
* BBB：表示某个model的一个具体实例的_id.
* teachers、students、courses、courseProcess用token验证
* token用用户名和密码验证
* teachers和students的POST方法无需验证。

###1 注册账号
学生的账号注册和获取token都在学吧课堂移动端进行，可以用拿到token可以直接通过辅导后端的验证。

老师的账号注册：

    POST http://192.168.0.2:5000/fudaoapi/v1/teachers
    username和password必填。
老师获得token：

	GET http://localhost:5000/fudaoapi/v1/tokens
	username和password必填。

###2 查询数据GET，重点REST查询条件灵活应用。

#### 通用查询，以老师为例
把所有老师信息（可能几百万条）按 _created(升序):第一顺序 -_updated(-为降序):第二顺序 max_results:一页显示2条 page=2:获取第二页。

可以根据需求更改、添加、删除查询条件：sort、max_results、page。

	http://192.168.0.2:5000/fudaoapi/v1/teachers?sort=_created,-_updated&max_results=2&page=2
	headers：
		Content-Type: application/json
		Authorization: Bearer BBB
	返回数据中： _id：是辅导后端老师ID。 accid：是云信等老师ID。
	可以把teachers换成其他model。

#### 内嵌其他实例
可以查询到course信息，内嵌了关联teacher、student、courseProcess的数据，避免多次请求

	http://192.168.0.2:5000/fudaoapi/v1/courses?where={"teacherID":"57b70fe709f67b5c44b127af"}&embedded={"processID":1,"studentID":1,"teacherID":1}
	teacherID：为老师实例中的_id
	embeded：表示返回课程实例的内存实例
	
#### 按时间区间查询
	http://192.168.0.2:5000/fudaoapi/v1/teachers?where={"username":"lihuan", "_updated":{"$gte":"2016-08-21 07:23:30"} ,"_updated":{"$lte":"2016-08-22 07:23:30"}}
	按username为lihuan，2016-08-21 07:23:30<更新资料时间<2016-08-22 07:23:30查询老师
	
	http://192.168.0.2/fudaoapi/v1/courses?where={"teacherID":"lihuan", "startTime":{"$gte":"2016-08-22 11:33:49"} ,"startTime":{"$lte":"2016-09-22 11:35:49"}}&sort=startTime&max_results=2&page=1
	按老师，上课时间日期范围，且上课时间排序，
	
#### 映射查询projection
	http://localhost:5000/fudaoapi/v1/students?projection={"AAA": 1,"BBB":1,"avatar":1}
	仅查询所有老师的AAA、BBB字段，例如avatar字段

#### 聚合查询Aggregation


#### GET某一个版本的json
	http://localhost:5000/fudaoapi/v1/students/100000000000000000000121?version=3
### 4 修改数据PUT/PATCH
	http://localhost:5000/fudaoapi/v1/MMM/CCC
	headers：
		Content-Type: application/json
		If-Match: AAA
		Authorization: Bearer BBB
	data：
		DDD
	字段解释：
		AAA:_etag
		BBB:token
		MMM:具体model
		CCC:_id
		DDD:具体数据


* [参照细节](http://python-eve.org/features.html)
* [RESTful API 设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)
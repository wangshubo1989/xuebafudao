#! /usr/bin/env python
# coding=utf-8
import logging
import logging.config  
import os
from eve.flaskapp import Eve
from tokenauth.eveapp import EveWithTokenAuth
import flask_admin as admin
from flask import Blueprint, render_template, jsonify, current_app as app,abort, g
from eve_swagger import swagger
from neteaseIM.neteaseIM import fudaoSrv
from eve.methods.common import payload as payload_
from bson import ObjectId
from eve.methods.post import post_internal as eve_post_internal
from eve.methods.patch import patch_internal as eve_patch_internal
from eve.methods.put import put_internal as eve_put_internal
from flask import request
import datetime
import json
from neteaseIM.workecAPI import workecSrv

# ret = workecSrv.gettoken()
# if "errCode" not in ret or ret["errCode"] != 200:
#     abort(401, ret)
# print ret["data"]["accessToken"]

# data = {"realname":"ceshi","realmobile":"13562859911","parentmoblie":"13562859911","parentrelation":"baba","realqq":"421"}
# ret = workecSrv.addcustomer(data,ret["data"]["accessToken"])
# if "errCode" not in ret or ret["errCode"] != 200:
#     abort(401, ret)
# Create custom admin view
class MyAdminView(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('myadmin.html')


class AnotherAdminView(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('anotheradmin.html')

    @admin.expose('/test/')
    def test(self):
        return self.render('test.html')

logging.config.fileConfig('config/logging.conf')   
logger = logging.getLogger('main')  
logger.info('main logger start')  

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.py')
apiapp = Eve(settings=SETTINGS_PATH, template_folder='/Users/hejiayi/Desktop/python/eve/fudao/templates')

# Flask views
@apiapp.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

@apiapp.route('/web')
def webindex():
    return render_template('/web/mycourse.html')

admin = admin.Admin(name="Example: Simple Views", template_mode='bootstrap3')
admin.add_view(MyAdminView(name="view1", category='Test'))
admin.add_view(AnotherAdminView(name="view2", category='Test'))
admin.init_app(apiapp)

# /api-docs
apiapp.register_blueprint(swagger)
apiapp.config['SWAGGER_INFO'] = {
    'title': '学吧辅导 API',
    'version': '0.1',
    'description': '一对一辅导，提供实时语音，和教学白板。',
    'termsOfService': 'my terms of service',
    'contact': {
        'name': 'hejiayi',
        'url': 'http://192.168.0.2:5000'
    },

}
apiapp.config['SWAGGER_HOST'] = '192.168.0.2:5000'

evewta = EveWithTokenAuth(apiapp)
apiapp.debug = True

def on_fetched_resource(resource, response):
    # print request.full_path
    for doc in response['_items']:
        if "password" in doc.keys():
            del(doc["password"])
    if(-1 != request.full_path.find("projection=",0,len(request.full_path))):
        for doc in response['_items']:
            for field in doc.keys():
                if field.startswith('_'):
                    del(doc[field])
        del response['_links']
    # del response['_meta']
apiapp.on_fetched_resource += on_fetched_resource
# werkzeug_logger = logging.getLogger('werkzeug')
# werkzeug_logger.setLevel(DEBUG)

def addToworkec(payload):
    ret = workecSrv.gettoken()
    if "errCode" not in ret or ret["errCode"] != 200:
        abort(401, ret)
    print ret["data"]["accessToken"]

    realname = ""
    realmobile = ""
    parentmoblie = ""
    parentrelation = ""
    realqq =""
    if "realname" in payload:
        realname = payload["realname"]
    if "realmobile" in payload:
        realmobile = payload["realmobile"]
    if "mobilenumber" in payload["parentID"]:
        parentmoblie = payload["parentID"]["mobilenumber"]
    if "gender" in payload["parentID"]:
        parentrelation = payload["parentID"]["gender"]
    if "realqq" in payload:
        realqq = payload["realqq"]

    data = {"realname":realname,
        "realmobile":realmobile,
        "parentmoblie":parentmoblie,
        "parentrelation":parentrelation,
        "realqq":realqq}
    ret = workecSrv.addcustomer(data,ret["data"]["accessToken"])
    if "errCode" not in ret or ret["errCode"] != 200:
        abort(401, ret)


# 添加学生家长信息parents
def on_pre_patch_students(resource, request):
    payload = payload_()
    if "parentID" not in payload:
        return

    addToworkec(payload)

    g.parent=payload["parentID"]
    del payload["parentID"]

def on_update_students(updates, original):

    if g.get('parent') and "parentID" in original:
        lookup = dict(_id=str(original['parentID']),)
        ret=eve_patch_internal("parents", g.parent,skip_validation=True, **lookup)
        if ret and ret[3]==200:
            return
        abort(415, ret)

    if g.get('parent'):
        g.parent["studentID"]=original["_id"]
        ret=eve_post_internal("parents", g.parent)
        if ret and ret[3]==201:
            if "_id" in ret[0]:
                updates["parentID"]=str(ret[0]["_id"])
            return
        abort(415, ret)
    return
apiapp.on_pre_PATCH_students += on_pre_patch_students
apiapp.on_update_students += on_update_students

# 添加课程评论teacomments,计算老师平均分
def on_pre_patch_courses(resource, request):
    payload = payload_()
    if "teacommentID" not in payload:
        return
    g.teacomment=payload["teacommentID"]
    del payload["teacommentID"]

def on_update_courses(updates, original):

    if g.get('teacomment'):
        teacomments = app.data.driver.db['teacomments']
        count = teacomments.find({"teacherID":original["teacherID"]}).count()
        teachers = app.data.driver.db['teachers']
        teacher = teachers.find_one({'_id': original["teacherID"]})
        avgScore = 0
        if "avgScore" in teacher:
            avgScore = teacher["avgScore"]

        if "teacommentID" in original:
            teacomment = teacomments.find_one({'_id': original["teacommentID"]})
            scoreChange = g.teacomment["scored"] - teacomment["scored"]
            avgScore = (avgScore * count + scoreChange)/(count+0.0)
            teachers.update_one({"_id":original["teacherID"]},{"$set":{"avgScore":avgScore}})

            lookup = dict(_id=str(original['teacommentID']),)
            ret=eve_patch_internal("teacomments", g.teacomment, **lookup)
            if ret and ret[3]==200:
                return
            abort(415, ret)

        g.teacomment["teacherID"]=original["teacherID"]
        g.teacomment["courseID"]=original["_id"]
        if "coursename" in original:
            g.teacomment["coursename"]=original["coursename"]

        students = app.data.driver.db['students']
        student = students.find_one({'_id': original["studentID"]})
        if "realname" in student:
            g.teacomment["studentname"]=student["realname"]
        elif "nickname" in student:
            g.teacomment["studentname"]=student["nickname"]

        avgScore = (avgScore * count + g.teacomment["scored"])/(count + 1.0)
        teachers.update_one({"_id":original["teacherID"]},{"$set":{"avgScore":avgScore}})

        ret=eve_post_internal("teacomments", g.teacomment)
        if ret and ret[3]==201:
            if "_id" in ret[0]:
                updates["teacommentID"]=ret[0]["_id"]
            return
        abort(415, ret)
    return

# 创建课程时，实时更新老师已预约schedule
courseStartTime={}
courseStartTime["09:00:00"] = 1
courseStartTime["09:45:00"] = 2
courseStartTime["10:30:00"] = 3
courseStartTime["11:15:00"] = 4
courseStartTime["13:45:00"] = 5
courseStartTime["14:30:00"] = 6
courseStartTime["15:15:00"] = 7
courseStartTime["16:00:00"] = 8
courseStartTime["16:45:00"] = 9
courseStartTime["19:00:00"] = 10
courseStartTime["19:45:00"] = 11
courseStartTime["20:30:00"] = 12
def on_insert_courses(items):
    for doc in items:
        if "startTime" in doc.keys() and "teacherID" in doc.keys():
            teachers = app.data.driver.db['teachers']
            teacher = teachers.find_one({'_id': doc["teacherID"]})
            schedule={}
            if "schedule" in teacher:
                schedule = teacher["schedule"]

            # startime = datetime.datetime.strptime(str(doc["startTime"]), "%Y-%m-%d %H:%M:%S")
            startime = doc["startTime"]
            syear=str(startime.year)
            smonth=str(startime.month)
            sday=str(startime.day)
            stime=str(startime.time())

            if syear not in schedule:
                schedule[syear]={}
            if smonth not in schedule[syear]:
                schedule[syear][smonth]={}
            if sday not in schedule[syear][smonth]:
                schedule[syear][smonth][sday]={}

            now=datetime.datetime.now()
            for key in schedule.keys():
                if key !="month" and key !="week" and key !="day" and int(key) < now.year:
                    del schedule[key]
                    # teachers.update_one({"_id":doc["teacherID"]},{"$unset":{"schedule."+key:1}})
            for key in schedule[syear].keys():
                if key !="month" and key !="week" and key !="day" and int(key) < now.month:
                    del schedule[syear][key]


            if stime not in courseStartTime:
                abort(415, "startTime error")
            snum = str(courseStartTime[stime])
            schedule[syear][smonth][sday][snum]=1

            teachers.update_one({"_id":doc["teacherID"]},{"$set":{"schedule":schedule}})

            # ret=eve_put_internal("teachers", teacher,skip_validation=True,  **lookup)
    return
apiapp.on_pre_PATCH_courses += on_pre_patch_courses
apiapp.on_update_courses += on_update_courses
apiapp.on_insert_courses += on_insert_courses

if __name__ == '__main__':
	# apiapp.debug = True
	apiapp.run(fudaoSrv["host"],fudaoSrv["port"])

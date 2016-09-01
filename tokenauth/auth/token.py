#! /usr/bin/env python
# coding=utf-8
from datetime import datetime
from eve.auth import TokenAuth
import jwt
from flask import current_app as app, request, abort, g
from neteaseIM.ServerAPI import neteaseIMsrv
from neteaseIM.neteaseIM import mysqlSrv, redisSrv
import MySQLdb
import redis
import json
from eve.methods.post import post_internal as eve_post_internal
from eve.methods.patch import patch_internal as eve_patch_internal
from eve.methods.put import put_internal as eve_put_internal
import uuid

class TokenAuthentication(TokenAuth):

    def check_auth(self, token, allowed_roles, resource, method):
        tokens = app.data.driver.db['tokens']
        teachers = app.data.driver.db['teachers']

        try:
            token, data = parse_token(request)
        except jwt.DecodeError:
            abort(401, "Token is invalid")
        except jwt.ExpiredSignature:
            abort(401, "Token is expired")

        good_token = tokens.find_one({'token': token})

        if good_token:
            account = teachers.find_one({'_id': good_token["account"]})
            curuser={}
            curuser["teacherID"] = account['_id']
            g.curuser=curuser
        # if account and '_id' in account:
        #      self.set_request_auth_value(account['_id'])
        return good_token

    def authorized(self, allowed_roles, resource, method):

        token = request.headers.get('Authorization')

        # hejiayi/Xue8Fudao
        if "Basic aGVqaWF5aTpYdWU4RnVkYW8=" == token:
            curuser={}
            g.curuser=curuser
            return token


        if token and (100 > len(token)):
            studentID = getStudentFromToken(token)
            if studentID:
                curuser={}
                curuser["studentID"] = studentID
                g.curuser=curuser
                return True

        return token and self.check_auth(token, allowed_roles, resource,
                                        method)

def getStudentFromToken(token):
    student = getredis_token(token)
    if not student:
        student = getmysql_token(token)
        if not student:
            abort(401, "student token is invalid")
            return False

    if student and student["uid"]:
        accid = getStudentAccid(student["uid"])
        student["accid"] = accid
    else:
        return False

    return postStudentMongo(student)


def getredis_token(token):
    r = redis.Redis(host=redisSrv["host"],port=6379,db=0,password=redisSrv["password"])
    studnetStr = r.hget('USERDATA',token[6:])
    if studnetStr:
        student = json.loads(studnetStr)
        return student
    return False


def getmysql_token(token):
    mysqldb = MySQLdb.connect(mysqlSrv["host"], mysqlSrv["user"],mysqlSrv["password"],mysqlSrv["database"],charset='utf8')
    cursor = mysqldb.cursor()

    # 通过token获得学生的uid
    userid=""
    sql = "SELECT uid FROM auth where token = " + " '" + token[6:] + "' "
    cursor.execute(sql)
    for row in cursor.fetchall():
        userid = row[0]

    if "" == userid:
        abort(401, "error: userid=null")

    # 通过uid获得学生信息users
    sql = "SELECT * FROM users where uid = " + str(userid)
    cursor.execute(sql)
    student={}
    for row in cursor.fetchall():
        student["uid"] = row[0]
        student["username"] = row[1]
        student["realname"] = row[3]
        student["mobilenumber"] = row[6]
        student["email"] = row[7]
        student["qq"] = row[8]
        student["gender"] = row[9]
        student["birthdate"] = row[10]
        student["province"] = row[11]
        student["city"] = row[12]
        student["school"] = row[13]
        student["astype"] = row[14]
        student["teachmaterial"] = row[15]
        student["nceetime"] = row[16]
    return student

def getStudentAccid(userid): 
    mysqldb = MySQLdb.connect(mysqlSrv["host"], mysqlSrv["user"],mysqlSrv["password"],mysqlSrv["database"],charset='utf8')
    cursor = mysqldb.cursor()
    # 通过uid获得学生的云信id：accid
    sql = "SELECT accid FROM imUsers where uid = " + str(userid)
    cursor.execute(sql)
    accid=""
    for row in cursor.fetchall():
        accid = row[0]
    return accid

def postStudentMongo(student):
    students = app.data.driver.db['students']
    ret = students.find_one({'username': student["username"]})
    if ret:
        return ret["_id"]

    gender = ""
    subjecttype = ""
    booktype = ""
    if 1 == student["gender"]:
        gender = "boy"
    elif 2 == student["gender"]:
        gender = "girl"
    if 1 == student["astype"]:
        subjecttype = "science"
    elif 2 == student["astype"]:
        subjecttype = "liberal"

    if 1 == student["teachmaterial"]:
        booktype = "people-A"
    elif 2 == student["teachmaterial"]:
        booktype = "people-B"

    post_payload = dict(
        _id=str(student["uid"]+100000000000000000000000),
        username=student["username"],
        nickname=student["realname"],
        mobilenumber=student["mobilenumber"],
        email=student["email"],
        qq=student["qq"],
        gender=gender,
        # birthdate=birthdate,
        accid=student["accid"],
        province=student["province"],
        city=student["city"],
        school=student["school"],
        subjecttype=subjecttype,
        booktype=booktype,
        NCEEtime=student["nceetime"],
    )

    ret=eve_post_internal("students", post_payload)
    if ret and ret[3]==201:
        return ret[0]["_id"]
    abort(401, ret)

def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return token, jwt.decode(token, app.config['TOKEN_SECRET'], algorithm='HS256')


def create_jwt_token(user, expiration):
    payload = dict(
        iat=datetime.utcnow(),
        id=str(user['_id']))
    token = jwt.encode(payload, app.config['TOKEN_SECRET'], algorithm='HS256')
    accidtoken = token[token.rindex('.', 0, len(token)):]

    teachers = app.data.driver.db['teachers']
    teacher = teachers.find_one({'_id': user['_id']})
    # if "accid" not in teacher:
    create_neteaseIM_token(user, accidtoken)

    post_payload = dict(
        account=user['_id'],
        expiration=expiration,
        token=token.decode('utf8'),
        accidtoken=accidtoken
    )
    ret = eve_post_internal("tokens", post_payload)
    if ret and ret[3]==201:
        return post_payload
    abort(401, ret)

def create_neteaseIM_token(user,token):
    teachers = app.data.driver.db['teachers']
    teacher = teachers.find_one({'_id': user['_id']})
    ret=""
    if "accid" in teacher:
        accid = teacher["accid"]
        ret = neteaseIMsrv.updateUserId(accid, token=token)
        if ret["code"] != 200:
            abort(401, ret)
        return

    accid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user['_id']))
    accid = str(accid)
    accid= accid.replace('-', '')
    ret = neteaseIMsrv.createUserId(accid, token=token)
    if ret["code"] != 200:
        abort(401, ret)

    patch_payload = dict( accid=accid,)
    lookup = dict(_id=str(user['_id']),)
    ret = eve_patch_internal('teachers', patch_payload, skip_validation=True, **lookup)
    if ret and ret[3]==200:
        return
    abort(401, ret)

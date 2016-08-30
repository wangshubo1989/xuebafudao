#! /usr/bin/env python
# coding=utf-8
from datetime import datetime
from eve.auth import TokenAuth
import jwt
from flask import current_app as app, request, abort, g
from neteaseIM.ServerAPI import neteaseIMsrv
from neteaseIM.neteaseIM import mysql
import MySQLdb
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


        if token and (38 == len(token) or 42 == len(token)):
            username = getmysql_token(token)
            if username:
                students = app.data.driver.db['students']
                account = students.find_one({'username': username})
                curuser={}
                curuser["studentID"] = account['_id']
                g.curuser=curuser
                return username

        return token and self.check_auth(token, allowed_roles, resource,
                                        method)

def getmysql_token(token):
    mysqldb = MySQLdb.connect(mysql["host"], mysql["user"],mysql["password"],mysql["database"],charset='utf8')
    cursor = mysqldb.cursor()

    userid = 0
    username = ""
    gender = ""
    subjecttype = ""
    booktype = ""
    accid = ""
    nickname = ""
    mobilenumber = ""
    email = ""
    qq = ""
    province = ""
    city = ""
    school = ""
    NCEEtime = ""

    # 通过token获得学生的uid
    sql = "SELECT uid FROM auth where token = " + " '" + token[6:] + "' "
    cursor.execute(sql)
    for row in cursor.fetchall():
        userid = row[0]

    # 通过uid获得学生信息users
    sql = "SELECT * FROM users where uid = " + str(userid)
    cursor.execute(sql)
    for row in cursor.fetchall():
        username = row[1]
        nickname = row[3]
        mobilenumber = row[6]
        email = row[7]
        qq = row[8]

        if 1 == row[9]:
            gender = "boy"
        elif 2 == row[9]:
            gender = "girl"

        birthdate = row[10]
        province = row[11]
        city = row[12]
        school = row[13]

        if 1 == row[14]:
            subjecttype = "science"
        elif 2 == row[14]:
            subjecttype = "liberal"

        if 1 == row[15]:
            booktype = "people-A"
        elif 2 == row[15]:
            booktype = "people-B"

        NCEEtime = row[16]
    # 通过uid获得学生的云信id：accid
    sql = "SELECT accid FROM imUsers where uid = " + str(userid)
    cursor.execute(sql)
    for row in cursor.fetchall():
        accid = row[0]

    post_payload = dict(
        username=username,
        nickname=nickname,
        mobilenumber=mobilenumber,
        email=email,
        qq=qq,
        gender=gender,
        # birthdate=birthdate,
        accid=accid,
        province=province,
        city=city,
        school=school,
        subjecttype=subjecttype,
        booktype=booktype,
        NCEEtime=NCEEtime,
    )
    print post_payload

    students = app.data.driver.db['students']
    student = students.find_one({'username': username})
    if student:
        lookup = dict(_id=str(student['_id']),)
        eve_patch_internal("students", post_payload, skip_validation=True, **lookup)
        return username

    eve_post_internal("students", post_payload)
    return username


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return token, jwt.decode(token, app.config['TOKEN_SECRET'], algorithm='HS256')


def create_jwt_token(user, expiration):
    # payload = dict(
    #     iat=datetime.utcnow(),
    #     exp=expiration,
    #     user=dict(
    #         id=str(user['_id']),
    #         username=str(user.get('username'))))
    payload = dict(
        iat=datetime.utcnow(),
        id=str(user['_id']))
    token = jwt.encode(payload, app.config['TOKEN_SECRET'], algorithm='HS256')
    print token
    print token[token.rindex('.', 0, len(token)):]
    create_neteaseIM_token(user, token[token.rindex('.', 0, len(token)):])

    return token

def create_neteaseIM_token(user,token):

    accid = uuid.uuid3(uuid.NAMESPACE_DNS, str(user['_id']))
    accid = str(accid)
    accid= accid.replace('-', '')

    ret1 = neteaseIMsrv.createUserId(accid, token=token)
    if ret1["code"] != 200:
        ret2 = neteaseIMsrv.updateUserId(accid, token=token)
        if ret2["code"] != 200:
            abort(401, "neteaseIM createUserId error: "+ ret1["desc"]+ "## updateUserId error: " +ret2["desc"])
    patch_payload = dict( accid=accid,)
    lookup = dict(_id=str(user['_id']),)
    eve_patch_internal('teachers', patch_payload, skip_validation=True, **lookup)

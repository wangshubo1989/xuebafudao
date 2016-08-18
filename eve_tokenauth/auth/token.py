#! /usr/bin/env python
# coding=utf-8
from datetime import datetime
from eve.auth import TokenAuth
import jwt
from flask import current_app as app, request, abort
from ServerAPI import neteaseIMsrv
import MySQLdb
from eve.methods.post import post_internal as eve_post_internal
from eve.methods.patch import patch_internal as eve_patch_internal

class TokenAuthentication(TokenAuth):

    def check_auth(self, token, allowed_roles, resource, method):
        tokens = app.data.driver.db['tokens']

        try:
            token, data = parse_token(request)
        except jwt.DecodeError:
            abort(401, "Token is invalid")
        except jwt.ExpiredSignature:
            abort(401, "Token is expired")

        good_token = tokens.find_one({'token': token})
        return good_token

    def authorized(self, allowed_roles, resource, method):

        token = request.headers.get('Authorization')

        username = getmysql_token(token)
        if username:
            return username

        return token and self.check_auth(token, allowed_roles, resource,
                                        method)

def getmysql_token(token):
    mysqldb = MySQLdb.connect("192.168.0.2","xueba","Xue-83177","xuebaedu")
    cursor = mysqldb.cursor()

    userid = 0
    username = ""
    gender = ""
    subjecttype = ""
    booktype = ""

    sql = "SELECT uid FROM auth where token = " + " '" + token[6:] + "' "
    cursor.execute(sql)
    for row in cursor.fetchall():
        userid = row[0]

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

    post_payload = dict(
        username=username,
        nickname=nickname,
        mobilenumber=mobilenumber,
        email=email,
        qq=qq,
        gender=gender,
        # birthdate=birthdate,
        province=province,
        city=city,
        school=school,
        subjecttype=subjecttype,
        booktype=booktype,
        NCEEtime=NCEEtime,
    )
    print post_payload
    eve_post_internal("students", post_payload)
    # ret=eve_patch_internal("students", post_payload)
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
        id=str(user['_id']))
    token = jwt.encode(payload, app.config['TOKEN_SECRET'], algorithm='HS256')

    ret = neteaseIMsrv.updateUserId(user['username'], token=token)
    if ret["code"] != 200:
        abort(401, "neteaseIM updateUserId is invalid")

    return token

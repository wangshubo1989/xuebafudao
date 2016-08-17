from datetime import datetime
from eve.auth import TokenAuth
import jwt
from flask import current_app as app, request, abort
from ServerAPI import neteaseIMsrv
import MySQLdb

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

    sql = "SELECT uid FROM auth where token = " + " '" + token[6:] + "' "
    cursor.execute(sql)
    for row in cursor.fetchall():
        userid = row[0]

    sql = "SELECT username FROM users where uid = " + str(userid)
    cursor.execute(sql)
    for row in cursor.fetchall():
        username = row[0]

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

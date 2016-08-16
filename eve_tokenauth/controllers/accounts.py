import bcrypt
from ServerAPI import neteaseIMsrv
from flask import current_app as app, request, abort

def hash_passwords(items):
    for item in items:
        item['password'] = bcrypt.hashpw(item['password'].encode('utf8'), bcrypt.gensalt())
        ret = neteaseIMsrv.createUserId(item['username'])
    	if ret["code"] != 200:
        	abort(401, "neteaseIM createUserId error: " + ret["desc"])
        pass
    return items

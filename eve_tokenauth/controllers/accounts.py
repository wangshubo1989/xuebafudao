import bcrypt
from ServerAPI import neteaseIMsrv

def hash_passwords(items):
    for item in items:
        item['password'] = bcrypt.hashpw(item['password'].encode('utf8'), bcrypt.gensalt())
        ret = neteaseIMsrv.createUserId(item['username'])
    	if ret["code"] != 200:
        	abort(401, "neteaseIM createUserId is invalid")
        pass
    return items

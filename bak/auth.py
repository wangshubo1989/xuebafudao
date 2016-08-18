import redis
import logging
import simplejson
import datetime
from models import Users, Auth
from django.conf import settings
from django.forms.models import model_to_dict

REDIS_USERDATA = "USERDATA"

class CJsonEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return simplejson.JSONEncoder.default(self, obj)


def auth(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return False
        else:
            token = token[6:]
    except:
        logging.exception("auth:cookie")
        return False

    user = get_user_by_token_cache(token)
    if not user:
        user = get_user_by_token(token)
        if not user:
            return False
        else:
            set_user_cache(token, user)

    request.xbuser = user
    return True


def get_user_by_uid(uid):
    try:
        authuser = Auth.objects.using('xuebaedu').get(uid=uid)
        if not authuser:
            return None

        user = get_user_by_token_cache(authuser.token)
        if user:
            user.serverid = authuser.serverid
            return user

        user = Users.objects.using('xuebaedu').get(uid=uid)
        if not user:
            return None

        user.serverid = authuser.serverid
        set_user_cache(authuser.token, user)

        return user
    except:
        pass
    return None


def get_user_by_token(token):
    try:
        authuser = Auth.objects.using('xuebaedu').get(token=token)
        if authuser:
            user = Users.objects.using('xuebaedu').get(uid=authuser.uid)
            if user:
                user.serverid = authuser.serverid
                return user
    except: pass
    return None


def get_user_by_token_cache(token):
    try:
        r = redis.StrictRedis(connection_pool=settings.GLOBAL_REDIS_POOL)
        if r:
            userdata = r.hget(REDIS_USERDATA, token)
            if not userdata:
                return None

            userjson = simplejson.loads(userdata)

            serverid = userjson['serverid']

            if 'grade' in userjson:
                del userjson['grade']
            if 'serverid' in userjson:
                del userjson['serverid']
            if 'signature' in userjson:
                del userjson['signature']

            user = Users(**userjson)

            user.serverid = serverid
            if not isinstance(user.creationdate, datetime.datetime):
                user.creationdate = datetime.datetime.strptime(user.creationdate, '%Y-%m-%d %H:%M:%S')

            return user
    except:
        logging.exception("cache:user:get")

    return None


def set_user_cache(token, user):
    try:
        userjson = model_to_dict(user)

        if 'psign' in userjson:
            del userjson['psign']
        if 'password' in userjson:
            del userjson['password']

        userjson['signature'] = user.psign
        userjson['serverid'] = user.serverid

        userdata = simplejson.dumps(userjson, cls=CJsonEncoder)

        r = redis.StrictRedis(connection_pool=settings.GLOBAL_REDIS_POOL)
        if r:
            if r.exists(REDIS_USERDATA):
                r.hset(REDIS_USERDATA, token, userdata)
            else:
                r.hset(REDIS_USERDATA, token, userdata)
                r.expire(REDIS_USERDATA, 24 * 3600 * 3)
    except:
        logging.exception("cache:user:set")


def invalid_user_cache(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if token != '':
            token = token[6:]
    except:
        logging.exception("auth:cookie")
        return False

    try:
        r = redis.StrictRedis(connection_pool=settings.GLOBAL_REDIS_POOL)
        if r:
            r.hdel(REDIS_USERDATA, token)
    except:
        logging.exception('invalid user cache')

    return True


def invalid_user_cache_by_uid(uid):
    try:
        authuser = Auth.objects.using('xuebaedu').get(uid=uid)
        if authuser:
            token = authuser.token

            r = redis.StrictRedis(connection_pool=settings.GLOBAL_REDIS_POOL)
            if r:
                r.hdel(REDIS_USERDATA, token)
    except:
        logging.exception('invalid user cache')

    return True


def black_it(request):
    try:
        user = Users.objects.using('xuebaedu').get(uid=request.xbuser.uid)
        user.groupid = 21
        user.save(force_update=True, update_fields=['groupid'])
    except Users.DoesNotExist:
        return False

    Auth.objects.using('xuebaedu').filter(uid=request.xbuser.uid).delete()

    invalid_user_cache(request)

    logging.info("BLACK: auth: uid:"+str(request.xbuser.uid))

    return True
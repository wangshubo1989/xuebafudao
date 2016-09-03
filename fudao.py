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
from flask import request
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

def on_pre_patch_students(resource, request):
    payload = payload_()
    if "parentID" not in payload:
        return
    g.parent=payload["parentID"]
    del payload["parentID"]

def on_update_students(updates, original):
    if g.parent and "parentID" in original:
        lookup = dict(_id=str(original['parentID']),)
        ret=eve_patch_internal("parents", g.parent,skip_validation=True, **lookup)
        return

    if g.parent:
        g.parent["studentID"]=original["_id"]
        ret=eve_post_internal("parents", g.parent)
        if ret and ret[0] and "_id" in ret[0]:
            updates["parentID"]=str(ret[0]["_id"])
    return

def on_pre_patch_courses(resource, request):
    payload = payload_()
    if "teacommentID" not in payload:
        return
    g.teacomment=payload["teacommentID"]
    del payload["teacommentID"]

def on_update_courses(updates, original):
    if g.teacomment and "teacommentID" in original:
        lookup = dict(_id=str(original['teacommentID']),)
        ret=eve_patch_internal("teacomments", g.teacomment,skip_validation=True, **lookup)
        return

    if g.teacomment:
        g.teacomment["teacherID"]=original["teacherID"]
        ret=eve_post_internal("teacomments", g.teacomment)
        print ret
        if ret and ret[0] and "_id" in ret[0]:
            updates["teacommentID"]=str(ret[0]["_id"])
    return

apiapp.on_pre_PATCH_students += on_pre_patch_students
apiapp.on_update_students += on_update_students
apiapp.on_pre_PATCH_courses += on_pre_patch_courses
apiapp.on_update_courses += on_update_courses
if __name__ == '__main__':
	# apiapp.debug = True
	apiapp.run(fudaoSrv["host"],fudaoSrv["port"])

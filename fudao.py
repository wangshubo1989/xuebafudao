#! /usr/bin/env python
# coding=utf-8
import logging
import logging.config  
import os
from eve.flaskapp import Eve
from tokenauth.eveapp import EveWithTokenAuth
import flask_admin as admin
from flask import Blueprint, render_template, jsonify
from eve_swagger import swagger


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

# werkzeug_logger = logging.getLogger('werkzeug')
# werkzeug_logger.setLevel(DEBUG)
if __name__ == '__main__':
	# apiapp.debug = True
	apiapp.run()

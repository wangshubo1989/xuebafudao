#! /usr/bin/env python
# coding=utf-8
import logging
import logging.config  
import os
from eve.flaskapp import Eve
from tokenauth.eveapp import EveWithTokenAuth
import flask_admin as admin

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


if __name__ == '__main__':


	settings = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.py')
	apiapp = Eve(settings=settings,template_folder='/Users/hejiayi/Desktop/python/eve/fudao/templates')

	# Flask views
	@apiapp.route('/')
	def index():
	    return '<a href="/admin/">Click me to get to Admin!</a>'
	@apiapp.route('web/')
    def index():
        return self.render('myadmin.html')

	# Create admin interface
	admin = admin.Admin(name="Example: Simple Views", template_mode='bootstrap3')
	admin.add_view(MyAdminView(name="view1", category='Test'))
	admin.add_view(AnotherAdminView(name="view2", category='Test'))
	admin.init_app(apiapp)

	evewta = EveWithTokenAuth(apiapp)
	apiapp.debug = True
	apiapp.run()

#! /usr/bin/env python
# coding=utf-8
import logging
import logging.config  
import os
from eve.flaskapp import Eve
from tokenauth.eveapp import EveWithTokenAuth


logging.config.fileConfig('config/logging.conf')   
logger = logging.getLogger('main')  
logger.info('main logger start')  


if __name__ == '__main__':


    settings = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.py')
    apiapp = Eve(settings=settings)
    evewta = EveWithTokenAuth(apiapp)
    apiapp.debug = True
    apiapp.run()

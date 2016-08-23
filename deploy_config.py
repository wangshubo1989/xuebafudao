#! /usr/bin/env python
# coding=utf-8

# import os
# import sys
# bind='127.0.0.1:8001' 
# workers=4 
# backlog=2048
# debug=True
# proc_name='gunicorn.pid'
# pidfile='/var/log/gunicorn/gunicorn.pid'
# accesslog='/var/log/gunicorn/gunicorn.log'
# loglevel='debug'

# coding=utf-8
import sys
import os
import multiprocessing

disable_existing_loggers = False
path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = os.path.basename(__file__)

sys.path.insert(0, path_of_current_dir)


worker_class = 'sync'
workers = multiprocessing.cpu_count()

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'info'

reload = True
debug = False



bind = "%s:%s" % ("0.0.0.0", 8002)
pidfile = '%s/run/%s.pid' % (path_of_current_dir, _file_name)
errorlog = '%s/logs/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/logs/%s_access.log' % (path_of_current_dir, _file_name)
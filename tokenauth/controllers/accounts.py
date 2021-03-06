#! /usr/bin/env python
# coding=utf-8
import bcrypt
from neteaseIM.ServerAPI import neteaseIMsrv
from flask import current_app as app, request, abort

def hash_passwords(items):
    for item in items:
        item['password'] = bcrypt.hashpw(item['password'].encode('utf8'), bcrypt.gensalt())
        pass
    return items

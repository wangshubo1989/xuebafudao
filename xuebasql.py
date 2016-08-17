#! /usr/bin/env python
# coding=utf-8
# SQLAlchemy Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    )

# Eve imports
from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL

# Eve-SQLAlchemy imports
from eve_sqlalchemy.decorators import registerSchema

Base = declarative_base()


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(80))
    lastname = Column(String(120))
    fullname = column_property(firstname + " " + lastname)

    @classmethod
    def from_tuple(cls, data):
        """Helper method to populate the db"""
        return cls(firstname=data[0], lastname=data[1])

class Users(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128))
    password = Column(String(35))
    realname = Column(String(20))
    usertype = Column(Integer)
    groupid = Column(Integer)
    mobilenumber = Column(String(15))
    email = Column(String(128))
    qq = Column(String(20))
    gender = Column(Integer)
    birthdate = Column(DateTime)
    province = Column(String(32))
    city = Column(String(64))
    school = Column(String(100))
    astype = Column(Integer)
    teachmaterial = Column(Integer)
    NCEETime = Column(Integer)  # Field name made lowercase.
    tendency = Column(Integer)
    achievement = Column(Integer)
    avatar = Column(String(128))
    psign = Column(String(128))
    creationdate = Column(DateTime)
    modificationdate = Column(DateTime)

    # class Meta:
    #     managed = False
    #     db_table = 'users'

class Auth(Base):
    __tablename__ = 'auth'
    uid =Column(Integer, primary_key=True, autoincrement=True)
    serverid = Column(Integer)
    token = Column(String(60))
    tokentime = Column(DateTime)  # Field name made lowercase.

    # class Meta:
    #     managed = False
    #     db_table = 'auth'


registerSchema('people')(People)
registerSchema('users')(Users)
registerSchema('auth')(Auth)

SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'mysql://xueba:Xue-83177@192.168.0.2:3306/xuebaedu',
    'DOMAIN': {
        'people': People._eve_schema['people'],
        'users': Users._eve_schema['users'],
        'auth': Auth._eve_schema['auth'],
        }
}

app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

# Insert some example data in the db

app.run(debug=True, use_reloader=False)
# using reloaded will destory in-memory sqlite db

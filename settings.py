#! /usr/bin/env python
# coding=utf-8

from tokenauth.auth.token import TokenAuthentication
from tokenauth.auth.basic import BasicAuthentication
# import os
# DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
MONGO_DBNAME = 'fudaodb'

URL_PREFIX = 'fudaoapi'
API_VERSION = 'v1'

TOKEN_SECRET = 'secret'
JSON = True
XML = False

statusList = ['created', 'qqcontact', 'prepared','telcontact', 'preHostVisit', 'started', 'completed', 'sendReport', 'preHostVisit', 'closed']
# PROJECTION = True
# SERVER_NAME = 'localhost:5000'

teachers = {
    'authentication': TokenAuthentication(),
    # 'datasource': {
    #     'projection': {'password': 0}  # hides password
    # },
    'public_methods': ['POST'],
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },

    # 'auth_field':'teachers_id',
    'schema': {
        'username': {
            'type': 'string',
            'required': True,
            'unique': True,},
        'password': {
            'type': 'string',
            'required': True,},
        'nickname': {
            'type': 'string',},
        'realname': {
            'type': 'string',},
        'accid': {
            'type': 'string',},
        'mobilenumber': {
            'type': 'string',},
        'avatar': {
            'type': 'string',},
        'avatarmin': {
            'type': 'string',},
        'gender': {
            'type': 'string',
            'allowed': ['man', 'woman']},
        'province': {
            'type': 'string',},
        'city': {
            'type': 'string',},
        'description': {
            'type': 'string',},
        'teachSection': {
            'type': 'list',
            'allowed': ['seniorSchool', 'juniorSchool']},
        'teachGrade': {
            'type': 'list',
            'allowed': ['seniorSync', 'seniorReview', 'grade-7', 'grade-8', 'grade-9']},
        'certifiedCardID': {
            'type': 'string',},
        'certifiedPhoto': {
            'type': 'string',},
        'educated': {
            'type': 'dict',
            'schema': {
                'begin': {
                'type': 'string'},
                'end': {
                'type': 'string'},
                'school': {
                'type': 'string'},
                'level': {
                'type': 'string',
                'allowed': ['college', 'bachelor', 'master', 'doctor', 'other']},
                'certificate': {
                'type': 'string'}
            }
        },
        'experiences':{
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'begin': {
                    'type': 'string'},
                    'end': {
                    'type': 'string'},
                    'organization': {
                    'type': 'string'},
                    'description': {
                    'type': 'string'}
                }
            }
        },
        'labels': {
            'type': 'list',
            'schema': {'type': 'string'}},
    }
}

students = {
    'authentication': TokenAuthentication(),
    # 'datasource': {
    #     'projection': {'password': 0}  # hides password
    # },
    'public_methods': ['POST'],
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },

    'schema': {
        '_id': {
            'type': 'objectid',
            'required': True,
            'unique': True,},
        'username': {
            'type': 'string',
            'required': True,
            'unique': True,},
        'password': {
            'type': 'string',},
        'nickname': {
            'type': 'string',},
        'realname': {
            'type': 'string',},
        'accid': {
            'type': 'string',},
        'mobilenumber': {
            'type': 'string',},
        'email': {
            'type': 'string',},
        'qq': {
            'type': 'string',},
        'gender': {
            'type': 'string',
            'allowed': ['', 'boy', 'girl']},
        'tendency': {
            'type': 'string',
            'allowed': ['', 'boy', 'girl']},
        'birthdate': {
            'type': 'string',},
        'province': {
            'type': 'string',},
        'city': {
            'type': 'string',},
        'school': {
            'type': 'string',},
        'booktype': {
            'type': 'string',
            'allowed': ['', 'people-A', 'people-B']},
        'subjecttype': {
            'type': 'string',
            'allowed': ['', 'science', 'liberal']},
        'NCEEtime': {
            'type': 'integer',},
        'parentID': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'parents',
                'field': '_id',
                'embeddable': True},
        },
        'realmobile': {
            'type': 'string',},
        'realqq': {
            'type': 'string',},
    }
}

parents = {
    'authentication': TokenAuthentication(),
    # 'datasource': {
    #     'projection': {'password': 0}  # hides password
    # },
    'public_methods': ['POST'],
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'schema': {
        'studentID': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'students',
                'field': '_id',
                'embeddable': True},
        },
        'gender': {
            'type': 'string',
            'allowed': ['man', 'woman']},
        'mobilenumber': {
            'type': 'string',}
    }
}

teacomments = {
    'authentication': TokenAuthentication(),
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'schema': {
        'teacherID': {
            'type': 'objectid',
            'unique': True,
            'required': True,
            'data_relation': {
                'resource': 'teachers',
                'field':'_id',
                'embeddable': True},
        },
        'scored': {
            'type': 'string',
            'required': True,
            'allowed': ['good', 'normal', 'bad']},
        'description': {
            'type': 'string'}
    }
}

courses = {
    'authentication': TokenAuthentication(),
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
    # 'auth_field':'teachers_id',

    'schema': {
        'teacherID': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'teachers',
                'field':'_id',
                'embeddable': True},
        },
        'studentID': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'students',
                'field': '_id',
                'embeddable': True},
        },
        'startTime': {
            'type': 'datetime',},
        'duration': {
            'type': 'integer',},
        'currentnum': {
            'type': 'integer',},
        'totalnum': {
            'type': 'integer',},
        'coursename': {
            'type': 'string',},
        'processID': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'courseProcess',
                'field': '_id',
                'embeddable': True},
        },
        'teacommentID': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'teacomments',
                'field': '_id',
                'embeddable': True},
        },
        # 'slides': {
        #     'type': 'list',
        #     'schema': {'type': 'string'}},
        'slide':{
                'type': 'dict',
                'schema': {
                    'num': {
                        'type': 'integer'
                    },
                    'slides': {
                        'type': 'list',
                        'schema': {
                            'type': 'string'}
                    },
                }
        },
        'status': {
            'type': 'string', 
            'allowed': statusList}
    }
}

courseProcess = {
    'authentication': TokenAuthentication(),
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'schema': {
        'processType': {
            'type': 'string',
            'allowed': ['experience', 'system']},
        'mainprocess': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'allowed': statusList}
        },
        'childprocess': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'coursenum': {
                        'type': 'list',
                        'schema': {
                            'type': 'integer'}
                    },
                    'process': {
                        'type': 'list',
                        'schema': {
                            'type': 'string',
                            'allowed': statusList}
                    },
                }
            }
        }
    }
}

tokens = {
    'authentication': BasicAuthentication(),
    'datasource': {
        'projection': {'token': 1},  # todo test this
        'default_sort': [("expiration", 1)]  # todo test this
    },
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'schema': {
        'expiration': {
            'type': 'datetime'},
        'token': {
            'type': 'string'},
        'accidtoken': {
            'type': 'string'},
        'account': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'teachers',
                'field': '_id'}
        }
    }
}

DOMAIN = {
    'teachers': teachers,
    'tokens': tokens,
    'parents': parents,
    'teacomments': teacomments,
    'students': students,
    'courseProcess': courseProcess,
    'courses': courses
}

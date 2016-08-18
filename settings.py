from tokenauth.auth.token import TokenAuthentication
from tokenauth.auth.basic import BasicAuthentication

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
MONGO_DBNAME = 'maindb'

URL_PREFIX = 'fudaoapi'
API_VERSION = 'v1'

TOKEN_SECRET = 'secret'

SERVER_NAME = 'localhost:5000'

teachers = {
    'authentication': TokenAuthentication(),
    'datasource': {
        'projection': {'password': 0}  # hides password
    },
    'public_methods': ['POST'],
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },

    'schema': {
        'username': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        },
        'nickname': {
            'type': 'string',
        },
        'realname': {
            'type': 'string',
        },
        'mobilenumber': {
            'type': 'string',
        },
    }
}

students = {
    'authentication': TokenAuthentication(),
    'datasource': {
        'projection': {'password': 0}  # hides password
    },
    'public_methods': ['POST'],
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },

    'schema': {
        'username': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
        },
        'nickname': {
            'type': 'string',
        },
        'realname': {
            'type': 'string',
        },
        'mobilenumber': {
            'type': 'string',
        },
        'email': {
            'type': 'string',
        },
        'qq': {
            'type': 'string',
        },
        'gender': {
            'type': 'string',
            'allowed': ['', 'boy', 'girl']
        },
        'tendency': {
            'type': 'string',
            'allowed': ['', 'boy', 'girl']
        },
        'birthdate': {
            'type': 'string',
        },
        'province': {
            'type': 'string',
        },
        'city': {
            'type': 'string',
        },
        'school': {
            'type': 'string',
        },
        'booktype': {
            'type': 'string',
            'allowed': ['', 'people-A', 'people-B']
        },
        'subjecttype': {
            'type': 'string',
            'allowed': ['', 'science', 'liberal']
        },
        'NCEEtime': {
            'type': 'integer',
        }
    }
}

courses = {
    'authentication': TokenAuthentication(),
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'schema': {
        'teacherID': {
            'type': 'string',
            'required': True,
            'data_relation': {
                'resource': 'teachers',
                'field':'username',
                'embeddable': True
            },
        },
        'studentID': {
            'type': 'string',
            'required': True,
            'data_relation': {
                'resource': 'students',
                'field':'username',
                'embeddable': True
            },
        },
        'startTime': {
            'type': 'datetime',
        },
        'duration': {
            'type': 'integer',
        },
        'status': {
            'type': 'string', 
            'allowed': ['created', 'qqcontact', 'prepared','telcontact', 'preHostVisit', 'started', 'completed', 'sendReport', 'preHostVisit', 'closed']
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
            'type': 'datetime'
        },
        'token': {
            'type': 'string'
        },
        'account': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'teachers',
                'field': '_id'
            }
        }
    }
}

DOMAIN = {
    'teachers': teachers,
    'tokens': tokens,
    'students': students,
    'courses': courses
}

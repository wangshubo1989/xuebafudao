from eve_tokenauth.auth.token import TokenAuthentication
from eve_tokenauth.auth.basic import BasicAuthentication

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
MONGO_DBNAME = 'maindb'

URL_PREFIX = 'api'
API_VERSION = 'v1'

TOKEN_SECRET = 'secret'

SERVER_NAME = 'localhost:5000'

teachers = {
    # 'authentication': TokenAuthentication(),
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
    }
}

students = {
    # 'authentication': TokenAuthentication(),
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
    }
}

courses = {
    # 'authentication': TokenAuthentication(),
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],

    'schema': {
        'teacherID': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'teachers',
                'embeddable': True
            },
        },
        'studentID': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'students',
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

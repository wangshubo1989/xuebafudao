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

books = {
    'authentication': TokenAuthentication(),
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
    'schema': {
        'name': {'type': 'string'}
    }
}

accounts = {
    'authentication': TokenAuthentication(),
    'datasource': {
        'projection': {'password': 0}  # hides password
    },
    'public_methods': ['POST'],
    'public_item_methods': [],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
    'schema': {
        'first_name': {
            'type': 'string'
        },
        'last_name': {
            'type': 'string'
        },
        'password': {
            'type': 'string',
            'required': True,
        },
        'email': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'is_email_confirmed': {
            'type': 'boolean'
        },
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
                'resource': 'accounts',
                'field': '_id'
            }
        }
    }
}

DOMAIN = {
    'accounts': accounts,
    'tokens': tokens,
    'books': books
}

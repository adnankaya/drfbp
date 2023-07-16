from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK.update({
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
})

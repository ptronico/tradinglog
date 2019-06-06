import os

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['tradinglog.nungo.com.br']

SECRET_KEY = os.environ['TRADINGLOG_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tradinglog',
        'USER': 'ptronico',
        'PASSWORD': os.environ['TRADINGLOG_DATABASE_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

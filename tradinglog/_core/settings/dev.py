from .base import *


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tradinglog',
        'USER': 'ptronico',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

import logging
from settings import *

DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '::memory::'}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'associados',
        'USER': 'osantana',
        'PASSWORD': '',
        'HOST': 'localhost'
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
LANGUAGE_CODE = 'en-us'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH = '/tmp/lead-messages'  # change this to a proper location

logging.disable(logging.CRITICAL)

import logging
from settings import *

DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '::memory::'}


INSTALLED_APPS = INSTALLED_APPS + (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

logging.disable(logging.CRITICAL)
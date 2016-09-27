import logging
from .settings import *

DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '::memory::'}

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append(
    'django_nose'
)
INSTALLED_APPS.append(
    'nose'
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
LANGUAGE_CODE = 'pt_BR'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH = '/tmp/lead-messages'  # change this to a proper location

logging.disable(logging.CRITICAL)

import logging
from .settings import *

DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '::memory::'}

LANGUAGE_CODE = 'pt_BR'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_FILE_PATH = '/tmp/lead-messages'  # change this to a proper location

logging.disable(logging.CRITICAL)

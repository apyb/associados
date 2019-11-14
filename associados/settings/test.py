"""
Django settings for associados project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import logging
import os

from split_settings.tools import include


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if os.environ['DJANGO_SETTINGS_MODULE'] == 'associados.settings.test':
    # must bypass this block if another settings module was specified
    include("base.py", scope=locals())


# Application definition

INSTALLED_APPS += [
    'django_nose',
    'nose'
]


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '::memory::'
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


# Default Tests Settings
# https://medium.com/@Zaccc123/django-tests-with-nose-and-coverage-dff5d3633b4b

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


# Email
# https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-EMAIL_HOST

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH = '/tmp/lead-messages'  # change this to a proper location


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

logging.disable(logging.CRITICAL)

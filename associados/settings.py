#!/usr/bin/env python
# coding: utf-8


import os
import dj_database_url
from django.core.urlresolvers import reverse_lazy

DEBUG = True
TEMPLATE_DEBUG = DEBUG
BASEDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))

ADMINS = (
    ('Marcos Daniel Petry', 'marcospetry@gmail.com'),
    ('Valder Gallo', 'valdergallo@gmail.com'),
    ('Osvaldo Santana Neto', 'osantana@python.org.br'),
    ('Carlos Leite', 'carlos.leite@znc.com.br'),
)
MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}


# Miscelaneous
APPEND_SLASH = True
SITE_ID = 1
ROOT_URLCONF = 'associados.urls'
WSGI_APPLICATION = 'associados.wsgi.application'


# i18n & l10n
USE_I18N = True
USE_L10N = True

USE_THOUSAND_SEPARATOR = True
LANGUAGES = [
    ('pt-BR', 'Portuguese Brazil')
]
LANGUAGE_CODE = 'pt-BR'
DEFAULT_LANGUAGE = 1
LOCALE_PATHS = (
    os.path.join(BASEDIR, "locale"),
)

USE_TZ = True
TIME_ZONE = 'America/Sao_Paulo'


# Media & Static
MEDIA_ROOT = os.path.join(BASEDIR, 'media')
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_ROOT = os.path.join(BASEDIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

PIPELINE_LESS_BINARY = ()
PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
  'pipeline.compilers.stylus.StylusCompiler',
)

COMPRESS_OUTPUT_DIR = 'cache'


# Security
SECRET_KEY = 'yc!+ii!psza0mi)&amp;vnn_rdsip5ipdyr(0w8hjllxw6p)!wgo1e'
LOGIN_URL = '/'
LOGIN_URL = reverse_lazy('auth-login')
LOGIN_REDIRECT_URL = reverse_lazy('members-dashboard')
AUTHENTICATION_BACKENDS = (
    'app.authemail.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# Templates & Middlewares
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = ()

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)


# Apps
INSTALLED_APPS = (
    #apps
    'associados',
    'app.payment',
    'app.core',
    'app.members',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',

    #extra
    'bootstrap_toolkit',
    'pipeline',
    'django_extensions',
    'sorl.thumbnail',
    'gravatar',
)


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Email
EMAIL_HOST_USER = os.getenv('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_PASSWORD')
EMAIL_HOST= 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# 3rd party applications
PAGSEGURO = {
    'email': os.environ.get('PAGSEGURO_EMAIL'),
    'charset': 'UTF-8',
    'token': os.environ.get('PAGSEGURO_TOKEN'),
    'currency': 'BRL',
    'itemId1': '0001',
    'itemQuantity1': 1,
}


PAGSEGURO_BASE = 'https://ws.pagseguro.uol.com.br/v2'
PAGSEGURO_CHECKOUT = '%s/checkout' % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS = '%s/transactions' % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS_NOTIFICATIONS = '%s/notifications' % PAGSEGURO_TRANSACTIONS
PAGSEGURO_WEBCHECKOUT = 'https://pagseguro.uol.com.br/v2/checkout/payment.html?code='

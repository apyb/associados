#!/usr/bin/env python
# coding: utf-8


import os
import dj_database_url
from django.core.urlresolvers import reverse_lazy
import decouple

DEBUG = decouple.config("DEBUG", cast=bool, default=False)
TEMPLATE_DEBUG = DEBUG
BASEDIR = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                        os.path.pardir))

ADMINS = (
    # ('Marcos Daniel Petry', 'marcospetry@gmail.com'),
    # ('Valder Gallo', 'valdergallo@gmail.com'),
    ('Osvaldo Santana Neto', 'osantana@python.org.br'),
    # ('Carlos Leite', 'carlos.leite@znc.com.br'),
)
MANAGERS = ADMINS

DATABASE_URL = decouple.config('DATABASE_URL', default='postgres://localhost')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL),
}

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

USE_TZ = decouple.config('USE_TZ', cast=bool, default=True)
TIME_ZONE = 'America/Sao_Paulo'


# Media & Static
DEFAULT_FILE_STORAGE = decouple.config(
    'DEFAULT_FILE_STORAGE',
    default='s3_folder_storage.s3.DefaultStorage'
)

STATICFILES_STORAGE = decouple.config(
    'STATICFILES_STORAGE',
    default='s3_folder_storage.s3.StaticStorage'
)

STATIC_S3_PATH = "static"
DEFAULT_S3_PATH = "media"

PIPELINE_LESS_BINARY = decouple.config('PIPELINE_LESS_BINARY',
                                       cast=decouple.Csv(),
                                       default='')
PIPELINE_COMPILERS = decouple.config(
    'PIPELINE_COMPILERS',
    cast=decouple.Csv(),
    default='pipeline.compilers.less.LessCompiler, '
    'pipeline.compilers.stylus.StylusCompiler',
)

# You've installed lessc, right?
if decouple.config('USE_PRECOMPILERS', cast=bool, default=False):
    COMPRESS_PRECOMPILERS = (
        ('text/less',
         '/opt/local/lib/node_modules/less/bin/lessc {infile} {outfile}'),
    )

COMPRESS_OUTPUT_DIR = decouple.config('COMPRESS_OUTPUT_DIR', default='CACHE')

AWS_ACCESS_KEY_ID = decouple.config('BUCKET_ACCESS_KEY', default='')
AWS_SECRET_ACCESS_KEY = decouple.config('BUCKET_SECRET_KEY', default='')
AWS_STORAGE_BUCKET_NAME = decouple.config('BUCKET_NAME', default='')
AWS_REGION_BUCKET_NAME = decouple.config("BUCKET_REGION", default='')

MEDIA_ROOT = decouple.config('MEDIA_ROOT', default='/%s/' % DEFAULT_S3_PATH)
MEDIA_URL = decouple.config(
    'MEDIA_URL',
    default='//%s.%s.amazonaws.com/media/' % (AWS_STORAGE_BUCKET_NAME,
                                              AWS_REGION_BUCKET_NAME)
)

if decouple.config('LOCAL_MEDIA', cast=bool, default=False):
    MEDIA_ROOT = os.path.join(BASEDIR, 'media')
    MEDIA_URL = '/media/'

STATIC_ROOT = decouple.config('STATIC_ROOT', default="/%s/" % STATIC_S3_PATH)
STATIC_URL = decouple.config(
    'STATIC_URL', default='//%s.%s.amazonaws.com/static/' %
    (AWS_STORAGE_BUCKET_NAME, AWS_REGION_BUCKET_NAME)
)

if decouple.config('LOCAL_STATIC', cast=bool, default=False):
    STATIC_ROOT = os.path.join(BASEDIR, 'static')
    STATIC_URL = '/static/'


ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Security
SECRET_KEY = decouple.config(
    'SECRET_KEY',
    default='yc!+ii!psza0mi)&amp;vnn_rdsip5ipdyr(0w8hjllxw6p)!wgo1e'
)

LOGIN_URL = '/'
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('members-dashboard')
AUTHENTICATION_BACKENDS = (
    'app.authemail.backends.EmailBackend',
)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = decouple.config('ALLOWED_HOSTS', cast=decouple.Csv(),
                                default='localhost')

INTERNAL_IPS = decouple.config('INTERNAL_IPS', default='127.0.0.1,',
                               cast=decouple.Csv())


# Templates & Middlewares
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = ()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    }
]


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
    'app.members',
    'app.payment',
    'app.core',

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
    'django_gravatar',
    'municipios',

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
EMAIL_BACKEND = decouple.config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

EMAIL_FILE_PATH = decouple.config('EMAIL_FILE_PATH', default='')
EMAIL_HOST_USER = decouple.config('SENDGRID_USERNAME', default='')
EMAIL_HOST_PASSWORD = decouple.config('SENDGRID_PASSWORD', default='')
EMAIL_HOST = decouple.config('EMAIL_HOST', default='smtp.sendgrid.net')
EMAIL_PORT = decouple.config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = decouple.config('EMAIL_USE_TLS', cast=bool, default=True)

# System contact email address
DEFAULT_FROM_EMAIL = decouple.config('DEFAULT_FROM_EMAIL',
                                     default="contato@python.org.br")
EMAIL_CONTACT_ADDRESS = DEFAULT_FROM_EMAIL

# 3rd party applications
PAGSEGURO = {
    'email': decouple.config('PAGSEGURO_EMAIL', default=''),
    'charset': 'UTF-8',
    'token': decouple.config('PAGSEGURO_TOKEN', default=''),
    'currency': 'BRL',
    'itemId1': '0001',
    'itemQuantity1': 1,
}

PAGSEGURO_BASE = decouple.config('PAGSEGURO_BASE',
                                 default='https://ws.pagseguro.uol.com.br/v2')

PAGSEGURO_WEBCHECKOUT = decouple.config(
    'PAGSEGURO_WEBCHECKOUT',
    default='https://pagseguro.uol.com.br/v2/checkout/payment.html?code='
)

PAGSEGURO_WEB_PRE_APPROVAL = decouple.config(
    'PAGSEGURO_WEB_PRE_APPROVAL',
    default='https://pagseguro.uol.com.br/v2/pre-approval/request.html?code='
)

PAGSEGURO_PRE_APPROVAL = '%s/pre-approvals/request' % PAGSEGURO_BASE
PAGSEGURO_CHECKOUT = '%s/checkout' % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS = '%s/transactions' % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS_NOTIFICATIONS = (
    '%s/notifications' % PAGSEGURO_TRANSACTIONS
)

GITHUB_CLIENT_SECRET = decouple.config('GITHUB_CLIENT_SECRET', default='')
GITHUB_CLIENT_ID = decouple.config('GITHUB_CLIENT_ID', default='')

DSN = decouple.config("DJANGO_DSN", default='')
if DSN:
    RAVEN_CONFIG = {'dsn': DSN}
    INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
    )

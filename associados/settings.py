import os
import dj_database_url
from django.urls import reverse_lazy
import decouple
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = decouple.config("DEBUG", cast=bool, default=False)
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
    ('pt-br', 'Portuguese Brazil')
]
LANGUAGE_CODE = 'pt-br'
DEFAULT_LANGUAGE = 1

USE_TZ = decouple.config('USE_TZ', cast=bool, default=True)
TIME_ZONE = 'America/Sao_Paulo'


# Media & Static
# set 's3_folder_storage.s3.DefaultStorage' in settings.ini for production
DEFAULT_FILE_STORAGE = decouple.config(
    'DEFAULT_FILE_STORAGE',
    default='django.core.files.storage.FileSystemStorage'
)

# set 's3_folder_storage.s3.StaticStorage' in settings.ini for production
STATICFILES_STORAGE = decouple.config(
    'STATICFILES_STORAGE',
    default='django.contrib.staticfiles.storage.StaticFilesStorage'
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
LOGIN_REDIRECT_URL = reverse_lazy('members:dashboard')
AUTHENTICATION_BACKENDS = (
    'app.authemail.backends.EmailBackend',
)

#SSL Setup
SECURE_SSL_REDIRECT=decouple.config('FORCE_HTTPS', cast=bool, default=False)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = decouple.config('ALLOWED_HOSTS', cast=decouple.Csv(),
                                default='localhost')

INTERNAL_IPS = decouple.config('INTERNAL_IPS', default='127.0.0.1,',
                               cast=decouple.Csv())


# Templates & Middlewares
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]


MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)


# Apps
INSTALLED_APPS = (
    # apps
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

    # extra
    'bootstrap3',
    'pipeline',
    'django_extensions',
    'sorl.thumbnail',
    'django_gravatar',
    'municipios',
    'phonenumber_field',

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

PAYMENT_SYSTEM = decouple.config('PAYMENT_SYSTEM', default="PAGSEGURO")

PAYMENT_CREDENTIALS = {
    'email': decouple.config('PAYMENT_CREDENTIALS_EMAIL',
                             default='fake@email.com'),
    'charset': 'UTF-8',
    'token': decouple.config('PAYMENT_CREDENTIALS_TOKEN', default='faketoken'),
    'currency': 'BRL',
    'itemId1': '0001',
    'itemQuantity1': 1,
}

PAYMENT_ENDPOINTS_BASE = decouple.config(
    'PAYMENT_CREDENTIALS_BASE',
    default='https://ws.pagseguro.uol.com.br/v2'
)
PAYMENT_ENDPOINT_WEBCHECKOUT = decouple.config(
    'PAYMENT_ENDPOINT_WEBCHECKOUT',
    default='https://pagseguro.uol.com.br/v2/checkout/payment.html?code='
)
PAYMENT_ENDPOINT_WEB_PRE_APPROVAL = decouple.config(
    'PAYMENT_ENDPOINT_WEB_PRE_APPROVAL',
    default='https://pagseguro.uol.com.br/v2/pre-approval/request.html?code='
)

PIPELINE = {

}

SENTRY_DSN = decouple.config("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
        SENTRY_DSN,
        traces_sample_rate=0.5,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )


# django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = 'BR'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'

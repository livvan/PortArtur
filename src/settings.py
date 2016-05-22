"""
Django settings for port project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import unicode_literals
import os
BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = '$osaxn9739un(n#9NDnu(#nd(UNDISNU32IO18h'
ALLOWED_HOSTS = ['port-artur.com.ru']
DOMAIN = 'port-artur.com.ru'

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'senni@mail.ru'
ADMINS = (('Glader', 'glader.ru@gmail.com'),)
MANAGERS = (('Senni', 'senni@mail.ru'),)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'pytils',
    'yafotki',
    'gunicorn',
    'redactor',

    'bus',
    'dump',
    'jsonfield',
    'messages',
    'news',
    'rpg',
    'staticpages',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rpg.middleware.GetUserRole',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'rpg.context_processors.fresh_mail_amount',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Redactor
REDACTOR_OPTIONS = {
    'lang': 'ru',
    'buttonSource': True,
}
REDACTOR_UPLOAD_HANDLER = 'yafotki.handlers.FotkiUploader'

# Yafotki
YAFOTKI_STORAGE_OPTIONS = {
    'username': 'user',
    'album': 'default',
}

# Logging
LOG_DIR = '/var/log/projects/port'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-15s %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'traceback.log'),
            'formatter': 'verbose',
        },
        'mail_admin': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admin', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}


try:
    from local_settings import *
except ImportError:
    pass

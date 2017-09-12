# -*- coding: utf-8 -*-
"""
Production Configurations

- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use mailgun to send emails
- Use Redis on Heroku

- Use sentry for error logging


- Use opbeat for error reporting

"""
from __future__ import absolute_import, unicode_literals

#from boto3.s3.connection import OrdinaryCallingFormat
from django.utils import six

import logging
import dj_database_url

from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# raven sentry client
# See https://docs.getsentry.com/hosted/clients/python/integrations/django/
INSTALLED_APPS += ('raven.contrib.django.raven_compat', )
RAVEN_MIDDLEWARE = ('raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware', )
MIDDLEWARE_CLASSES = RAVEN_MIDDLEWARE + MIDDLEWARE_CLASSES
# opbeat integration
# See https://opbeat.com/languages/django/
INSTALLED_APPS += ('opbeat.contrib.django',)
OPBEAT = {
    'ORGANIZATION_ID': env('DJANGO_OPBEAT_ORGANIZATION_ID'),
    'APP_ID': env('DJANGO_OPBEAT_APP_ID'),
    'SECRET_TOKEN': env('DJANGO_OPBEAT_SECRET_TOKEN')
}
MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
) + MIDDLEWARE_CLASSES


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/1.9/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/ja/1.9/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = env.bool('SESSION_COOKIE_SECURE', default=False)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)
SESSION_COOKIE_HTTPONLY = env.bool('SESSION_COOKIE_HTTPONLY', default=False)
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)
CSRF_COOKIE_HTTPONLY = env.bool('CSRF_COOKIE_HTTPONLY', default=False)
X_FRAME_OPTIONS = 'DENY'

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['ojoalplato.com'])
# END SITE CONFIGURATION

INSTALLED_APPS += ('gunicorn', )


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ('storages',)

AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
#AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.

#  See:http://stackoverflow.com/questions/10390244/
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3BotoStorage(S3Boto3Storage):

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        return name


StaticRootS3BotoStorage = lambda: CustomS3BotoStorage(location='static')
MediaRootS3BotoStorage = lambda: CustomS3BotoStorage(location='media')

DEFAULT_FILE_STORAGE = 'config.settings.production.MediaRootS3BotoStorage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_MEDIA_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

# Static Assets
# ------------------------

#STATIC_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
#STATICFILES_STORAGE = 'config.settings.production.StaticRootS3BotoStorage'
AWS_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# See: https://github.com/antonagestam/collectfast
# For Django 1.7+, 'collectfast' should come before
# 'django.contrib.staticfiles'
AWS_PRELOAD_METADATA = True
INSTALLED_APPS = ('collectfast', ) + INSTALLED_APPS
# COMPRESSOR
# ------------------------------------------------------------------------------
#COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
COMPRESS_URL = STATIC_URL
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)
# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='Ojoalplato <noreply@ojoalplato.com>')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Ojoalplato] ')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ("anymail", )
ANYMAIL = {
    "MAILGUN_API_KEY": env('DJANGO_MAILGUN_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
#DATABASES['default'] = env.db('DATABASE_URL')
POSTGRES_USER=env("POSTGRES_USER", default="ojoalplato")
POSTGRES_PASSWORD=env("POSTGRES_PASSWORD")
POSTGRES_URL="postgis://{}:{}@postgres/ojoalplato".format(POSTGRES_USER, POSTGRES_PASSWORD)

MYSQL_USER = env("MYSQL_USER", default="ojoalplato")
MYSQL_PASSWORD = env("MYSQL_PASSWORD")
MYSQL_DATABASE = env("MYSQL_DATABASE")
MYSQL_URL = "mysql://{}:{}@mysql:3306/{}".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)

DATABASES = {
    'mysql': dj_database_url.parse(MYSQL_URL),
    'default': dj_database_url.parse(POSTGRES_URL),
}

# CACHING
# ------------------------------------------------------------------------------
# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '{0}/{1}'.format(env('REDIS_URL', default='redis://127.0.0.1:6379'), 0),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}


# Sentry Configuration
SENTRY_DSN = env('DJANGO_SENTRY_DSN')
SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}
SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
RAVEN_CONFIG = {
    'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
    'DSN': SENTRY_DSN
}

# Custom Admin URL, use {% url 'admin:index' %}
ADMIN_URL = env('DJANGO_ADMIN_URL')


# Your production stuff: Below this line define 3rd party library settings
WP_TABLE_PREFIX = 'wp_d3r46v'
WP_READ_ONLY = True

DEBUG=True

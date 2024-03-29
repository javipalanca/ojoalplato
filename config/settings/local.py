# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""
import dj_database_url

from .common import *  # noqa
import socket
import os

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='4tg6no4=eh0@yf#v1+*kqcho!0q(@^4m81t94yeivxhmkmg5(n')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = env("EMAIL_HOST", default='mailhog')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1]+"1"]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# CELERY
# In development, all tasks will be executed locally by blocking until the task returns
# CELERY_ALWAYS_EAGER = True
# END CELERY

MEDIA_ROOT = str(APPS_DIR('media'))

# Your local stuff: Below this line define 3rd party library settings
DATABASES = {
    # 'mysql': env.db("DATABASE_URL", default="mysql://ojoalplato:ojoalplato@mysql:3306/wordpress"),
    'default': dj_database_url.parse("postgis://ojoalplato:ojoalplato@postgres/ojoalplato"),
}

WP_TABLE_PREFIX = 'wp_d3r46v'
WP_READ_ONLY = True


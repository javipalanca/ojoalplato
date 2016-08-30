# -*- coding: utf-8 -*-
"""
Django settings for Ojoalplato project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ
from django.contrib import messages

ROOT_DIR = environ.Path(__file__) - 3  # (ojoalplato/config/settings/common.py - 3 = ojoalplato/)
APPS_DIR = ROOT_DIR.path('ojoalplato')

env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'adminactions',
    # 'suit',
    # 'material',
    # 'material.admin',
    'admin_bootstrapped_plus',
    'django_admin_bootstrapped',
    'bootstrap3',
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'floppyforms',
    # 'allauth',  # registration
    # 'allauth.account',  # registration
    # 'allauth.socialaccount',  # registration
    'mptt',
    'guardian',
    'reversion',
    'redactor',
    # 'suit_redactor',
    'django_social_share',
    'categories',
    'categories.editor',
    'taggit',
    'taggit_autosuggest',
    'likert_field',
    'leaflet',
    'envelope',
    'wordpress',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    'ojoalplato.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'ojoalplato.blog',
    'ojoalplato.category',
    'ojoalplato.cards',
    'ojoalplato.contactform',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'ojoalplato.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Javi Palanca""", 'jpalanca@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db('DATABASE_URL', default='postgres:///ojoalplato'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'es-es'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', False)
ACCOUNT_ADAPTER = 'ojoalplato.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'ojoalplato.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# CELERY
INSTALLED_APPS += ('ojoalplato.taskapp.celery.CeleryConfig',)
# if you are not using the django database broker (e.g. rabbitmq, redis, memcached), you can remove the next line.
INSTALLED_APPS += ('kombu.transport.django',)
BROKER_URL = env('CELERY_BROKER_URL', default='django://')
if BROKER_URL == 'django://':
    CELERY_RESULT_BACKEND = 'redis://'
else:
    CELERY_RESULT_BACKEND = BROKER_URL
# END CELERY


# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("compressor",)
STATICFILES_FINDERS += ("compressor.finders.CompressorFinder",)

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger' # 'error' by default
}

# Your common stuff: Below this line define 3rd party library settings
# DJANGO SUIT CONFIGURATION
SUIT_CONFIG = {
    'ADMIN_NAME': 'Ojoalplato',
    'MENU': (
        {'app': 'auth', 'icon': 'icon-lock'},
        {'app': 'users', 'label': 'Usuarios', 'icon': 'icon-user'},
        {'app': 'blog', 'label': 'Blog', 'icon': 'icon-pencil'},
        {'app': 'category', 'label': 'Categorías', 'icon': 'icon-inbox'},
        {'app': 'taggit', 'label': 'Etiquetas', 'icon': 'icon-tags'},
        {'app': 'sites', 'icon': 'icon-globe'},
    ),
    'CONFIRM_UNSAVED_CHANGES': True,
}
# END DJANGO SUIT CONFIGURATION

REDACTOR_OPTIONS = {'lang': 'es'}
REDACTOR_UPLOAD = 'gallery/'
REDACTOR_UPLOAD_HANDLER = 'redactor.handlers.SimpleUploader'
REDACTOR_AUTH_DECORATOR = 'django.contrib.auth.decorators.login_required'
REDACTOR_FILE_STORAGE = 'django.core.files.storage.DefaultStorage'

# DISQUS_API_KEY = env('DISQUS_API_KEY', default='XXXXXXXXX')
DISQUS_WEBSITE_SHORTNAME = 'ojoalplato'

# Taggit settings
# ------------------------------------------------------------------------------
TAGGIT_CASE_INSENSITIVE = True

SESSION_COOKIE_NAME = "ojoalplato_cookie"

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

ADMIN_SITE_HEADER = 'Administración de Ojo al plato'

LEAFLET_CONFIG = {
    # conf here
    'DEFAULT_CENTER': (40.383, -3.716),
    'DEFAULT_ZOOM': 6,
    'TILES': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'RESET_VIEW': True,
}

# Envelope config
DEFAULT_FROM_EMAIL = "jpalanca@ojoalplato.com"
ENVELOPE_SUBJECT_INTRO = "[Ojoalplato]"

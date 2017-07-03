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
    # 'otto_admin',
    # 'suit',
    # 'material',
    # 'material.admin',
    # 'ojoalplato.analytics_admin',
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
    'analytical',
    'request',
    'hitcount',
    'newsletter',
    'haystack',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    'ojoalplato.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'ojoalplato.blog.apps.BlogConfig',
    'ojoalplato.category.apps.CategoryConfig',
    'ojoalplato.cards.apps.CardConfig',
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
    'request.middleware.RequestMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
TIME_ZONE = 'Europe/Madrid'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'es-ES'

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
#STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_ROOT = '/staticfiles'

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
# MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_ROOT = '/media'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

LOCALE_PATHS = (str(ROOT_DIR('locale')),)

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
CELERY_BROKER_POOL_LIMIT = 10
CELERY_BROKER_CONNECTION_TIMEOUT = 5

CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_WORKER_DISABLE_RATE_LIMITS = False

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_BROKER_HEARTBEAT = 0
CELERY_TIMEZONE = TIME_ZONE
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

# Redactor settings
# ------------------------------------------------------------------------------
REDACTOR_OPTIONS = {'plugins': ['source', 'table', 'fontcolor', 'fontsize', 'video', 'inlinestyle', 'alignment'],
                    'lang': 'es', 'imageResizable': True, 'imagePosition': True, 'imageFloatMargin': '20px'}
REDACTOR_UPLOAD = 'gallery/'
# REDACTOR_UPLOAD_HANDLER = 'redactor.handlers.SimpleUploader'
REDACTOR_UPLOAD_HANDLER = 'ojoalplato.blog.handlers.DateDirectoryWatermarkUploader'
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

# Leaflet settings
# ------------------------------------------------------------------------------
LEAFLET_CONFIG = {
    # conf here
    'DEFAULT_CENTER': (40.383, -3.716),
    'DEFAULT_ZOOM': 6,
    'TILES': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'RESET_VIEW': True,
}

# Envelope settings
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = "jpalanca@ojoalplato.com"
ENVELOPE_SUBJECT_INTRO = "[Ojoalplato] "
ENVELOPE_USE_HTML_EMAIL = True

# Google Analytics settings
# ------------------------------------------------------------------------------
OA_ANALYTICS_CREDENTIALS_JSON = {}
OA_ANALYTICS_VIEW_ID = "UA-5491851-1"

GOOGLE_ANALYTICS_PROPERTY_ID = "UA-5491851-1"
GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True
GOOGLE_ANALYTICS_SITE_SPEED = True

URI_WITH_GET_PARAMS=True

# Requests settings
# ------------------------------------------------------------------------------
REQUEST_PLUGINS = (
    'request.plugins.TrafficInformation',
    'request.plugins.LatestRequests',
    'request.plugins.TopPaths',
    'request.plugins.TopErrorPaths',
    'request.plugins.TopReferrers',
    'request.plugins.TopSearchPhrases',
    'request.plugins.TopBrowsers',
    # 'request.plugins.ActiveUsers',
)
REQUEST_TRAFFIC_MODULES = (
    'request.traffic.UniqueVisitor',
    'request.traffic.UniqueVisit',
    'request.traffic.Hit',
    'request.traffic.Error',
    'request.traffic.Error404',
    # 'request.traffic.User',
    # 'request.traffic.UniqueUser',
)

REQUEST_IGNORE_PATHS = (
    r'^admin/',
    r'^media/',
    r'^static/',
)

# Newsletter settings
# ------------------------------------------------------------------------------
NEWSLETTER_CONFIRM_EMAIL = True
# Amount of seconds to wait between each email. Here 100ms is used.
NEWSLETTER_EMAIL_DELAY = 0.1
# Amount of seconds to wait between each batch. Here one minute is used.
NEWSLETTER_BATCH_DELAY = 60
# Number of emails in one batch
NEWSLETTER_BATCH_SIZE = 100

# Facebook and Twitter settings
# ------------------------------------------------------------------------------
FACEBOOK_CLIENT_ID = env("FACEBOOK_CLIENT_ID", default="")
FACEBOOK_CLIENT_SECRET = env("FACEBOOK_CLIENT_SECRET", default="")
FACEBOOK_PAGE_NAME = env("FACEBOOK_PAGE_NAME", default="ojoalplato.com")
FACEBOOK_PAGE_ID = env("FACEBOOK_PAGE_ID", default="ojoalplato")
FACEBOOK_PAGE_ACCESS_TOKEN = env("FACEBOOK_PAGE_ACCESS_TOKEN", default="")
TWITTER_CONSUMER_KEY = env("TWITTER_CONSUMER_KEY", default="")
TWITTER_CONSUMER_SECRET = env("TWITTER_CONSUMER_SECRET", default="")
TWITTER_ACCESS_TOKEN = env("TWITTER_ACCESS_TOKEN", default="")
TWITTER_ACCESS_TOKEN_SECRET = env("TWITTER_ACCESS_TOKEN_SECRET", default="")

# Google Maps settings
# ------------------------------------------------------------------------------
GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY", default="")


# Haystack search engine
# ------------------------------------------------------------------------------
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack',
    },
}

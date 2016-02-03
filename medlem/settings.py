"""
Django settings for medlem project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

import dj_database_url
from decouple import Csv, config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.join(BASE_DIR, '..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    # Project specific apps
    'medlem.base',
    'medlem.api',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
]

for app in config('EXTRA_APPS', default='', cast=Csv()):
    INSTALLED_APPS.append(app)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_csrf.CsrfMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
)

ROOT_URLCONF = 'medlem.urls'

WSGI_APPLICATION = 'medlem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=dj_database_url.parse
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = config('USE_I18N', default=False, cast=bool)

USE_L10N = config('USE_L10N', default=False, cast=bool)

USE_TZ = config('USE_TZ', default=True, cast=bool)


SESSION_COOKIE_SECURE = config(
    'SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)


# This is needed to get a CRSF token in /admin
ANON_ALWAYS = True

# LDAP related settings
LDAP_SERVER_URI = config('LDAP_SERVER_URI', default='ldap://pm-ns.mozilla.org')
LDAP_BIND_DN = config('LDAP_BIND_DN', '')
LDAP_BIND_PASSWORD = config('LDAP_BIND_PASSWORD', '')
LDAP_SEARCH_BASE = config(
    'LDAP_SEARCH_BASE', default='dc=mozilla'
)
GROUP_LDAP_SEARCH_BASE = config(
    'GROUP_LDAP_SEARCH_BASE', default='ou=groups,dc=mozilla'
)
# XXX might need to be broken up
_LDAP_GLOBAL_OPTIONS = config('LDAP_GLOBAL_OPTIONS', cast=Csv(), default='')
LDAP_GLOBAL_OPTIONS = dict(x.split(':', 1) for x in _LDAP_GLOBAL_OPTIONS)
# For extra LDAP debugging if need be
# import ldap
# AUTH_LDAP_GLOBAL_OPTIONS = {
#  ldap.OPT_DEBUG_LEVEL: 4095
# }


# When running tests, you want to absolute make sure you don't actually
# fly with real values for certain things:
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    # We're in the middle of a django test run
    LDAP_SERVER_URI = 'ldap://example.com'
    LDAP_BIND_DN = 'cosmo'
    LDAP_BIND_PASSWORD = 'kramer'

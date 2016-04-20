"""
Django settings for djanalytics_testproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%f!lwx6*4ac8%zr9j)59i(cz+p8ldj5v2rsra5_kseccfog!i$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djanalytics',
    'graphos',
)

# south is no longer used in django 1.7
if django.VERSION[1] < 7:
    INSTALLED_APPS = INSTALLED_APPS + ( 'south', )
else:
    MIGRATION_MODULES = {
        'djanalytics': 'djanalytics.django_migrations'
    }

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if django.VERSION[1] >= 7:
    MIDDLEWARE_CLASSES += ('django.contrib.auth.middleware.SessionAuthenticationMiddleware',)

ROOT_URLCONF = 'djanalytics_testproject.urls'

WSGI_APPLICATION = 'djanalytics_testproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # 'default': {
    #     'NAME': 'analytics',
    #     'ENGINE': 'django.db.backends.mysql',
    #     'STORAGE_ENGINE': 'InnoDB',
    #     'USER': 'root',
    #     'PASSWORD': 'root',
    # }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

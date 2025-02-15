"""
Django settings for ilkaddimlar-video project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

import redis

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6##^u4--4$0np2viuarur!h0rvh%i3z50hz8!l!yhw^m3oab-t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # False if os.environ.get('DEBUG') else True

ALLOWED_HOSTS = ['*']


# Application definition


INSTALLED_APPS = [
    # 'modeltranslation',
    # 'rosetta',
    'baton',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework_simplejwt',
    'nested_admin',
    'widget_tweaks',
    'embed_video',
    'django_celery_beat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'courses',
    'rest_framework',
    'order',
    'gallery',
    'core',
]

AUTH_USER_MODEL = 'user.User'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        #  'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',

    ],
    'DATETIME_FORMAT': '%B %d, %Y',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ilkaddimlar-video.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ilkaddimlar-video.wsgi.application'

LOGIN_URL = 'user/login/'
 
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'ilkaddimlar'),
        'USER': os.environ.get('POSTGRES_USER', 'user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '12345'),
        'PORT':  os.environ.get('POSTGRES_PORT', 5432),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
    }
}

# CELERY STUFF
CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}"
CELERY_RESULT_BACKEND = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Baku'

REDIS_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}"

REDIS_CLIENT = redis.Redis.from_url(REDIS_BROKER_URL)

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'TOKEN_OBTAIN_SERIALIZER': "user.api.serializers.CustomTokenObtainPairSerializer",
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'JTI_CLAIM': 'jti',
}
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# LANGUAGE_CODE = 'az'

# LANGUAGES = [
#     ('en', _('English')),
#     ('az', _('Azerbaijan')),

# ]

# MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE

# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, 'locale'),
# ]



# JAZZMIN_SETTINGS = {
#     "language_chooser": True,
# }

# MODELTRANSLATION_DEFAULT_LANGUAGE = 'az'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

if DEBUG:
    STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")


CKEDITOR_UPLOAD_PATH = 'uploads/'


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rustamakifli2003@gmail.com'
EMAIL_HOST_PASSWORD = 'pbmdmrkvjjofppjx'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

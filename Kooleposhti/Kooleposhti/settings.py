"""
Django settings for Kooleposhti project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys
import os
from datetime import timedelta
from pathlib import Path
import dj_database_url
from environs import Env
import django_heroku

# Environment Variables
env = Env()  # new
env.read_env()  # ne

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

# ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
'''
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ('http://localhost:5000',)
'''


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'djoser',
    'accounts',
    'courses',
    'corsheaders',
    'drf_yasg',
    'rest_framework_simplejwt',
    'jalali_date',
    'jalali',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Kooleposhti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # str(BASE_DIR.joinpath('templates')),
        ],
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

WSGI_APPLICATION = 'Kooleposhti.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dcnob3lebr55o2',
        'USER': 'hzgvghwtcuhwbt',
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': 'ec2-35-171-90-188.compute-1.amazonaws.com',
        'PORT': '5432',
    },
    'TEST': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}
if 'test' in sys.argv:
    DATABASES['default'] = DATABASES['TEST']


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Iran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'


MEDIA_URL = STATIC_URL + "/media/"
MEDIA_ROOT = os.path.join(STATIC_ROOT, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ActivateDjango-Heroku
django_heroku.settings(locals())


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_ID')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PW')

DEFAULT_FROM_EMAIL = 'Kooleposhti <no_reply@domain.com>'


# Rest Framework Settings
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    # 'PAGE_SIZE': 10,
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated'
    ]
}

# request header prefix JWT
# SIMPLE JWT
SIMPLE_JWT = {
    # JWT ACCESS_TOKEN
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
}

# User Model For AUTH
AUTH_USER_MODEL = 'accounts.User'


# Reset password Email
PASSWORD_RESET_CONFIRM_URL = 'reset-password/?uid={uid}&token={token}'

# DJOSER
DJOSER = {
    # "SEND_ACTIVATION_EMAIL": True, # login ro tahte tasir gharar mide
    # "SEND_CONFIRMATION_EMAIL": True,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    'PASSWORD_RESET_CONFIRM_URL': PASSWORD_RESET_CONFIRM_URL,
    'USERNAME_RESET_CONFIRM_URL': 'accounts/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'accounts/activate/{uid}/{token}',
    "SERIALIZERS": {
        'user_create': 'accounts.serializers.UserCreateSerializer',
        'current_user': 'accounts.serializers.UserSerializer',
    },
    'EMAIL': {
        # 'activation': 'accounts.email.ActivationEmail',
        # 'confirmation': 'accounts.email.ConfirmationEmail',
        # 'password_reset': 'accounts.email.PasswordResetEmail',
        # 'password_changed_confirmation': 'accounts.email.PasswordChangedConfirmationEmail',
        # 'username_changed_confirmation': 'accounts.email.UsernameChangedConfirmationEmail',
        # 'username_reset': 'accounts.email.UsernameResetEmail',
    }
}

# WEBSITE URL that deployed
WEBSITE_URL = os.environ.get('WEBSITE_URL')


# Token Expiration Time for Email verification in days
TOKEN_EXPIRATION_TIME = 1


# Authentication Backend
AUTHENTICATION_BACKENDS = [
    'accounts.backends.MyModelBackend',
]


FRONTEND_URL = 'kooleposhti-front.herokuapp.com'


USERNAME_RESET_SHOW_EMAIL_NOT_FOUND = True
PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND = True


JALALI_DATE_DEFAULTS = {
   'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

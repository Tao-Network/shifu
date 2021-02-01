"""
Django settings for shifu project.

Generated by 'django-admin startproject' using Django 3.0.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if os.getenv('CRAWLER'):
    DEBUG = False

ALLOWED_HOSTS = ['*']

BLOCKS_PER_EPOCH = 360
CHAIN_ID = 558
RPC_ENDPOINT = os.getenv('RPC_ENDPOINT')
RESTFUL_ENDPOINT = os.getenv('RESTFUL_ENDPOINT')
VALIDATOR_CONTRACT_ADDRESS = '0x0000000000000000000000000000000000000088'
SIGNER_CONTRACT_ADDRESS = '0x0000000000000000000000000000000000000089'
RANDOMIZER_CONTRACT_ADDRESS = '0x0000000000000000000000000000000000000090'
SEALER_CONTRACT_ADDRESS = '0x0000000000000000000000000000000000000092'
EXODUS_HOT_WALLET = '0x5DD061e82fc7c31a4492a9D8F1B5557273c943A9'
EXODUS_COLD_WALLET = '0x92ef21492f31eeE0BC2C9573C3c4DCF0B3C1C312'
LIQUIDITY_WALLET = '0x24B4285fB35ae9b9bA997f6eb110d7BB757637e2'
SEALER_CONTRACT_ADDRESS = '0x0000000000000000000000000000000000000092'
BOARD_CONTRACT_ADDRESS = '0x4e596130c6ed2f47ae72e30814ddbf0edf2df8f6'
UPDATE_RANK_FREQUENCY = 25
MAX_RETRIES = 10
ADMINS = (
    ('Admin', 'admin@tao.network')
)

###
# RESTful API Settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
###

MANAGERS = ADMINS

# Application definition
CORS_ORIGIN_ALLOW_ALL=True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_gravatar',
    'rest_framework',
    'drf_yasg',
    'web',
    'corsheaders',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shifu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, os.path.join(BASE_DIR, 'web', 'templates')],
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

WSGI_APPLICATION = 'shifu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shifu',
        'USER': os.getenv('POSTGRES_USERNAME'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'web.backend.Web3Backend'
]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

WEB3AUTH_USER_ADDRESS_FIELD = 'username'
WEB3AUTH_USER_SIGNUP_FIELDS=['email']
WEB3AUTH_SIGNUP_ENABLED=True
GRAVATAR_DEFAULT_IMAGE = 'identicon'
LOGIN_REDIRECT_URL = '/profile'
LOGIN_URL = '/auto_login'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_DIRS = [
    "{0}/web/templates/assets/".format(BASE_DIR),
]
if DEBUG:
    MING_API_URL = "http://localhost:8000"
else:
    MING_API_URL = "https://ming.tao.network"
MAX_RETRIES = 100

SWAGGER_SETTINGS = {
   'DEFAULT_INFO': 'shifu.urls.api_info',
}
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
   'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.CoreJSONRenderer',
    ),
}
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
    # root logger
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
}
from logging.config import dictConfig
dictConfig(LOGGING)
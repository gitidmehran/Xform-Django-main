from pathlib import Path
from smtplib import SMTP
import pymysql
import os
from pathlib import Path

import requests
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.name-serv.com'
EMAIL_HOST_USER = 'admin@researchquran.org'
EMAIL_HOST_PASSWORD = 'ZiaIqbal@123'
EMAIL_PORT = '587'
DEFAULT_FROM_EMAIL = 'admin@researchquran.org'  # Default sender email address
EMAIL_USE_TLS = True  # Use TLS (Transport Layer Security)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
pymysql.version_info = (1, 4, 6, 'final', 0)  # (major, minor, micro, releaselevel, serial)
pymysql.install_as_MySQLdb()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-d$+k_#fwpdw!*ts$gpr*20x%*4wy1feolw)rhk1*$al9&cosrp"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
requests.adapters.DEFAULT_TIMEOUT = None
CSRF_COOKIE_SECURE = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://49.13.21.18:5173",
    "https://morpheme-uploader.researchquran.org",
    "https://morpheme-uploader-dj.researchquran.org"
]
ALLOWED_HOSTS = ["*"]


# Application definition
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
INSTALLED_APPS = [
    "corsheaders",
    'django_db_logger',
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'myapi'
]
if os.environ.get('DJANGO_ENV') == 'production':
    MEDIA_URL = 'https://morpheme-uploader-dj.researchquran.org/media/'
else:
    MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'myapi.middlewares.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "drk.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "drk.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     'NAME': BASE_DIR / 'db_morphemes3.sqlite3',
    # # },
    # "default": {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'new_database_admin',
    #     'USER': 'root',
    #     'PASSWORD': '',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306', 
    # },
    
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'mrph_testdb'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'ZiaIqbal@123'),
        'HOST': '49.13.21.18',
        'PORT': '33061',
},
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DB_LOG_SETTINGS = {
    'tablename': 'django_db_logger_error',
    'module': 'db_logger.models',
    'fields': {
        'level': 'level',
        'msg': 'message',
        'time': 'created_at',
        'request_id': 'request_id',
        'logger': 'logger_name',
        'path': 'path_info',
        'method': 'request_method',
        'server': 'server_protocol',
        'status_code': 'status_code',
        'user_agent': 'http_user_agent',
        'remote_ip': 'remote_addr',
    },
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    "handlers": {
        "db_log": {
            'level': 'INFO',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    "loggers": {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'drk': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'myapi': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },

        'myapidb_log': {
            'handlers': ['db_log'],
            'level': 'INFO'
        },
        
       'django.request': { # logging 500 errors to database
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        }
    },
}
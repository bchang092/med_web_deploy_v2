from pathlib import Path
import os 
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',
    'reviews',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reviews.middleware.NoCacheMiddleware',
]

#ensures logout after getting kicked off
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import dj_database_url
import os

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for local development
#         'NAME': BASE_DIR / 'db.sqlite3',  # SQLite database file
#     }
# }

# # Check if DATABASE_URL environment variable is set (usually for production)
# if 'DATABASE_URL' in os.environ:
#     DATABASES['default'] = dj_database_url.config(
#         conn_max_age=500,  # Make the connection persistent
#         conn_health_checks=True  # Enable connection health checks
#     )

# DATABASE_URL = os.environ.get("DB_URL")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("NAME"),       # Your PostgreSQL database name
        'USER': 'brandonC',     # Your PostgreSQL username
        'PASSWORD': os.environ.get("db_pw"),    # Your PostgreSQL password
        'HOST': os.environ.get("HOST"),         # Hostname (use IP if on a remote server)
        'PORT': os.environ.get("PORT"),              # Default PostgreSQL port
    }
}

# DATABASES = { 
#     'default': { 
#         'ENGINE': 'django.db.backends.postgresql', 
#         'NAME': 'postgres', 
#         'USER': 'brandonchang092', 
#         'PASSWORD': 'yourpassword', 
#         'HOST': 'localhost', 
#         'PORT': '', # If using default PostgreSQL port, keep this empty 
#         } }
                          
LOGOUT_REDIRECT_URL = '/'
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'portal.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

TIME_FORMAT = 'm/d/Y g:i a'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

mail = os.environ.get("EMAIL")
mail_pass = os.environ.get("MAIL_PASSWORD")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = mail
EMAIL_HOST_PASSWORD = mail_pass
DEFAULT_FROM_EMAIL = mail
EMAIL_SUBJECT_PREFIX = "Password Recovery"

#logout view
LOGOUT_REDIRECT_URL="/"
LOGIN_REDIRECT_URL="/"


AWS_ACCESS_KEY_ID= os.environ.get("acc_key")
AWS_SECRET_ACCESS_KEY=os.environ.get("secret_acc_key")
AWS_STORAGE_BUCKET_NAME=os.environ.get("storage_bucket_name")
AWS_S3_SIGNATURE_NAME=os.environ.get("aws_s3_signature_name")
AWS_S3_REGION_NAME=os.environ.get("aws_s3_region_name")
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
AWS_S3_VERIFY=True
DEFAULT_FILE_STORAGE= 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

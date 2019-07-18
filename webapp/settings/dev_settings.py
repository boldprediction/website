"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

from configparser import RawConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','eed4563a.ngrok.io','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'boldpredict',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [] , 
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

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'boldpredict',
    #     'USER': 'boldpredict',
    #     'PASSWORD': 'Bold@15213',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images/')


#Login in Url
LOGIN_URL = '/login'

#After login render to url
LOGIN_REDIRECT_URL = ''

config = RawConfigParser()
print("\n\n\n" + BASE_DIR + "\n\n\n")

config.read(os.path.join(BASE_DIR, '../config/config.ini'))

EMAIL_HOST = config.get('Email', 'Host')
EMAIL_PORT = int(config.get('Email', 'Port'))
EMAIL_HOST_USER = config.get('Email', 'User')
EMAIL_HOST_PASSWORD = config.get('Email', 'Password')
EMAIL_USE_TLS = True

print('Email host:port = {host}:{port}, user={user}'.format(
        host=EMAIL_HOST, port=EMAIL_PORT, user=EMAIL_HOST_USER))

SECRET_KEY = config.get('System', 'SECRET_KEY')
HOST_IP = '127.0.0.1'
APPLICATION_PORT = '8000'
SUBJECT_NUM = 3
SQS_QUERY_URL = 'https://sqs.us-east-2.amazonaws.com/280175692519/bold_sqs'

AWS_ACCESS_KEY = config.get('System', 'AWS_ACCESS_KEY')
AWS_SECRET_KEY = config.get('System', 'AWS_SECRET_KEY')
REGION_NAME =  'us-east-2'

SUBJECTS_URL = '/static/boldpredict/subjects/'
DATA_URL = '/static/boldpredict/data/'


# load contrast configuration 
CONTRAST_CONFIG_DIR = os.path.join(BASE_DIR, '../config/contrast_config.json')
with open(CONTRAST_CONFIG_DIR, 'r') as f:
    contrast_config = json.load(f)

SUBJECTS = contrast_config.get('subjects',None)
SUBJECT_NUM = len(SUBJECTS)
SUBJECTS_JSON = contrast_config.get('subjects_json',None)

# STIMULI_TYPES = contrast_config.get('stimuli_type',None)
# MODEL_TYPES = contrast_config.get('model_type',None)
# WORD_LIST_CONDITIONS = contrast_config.get('word_list_conditions',None)

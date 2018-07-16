#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
"""
Django settings for OpsManage project.

Generated by 'django-admin startproject' using Django 1.9.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import djcelery
from celery import  platforms
from kombu import Queue,Exchange

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

''' celery config '''
djcelery.setup_loader()
BROKER_URL = 'redis://172.18.107.97:6379/4'
CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER='pickle'
CELERY_ACCEPT_CONTENT = ['pickle','json']
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERYD_MAX_TASKS_PER_CHILD = 40
CELERY_TRACK_STARTED = True
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE='Asia/Shanghai'
platforms.C_FORCE_ROOT = True

#celery route config
CELERY_IMPORTS = ("OpsManage.tasks.assets","OpsManage.tasks.ansible",
                  "OpsManage.tasks.cron","OpsManage.tasks.deploy",
                  "OpsManage.tasks.sql","OpsManage.tasks.sched")
CELERY_QUEUES = (
    Queue('default',Exchange('default'),routing_key='default'),
    Queue('ansible',Exchange('ansible'),routing_key='ansible'),
)
CELERY_ROUTES = {
    'OpsManage.tasks.sql.*':{'queue':'default','routing_key':'default'},
    'OpsManage.tasks.assets.*':{'queue':'default','routing_key':'default'},
    'OpsManage.tasks.cron.*':{'queue':'default','routing_key':'default'},
    'OpsManage.tasks.sched.*':{'queue':'default','routing_key':'default'},
    'OpsManage.tasks.ansible.AnsibleScripts':{'queue':'ansible','routing_key':'ansible'},
    'OpsManage.tasks.ansible.AnsiblePlayBook':{'queue':'ansible','routing_key':'ansible'},
}
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'



REDSI_KWARGS_LPUSH = {"host":'172.18.107.97','port':6379,'db':3}
REDSI_LPUSH_POOL = None
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kd8f&jx1h^1m-uldfdo3d#10d9mbc-ijjz!tozusy@aw#h+875'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Channels settings
CHANNEL_LAYERS = {
    "default": {
       "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
       "CONFIG": {
            "hosts": [("172.18.107.97", 6379)],  #无密码方式
            "channel_capacity": {
                                   "http.request": 1000,
                                   "websocket.send*": 10000,
                                },
            "capacity": 10000,           
           },
       "ROUTING": "OpsManage.routing.channel_routing",  # load routing from our routing.py file
       },
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'OpsManage',
    'rest_framework',
    'djcelery',
    'channels',
    'elfinder',
    'storages',
    'wiki',
    'orders',
    'api',
    'filemanage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#     'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),             
}


ROOT_URLCONF = 'OpsManage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["/data/web/opsmanage.eelly.test/OpsManage/static/",'/data/web/opsmanage.eelly.test/OpsManage/templates/'],
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


WSGI_APPLICATION = 'OpsManage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'opsmanage',
        'USER':'root',
        'PASSWORD':'Eelly@15W#96Sb7',
        'HOST':'172.18.107.97',
        'PORT': 3306
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'


STATIC_URL = '/static/'
STATICFILES_DIRS = (
     '/data/web/opsmanage.eelly.test/OpsManage/static/',
    )

MEDIA_ROOT = os.path.join(BASE_DIR,'upload/')
MEDIA_URL = '/upload/'

SFTP_CONF = {
             'port':22,
             'username':'root',
             'password':'welliam',
             'timeout':30
             }  #修改成能sftp登陆OpsManage的账户

WORKSPACES = '/data/web/opsmanage.eelly.test/workspaces/'

LOGIN_URL = '/login'


# -*- coding: utf-8 -*-

# Django settings for volta project.
import os
gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SERVER_EMAIL = 'sara.farmer@btinternet.com'
ADMINS = (
    ('Sara', 'sara@changeassembly.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': os.path.join(PROJECT_PATH, 'database.sqlite'),
        'USER': '', 
        'PASSWORD': '', 
        'HOST': '', 
        'PORT': '', 
    }
}

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
]
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/login/'
ROOT_URLCONF = 'volta.urls'
WSGI_APPLICATION = 'volta.wsgi.application'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = "/static/admin/"
STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'latt3sarenice1att354reg00d!w4ntc0ff#$!nthem0rning'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
##    'cms.context_processors.media',
##    'sekizai.context_processors.sekizai',
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

##CMS_TEMPLATES = (
##    ('cms_volta.html', 'Cms Volta'),
##    ('cms_members.html', 'Cms Members'),
##)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
##    'cms.middleware.multilingual.MultilingualURLMiddleware',
##    'cms.middleware.page.CurrentPageMiddleware',
##    'cms.middleware.user.CurrentUserMiddleware',
##    'cms.middleware.toolbar.ToolbarMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
##    'cms',
##    'mptt',
##    'menus',
##    'south',
##    'sekizai',
##    'filer',
##    'cmsplugin_filer_file',
##    'cmsplugin_filer_folder',
##    'cmsplugin_filer_image',
##    'cmsplugin_filer_teaser',
##    'cmsplugin_filer_video',    
    'groups',
    'channels',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Parse database configuration from $DATABASE_URL
##import dj_database_url
##DATABASES['default'] =  dj_database_url.config()

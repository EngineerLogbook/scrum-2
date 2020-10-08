# Common base template for production and development settings.py

import os
from decouple import config
from django.contrib import messages


SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', "*").split(' ')

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core_management',
    'user_management.apps.UserManagementConfig',
    # 'landingpage.apps.LandingpageConfig',
    'kanban.apps.KanbanConfig',
    'history.apps.HistoryConfig',
    'log.apps.LogConfig',
    'project.apps.ProjectConfig',
    'django.contrib.sites',
    'django_comments',  # https://django-contrib-comments.readthedocs.io/en/latest/
    'crispy_forms',  # https://django-crispy-forms.readthedocs.io/en/latest/
    'formtools',  # https://django-formtools.readthedocs.io/en/latest/
    # 'localflavour',  # https://django-localflavor.readthedocs.io/en/latest /
    'django_extensions',  # https://django-extensions.readthedocs.io/en/latest/index.html
    'imagekit',
    #restframework
    'rest_framework'
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

ROOT_URLCONF = 'engbook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'engbook.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# For login pages
# To be uncommented once these urls are made.

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'log-list'

# Email Support for Database

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default='')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default='')


# # Repcaptcha KEYS

# RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY", default='')
# RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY", default='')


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


LOGOUT_REDIRECT_URL = "landing-page"

CRISPY_TEMPLATE_PACK = "bootstrap4"

#rest framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

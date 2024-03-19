from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'lombard.flexidev.ru']

CLIENT_URL = 'lombard.flexidev.ru'

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alfa_lombard',
        'USER': 'flexites',
        'PASSWORD': 'flexites',
        'HOST': 'localhost',
    },
} """

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 

for k in LOGGING['loggers']:
    LOGGING['loggers'][k]['level'] = 'DEBUG'

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ('rest_framework.permissions.AllowAny',)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "mailtest@flexites.org"
EMAIL_HOST_PASSWORD = "itPja8%YVm"
EMAIL_USE_SSL = True
DEFAULT_EMAIL = 'mikos@flexites.org'

TRANSPORT_1C = {
    'URL': 'https://188.17.149.120:19443/',
    'USERNAME': 'ObmenSait',
    'PASSWORD': '1z@77CV!11',
    'TIMEOUT': 75,
    'LOMBARD_PATH': 'testFPKLK',
    'SERVICE_PATH': '/hs/websiteExchange/'
}

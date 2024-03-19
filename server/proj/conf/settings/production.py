from .base import *

DEBUG = False
ALLOWED_HOSTS = ['lk.permlom.ru', '85.193.87.144']

CLIENT_URL = 'lk.permlom.ru'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alfa_lombard',
        'USER': 'flexites',
        'PASSWORD': 'flexites',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.nic.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'lk@permlom.ru'
EMAIL_HOST_PASSWORD = 'Lk08@)@@'
EMAIL_USE_SSL = True
DEFAULT_EMAIL = 'lk@permlom.ru'

TRANSPORT_1C = {
    'URL': 'https://188.17.149.120:19443/',
    'USERNAME': 'ObmenSait',
    'PASSWORD': '1z@77CV!11',
    'TIMEOUT': 75,
    'LOMBARD_PATH': 'FPKLK',
    'SERVICE_PATH': '/hs/websiteExchange/'
}

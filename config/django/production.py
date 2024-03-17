from config.django.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i3@l3o*a0rx%zg9cl8wo5$x32wed2mx7nu28ah7==7rk*11hun'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'masteruser',
        'PASSWORD': '123qwe',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
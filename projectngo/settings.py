"""
Django settings for projectngo project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xpbs42h2=l)6uudhk))78b(4u5bf3*ela8b*_!1e)ndixhgq)0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'projects',
    'farmers',
    'land_parcels',
    'beneficiaries',
    'users',
    'local_directories',
    'files_manager',
    'carbon_sequestration',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'UNAUTHENTICATED_USER': 'users.models.AnonymousUser',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
}

RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAwQi+6QT1XsRxMD0j5wY6+MDW7JaBVsls1qgyDSfM4wPPpM1Y
zqwNRHNMkufTjdW+9g86WSukeZntUX3ORm4DFXV1yOyPS4EY60lyhoX7qjXfUAk6
iAsRpEfS0WpEanQBB5fQjNLVFI+WXP0o1jwecV0uc8LJJM/dWaWWZ6b0yfmYIjPR
CHhDENp2CznjB4hDbIkTyt855/QivG67AWc5O/mBGN9i1fCmVLUUoVFu2/1WRbGq
UwGg8fsxrZj80+hmD+ib5cu8P4wkuXNEITLAYo7xTRvgiCN5GzrsGhMGk5FHCtpH
VgbSp9RRddLRKWBYjMGFkTUYnEpEMKpnIWlMNQIDAQABAoIBAE13sg4X9FT05yvh
zY/Ae1grI9XMzNlEes5mr7eB2oLcm69azaIbgDORRhDKwqbwOfPLxrHUhuxaLth+
cZLoQYqSGhPpg9RcWeDLGBAOoyH6/sTC/19recgBHwT17cD/Dw66CXMKhYL74O8u
lf3sIJeEOskwScLhPMbmYkb0xNZtBeaLfgSTik8hoO/bynDlcecBj+UH4ofV3yrr
PqwYkv9IqFAsUi9XZDaUbVyVvQb//qJhWcV5mcj9JTEokd5+Y9a6dGxP+tMHjv70
s07uht3nWhn5EQcQHr4cWRD1caA0d2++rs5Umj+izhr3cfsLgnwT9mL4ptQ6jiXY
6ksIxP0CgYEA+M8ADreYGMIreGIyt5kWGqNJ44RKnm9E/CtltJjD3xvhaL7RUmXh
K/a2u3aK2cVsR0GDKoZrUfLp3X6evInToFt669nzBpkY1q5JCB8zqGwvMn/2PkB6
KWO9VdA/00pEcIqhFjUxXOxt7LBXK5yPrk+7CAZxycoH+hAuPk9XN48CgYEAxp0O
UZKNOjwI6vAktTO3HPmboNjlazmvbFQPj2dtwjdrO4y2I2bdz/uo6JH4D7aEO8bj
3wh7uVQrCH460pytRec3AOoJy0wevX8fbXySV++x2NrNKpiOB8ZBX8SqibaWLt52
Mijtl9/t3dkooWObyaIBeR+qSPt+9GF+hfhrffsCgYEAqxN50KTAOdXYme+7O65R
GoPIHF4sCIAtiM42IlUf6Np8xM7fkq5mgxoiTweVNWOfrecHz0eZp0FFOH0FnFGQ
Z6Q/AshbZ+AAyiwQHzuFA3tPgIOnxuoClU71Mnn8SMW6BT/svx5YELKoaqRda6k8
yfgce8oil0MI9RIHGeTn7VUCgYA+GuxYS5hHxnAPbuo7kyFGOTMV99y9S7t0B1Ea
SYBDw+qPI2/s4ASqPYpStxo3Z54vxwCIRHHTwOL38+jW5NE105gafBR18qaGINMl
/FcSkkwtgDW5hRych7z3glrFV0fc/gk9pBivbgFGZtpSpQAY68TEKEeqLKJFLptO
ryCFswKBgBYzbIx6dD5eEKl+P2pVIMbNNPoIFOtUsDiMym0cbmLDmOwiTd5ANr1O
6V/EmN69NkFWMqX6c1q/0pb43WquX8LkD2kcAOc9bnWeJX9xUVd7xfJ8hZdwvpTR
P3iN/ByRe60cS7ttQBrAdnWEn2z8GODK6Wt6tDmUE4+esG0quF4W
-----END RSA PRIVATE KEY-----"""

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwQi+6QT1XsRxMD0j5wY6
+MDW7JaBVsls1qgyDSfM4wPPpM1YzqwNRHNMkufTjdW+9g86WSukeZntUX3ORm4D
FXV1yOyPS4EY60lyhoX7qjXfUAk6iAsRpEfS0WpEanQBB5fQjNLVFI+WXP0o1jwe
cV0uc8LJJM/dWaWWZ6b0yfmYIjPRCHhDENp2CznjB4hDbIkTyt855/QivG67AWc5
O/mBGN9i1fCmVLUUoVFu2/1WRbGqUwGg8fsxrZj80+hmD+ib5cu8P4wkuXNEITLA
Yo7xTRvgiCN5GzrsGhMGk5FHCtpHVgbSp9RRddLRKWBYjMGFkTUYnEpEMKpnIWlM
NQIDAQAB
-----END PUBLIC KEY-----"""

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ALGORITHM": "RS256",
    "SIGNING_KEY": RSA_PRIVATE_KEY,
    "VERIFYING_KEY": RSA_PUBLIC_KEY,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projectngo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'projectngo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "project-ngo",
        "USER": "project-ngo-admin",
        "PASSWORD": "Project-NGO@Admin",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

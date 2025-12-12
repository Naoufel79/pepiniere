###
from .base import *
import dj_database_url
import os
########
DEBUG = False

ALLOWED_HOSTS = ['*']  # Update this with your actual domain in production

###### Database configuration for Railway (PostgreSQL)
# Supports both DATABASE_URL and DATABASE_PUBLIC_URL with fallback
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_PUBLIC_URL')
    )
}

# Static files configuration for production (WhiteNoise)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

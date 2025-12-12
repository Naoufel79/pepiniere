###
from .base import *
import dj_database_url
import os
########
DEBUG = False

ALLOWED_HOSTS = ['*']  # Update this with your actual domain in production

###### Database configuration for Railway (PostgreSQL)
# Prioritize internal database for Railway
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Debug: Print database info (remove in production)
import sys
if 'runserver' in sys.argv:
    print(f"Database URL: {os.environ.get('DATABASE_URL', 'Not set')}")
    print(f"Database config: {DATABASES['default']}")

# Static files configuration for production (WhiteNoise)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']
# SECURE_SSL_REDIRECT = True  # Railway handles SSL automatically
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

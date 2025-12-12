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

# Debug: Always print database info for Railway debugging
print("=== Railway Database Debug ===")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')}")
print(f"DATABASE_PUBLIC_URL: {os.environ.get('DATABASE_PUBLIC_URL', 'Not set')}")
print(f"Using database config: {DATABASES['default']}")
print("===============================")

# Debug: Print database info (remove in production)
import sys
if 'runserver' in sys.argv:
    print(f"Database URL: {os.environ.get('DATABASE_URL', 'Not set')}")
    print(f"Database config: {DATABASES['default']}")

# Static files configuration for production (WhiteNoise)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration for production
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Add media files to static finders so WhiteNoise serves them
STATICFILES_DIRS = [
    MEDIA_ROOT,
]

# Ensure media directories exist
import os
os.makedirs(MEDIA_ROOT / 'products', exist_ok=True)

# Security settings for production
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']
# SECURE_SSL_REDIRECT = True  # Railway handles SSL automatically
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

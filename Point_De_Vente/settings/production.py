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

# Create superuser with password after migrations
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line
import sys

# Create superuser if it doesn't exist
try:
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'Admin1234')
        print("Superuser 'admin' created successfully")
    else:
        print("Superuser 'admin' already exists")
except Exception as e:
    print(f"Superuser creation failed: {e}")

# Debug: Print database info (remove in production)
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

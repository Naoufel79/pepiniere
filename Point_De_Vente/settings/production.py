###
from .base import *
import dj_database_url
import os
########
DEBUG = False

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*.railway.app,pepiniere-production.up.railway.app').split(',') if h.strip()]

###### Database configuration for Railway (PostgreSQL)
# Prioritize internal database for Railway
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Optional: minimal DB info (no secrets)
try:
    _db = DATABASES.get('default', {})
    print(f"DB: engine={_db.get('ENGINE')} host={_db.get('HOST')} port={_db.get('PORT')} name={_db.get('NAME')}")
except Exception:
    pass

# Debug: Always print database info for Railway debugging

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
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.railway.app,https://pepiniere-production.up.railway.app').split(',') if o.strip()]
# SECURE_SSL_REDIRECT = True  # Railway handles SSL automatically
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SERVE_MEDIA = True

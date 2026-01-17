###
from .base import *
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*.railway.app,pepiniere-production.up.railway.app').split(',') if h.strip()]

###### Database configuration for Railway (PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Static files configuration for production (WhiteNoise)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Disable compression and manifest for maximum compatibility
# This ensures all static files (including images) are served correctly
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# WhiteNoise will still serve files, but without compression issues
WHITENOISE_USE_FINDERS = False
WHITENOISE_AUTOREFRESH = False
WHITENOISE_MAX_AGE = 31536000  # 1 year cache

# Cloudinary Configuration (For Persistent Media ONLY - not static files)
# Only use Cloudinary if the URL is set in environment variables
if os.environ.get('CLOUDINARY_URL'):
    # Add cloudinary apps for MEDIA files only
    INSTALLED_APPS = INSTALLED_APPS + ['cloudinary_storage', 'cloudinary']
    
    # Cloudinary settings - Parse from CLOUDINARY_URL
    import cloudinary
    cloudinary.config(cloudinary_url=os.environ.get('CLOUDINARY_URL'))
    
    # Use Cloudinary for Media files (images, uploads) via STORAGES (Django 5.x way)
    STORAGES["default"] = {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }
    
    # Media URL from Cloudinary
    MEDIA_URL = '/media/'
    
    print("✅ Cloudinary storage activated for media files")
else:
    # Fallback to local file system (Ephemeral on Railway - will lose files on restart!)
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'
    
    # Ensure media directories exist
    os.makedirs(MEDIA_ROOT / 'products', exist_ok=True)
    SERVE_MEDIA = True
    
    print("⚠️ WARNING: Using ephemeral file storage - media files will be lost on restart!")

# Security settings for production
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.railway.app,https://pepiniere-production.up.railway.app').split(',') if o.strip()]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


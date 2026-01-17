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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cloudinary Configuration (For Persistent Media)
# Only use Cloudinary if the URL is set in environment variables
if os.environ.get('CLOUDINARY_URL'):
    # Add cloudinary apps BEFORE other apps to ensure proper initialization
    INSTALLED_APPS = ['cloudinary_storage', 'cloudinary'] + INSTALLED_APPS
    
    # Use Cloudinary for Media files (images, uploads)
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    
    # Cloudinary settings - Parse from CLOUDINARY_URL if individual vars not set
    import cloudinary
    cloudinary.config(cloudinary_url=os.environ.get('CLOUDINARY_URL'))
    
    # Media URL from Cloudinary
    MEDIA_URL = '/media/'  # Cloudinary storage will handle the actual URLs
    
    print("✅ Cloudinary storage activated for media files")
else:
    # Fallback to local file system (Ephemeral on Railway - will lose files on restart!)
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'
    
    # Add media files to static finders so WhiteNoise serves them
    STATICFILES_DIRS = [MEDIA_ROOT]
    
    # Ensure media directories exist
    os.makedirs(MEDIA_ROOT / 'products', exist_ok=True)
    SERVE_MEDIA = True
    
    print("⚠️ WARNING: Using ephemeral file storage - media files will be lost on restart!")

# Security settings for production
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.railway.app,https://pepiniere-production.up.railway.app').split(',') if o.strip()]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


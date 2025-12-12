# 🚂 Railway Deployment Guide for Pepiniere Django App

This guide will help you deploy your Django application to Railway.app.

## 📋 Current Setup

Your application is already well-prepared for Railway deployment with:

- ✅ **Procfile** configured for Gunicorn
- ✅ **requirements.txt** with all necessary dependencies
- ✅ **runtime.txt** specifying Python 3.13.1
- ✅ **Production settings** configured for Railway
- ✅ **WhiteNoise** for static file serving
- ✅ **PostgreSQL** database support via `dj-database-url`

## 🚀 Deployment Steps

### 1. Prepare Your Code

```bash
# Run the deployment preparation script
deploy_railway_fast.bat
```

This will:
- Run database migrations
- Collect static files
- Create admin user (if not exists)

### 2. Push to GitHub

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 3. Create Railway Project

1. Go to [Railway.app](https://railway.app/) and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect it's a Python/Django app

### 4. Configure Environment Variables

Add these variables in Railway's project settings:

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | `your-secret-key-here` | Generate a secure one |
| `DATABASE_URL` | (Auto-provisioned) | Railway provides this |
| `DATABASE_PUBLIC_URL` | (Optional fallback) | Alternative database URL |
| `DEBUG` | `False` | Already set in production.py |
| `ALLOWED_HOSTS` | `*.railway.app,yourdomain.com` | Update as needed |

### 5. Deploy!

Click "Deploy" and Railway will:
1. Install dependencies from `requirements.txt`
2. Run the commands from your `Procfile`
3. Start your Gunicorn server

## � File Structure

```
pepiniere/
├── Procfile                  # Railway entry point
├── requirements.txt          # Python dependencies
├── runtime.txt               # Python version
├── deploy_railway_fast.bat   # Deployment prep script
├── Point_De_Vente/
│   └── settings/
│       └── production.py     # Production settings
└── ... (your app files)
```

## � Troubleshooting

**If you get Django import errors:**
```bash
pip install -r requirements.txt
```

**If static files don't load:**
- Ensure `WHITENOISE` is in your middleware
- Check `STATIC_ROOT` is set correctly
- Run `python manage.py collectstatic` again

## 🎉 Success!

Your app should now be live at: `https://your-project-name.up.railway.app`

## 📝 Notes

- Railway automatically provisions PostgreSQL databases
- The `Procfile` handles all deployment commands
- WhiteNoise serves static files efficiently
- Production settings are security-hardened

## ⚠️ Important Settings Information

**About DEBUG and ALLOWED_HOSTS:**

Your app has two settings configurations:
- `base.py`: Has `DEBUG = True` and `ALLOWED_HOSTS = []` (for development)
- `production.py`: Correctly overrides these with `DEBUG = False` and `ALLOWED_HOSTS = ['*']`

**For Railway deployment:**
1. The deployment script sets `DJANGO_SETTINGS_MODULE=Point_De_Vente.settings.production`
2. This ensures production settings are used
3. The script also explicitly sets environment variables for extra safety

**Your production.py is correctly configured:**
```python
DEBUG = False
ALLOWED_HOSTS = ['*']  # Safe for Railway, but update with your actual domain later
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']
SECURE_SSL_REDIRECT = True
```

This is perfectly normal and secure for Railway deployment!

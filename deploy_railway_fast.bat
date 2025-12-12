@echo off
REM Railway Deployment Script for Django App (Windows) - Fast Version
REM This script prepares the application for deployment on Railway.app
REM Skips dependency installation (assumes they're already installed)

echo 🚀 Starting Railway deployment preparation...

REM Set environment variables if not already set
set DJANGO_SETTINGS_MODULE=Point_De_Vente.settings.production
set PYTHONUNBUFFERED=1
set DEBUG=False
set ALLOWED_HOSTS=*.railway.app

echo 🔄 Running database migrations...
python manage.py migrate --noinput

echo 📦 Collecting static files...
python manage.py collectstatic --noinput

echo 👤 Creating superuser (if not exists)...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'Admin1234') | python manage.py shell

echo 🎉 Deployment preparation complete!
echo Your app is ready to be deployed to Railway!
echo.
echo Next steps:
echo 1. Push your code to GitHub
echo 2. Create a new project on Railway.app
echo 3. Connect your GitHub repository
echo 4. Add required environment variables:
echo    - SECRET_KEY (generate a secure one)
echo    - DATABASE_URL (Railway will provide this)
echo    - DEBUG=False
echo    - ALLOWED_HOSTS=your-domain.com,*.railway.app
echo 5. Deploy!

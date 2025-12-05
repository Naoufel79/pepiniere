web: python manage.py migrate && python manage.py collectstatic --no-input && gunicorn Point_De_Vente.wsgi:application --bind 0.0.0.0:$PORT


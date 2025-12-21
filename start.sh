#!/bin/bash
set -e

# Ensure production settings
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-Point_De_Vente.settings.production}

python manage.py migrate --noinput

# Optional superuser creation (no hardcoded passwords)
if [ "${CREATE_SUPERUSER}" = "true" ]; then
  if [ -z "${DJANGO_SUPERUSER_PASSWORD}" ]; then
    echo "CREATE_SUPERUSER=true but DJANGO_SUPERUSER_PASSWORD is not set; skipping superuser creation."
  else
    python manage.py create_superuser       --username "${DJANGO_SUPERUSER_USERNAME:-admin}"       --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"       --password "${DJANGO_SUPERUSER_PASSWORD}"
  fi
fi

python manage.py collectstatic --noinput

exec gunicorn Point_De_Vente.wsgi:application --bind 0.0.0.0:${PORT}

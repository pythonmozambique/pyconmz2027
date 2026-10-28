#!/bin/sh
set -eu

uv sync

uv run python manage.py migrate
uv run python manage.py createcachetable wafer_cache_table
uv run python manage.py wafer_add_default_groups

if ! uv run python manage.py shell -c "from django.contrib.auth import get_user_model; import sys; sys.exit(0 if get_user_model().objects.filter(username='super').exists() else 1)"; then
  DJANGO_SUPERUSER_PASSWORD='super' uv run python manage.py createsuperuser \
    --noinput --username super --email super@pycon.mz
fi

uv run python manage.py load_md_content
uv run python manage.py seed_conference

uv run python manage.py shell -c "from django.contrib.sites.models import Site; site = Site.objects.get(pk=1); site.domain='localhost:8000'; site.name='PyCon Mozambique 2027'; site.save()"

npm install
npm run tailwind

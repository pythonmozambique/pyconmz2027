# PyCon Mozambique 2027

Conference site built on [wafer](https://github.com/CTPUG/wafer) 0.17, following the layout of [PyCon ZA 2026](https://github.com/PyConZA/pyconza2026). Talks, the schedule, sponsors, and ticket claims are edited in the Django admin and read from the database.

## Local setup

Python 3.13 and uv.

```bash
./install_dev.sh
uv run python manage.py runserver
```

The development admin user is `super` / `super`.

After changing `static/css/main.css` or Tailwind classes in a template, rebuild CSS:

```bash
npm run tailwind
```

`npm run tailwind-w` rebuilds while you edit.

Production settings live in `settings_prod.py` and expect `SECRET_KEY`. Postgres is used when `DATABASE_URL` is set.

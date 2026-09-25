# Manufacturing ERP Backend

Backend API untuk aplikasi Manufacturing ERP menggunakan Django dan Django REST Framework.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- UV

Install dependencies:

```bash
uv sync
```

## Database Migration

Buat migration:

```bash
uv run python manage.py makemigrations
```

Jalankan migration:

```bash
uv run python manage.py migrate
```

## Seed Data

Seed Category:

```bash
uv run python manage.py seed_category
```

Seed Unit:

```bash
uv run python manage.py seed_unit
```

## Run Server

```bash
uv run python manage.py runserver
```

## Development Commands

Check project:

```bash
uv run python manage.py check
```

Create migrations:

```bash
uv run python manage.py makemigrations
```

Apply migrations:

```bash
uv run python manage.py migrate
```

Run server:

```bash
uv run python manage.py runserver
```

dengan URL repository backend kamu.

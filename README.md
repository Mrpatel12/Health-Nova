# Health Nova

A complete full-stack doctor appointment booking system built with Django, SQLite3, Bootstrap 5, and a responsive healthcare UI.

## Features

- Patient registration, login, and profile management
- Doctor listing, search, and filtering
- Appointment booking with date validation and duplicate prevention
- Patient dashboard with appointment summaries
- Doctor dashboard for managing appointment requests
- Admin dashboard support via Django admin
- Bootstrap 5 responsive UI with clean professional styling

## Project Structure

- `manage.py` - Django management entrypoint
- `health_nova_project/` - Django project configuration
- `booking/` - Django app containing models, views, forms, and URLs
- `templates/booking/` - HTML templates for pages and layout
- `static/css/style.css` - Custom styling for the UI
- `static/js/main.js` - Frontend helper scripts

## Setup Instructions

1. Create and activate a Python virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser

```bash
python manage.py createsuperuser
```

5. Run the server

```bash
python manage.py runserver
```

6. Open the app:

```bash
http://127.0.0.1:8000/
```

## Admin Panel

Open the admin dashboard:

```bash
http://127.0.0.1:8000/admin/
```

Use your superuser credentials to manage doctors, appointments, and users.

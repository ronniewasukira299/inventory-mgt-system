# Serial & Parallel Devices Web Platform

A Django-based web platform for managing and comparing serial and parallel devices.

## Project Structure

- `inventory_mgt/` - Main Django project settings
- `accounts/` - User authentication and profiles
- `api/` - REST API endpoints
- `blog/` - Blog functionality
- `content/` - Main site content
- `core/` - Core models and business logic
- `notifications/` - Notification system

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your values
6. Run migrations: `python manage.py makemigrations && python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

## Development

- Use feature branches for development
- Main branch is protected
- Pull requests required for merging

## Database Schema

See `DATABASE_SCHEMA.md` for detailed ERD and model relationships.

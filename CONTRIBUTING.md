# Contributing Guidelines

## Getting Started

1. Clone the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Set up your environment (see Development Setup below)
4. Make your changes
5. Write tests for your changes
6. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/inventory-mgt-system.git
cd inventory-mgt-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Docker Setup

```bash
# Build and start containers
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Branching Strategy

- `main`: Production-ready code (protected)
- `dev`: Integration branch for features
- `feature/*`: Feature branches (create from `dev`)
- `bugfix/*`: Bug fix branches (create from `dev`)
- `hotfix/*`: Production hotfixes (create from `main`)

## Code Standards

### Python/Django
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use Django's ORM when possible

### Commits
- Use clear, descriptive commit messages
- Reference issue numbers: `fix: #123 description`
- Keep commits atomic and logical
- Format: `type: short description`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Testing
- Write tests as you develop
- Aim for >80% code coverage
- Test models, views, and forms
- Use Django's TestCase for database tests

```bash
# Run tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

## Project Ownership

### Backend (Rwot)
- inventory_mgt/settings.py
- inventory_mgt/urls.py
- accounts/
- api/
- core/
- Docker files

### Frontend (Nsimbi)
- Templates in templates/
- Static files (CSS, JS)
- UI/UX components

### Team coordination
- Post in team chat when changes affect other areas
- Review each other's code before merging

## Pull Request Process

1. Update your `dev` branch with latest changes
2. Create feature branch: `feature/your-feature`
3. Make changes and commit with clear messages
4. Push to your fork
5. Create pull request with description of changes
6. Address code review comments
7. Get approval from another developer
8. Merge to `dev` branch

## Security Considerations

- Never commit secrets or passwords
- Use environment variables for sensitive data
- Always validate user input
- Sanitize output to prevent XSS
- Use Django's built-in CSRF protection
- Follow principle of least privilege for permissions

## Performance Guidelines

- Use select_related() and prefetch_related() for database queries
- Add database indexes on frequently queried fields
- Cache expensive operations
- Profile code before optimizing
- Avoid N+1 queries

## Documentation

- Update README.md for new features
- Add docstrings to all code
- Keep API_DOCUMENTATION.md current
- Document complex business logic
- Update ARCHITECTURE_DECISIONS.md for major changes

## Questions or Issues?

- Open an issue on the repository
- Post in team chat for discussion
- Check existing documentation first
Naming Convention: Use fetaure/name-feature-description( e.g feature/rwot-auth)
Pull Requests: No direct merges to dev. Every change requires a pull request review
Coding Rules:
Separation of Concerns: Do not modify files an app assigned to another developer.
Shared constants: Add project-wide constants( like DEVICE_TYPES) to constants.py instead of hard coding.
Blockers: If you are stuck for more, ping Ronnie or Rwot for help.
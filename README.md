# Supplier, Inventory, Invoicing & Customer Debt Management System

A comprehensive Django-based web application for managing suppliers, customers, inventory, invoicing, receipts, and customer debts with a real-time manager monitoring dashboard.

## Project Overview

This system provides businesses with a centralized platform to:
- Manage customer and supplier relationships
- Track inventory and stock movements
- Generate and manage invoices and receipts
- Monitor customer debts and collection periods
- View real-time dashboards for management oversight
- Generate comprehensive reports
- Maintain complete audit logs for compliance

## Key Features

### 1. User Management
- Role-based access control (Admin, Editor, Viewer, Manager)
- Secure authentication and authorization
- User activity tracking

### 2. Organization Management
- **Supplier Management**: Track suppliers, contact info, payment terms, and ratings
- **Customer Management**: Manage customers, credit limits, credit tracking, and status

### 3. Inventory Management
- **Product Management**: Full product lifecycle with pricing and specifications
- **Stock Tracking**: Real-time inventory levels with reorder management
- **Stock Movements**: Track all inventory in/out transactions with audit trail
- **Category Management**: Organize products by categories

### 4. Invoicing System
- Generate professional invoices
- Track invoice status (Draft, Issued, Partially Paid, Paid, Cancelled, Overdue)
- Item-level details with tax calculations
- Approval workflow for financial control
- Invoice aging and payment tracking

### 5. Receipt System
- Record supplier receipts and deliveries
- Match received quantities with purchase orders
- Approval workflow before stock update
- Historical receipt tracking

### 6. Debt Management
- **Automatic Debt Creation** from unpaid invoices
- **Payment Tracking**: Record customer payments with multiple methods
- **Overdue Management**: Track days overdue and collection attempts
- **Collection Period Analysis**: Monitor debt aging
- **Debt Status** tracking: Pending, Partially Paid, Paid, Overdue, Written Off

### 7. Real-Time Manager Dashboard
- Key metrics at a glance
- Recent transactions monitoring
- Pending approvals display
- Stock level alerts
- Overdue debt notifications
- Quick links to all management areas

### 8. Audit & Compliance
- Complete action logging for all transactions
- Track user actions with timestamps
- Record changes with before/after values
- IP address and user agent capture
- Non-editable audit trail for compliance

### 9. Reports & Analytics
- Inventory reports
- Sales and revenue reports
- Debt aging reports
- Customer activity reports
- Supplier performance metrics

## Technology Stack

- **Backend**: Django 6.0 (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **API**: Django REST Framework (for programmatic access)

## Project Structure

```
inventory-mgt-system/
├── accounts/                 # User authentication and profiles
│   ├── models.py            # Custom User model with roles
│   ├── views.py             # Auth views
│   ├── forms.py             # Auth forms
│   └── templates/
│
├── core/                     # Main business logic
│   ├── models.py            # All business models
│   ├── views.py             # Business logic views
│   ├── forms.py             # Business forms
│   ├── admin.py             # Django admin configuration
│   ├── urls.py              # URL routing
│   ├── management/          # Custom management commands
│   ├── migrations/          # Database migrations
│   └── templates/
│
├── api/                      # REST API endpoints
│   ├── views.py             # API views
│   ├── urls.py              # API routing
│   └── serializers.py       # API serializers
│
├── notifications/           # Notification system
├── blog/                     # Blog functionality
├── content/                  # Static content
├── inventory_mgt/           # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Auth templates
│   └── core/                # Business templates
│
├── static/                  # Static files (CSS, JS, images)
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker configuration
├── Dockerfile               # Docker image definition
├── .env.example             # Environment variables template
└── db.sqlite3               # SQLite database (development)
```

## Core Models

### Organization Models
- **Supplier**: Supplier information, contact details, payment terms, ratings
- **Customer**: Customer information, credit limits, credit tracking, status

### Inventory Models
- **Category**: Product categories for organization
- **Tag**: Product tags for additional categorization
- **Product**: Core product model with pricing and stock information
- **Stock**: Stock levels per product and location
- **StockMovement**: Audit trail of all inventory movements

### Transaction Models
- **Invoice**: Customer invoices with items and status tracking
- **InvoiceItem**: Individual line items in invoices
- **Receipt**: Supplier receipts with delivery tracking
- **ReceiptItem**: Individual line items in receipts

### Financial Models
- **Debt**: Customer debt tracking with status and aging
- **DebtPayment**: Individual payment records against debts

### System Models
- **AuditLog**: Complete action audit trail for compliance
- **ManagerDashboardMetrics**: Real-time dashboard metrics

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory-mgt-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Copy environment variables**
   ```bash
   cp .env.example .env
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Load sample data (optional)**
   ```bash
   python manage.py seed_devices
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Web: http://localhost:8000
    - Admin: http://localhost:8000/admin

## Usage

### Admin Dashboard
- Access at `/admin` with superuser credentials
- Manage all entities (Products, Customers, Suppliers, Invoices, etc.)
- View and analyze audit logs
- Manage user accounts

### Manager Dashboard
- Access at `/dashboard` (requires login)
- View real-time metrics and KPIs
- Monitor pending approvals
- See recent transactions
- Quick access to management areas

### API Endpoints
- Products: `/api/products/`
- Search: `/api/search/`

## Development

### Creating New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Running Tests
```bash
python manage.py test
```

### Management Commands
```bash
# Seed sample data
python manage.py seed_devices
```

## Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Production Deployment

#### 1. Environment Setup
```bash
# Create production environment file
cp .env.example .env.production

# Edit .env.production with production values:
# - DEBUG=False
# - SECRET_KEY=<generate-long-random-key>
# - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# - DATABASE_URL=postgresql://user:password@host:port/database
# - EMAIL_HOST=smtp.yourprovider.com
# - EMAIL_HOST_USER=your-email@domain.com
# - EMAIL_HOST_PASSWORD=your-email-password
# - REDIS_URL=redis://localhost:6379/1 (for caching/session storage)
```

#### 2. Database Setup (PostgreSQL)
```bash
# Install PostgreSQL and create database
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres createdb inventory_db
sudo -u postgres createuser inventory_user
sudo -u postgres psql -c "ALTER USER inventory_user PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;"
```

#### 3. Application Deployment
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary django-redis redis

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Load initial data (optional)
python manage.py seed_data
```

#### 4. Gunicorn Setup
Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/inventory-mgt-system
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock inventory_mgt.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start Gunicorn
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

#### 5. Nginx Setup
Create `/etc/nginx/sites-available/inventory_app`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /path/to/inventory-mgt-system/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/inventory_app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test renewal
sudo certbot renew --dry-run
```

#### 7. Security Hardening
```bash
# Update settings.py for production:
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Set up firewall
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Secure SSH
sudo nano /etc/ssh/sshd_config
# Change Port to non-standard
# PermitRootLogin no
# PasswordAuthentication no
sudo systemctl restart sshd
```

#### 8. Monitoring & Backups
```bash
# Install monitoring tools
pip install django-prometheus sentry-sdk

# Set up automated backups
# Create backup script in /usr/local/bin/backup_inventory.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump inventory_db > /backups/inventory_$DATE.sql
find /backups -name "inventory_*.sql" -mtime +30 -delete

# Add to crontab
crontab -e
# 0 2 * * * /usr/local/bin/backup_inventory.sh
```

### Production Checklist
- [ ] Set DEBUG = False in settings
- [ ] Configure ALLOWED_HOSTS with actual domains
- [ ] Set strong SECRET_KEY (50+ characters, random)
- [ ] Configure PostgreSQL database
- [ ] Set up static files serving with Nginx
- [ ] Configure email settings for notifications
- [ ] Enable HTTPS with SSL certificate
- [ ] Set up automated database backups
- [ ] Configure logging to files
- [ ] Set up monitoring and alerts
- [ ] Test all functionality in production
- [ ] Configure firewall rules
- [ ] Disable root SSH access
- [ ] Set up log rotation
- [ ] Configure rate limiting
- [ ] Set up error reporting (Sentry)

## Security Considerations

- Always keep SECRET_KEY confidential
- Use environment variables for sensitive data
- Enable CSRF protection
- Use HTTPS in production
- Regularly update dependencies
- Monitor audit logs for suspicious activity
- Implement rate limiting
- Use strong passwords
- Enable two-factor authentication for admin users

## Performance Optimization

- Database query optimization with select_related/prefetch_related
- Indexed database fields for fast searching
- Pagination for list views
- Caching for frequently accessed data
- Async task processing for heavy operations

## Troubleshooting

### Database Issues
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

### Cache Clearing
```bash
python manage.py clear_cache
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## Documentation Files

- [API Documentation](API_DOCUMENTATION.md)
- [Architecture Decisions](ARCHITECTURE_DECISIONS.md)
- [Database Schema](DATABASE_SCHEMA.md)
- [Project Structure](PROJECT_STRUCTURE.md)

## Support

For issues and questions:
1. Check existing GitHub issues
2. Create a new issue with detailed information
3. Contact the development team

## License

[Specify your license here]

## Changelog

### Version 1.0.0 - Current Release
- Full supplier management system
- Complete inventory management
- Invoicing and receipting system
- Customer debt tracking
- Real-time manager dashboard
- Comprehensive audit logging
- Bootstrap 5 responsive UI

## Future Enhancements

- Multi-currency support
- Advanced reporting and analytics
- Mobile application
- Real-time notifications
- Dashboard export functionality
- Integration with accounting software
- Barcode scanning for inventory
- Payment gateway integration
- Customer portal
- Automated collection reminders


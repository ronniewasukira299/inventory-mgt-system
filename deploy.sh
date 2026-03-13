#!/bin/bash

# Inventory Management System - Production Deployment Script
# This script helps deploy the application to a production server

set -e  # Exit on any error

echo "🚀 Starting Inventory Management System Deployment"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    print_error ".env.production file not found!"
    print_status "Copy .env.production.example to .env.production and configure your settings"
    exit 1
fi

print_status "Checking system requirements..."

# Check if Python 3.10+ is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

print_status "Python version check passed: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate --settings=inventory_mgt.settings_production

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput --settings=inventory_mgt.settings_production

# Create logs directory
print_status "Creating logs directory..."
mkdir -p logs

# Create media directory
print_status "Creating media directory..."
mkdir -p media

print_status "✅ Deployment preparation complete!"
print_warning "Next steps:"
echo "  1. Configure your web server (Nginx/Apache)"
echo "  2. Set up SSL certificate"
echo "  3. Configure systemd service for Gunicorn"
echo "  4. Set up database backups"
echo "  5. Configure monitoring"
echo "  6. Test the application"
print_status "See README.md for detailed production deployment instructions"
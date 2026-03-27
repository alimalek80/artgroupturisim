#!/bin/bash

# Accounts App Setup Script
# This script will set up the accounts app database

echo "=================================="
echo "ACCOUNTS APP - DATABASE SETUP"
echo "=================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please activate first with: source .venv/bin/activate"
    exit 1
fi

echo "✅ Virtual environment detected"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"
echo ""

# Make migrations
echo "🔨 Creating migrations for accounts app..."
python manage.py makemigrations accounts
if [ $? -ne 0 ]; then
    echo "❌ Failed to create migrations"
    exit 1
fi
echo "✅ Migrations created"
echo ""

# Apply migrations
echo "🗄️  Applying migrations to database..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Failed to apply migrations"
    exit 1
fi
echo "✅ Migrations applied"
echo ""

# Create superuser
echo "👤 Creating superuser..."
echo "Please enter superuser details:"
python manage.py createsuperuser

echo ""
echo "=================================="
echo "✅ SETUP COMPLETE!"
echo "=================================="
echo ""
echo "You can now:"
echo "  1. Run the dev server: python manage.py runserver"
echo "  2. Visit http://127.0.0.1:8000/accounts/register/"
echo "  3. Visit http://127.0.0.1:8000/admin/"
echo ""
echo "For more information, see:"
echo "  - IMPLEMENTATION_SUMMARY.md"
echo "  - ACCOUNTS_SETUP_GUIDE.md"
echo ""

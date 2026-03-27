# ACCOUNTS APP SETUP - CONFIGURATION GUIDE

## ✅ FILES CREATED

### Backend Files
- `accounts/models.py` - CustomUser and Profile models
- `accounts/managers.py` - CustomUserManager for email authentication
- `accounts/forms.py` - All forms with Tailwind styling
- `accounts/views.py` - All views (register, login, logout, profile, edit_profile, change_password)
- `accounts/urls.py` - URL patterns for accounts app
- `accounts/admin.py` - Admin configuration
- `accounts/signals.py` - Auto profile creation signal
- `accounts/apps.py` - App config with signal import

### Template Files (Tailwind CSS)
- `templates/accounts/register.html`
- `templates/accounts/login.html`
- `templates/accounts/profile.html`
- `templates/accounts/edit_profile.html`
- `templates/accounts/change_password.html`

---

## 🔧 REQUIRED CHANGES TO settings.py

Open `artturisim/settings.py` and add/modify the following:

### 1. Add Custom User Model (CRITICAL - Must be done before first migration)

```python
# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'
```

**⚠️ IMPORTANT:** This must be set BEFORE running any migrations if this is a new project!

### 2. Add Authentication URLs

```python
# Authentication URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:profile'
LOGOUT_REDIRECT_URL = 'accounts:login'
```

### 3. Add Media Files Configuration

```python
# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 4. Verify TEMPLATES Configuration

Make sure your TEMPLATES setting includes the templates directory:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # This should already be set
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # Add this for media files
            ],
        },
    },
]
```

### 5. Verify INSTALLED_APPS

Make sure 'accounts' is in INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'core',
    'accounts',  # Should already be here
    'tours',
    'bookings',
    'blog',
    'contact',
    'newsletter',
]
```

---

## 🔗 REQUIRED CHANGES TO Main urls.py

Open `artturisim/urls.py` and update it:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Add this line
    # Add your other app URLs here
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📁 CREATE MEDIA DIRECTORY

Create the media directory structure:

```bash
mkdir -p media/profile_images
```

Optionally, add a default profile image:

```bash
# You can add a default.jpg image to media/profile_images/
```

---

## 🗄️ DATABASE MIGRATIONS

Run these commands in order:

### Step 1: Make Migrations
```bash
python manage.py makemigrations accounts
```

### Step 2: Apply Migrations
```bash
python manage.py migrate
```

### Step 3: Create Superuser
```bash
python manage.py createsuperuser
```

When prompted, enter:
- **Email:** your-email@example.com
- **Password:** your-secure-password
- **Password (again):** your-secure-password

---

## ✨ FEATURES IMPLEMENTED

### Authentication
- ✅ Email-based authentication (no username)
- ✅ Custom User Model with CustomUserManager
- ✅ User registration with email validation
- ✅ User login
- ✅ User logout
- ✅ Password change

### Profile Management
- ✅ Automatic profile creation via signals
- ✅ Profile view
- ✅ Edit profile (user info + profile info)
- ✅ Profile image upload
- ✅ Phone number field
- ✅ Bio field

### Admin Panel
- ✅ Custom User admin with proper fields
- ✅ Profile admin
- ✅ Search and filter capabilities

### Templates
- ✅ Modern Tailwind CSS design
- ✅ Mobile responsive
- ✅ Clean form validation messages
- ✅ Professional layout extending base.html

---

## 🚀 TESTING THE APP

### Test User Registration
1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Visit: http://127.0.0.1:8000/accounts/register/

3. Create a new account

### Test Profile
4. After registration, you should be redirected to: http://127.0.0.1:8000/accounts/profile/

5. Test editing profile: http://127.0.0.1:8000/accounts/profile/edit/

6. Test password change: http://127.0.0.1:8000/accounts/password/change/

### Test Admin Panel
7. Visit: http://127.0.0.1:8000/admin/

8. Login with superuser credentials

9. Verify CustomUser and Profile models are registered

---

## 📋 URL ENDPOINTS

All accounts URLs are namespaced under 'accounts:':

| URL | Name | Description |
|-----|------|-------------|
| `/accounts/register/` | `accounts:register` | User registration |
| `/accounts/login/` | `accounts:login` | User login |
| `/accounts/logout/` | `accounts:logout` | User logout |
| `/accounts/profile/` | `accounts:profile` | View profile |
| `/accounts/profile/edit/` | `accounts:edit_profile` | Edit profile |
| `/accounts/password/change/` | `accounts:change_password` | Change password |

---

## 🔐 Security Features

- Passwords are hashed using Django's default PBKDF2 algorithm
- CSRF protection on all forms
- Login required decorators on protected views
- Email uniqueness enforced
- Session maintained after password change
- Profile image upload validation

---

## 📝 Model Fields Reference

### CustomUser Model
- `email` - EmailField (unique, required)
- `first_name` - CharField (optional)
- `last_name` - CharField (optional)
- `is_active` - BooleanField (default: True)
- `is_staff` - BooleanField (default: False)
- `is_superuser` - BooleanField (default: False)
- `date_joined` - DateTimeField (auto)
- `last_login` - DateTimeField (auto)

### Profile Model
- `user` - OneToOneField to CustomUser
- `phone_number` - CharField (optional)
- `profile_image` - ImageField (optional)
- `bio` - TextField (optional, max 500 chars)
- `created_at` - DateTimeField (auto)
- `updated_at` - DateTimeField (auto)

---

## 🎨 Customization Tips

### Change Default Profile Image
Edit the `default` parameter in `models.py`:
```python
profile_image = models.ImageField(
    upload_to='profile_images/',
    blank=True,
    null=True,
    default='profile_images/your-default.jpg'  # Change this
)
```

### Add More Profile Fields
Add fields to the Profile model in `models.py`, then:
1. Add field to ProfileUpdateForm in `forms.py`
2. Add field display in templates
3. Run `makemigrations` and `migrate`

### Customize Tailwind Styling
All form fields have Tailwind classes in `forms.py`. Modify the `attrs` dictionary to change styling.

---

## ⚠️ IMPORTANT NOTES

1. **First Migration**: The `AUTH_USER_MODEL` setting must be configured BEFORE the first migration if starting fresh.

2. **Existing Project**: If you have existing migrations, you may need to delete the database and start fresh, or create data migrations.

3. **Pillow Required**: For image upload functionality, install Pillow:
   ```bash
   pip install Pillow
   ```
   Add it to requirements.txt:
   ```
   Pillow>=10.0.0
   ```

4. **Production**: Remember to configure proper file storage (like S3) for production instead of local media files.

5. **Email Backend**: For production, configure a proper email backend for password reset functionality.

---

## 🆘 TROUBLESHOOTING

### Error: "accounts.CustomUser doesn't exist"
- Make sure you've run migrations: `python manage.py migrate`

### Error: "No module named 'PIL'"
- Install Pillow: `pip install Pillow`

### Profile not created automatically
- Check if signals are imported in `apps.py`
- Verify `ready()` method is called

### Template not found
- Verify TEMPLATES 'DIRS' setting includes templates directory
- Check template files are in correct location

### Static files not loading
- Run: `python manage.py collectstatic` (for production)
- Verify STATIC_URL and STATICFILES_DIRS settings

---

## ✅ PRODUCTION CHECKLIST

Before deploying to production:

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Configure production database
- [ ] Set up proper email backend
- [ ] Configure file storage (S3, etc.)
- [ ] Run `collectstatic`
- [ ] Set up HTTPS
- [ ] Configure proper logging
- [ ] Test all functionality on staging environment

---

## 📚 NEXT STEPS

1. Complete the migration process
2. Test all functionality
3. Customize styling if needed
4. Add password reset functionality (optional)
5. Add email verification (optional)
6. Integrate with other apps in your project
7. Add social authentication (optional)

---

**Created for Art Tourism Django Project**
**Date:** March 27, 2026
**Accounts App Version:** 1.0

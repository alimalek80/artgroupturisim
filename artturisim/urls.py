"""
URL configuration for artturisim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

# Non-translated URLs (admin, media, language switching)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor file uploads
]

# Translated URLs (will be prefixed with language code: /en/, /tr/, /ru/)
urlpatterns += i18n_patterns(
    path('accounts/', include('accounts.urls')),
    path('tours/', include('tours.urls')),
    path('blog/', include('blog.urls')),
    path('', include('core.urls')),
    prefix_default_language=False,  # Don't prefix default language (English)
)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

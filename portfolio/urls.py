"""
Main URL configuration for the Portfolio project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Core app handles all frontend routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

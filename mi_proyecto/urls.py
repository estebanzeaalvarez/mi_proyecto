# mi_proyecto/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # Incluye las URLs de la aplicación base
    path('api/', include('base.api.urls')),  # Incluye las URLs de la aplicación api dentro de base
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('dj_rest_auth.urls')),  # Endpoints de autenticação padrão
    path('users/registration/', include('dj_rest_auth.registration.urls')),  # Endpoints de registro
    path('users/', include('users.urls')),  # URLs específicas da app 'users'
    path('', include('investments.urls')),  # URLs específicas da app 'investments'
]

# Servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

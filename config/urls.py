from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.publico.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('cursos/', include('apps.formacion.urls')),
    
    # --- VERIFICA QUE ESTA LÍNEA ESTÉ PRESENTE ---
    path('comunidad/', include('apps.comunidad.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    
    # Rutas de Gestión de Tienda
    path('producto/nuevo/', views.crear_producto, name='crear_producto'),
    path('producto/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    
    # <--- AQUÍ ES DONDE DEBE ESTAR:
    path('categoria/nueva/', views.crear_categoria, name='crear_categoria'),
]
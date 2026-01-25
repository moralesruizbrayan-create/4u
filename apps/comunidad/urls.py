from django.urls import path
from . import views

urlpatterns = [
    path('', views.foro, name='foro'),
    path('nuevo/', views.crear_tema, name='crear_tema'),
    # Nueva ruta para ver el detalle y comentar
    path('tema/<int:tema_id>/', views.ver_tema, name='ver_tema'),
]
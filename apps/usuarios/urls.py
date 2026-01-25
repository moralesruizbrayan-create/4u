from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rutas de Acceso
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Rutas del Panel
    path('dashboard/', views.dashboard, name='dashboard'),
    path('gestion-interna/', views.panel_admin, name='panel_admin'),
]
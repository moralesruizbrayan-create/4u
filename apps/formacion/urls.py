from django.urls import path
from . import views

urlpatterns = [
    # Vista Estudiante
    path('leccion/<int:leccion_id>/', views.ver_leccion, name='ver_leccion'),

    # Vistas Gestión Admin (Solo cursos y exámenes)
    path('crear-modulo/', views.crear_modulo, name='crear_modulo'),
    path('crear-leccion/<int:modulo_id>/', views.crear_leccion, name='crear_leccion'),
    
    # Exámenes
    path('modulo/examen/agregar/<int:modulo_id>/', views.agregar_pregunta_examen, name='agregar_pregunta_examen'),
    path('modulo/examen/realizar/<int:modulo_id>/', views.realizar_examen, name='realizar_examen'),
    path('leccion/test/agregar/<int:leccion_id>/', views.agregar_pregunta_test, name='agregar_pregunta_test'),

]
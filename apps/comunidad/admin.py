from django.contrib import admin
from .models import Tema, Comentario

# Registramos los modelos para que aparezcan en el panel de administración
@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion')
    search_fields = ('titulo', 'contenido')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'tema', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
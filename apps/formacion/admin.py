from django.contrib import admin
from .models import Modulo, LeccionVideo, PreguntaTest, ProgresoUsuario

class PreguntaInline(admin.StackedInline):
    model = PreguntaTest
    extra = 1

class LeccionAdmin(admin.ModelAdmin):
    inlines = [PreguntaInline] # Esto permite crear preguntas dentro de la lección

admin.site.register(Modulo)
admin.site.register(LeccionVideo, LeccionAdmin)
admin.site.register(ProgresoUsuario)
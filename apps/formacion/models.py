from django.db import models
from django.contrib.auth.models import User

class Modulo(models.Model):
    titulo = models.CharField(max_length=200)
    # Agregamos este campo que faltaba:
    descripcion = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.titulo

class LeccionVideo(models.Model):
    modulo = models.ForeignKey(Modulo, related_name='lecciones', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    video_archivo = models.FileField(upload_to='videos/') # Asegúrate de tener instalado pillow si usas ImageField, pero FileField es mejor para video
    descripcion = models.TextField(blank=True, null=True)
    puntos_recompensa = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.titulo} ({self.modulo.titulo})"

class ProgresoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    leccion = models.ForeignKey(LeccionVideo, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    puntaje_obtenido = models.IntegerField(default=0)
    fecha_completado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.leccion.titulo}"
    
class PreguntaTest(models.Model):
    leccion = models.ForeignKey(LeccionVideo, related_name='preguntas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=300)
    opcion_a = models.CharField(max_length=100)
    opcion_b = models.CharField(max_length=100)
    opcion_c = models.CharField(max_length=100)
    correcta = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C')])

    def __str__(self):
        return self.texto
    
class PreguntaExamen(models.Model):
    modulo = models.ForeignKey(Modulo, related_name='preguntas_examen', on_delete=models.CASCADE)
    texto = models.CharField(max_length=300, verbose_name="Pregunta")
    opcion_a = models.CharField(max_length=100)
    opcion_b = models.CharField(max_length=100)
    opcion_c = models.CharField(max_length=100)
    correcta = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C')])

    def __str__(self):
        return f"Examen {self.modulo.titulo}: {self.texto}"
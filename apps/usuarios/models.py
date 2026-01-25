from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    NIVELES = [
        ('Novato', 'Novato'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
        ('Maestro', 'Maestro'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntos = models.PositiveIntegerField(default=0)
    nivel = models.CharField(max_length=20, choices=NIVELES, default='Novato')
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.nivel}"

# Señal: Crea automáticamente un Perfil cuando se crea un User
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
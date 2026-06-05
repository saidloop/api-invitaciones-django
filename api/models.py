import uuid
from django.db import models

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    fecha_evento = models.DateTimeField()
    activo = models.BooleanField(default=True)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    url_mapa = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Invitado(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('rechazado', 'Rechazado'),
    )
    
    # Este UUID será el token único en la URL de WhatsApp
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='invitados')
    nombre = models.CharField(max_length=200)
    estado_asistencia = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    pases = models.IntegerField(default=1) # Por si invitas a parejas o familias

    def __str__(self):
        return f"{self.nombre} - {self.evento.nombre}"

class RegistroEntrada(models.Model):
    invitado = models.ForeignKey(Invitado, on_delete=models.CASCADE)
    hora_llegada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrada de {self.invitado.nombre}"
# Create your models here.

import urllib.parse
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
    telefono = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: 573001234567 (Código de país + número sin el +)")
    
    def __str__(self):
        return f"{self.nombre} - {self.evento.nombre}"

    def enlace_whatsapp(self):
        if not self.id:
            return ""
            
        # 👉 SOLUCIÓN: Definir la variable enlace_vercel antes de usarla
        enlace_vercel = f"https://invitaciones-v.vercel.app/evento/{self.evento.slug}/{self.id}"
            
        mensaje = (
            f"¡Hola {self.nombre}! 🌸 \n\n"
            f"¡Nos emociona muchísimo invitarte a {self.evento.nombre}! 🌸 Tu presencia hará que este día sea aún más especial.\n\n"
            f"Haz clic en el enlace para ver la invitación completa y confirmar tu asistencia; Te esperamos!🩷\n\n"
            f"{enlace_vercel}"
        )
        
        mensaje_codificado = urllib.parse.quote(mensaje.encode('utf-8'))
        
        # Si el invitado tiene teléfono asignado, se envía directo a su número
        if self.telefono:
            numero_limpio = str(self.telefono).replace("+", "").replace(" ", "")
            return f"https://wa.me/{numero_limpio}?text={mensaje_codificado}"
        
        # Si no tiene teléfono, abre la lista de contactos general como antes
        return f"https://wa.me/?text={mensaje_codificado}"

class RegistroEntrada(models.Model):
    invitado = models.ForeignKey(Invitado, on_delete=models.CASCADE)
    hora_llegada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrada de {self.invitado.nombre}"
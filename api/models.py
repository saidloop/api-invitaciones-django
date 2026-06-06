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
        enlace_vercel = f"https://invitaciones-v.vercel.app/{self.evento.slug}/{self.id}"
            
        # 1. Separamos el texto en bloques (sin emojis)
        txt_1 = f"¡Hola {self.nombre}! "
        txt_2 = f"\n\n¡Nos emociona muchísimo invitarte a {self.evento.nombre}! "
        txt_3 = f" Tu presencia hará que este día sea aún más especial.\n\n"
        txt_4 = f"Haz clic en el enlace para ver la invitación completa y confirmar tu asistencia; Te esperamos! "
        txt_5 = f"\n\n{enlace_vercel}"
        
        # 2. Convertimos el texto normal a formato de enlace
        url_1 = urllib.parse.quote(txt_1)
        url_2 = urllib.parse.quote(txt_2)
        url_3 = urllib.parse.quote(txt_3)
        url_4 = urllib.parse.quote(txt_4)
        url_5 = urllib.parse.quote(txt_5)
        
        # 3. Definimos los emojis exactos en lenguaje URL
        flor = "%F0%9F%8C%B8"  # Código web para 🌸
        brillo = "%E2%9C%A8"   # Código web para ✨
        
        # 4. Unimos todo como si fueran piezas de Lego
        mensaje_final = f"{url_1}{flor}{url_2}{flor}{url_3}{url_4}{brillo}{url_5}"
        
        # Si el invitado tiene teléfono asignado, se envía directo a su número
        if self.telefono:
            numero_limpio = str(self.telefono).replace("+", "").replace(" ", "")
            return f"https://wa.me/{numero_limpio}?text={mensaje_final}"
        
        # Si no tiene teléfono, abre la lista de contactos general como antes
        return f"https://wa.me/?text={mensaje_final}"

class RegistroEntrada(models.Model):
    invitado = models.ForeignKey(Invitado, on_delete=models.CASCADE)
    hora_llegada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrada de {self.invitado.nombre}"
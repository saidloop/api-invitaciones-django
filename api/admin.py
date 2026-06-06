from django.contrib import admin
from django.utils.html import format_html # Requerido para renderizar el botón verde en HTML
from .models import Evento, Invitado, RegistroEntrada

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_evento', 'ubicacion', 'activo')
    prepopulated_fields = {'slug': ('nombre',)} 


@admin.register(Invitado)
class InvitadoAdmin(admin.ModelAdmin):
    # Añadimos 'boton_whatsapp' al final de las columnas de la lista
    list_display = ('nombre', 'evento', 'estado_asistencia', 'pases', 'id', 'boton_whatsapp')
    list_filter = ('evento', 'estado_asistencia')
    search_fields = ('nombre',)
    
    # Esto permite que el botón y el ID (UUID) se muestren también al entrar a editar un invitado
    readonly_fields = ('id', 'boton_whatsapp',)

    # Definimos la función que dibuja el botón usando el enlace del modelo
    def boton_whatsapp(self, obj):
        url = obj.enlace_whatsapp()
        if url:
            return format_html(
                '<a href="{}" target="_blank" style="background-color: #25D366; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-weight: bold; display: inline-block;">📲 Compartir</a>', 
                url
            )
        return "Guarda para generar"
    
    # Nombre que aparecerá en la cabecera de la columna
    boton_whatsapp.short_description = 'Enviar WhatsApp'


admin.site.register(RegistroEntrada)
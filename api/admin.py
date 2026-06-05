from django.contrib import admin
from .models import Evento, Invitado, RegistroEntrada

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_evento', 'ubicacion', 'activo')
    prepopulated_fields = {'slug': ('nombre',)} 

@admin.register(Invitado)
class InvitadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'evento', 'estado_asistencia', 'pases', 'id')
    list_filter = ('evento', 'estado_asistencia')
    search_fields = ('nombre',)

admin.site.register(RegistroEntrada)
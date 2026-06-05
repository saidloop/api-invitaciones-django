from rest_framework import serializers
from .models import Evento, Invitado

class EventoSerializer(serializers.ModelSerializer):
    # 1. Declaramos el nuevo campo personalizado
    fecha_formateada = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        # 2. Añadimos 'fecha_formateada' a la lista de fields
        fields = ['nombre', 'fecha_evento', 'fecha_formateada', 'ubicacion', 'url_mapa']

    # 3. Creamos la función que procesa y formatea la fecha
    def get_fecha_formateada(self, obj):
        if not obj.fecha_evento:
            return ""
            
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        
        fecha = obj.fecha_evento
        
        dia_semana = dias[fecha.weekday()]
        dia = fecha.day
        mes = meses[fecha.month - 1]
        anio = str(fecha.year) # Obtiene "2026" en lugar de "26"
        
        # Formato de hora 12h (am/pm)
        hora_24 = fecha.hour
        minutos = fecha.minute
        ampm = 'pm' if hora_24 >= 12 else 'am'
        hora_12 = hora_24 % 12
        hora_12 = 12 if hora_12 == 0 else hora_12
            
        # Construye: "sábado 7 de junio del 26 8:00 pm"
        return f"{dia_semana} {dia} de {mes} del {anio} {hora_12}:{minutos:02d} {ampm}"

class InvitadoSerializer(serializers.ModelSerializer):
    evento = EventoSerializer(read_only=True) 

    class Meta:
        model = Invitado
        fields = ['id', 'nombre', 'estado_asistencia', 'pases', 'evento']
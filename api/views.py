from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Invitado
from .serializers import InvitadoSerializer

class DetallesInvitacionView(generics.RetrieveAPIView):
    queryset = Invitado.objects.all()
    serializer_class = InvitadoSerializer
    lookup_field = 'id' 
    

class ResponderAsistenciaView(APIView):
    def patch(self, request, id):
        # Buscamos al invitado por su UUID
        invitado = get_object_or_404(Invitado, id=id)
        
        # Extraemos el dato que nos enviará Astro en el "body" de la petición
        nuevo_estado = request.data.get('estado_asistencia')
        
        # Validamos por seguridad que no nos envíen textos extraños
        if nuevo_estado in ['confirmado', 'rechazado']:
            invitado.estado_asistencia = nuevo_estado
            invitado.save() # Guardamos el cambio en la base de datos
            
            return Response(
                {"mensaje": f"¡Éxito! El estado cambió a {nuevo_estado}"}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Estado no válido. Usa 'confirmado' o 'rechazado'."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
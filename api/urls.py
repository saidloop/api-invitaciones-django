from django.urls import path
from .views import DetallesInvitacionView, ResponderAsistenciaView

urlpatterns = [
    path('invitacion/<uuid:id>/', DetallesInvitacionView.as_view(), name='detalles-invitacion'),
    path('invitacion/<uuid:id>/responder/', ResponderAsistenciaView.as_view(), name='responder-asistencia'),
]
from django.contrib import admin
from .models import Equipo, Torneo, Jugador, EstadisticasJugador, EstadisticasEquipo, Posicion

admin.site.register(Equipo)
admin.site.register(Torneo)
admin.site.register(Jugador)
admin.site.register(EstadisticasJugador)
admin.site.register(EstadisticasEquipo)
admin.site.register(Posicion)

from django.urls import path
from . import views
from .grafico_equipo import ajax_radar_equipo
from .estadistica_jugador import *
from . import comparacion
from .statsequipo import stats_equipos  # ← IMPORTAR DIRECTAMENTE



urlpatterns = [
    path('', views.home, name='home'), 
    path('grafico/', views.grafico, name='grafico'),
    path('menu/', views.menu, name='menu'),
    path('ligas/', views.ligas, name='ligas'),
    path('stats_equipos/', stats_equipos, name='stats_equipos'),  # ← USAR DIRECTAMENTE
    path('stats_jugadores/', views.stats_jugadores, name='stats_jugadores'),
    path('equipo/', views.equipo, name='equipo'),
    path('equipo/<int:equipo_id>/', views.equipo_detalle, name='equipo_detalle'),
    path('equipo/<int:equipo_id>/estadistica/<str:estadistica>/', views.grafico_equipo, name='grafico_equipo'),
    path('equipo/<int:equipo_id>/<str:stat_name>/', views.grafico_equipo, name='grafico_equipo'),
    path('jugador/<int:jugador_id>/', views.jugador_detalle, name='jugador_detalle'),
    path('jugador/<int:jugador_id>/grafico/<str:estadistica>/', views.grafico_jugador_view,  name='grafico_jugador'),
    path('comparacion/', views.comparacion, name='comparacion'),
    path('recomendacion/', views.recomendacion, name='recomendacion'),  # ← CAMBIAR name A 'recomendacion'
    path('ajax/recomendar-jugadores/', views.ajax_recomendar_jugadores, name='ajax_recomendar_jugadores'),
    path('ajax/grafico-dispersion/', views.ajax_grafico_dispersion, name='ajax_grafico_dispersion'),
    path('ajax/analisis-correlacion/', views.ajax_analisis_correlacion, name='ajax_analisis_correlacion'),
    path('ajax/radar-equipo/', ajax_radar_equipo, name='ajax_radar_equipo'),
    path('ajax/boxplot-estadistica/', views.ajax_boxplot_estadistica, name='ajax_boxplot_estadistica'),
    path('ajax/radar-jugador/', ajax_radar_jugador, name='ajax_radar_jugador'),
    path('ajax/ranking-jugadores/', ajax_ranking_jugadores, name='ajax_ranking_jugadores'),
    path('ajax/evolucion-jugador/', ajax_evolucion_jugador, name='ajax_evolucion_jugador'),
    path('ajax/percentil-jugador/', ajax_percentil_jugador, name='ajax_percentil_jugador'),
    path('ajax/grafico-dispersion-jugador/', ajax_grafico_dispersion_jugador, name='ajax_grafico_dispersion_jugador'),
    path('api/jugador/<int:jugador_id>/posiciones/', api_jugador_posiciones, name='api_jugador_posiciones'),
    path('ajax/boxplot-jugador/', ajax_boxplot_jugador, name='ajax_boxplot_jugador'),
]

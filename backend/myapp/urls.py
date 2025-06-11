from django.urls import path
from . import views
from .grafico_equipo import ajax_radar_equipo



urlpatterns = [
    path('', views.home, name='home'), 
    path('grafico/', views.grafico, name='grafico'),
    path('menu/', views.menu, name='menu'),
    path('ligas/', views.ligas, name='ligas'),
    path('stats_equipos/', views.stats_equipos, name='stats_equipos'),
    path('stats_jugadores/', views.stats_jugadores, name='stats_jugadores'),
    path('equipo/', views.equipo, name='equipo'),
    path('equipo/<int:equipo_id>/', views.equipo_detalle, name='equipo_detalle'),
    path('equipo/<int:equipo_id>/estadistica/<str:estadistica>/', views.grafico_equipo, name='grafico_equipo'),
    path('equipo/<int:equipo_id>/<str:stat_name>/', views.grafico_equipo, name='grafico_equipo'),
    path('jugador/<int:jugador_id>/', views.jugador_detalle, name='jugador_detalle'),
   path('jugador/<int:jugador_id>/grafico/<str:estadistica>/', views.grafico_jugador_view,  name='grafico_jugador'),



    path('ajax/grafico-dispersion/', views.ajax_grafico_dispersion, name='ajax_grafico_dispersion'),
    path('ajax/analisis-correlacion/', views.ajax_analisis_correlacion, name='ajax_analisis_correlacion'),
    path('ajax/radar-equipo/', ajax_radar_equipo, name='ajax_radar_equipo'),
    path('ajax/boxplot-estadistica/', views.ajax_boxplot_estadistica, name='ajax_boxplot_estadistica'),


]

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




    path('ajax/grafico-dispersion/', views.ajax_grafico_dispersion, name='ajax_grafico_dispersion'),
    path('ajax/analisis-correlacion/', views.ajax_analisis_correlacion, name='ajax_analisis_correlacion'),
    path('ajax/radar-equipo/', ajax_radar_equipo, name='ajax_radar_equipo'),

]

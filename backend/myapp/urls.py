from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('grafico/', views.grafico, name='grafico'),
    path('menu/', views.menu, name='menu'),
    path('ligas/', views.ligas, name='ligas'),
    path('stats_equipos/', views.stats_equipos, name='stats_equipos'),
    path('stats_jugadores/', views.stats_jugadores, name='stats_jugadores'),
]

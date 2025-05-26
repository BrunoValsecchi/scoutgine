from django.urls import path
from . import views
from . import ligas

urlpatterns = [
    path('', views.home, name='home'), 
    path('grafico/', views.grafico, name='grafico'),
    path('menu/', views.menu, name='menu'),
    path('ligas/', views.ligas, name='ligas'),
    path('api/ligas/', ligas.ligas_api, name='ligas_api'),
]

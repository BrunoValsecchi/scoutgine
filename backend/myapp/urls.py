from django.urls import path
from . import views  # o from .views import home
from .views import grafico

urlpatterns = [
    path('', views.home, name='home'), 
    path('grafico/', views.grafico, name='grafico'),
    path('menu/', views.menu, name='menu'),

]

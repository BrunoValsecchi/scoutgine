from django.urls import path
from . import views  # o from .views import home

urlpatterns = [
    path('', views.home, name='home'),  
]

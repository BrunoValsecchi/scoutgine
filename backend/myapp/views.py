from django.shortcuts import render
import datetime
import pandas as pd
import requests
from pyecharts.charts import Bar, Radar  
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Page
from pyecharts.globals import ThemeType
from django.http import JsonResponse
from myapp.grafico import grafico
from myapp.menu import menu
from myapp.ligas import ligas
from .models import Posicion

import json
import numpy as np
import os
from django.conf import settings

COLORES_NEON = [
    '#00ffff',  
    '#ff00ff',  
    '#00ff00',  
    '#ffff00',  
    '#ff0000',  
    '#0000ff'   
]

def home(request):
    
    

    return render(request, "index.html")

def posiciones_api(request):
    torneos = {
        'apertura_a': Posicion.objects.filter(torneo_id=34),
        'apertura_b': Posicion.objects.filter(torneo_id=49),
        'clausura_a': Posicion.objects.filter(torneo_id=4),
        'clausura_b': Posicion.objects.filter(torneo_id=19)
    }
    
    data = {key: list(torneo.values()) for key, torneo in torneos.items()}
    return JsonResponse(data)
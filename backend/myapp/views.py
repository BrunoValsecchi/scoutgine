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
from .models import Posicion

import json
import numpy as np
import os
from django.conf import settings


def home(request):
    return render(request, "index.html")

def grafico(request):
    # Tu función de gráfico aquí
    return render(request, "grafico.html")

def menu(request):
    # Tu función de menú aquí
    return render(request, "menu.html")

def equipo(request):
    """FUNCIÓN CORREGIDA - Ahora SÍ llama a equipo.py"""
    print("🔥 VIEWS.PY - FUNCIÓN EQUIPO LLAMADA")
    print("📍 Importando desde equipo.py...")
    
    try:
        # Importar aquí para evitar imports circulares
        from .equipo import equipo as equipo_func
        print("✅ Import exitoso")
        
        result = equipo_func(request)
        print("✅ Función equipo_func ejecutada")
        return result
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return render(request, "equipo.html", {'error': f'Import error: {e}'})
    except Exception as e:
        print(f"❌ Error general: {e}")
        return render(request, "equipo.html", {'error': f'General error: {e}'})

def ligas(request):
    # Importar aquí para evitar imports circulares
    from .ligas import ligas as ligas_func
    return ligas_func(request)

def stats_equipos(request):
    # Importar aquí para evitar imports circulares
    from .statsequipo import stats_equipos as stats_equipos_func
    return stats_equipos_func(request)

def stats_jugadores(request):
    # Importar aquí para evitar imports circulares
    from .statsjugadores import stats_jugadores as stats_jugadores_func
    return stats_jugadores_func(request)

def posiciones_api(request):
    torneos = {
        'apertura_a': Posicion.objects.filter(torneo_id=34),
        'apertura_b': Posicion.objects.filter(torneo_id=49),
        'clausura_a': Posicion.objects.filter(torneo_id=4),
        'clausura_b': Posicion.objects.filter(torneo_id=19)
    }
    
    data = {key: list(torneo.values()) for key, torneo in torneos.items()}
    return JsonResponse(data)


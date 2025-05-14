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

def menu(request):
    
    

    return render(request, "menu.html")




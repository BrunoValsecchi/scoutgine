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

def grafico(request):
    
    #sofascore = sfc.Sofascore()

    ruta_json_delanteros = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'data', 'delanteros.json')
    with open(ruta_json_delanteros, 'r', encoding='utf-8') as archivo:
        stats_player_delanteros = json.load(archivo)

    ruta_json_defensores = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'data', 'defensores.json')
    print(f"Buscando archivo en: {ruta_json_defensores}")  
    
    if not os.path.exists(ruta_json_defensores):
        print(f"El archivo {ruta_json_defensores} no existe")  
        os.makedirs(os.path.dirname(ruta_json_defensores), exist_ok=True)
      
        
        with open(ruta_json_defensores, 'w', encoding='utf-8') as archivo:
            json.dump(datos_muestra, archivo, ensure_ascii=False, indent=4)
    
    with open(ruta_json_defensores, 'r', encoding='utf-8') as archivo:
        stats_player_defensores = json.load(archivo)

    def graficos_liga(df, neon=True):
        jugadores = df['player'].tolist()
        stats_completas = [col for col in df.columns if col != 'player']
        bar = Bar(init_opts=opts.InitOpts(bg_color="rgba(10, 10, 10, 0.8)" if neon else None))
        bar.add_xaxis(jugadores)
        
        for idx, stat in enumerate(stats_completas):
            if stat in df.columns:
                valores = df[stat].fillna(0).tolist()
                color_idx = idx % len(COLORES_NEON)
                
                if neon:
                    bar.add_yaxis(
                        stat.capitalize(), 
                        valores,
                        itemstyle_opts=opts.ItemStyleOpts(
                            color=COLORES_NEON[color_idx],
                            border_color=COLORES_NEON[color_idx],
                            border_width=1
                        )
                    )
                else:
                    bar.add_yaxis(stat.capitalize(), valores)
        
        if neon:
            bar.set_global_opts(
                title_opts=opts.TitleOpts(
                    title='Estadísticas',
                    title_textstyle_opts=opts.TextStyleOpts(
                        color="#00ffff",
                        font_weight="bold",
                        font_family="Orbitron"
                    )
                ),
                xaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(rotate=45, color="#ffffff"),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color="#00ffff", width=2)
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    name="Valor",
                    axislabel_opts=opts.LabelOpts(color="#ffffff"),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color="#00ffff", width=2)
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color="rgba(0, 255, 255, 0.1)", type_="dashed")
                    )
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    background_color="rgba(0, 0, 0, 0.7)",
                    border_color="#00ffff",
                    textstyle_opts=opts.TextStyleOpts(color="#ffffff")
                ),
                legend_opts=opts.LegendOpts(
                    textstyle_opts=opts.TextStyleOpts(color="#ffffff")
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(
                    )
                ]
            )
        else:
            bar.set_global_opts(
                title_opts=opts.TitleOpts(title='Estadísticas'),
                xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
                yaxis_opts=opts.AxisOpts(name="Valor")
            )
        
        return bar.render_embed()

    df = pd.DataFrame(stats_player_delanteros)
    grafico = graficos_liga(df, neon=True)

    def crear_tabla_pyecharts(df, neon=True):
        tabla = Table()

        if 'minutesPlayed' in df.columns:
            df = df[df['minutesPlayed'] > 200]

        columnas = list(df.columns)
        if 'player' in columnas:
            columnas.remove('player')
            columnas = ['player'] + columnas
            df = df[columnas]
        
        headers = list(df.columns)
        rows = df.head(10).astype(str).values.tolist()

        tabla.add(headers, rows)
        
        if neon:
            tabla.set_global_opts(
                title_opts=ComponentTitleOpts(
                    title="Estadísticas de Jugadores",
                    title_style={"color": "#00ffff", "font-family": "Orbitron", "text-shadow": "0 0 10px rgba(0, 255, 255, 0.7)"}
                )
            )
        else:
            tabla.set_global_opts(
                title_opts=ComponentTitleOpts(title="Estadísticas de Jugadores")
            )

        page = Page(layout=Page.SimplePageLayout)
        page.add(tabla)
        return tabla.render_embed()

    tabla = crear_tabla_pyecharts(df, neon=True)

    df2 = pd.DataFrame(stats_player_delanteros)
    df2.fillna(0, inplace=True)
    df2 = df2.astype(str)

    tabla_json = json.dumps(df.to_dict(orient="records"))
    columnas_json = json.dumps([
        {"headerName": col.capitalize(), "field": col, "sortable": True, "filter": True} 
        for col in df2.columns
    ])

    def calcular_percentiles_delanteros(df_delanteros):
        columna_delanteros = [
            'goals', 'expectedGoals', 'shotsOnTarget', 'totalShots',
            'goalConversionPercentage', 'assists', 'keyPasses', 'bigChancesCreated',
            'bigChancesMissed', 'successfulDribbles', 'successfulDribblesPercentage',
            'accurateFinalThirdPasses', 'passToAssist', 'hitWoodwork', 'offsides'
        ]
        resultados_delanteros = []
        for _, jugador in df_delanteros.iterrows():
            percentile_delantero = {'player': jugador['player']}
            for columna in columna_delanteros:
                if columna in df_delanteros.columns:
                    valor_jugador = jugador[columna]
                    percentil = (df_delanteros[columna] <= valor_jugador).mean() * 100
                    percentil = round(percentil)
                    percentile_delantero[columna] = percentil
            resultados_delanteros.append(percentile_delantero)
        return pd.DataFrame(resultados_delanteros)

    df_delanteros = pd.DataFrame(stats_player_delanteros)
    percentiles_delanteros = calcular_percentiles_delanteros(df_delanteros)

    def grafico_percentiles_delanteros(df_percentiles, neon=True):
        df_percentiles = df_percentiles.head(10)
        jugadores = df_percentiles['player'].tolist()
        
        init_opts = opts.InitOpts(bg_color="rgba(10, 10, 10, 0.8)") if neon else None
        bar = Bar(init_opts=init_opts)
        
        bar.add_xaxis(jugadores)
        columnas_estadisticas = [col for col in df_percentiles.columns if col != 'player']
        
        for idx, stat in enumerate(columnas_estadisticas):
            valores = df_percentiles[stat].fillna(0).tolist()
            color_idx = idx % len(COLORES_NEON)
            
            if neon:
                bar.add_yaxis(
                    stat.capitalize(), 
                    valores,
                    itemstyle_opts=opts.ItemStyleOpts(
                        color=COLORES_NEON[color_idx],
                        border_color=COLORES_NEON[color_idx],
                        border_width=1
                    )
                )
            else:
                bar.add_yaxis(stat.capitalize(), valores)
        
        if neon:
            bar.set_global_opts(
                title_opts=opts.TitleOpts(
                    title='Percentiles de Delanteros (Top 10)',
                    title_textstyle_opts=opts.TextStyleOpts(
                        color="#00ffff",
                        font_weight="bold",
                        font_family="Orbitron"
                    )
                ),
                xaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(rotate=45, color="#ffffff"),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color="#00ffff", width=2)
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    name="Percentil", 
                    min_=0, 
                    max_=100,
                    axislabel_opts=opts.LabelOpts(color="#ffffff"),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color="#00ffff", width=2)
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color="rgba(0, 255, 255, 0.1)", type_="dashed")
                    )
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    background_color="rgba(0, 0, 0, 0.7)",
                    border_color="#00ffff",
                    textstyle_opts=opts.TextStyleOpts(color="#ffffff")
                ),
                legend_opts=opts.LegendOpts(
                    textstyle_opts=opts.TextStyleOpts(color="#ffffff")
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(
                       
                    )
                ]
            )
        else:
            bar.set_global_opts(
                title_opts=opts.TitleOpts(title='Percentiles de Delanteros (Top 10)'),
                xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
                yaxis_opts=opts.AxisOpts(name="Percentil", min_=0, max_=100),
                datazoom_opts=[opts.DataZoomOpts()]
            )
        
        return bar.render_embed()

    grafico_percentiles = grafico_percentiles_delanteros(percentiles_delanteros, neon=True)

    datos_radar = []
    for jugador in stats_player_delanteros:
        datos_jugador = {
            'player': jugador['player'],
            'percentiles': {k: v for k, v in jugador.items() if k != 'player'}
        }
        datos_radar.append(datos_jugador)

    df_delanteros = pd.DataFrame(stats_player_delanteros)

    jugadores_disponibles = df_delanteros['player'].tolist()

    datos_radar = []
    for _, jugador in percentiles_delanteros.iterrows():
        datos_jugador = {
            'player': jugador['player'],
            'percentiles': jugador.drop('player').to_dict()
        }
        datos_radar.append(datos_jugador)

    jugador1 = request.GET.get('jugador1')
    jugador2 = request.GET.get('jugador2')

    if not jugador1 or not jugador2:
        jugador1 = datos_radar[0]['player'] if datos_radar else None
        jugador2 = datos_radar[1]['player'] if len(datos_radar) > 1 else None

    radar = Radar(init_opts=opts.InitOpts(bg_color="rgba(10, 10, 10, 0.8)"))
    
    if datos_radar:
        schema = [{"name": stat, "max": 100} for stat in datos_radar[0]['percentiles'].keys()]

        radar.add_schema(
            schema=schema,
            shape="circle",
            center=["50%", "50%"],
            radius="70%",
            textstyle_opts=opts.TextStyleOpts(color="#ffffff"),
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, 
                areastyle_opts=opts.AreaStyleOpts(opacity=0.1, color="rgba(0, 255, 255, 0.1)")
            ),
            axisline_opt=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#00ffff", width=2)
            ),
            splitline_opt=opts.SplitLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#00ffff", width=1, type_="dashed")
            ),
        )

        jugador1_data = next((j for j in datos_radar if j['player'] == jugador1), None)
        jugador2_data = next((j for j in datos_radar if j['player'] == jugador2), None)

        if jugador1_data and jugador2_data:
            radar.add(
                jugador1,
                [list(jugador1_data['percentiles'].values())],
                color="#00ffff",  
                symbol="circle",
                linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
            )
            radar.add(
                jugador2,
                [list(jugador2_data['percentiles'].values())],
                color="#ff00ff",  
                symbol="circle",
                linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
            )

        radar.set_global_opts(
            title_opts=opts.TitleOpts(
                title="Comparación de Percentiles",
                title_textstyle_opts=opts.TextStyleOpts(
                    color="#00ffff",
                    font_weight="bold",
                    font_family="Orbitron"
                )
            ),
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(color="#ffffff")
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                background_color="rgba(0, 0, 0, 0.7)",
                border_color="#00ffff",
                textstyle_opts=opts.TextStyleOpts(color="#ffffff")
            ),
        )

    grafico_radar = radar.render_embed()

    jugadores_disponibles = [j['player'] for j in datos_radar]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'grafico_radar': grafico_radar})

    info_partido = {
        "torneo": "La Liga",
        "ronda": "Jornada 10",
        "fecha": "28/04/2025",
        "equipo_local": "FC Barcelona",
        "equipo_visitante": "Real Madrid",
        "marcador": "2-1",
        "estadio": "Camp Nou",
        "ciudad": "Barcelona",
        "arbitro": "Mateu Lahoz"
    }
    print(f"Ruta de delanteros: {ruta_json_delanteros}")
    print(f"Ruta de defensores: {ruta_json_defensores}")


    context = {
        'stats_delanteros': pd.DataFrame(stats_player_delanteros).to_dict(orient='records'),
        'stats_defensores': pd.DataFrame(stats_player_defensores).to_dict(orient='records'),
        'player_url': 'https://www.sofascore.com/es/jugador/lionel-messi/12994',
        'jugadores_disponibles': jugadores_disponibles,
        'jugador1_seleccionado': jugador1,
        'jugador2_seleccionado': jugador2,
        'grafico_radar': grafico_radar,
        'grafico': grafico,
        'tabla': tabla,
        'grafico_percentiles': grafico_percentiles,
        'tabla_json': tabla_json,
        'columnas_json': columnas_json,
        'info': info_partido, 
        'estilos_neon': True,  
    }

    return render(request, "grafico.html", context)


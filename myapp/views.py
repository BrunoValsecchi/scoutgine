from django.shortcuts import render
import ScraperFC as sfc
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

# Paleta de colores neón
COLORES_NEON = [
    '#00ffff',  # Cian
    '#ff00ff',  # Magenta
    '#00ff00',  # Verde
    '#ffff00',  # Amarillo
    '#ff0000',  # Rojo
    '#0000ff'   # Azul
]

def home(request):
    
    sofascore = sfc.Sofascore()

    ruta_json_delanteros = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'data', 'delanteros.json')
    with open(ruta_json_delanteros, 'r', encoding='utf-8') as archivo:
        stats_player_delanteros = json.load(archivo)

    # ⚡ AHORA CARGAMOS DEFENSORES DESDE EL JSON
    ruta_json_defensores = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'data', 'defensores.json')
    print(f"Buscando archivo en: {ruta_json_defensores}")  # Debug
    
    # Comprobar si el archivo existe
    if not os.path.exists(ruta_json_defensores):
        print(f"El archivo {ruta_json_defensores} no existe")  # Debug
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(ruta_json_defensores), exist_ok=True)
        
        # Crear un archivo JSON vacío con datos de muestra si no existe
        datos_muestra = [
            {"player": "Defensor 1", "tackling": 85, "marking": 80, "heading": 75},
            {"player": "Defensor 2", "tackling": 70, "marking": 90, "heading": 65}
        ]
        
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

    # Usamos los datos de delanteros
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

    # Definimos los percentiles para los delanteros
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
        
        # Usar estilo neón para el gráfico
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

    # Preparación para radar
    datos_radar = []
    for jugador in stats_player_delanteros:
        datos_jugador = {
            'player': jugador['player'],
            'percentiles': {k: v for k, v in jugador.items() if k != 'player'}
        }
        datos_radar.append(datos_jugador)

    # Obtener los jugadores seleccionados desde los parámetros GET
    df_delanteros = pd.DataFrame(stats_player_delanteros)

    # Obtener los jugadores disponibles
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

    # Configuración del gráfico radar con estilo neón
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
                color="#00ffff",  # Cian neón
                symbol="circle",
                linestyle_opts=opts.LineStyleOpts(width=2),
                areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
            )
            radar.add(
                jugador2,
                [list(jugador2_data['percentiles'].values())],
                color="#ff00ff",  # Magenta neón
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

    # Si el request vino por fetch/ajax, solo devolvemos el HTML del gráfico
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'grafico_radar': grafico_radar})

    # Datos de información del partido (ejemplo para estética neón)
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
        'info': info_partido,  # Añadido para la estética neón
        'estilos_neon': True,  # Flag para activar estilos neón en la plantilla
    }

    return render(request, "index.html", context)



# from django.shortcuts import render
# import ScraperFC as sfc
# import datetime
# import pandas as pd
# import requests
# from pyecharts.charts import Bar, Radar  
# from pyecharts import options as opts
# from pyecharts.components import Table
# from pyecharts.options import ComponentTitleOpts
# from pyecharts.charts import Page
# from pyecharts.globals import ThemeType
# import json
# import numpy as np



# #python manage.py runserver 0.0.0.0:8000

# #python manage.py runserver 0.0.0.0:8000

# def home(request):
#     sofascore = sfc.Sofascore()
#     transfermarkt=sfc.Transfermarkt()

#     #def crear_grafico():
#     #    jugadores=["meassi", ["aguero"],["lavezzi"]]
#     #    goles=[50,35,15]
#     #    bar= (
#     #        Bar()
#     #        .add_xaxis(jugadores)
#     #        .add_yaxis("Goles", goles)
#     #        .set_global_opts(title_opts=opts.TitleOpts(title="Goles por Jugador"))
#     #    )
#     #    return bar.render_embed()

#     #grafico=crear_grafico()

#     player_url='https://www.sofascore.com/es/jugador/lionel-messi/12994'
#     stats_player = sofascore.scrape_player_league_stats(
#         '2025',
#         'Argentina Liga Profesional',
#         'total',
#         ['Forwards']
#     )
#     stats_player_midfielders = sofascore.scrape_player_league_stats(
#         '2025',
#         'Argentina Liga Profesional',
#         'total',
#         ['Midfielders']
#     )
#     stats_player_defenders = sofascore.scrape_player_league_stats(
#         '2025',
#         'Argentina Liga Profesional',
#         'total',
#         ['Defenders']
#     )
#     stats_player_goalkeepers = sofascore.scrape_player_league_stats(
#         '2025',
#         'Argentina Liga Profesional',
#         'total',
#         ['Goalkeepers']
#     )
    
    
    
    
#     def graficos_liga(df):
#         jugadores=df['player'].tolist()
#         stats_completas=[col for col in df.columns if col!='player']
#         bar= Bar()
#         bar.add_xaxis(jugadores)
#         for stat in stats_completas:
#             if stat in df.columns:
#                 valores=df[stat].fillna(0).tolist()
#                 bar.add_yaxis(stat.capitalize(), valores)
#         bar.set_global_opts(
#             title_opts=opts.TitleOpts(title='estadisticas'),
#             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
#             yaxis_opts=opts.AxisOpts(name="Valor")
#         )
#         return bar.render_embed()
    
#     df=pd.DataFrame(stats_player)
#     grafico =graficos_liga(df)
    
#     def crear_tabla_pyecharts(df):
#         tabla = Table()

#         if 'minutesPlayed' in df.columns:
#             df = df[df['minutesPlayed'] > 200]

#         columnas = list(df.columns)
#         if 'player' in columnas:
#             columnas.remove('player')
#             columnas = ['player'] + columnas
#             df = df[columnas]
        
#         headers = list(df.columns)
#         rows = df.head(10).astype(str).values.tolist()

#         tabla.add(headers, rows)
#         tabla.set_global_opts(
#             title_opts=ComponentTitleOpts(title="Estadísticas de Jugadores")
#         )

#         page = Page()
#         page.add(tabla)
#         return tabla.render_embed()


#     tabla = crear_tabla_pyecharts(df)

#     df2 = pd.DataFrame(stats_player)
#     df2.fillna(0, inplace=True)
#     df2 = df2.astype(str)

#     tabla_json = json.dumps(df.to_dict(orient="records"))
#     columnas_json = json.dumps([{"field": col, "sortable": True, "filter": True} for col in df2.columns])

#     match_url = 'https://www.sofascore.com/es/football/match/inter-miami-cf-los-angeles-fc/aTjcsccKc#id:13616395'
#     match_data = sofascore.get_match_dict(match_url)
    
    
    
#     info = {
#         'torneo': match_data['tournament']['name'],
#         'ronda': match_data['roundInfo']['name'],
#         'fecha': datetime.datetime.fromtimestamp(match_data['startTimestamp']).strftime('%d/%m/%Y %H:%M'),
#         'equipo_local': match_data['homeTeam']['name'],
#         'equipo_visitante': match_data['awayTeam']['name'],
#         'marcador': f"{match_data['homeScore']['current']} - {match_data['awayScore']['current']}",
#         'estadio': match_data['venue']['name'],
#         'ciudad': match_data['venue']['city']['name'],
#         'arbitro': match_data['referee']['name'],
#     }

#     match_url2 = 'https://www.sofascore.com/es/football/match/barcelona-borussia-dortmund/ydbsrgb#id:13513404'
#     match_data2 = sofascore.get_match_dict(match_url2)
    
    
    
#     info2 = {
#         'torneo': match_data2['tournament']['name'],
#         'ronda': match_data2['roundInfo']['name'],
#         'fecha': datetime.datetime.fromtimestamp(match_data['startTimestamp']).strftime('%d/%m/%Y %H:%M'),
#         'equipo_local': match_data2['homeTeam']['name'],
#         'equipo_visitante': match_data2['awayTeam']['name'],
#         'marcador': f"{match_data2['homeScore']['current']} - {match_data2['awayScore']['current']}",
#         'estadio': match_data2['venue']['name'],
#         'ciudad': match_data2['venue']['city']['name'],
#         'arbitro': match_data2['referee']['name'],
#     }

#    # class InvalidYearException(Exception):
#     #    def __init__(self, year, league, valid_years):
#      #       message = f"Año inválido: {year} para la liga {league}. Años válidos: {', '.join(valid_years)}"
#       #      super().__init__(message)


#     #def get_tablas(self, year: str, league: str)-> pd.DataFrame:
#      #   valid_seasons=self.get_valid_seasons(league)
#       #  if year not in valid_seasons:
#        #     raise InvalidYearException(year, league, list(valid_Seasons.keys()))
        
#         #season_id=valid_seasons[year]
#         #tablas_url=transfermarkt.comps[league].replace
        
#     delanteros_fields = [
#     'goals', 'expectedGoals', 'shotsOnTarget', 'totalShots',
#     'goalConversionPercentage', 'assists', 'keyPasses', 'bigChancesCreated',
#     'bigChancesMissed', 'successfulDribbles', 'successfulDribblesPercentage',
#     'accurateFinalThirdPasses', 'passToAssist', 'hitWoodwork', 'offsides'
# ]
#     mediocampistas_fields = [
#     'assists', 'keyPasses', 'accuratePasses', 'accurateFinalThirdPasses',
#     'expectedGoals', 'expectedAssists', 'passToAssist',
#     'accurateLongBalls', 'accurateLongBallsPercentage',
#     'accurateCrosses', 'accurateCrossesPercentage',
#     'interceptions', 'duelsWon', 'tacklesWon', 'successfulDribbles',
#     'successfulDribblesPercentage', 'ballRecoveries'
# ]
#     defensores_fields = [
#     'tacklesWon', 'interceptions', 'clearances', 'blocks', 'duelsWon',
#     'aerialDuelsWon', 'aerialDuelsWonPercentage', 'accuratePasses',
#     'accurateLongBalls', 'accurateLongBallsPercentage', 'ballRecoveries',
#     'foulsCommitted', 'yellowCards', 'redCards'
# ]
#     portero_fields = [
#     'saves', 'shotsSaved', 'savePercentage', 'cleanSheets',
#     'goalsConceded', 'expectedGoalsConceded', 'penaltiesSaved',
#     'accuratePasses', 'accurateLongBalls', 'accurateLongBallsPercentage',
#     'highClaims', 'punches', 'errorsLeadingToGoal'
# ]


        
#     def calcular_percentiles_defensa(df):
#         columna_defensores = [
#         'goals', 'assists', 'totalShots', 'shotsOnTarget', 'blockedShots',
#         'goalConversionPercentage', 'expectedGoals', 'keyPasses',
#         'accurateFinalThirdPasses', 'accuratePasses', 'passToAssist',
#         'bigChancesCreated', 'bigChancesMissed', 'successfulDribbles',
#         'successfulDribblesPercentage', 'accurateCrosses', 'accurateCrossesPercentage',
#         'accurateLongBalls', 'accurateLongBallsPercentage', 'hitWoodwork', 'offsides'
#     ]
        
#         resultados_defensores=[]
#         for _,jugador in df_defensores.iterrows():
#             percentile_defensor={'player':jugador['player']}

#             for columna in columna_defensores:
#                 if columna in df_defensores.columns:
#                     valor_jugador=jugador[columna]
#                     percentil=(df_defensores[columna]<=valor_jugador).mean()*100
#                     percentil=round(percentil)
#                     percentile_defensor[columna]=percentil
#             resultados_defensores.append(percentile_defensor)
#         return pd.DataFrame(resultados_defensores)
    
#     df_defensores=pd.DataFrame(stats_player_defenders)
#     percentiles_defensores=calcular_percentiles_defensa(df_defensores)
        
        
#     def grafico_percentiles_defensa(df_percentiles):
#         df_percentiles = df_percentiles.head(10)
        
#         jugadores = df_percentiles['player'].tolist()
#         bar = Bar()
#         bar.add_xaxis(jugadores)
        
#         columnas_estadisticas = [col for col in df_percentiles.columns if col != 'player']
        
#         for stat in columnas_estadisticas:
#             valores = df_percentiles[stat].fillna(0).tolist()
#             bar.add_yaxis(stat.capitalize(), valores)
        
#         bar.set_global_opts(
#             title_opts=opts.TitleOpts(title='Percentiles de Defensores (Top 10)'),
#             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
#             yaxis_opts=opts.AxisOpts(
#                 name="Percentil",
#                 min_=0,
#                 max_=100
#             ),
#             datazoom_opts=[opts.DataZoomOpts()]
#         )
        
#         return bar.render_embed()
#     grafico_percentiles = grafico_percentiles_defensa(percentiles_defensores)
    
    
#     datos_radar = []
#     for _, jugador in percentiles_defensores.iterrows():
#         datos_jugador = {
#             'player': jugador['player'],
#             'percentiles': jugador.drop('player').to_dict()
#             }
#         datos_radar.append(datos_jugador)
    

#     jugador1 = request.GET.get('jugador1')
#     jugador2 = request.GET.get('jugador2')

#     if not jugador1 or not jugador2:
#         jugador1 = datos_radar[0]['player'] if datos_radar else None
#         jugador2 = datos_radar[1]['player'] if len(datos_radar) > 1 else None

#     radar = Radar()
    
#     schema = []
#     for stat in datos_radar[0]['percentiles'].keys():
#         schema.append({"name": stat, "max": 100})

#     radar.add_schema(
#     schema=schema,
#     shape="circle",
#     center=["50%", "50%"],
#     radius="70%",
    
#     )

        
    
#     if jugador1 and jugador2:
#         jugador1_data = next((j for j in datos_radar if j['player'] == jugador1), None)
#         jugador2_data = next((j for j in datos_radar if j['player'] == jugador2), None)
    
#     if jugador1_data and jugador2_data:
#         radar.add(
#             jugador1,
#             [list(jugador1_data['percentiles'].values())],
#             color="#f9713c",
#             symbol="circle",
            
#         )
#         radar.add(
#             jugador2,
#             [list(jugador2_data['percentiles'].values())],
#             color="#4169e1",
#             symbol="circle",
#         )
    
#     radar.set_global_opts(
#         title_opts=opts.TitleOpts(title="Comparación de Percentiles"),
#         legend_opts=opts.LegendOpts(),
        
#     )
    
#     grafico_radar = radar.render_embed()

#     context = {
#         'stats': stats_player.to_dict(orient='records'),
#         'player_url': player_url,
#         'info': info,
#         'info2': info2,
#         'grafico': grafico,
#         'tabla': tabla,
#         'tabla_data': tabla_json,
#         'column_defs': columnas_json,
#         'percentiles_defensores': percentiles_defensores.to_dict(orient='records'),
#         'grafico_percentiles': grafico_percentiles,
#         'datos_radar': datos_radar,
#         'grafico_radar': grafico_radar,
#         'jugadores_disponibles': [j['player'] for j in datos_radar],
#         'jugador1_seleccionado': jugador1,
#         'jugador2_seleccionado': jugador2
#     }

#     return render(request, 'index.html', context)
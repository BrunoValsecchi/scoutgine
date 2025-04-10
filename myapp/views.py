from django.shortcuts import render
import ScraperFC as sfc
import datetime
import pandas as pd
import requests
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Page
from pyecharts.globals import ThemeType
import json


#python manage.py runserver 0.0.0.0:8000

#python manage.py runserver 0.0.0.0:8000

def home(request):
    sofascore = sfc.Sofascore()
    transfermarkt=sfc.Transfermarkt()

    #def crear_grafico():
    #    jugadores=["meassi", ["aguero"],["lavezzi"]]
    #    goles=[50,35,15]
    #    bar= (
    #        Bar()
    #        .add_xaxis(jugadores)
    #        .add_yaxis("Goles", goles)
    #        .set_global_opts(title_opts=opts.TitleOpts(title="Goles por Jugador"))
    #    )
    #    return bar.render_embed()

    #grafico=crear_grafico()

    player_url='https://www.sofascore.com/es/jugador/lionel-messi/12994'
    stats_player = sofascore.scrape_player_league_stats(
        '2025',
        'Argentina Liga Profesional',
        'total',
        ['Forwards']
    )

    def graficos_liga(df):
        jugadores=df['player'].tolist()
        stats_completas=[col for col in df.columns if col!='player']
        bar= Bar()
        bar.add_xaxis(jugadores)
        for stat in stats_completas:
            if stat in df.columns:
                valores=df[stat].fillna(0).tolist()
                bar.add_yaxis(stat.capitalize(), valores)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title='estadisticas'),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 45}),
            yaxis_opts=opts.AxisOpts(name="Valor")
        )
        return bar.render_embed()
    
    df=pd.DataFrame(stats_player)
    grafico =graficos_liga(df)
    
    def crear_tabla_pyecharts(df):
        tabla = Table()

        # Reordenar columnas: poner 'player' primero
        columnas = list(df.columns)
        if 'player' in columnas:
            columnas.remove('player')
            columnas = ['player'] + columnas
            df = df[columnas]

        headers = list(df.columns)
        rows = df.head(10).astype(str).values.tolist()

        tabla.add(headers, rows)
        tabla.set_global_opts(
            title_opts=ComponentTitleOpts(title="Estadísticas de Jugadores")
        )

        page = Page()
        page.add(tabla)
        return tabla.render_embed()


    tabla = crear_tabla_pyecharts(df)

    df2 = pd.DataFrame(stats_player)
    df2.fillna(0, inplace=True)
    df2 = df2.astype(str)

    tabla_json = json.dumps(df.to_dict(orient="records"))
    columnas_json = json.dumps([{"field": col, "sortable": True, "filter": True} for col in df2.columns])

    match_url = 'https://www.sofascore.com/es/football/match/inter-miami-cf-los-angeles-fc/aTjcsccKc#id:13616395'
    match_data = sofascore.get_match_dict(match_url)
    
    
    
    info = {
        'torneo': match_data['tournament']['name'],
        'ronda': match_data['roundInfo']['name'],
        'fecha': datetime.datetime.fromtimestamp(match_data['startTimestamp']).strftime('%d/%m/%Y %H:%M'),
        'equipo_local': match_data['homeTeam']['name'],
        'equipo_visitante': match_data['awayTeam']['name'],
        'marcador': f"{match_data['homeScore']['current']} - {match_data['awayScore']['current']}",
        'estadio': match_data['venue']['name'],
        'ciudad': match_data['venue']['city']['name'],
        'arbitro': match_data['referee']['name'],
    }

    match_url2 = 'https://www.sofascore.com/es/football/match/barcelona-borussia-dortmund/ydbsrgb#id:13513404'
    match_data2 = sofascore.get_match_dict(match_url2)
    
    
    
    info2 = {
        'torneo': match_data2['tournament']['name'],
        'ronda': match_data2['roundInfo']['name'],
        'fecha': datetime.datetime.fromtimestamp(match_data['startTimestamp']).strftime('%d/%m/%Y %H:%M'),
        'equipo_local': match_data2['homeTeam']['name'],
        'equipo_visitante': match_data2['awayTeam']['name'],
        'marcador': f"{match_data2['homeScore']['current']} - {match_data2['awayScore']['current']}",
        'estadio': match_data2['venue']['name'],
        'ciudad': match_data2['venue']['city']['name'],
        'arbitro': match_data2['referee']['name'],
    }

   # class InvalidYearException(Exception):
    #    def __init__(self, year, league, valid_years):
     #       message = f"Año inválido: {year} para la liga {league}. Años válidos: {', '.join(valid_years)}"
      #      super().__init__(message)


    #def get_tablas(self, year: str, league: str)-> pd.DataFrame:
     #   valid_seasons=self.get_valid_seasons(league)
      #  if year not in valid_seasons:
       #     raise InvalidYearException(year, league, list(valid_Seasons.keys()))
        
        #season_id=valid_seasons[year]
        #tablas_url=transfermarkt.comps[league].replace
        
    context = {
        'stats': stats_player.to_dict(orient='records'),
        'player_url': player_url,
        'info': info,
        'info2': info2,
        'grafico':grafico,
        'tabla':tabla,
        'tabla_data': tabla_json,
        'column_defs': columnas_json,
        
    }


    return render(request, 'index.html',context)
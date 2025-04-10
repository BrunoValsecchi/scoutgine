from django.shortcuts import render
import ScraperFC as sfc
import datetime
import pandas as pd
import requests
import json

#python manage.py runserver 0.0.0.0:8000

def home(request):
    sofascore = sfc.Sofascore()
    transfermarkt=sfc.Transfermarkt()



    player_url='https://www.sofascore.com/es/jugador/lionel-messi/12994'
    stats_player = sofascore.scrape_player_league_stats(
        '2025',
        'Argentina Liga Profesional',
        'total',
        ['Forwards']
    )


   

    match_url = 'https://www.sofascore.com/es/football/match/inter-miami-cf-los-angeles-fc/aTjcsccKc#id:13616395'
    match_data = sofascore.get_match_dict(match_url)
    
    
    
    info = {
        'torneo': match_data['tournament']['name'],
        'ronda': match_data['roundInfo'],
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
        'stats_json': json.dumps(stats_player.to_dict(orient='records')),
        'player_url': player_url,
        'info': info,
        'info2': info2
    }


    return render(request, 'index.html',context)
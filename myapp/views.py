from django.shortcuts import render
import ScraperFC as sfc
import datetime
import pandas as pd
import requests

def home(request):
    sofascore = sfc.Sofascore()
    transfermarkt=sfc.Transfermarkt()

    match_url = 'https://www.sofascore.com/es/football/match/real-madrid-arsenal/RsEgb#id:13513403'
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
        

    def get_current_season_id(tournament_id):
        url = f"https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/active"
        response = requests.get(url)
        data = response.json()
        return data['season']['id']

    
    def get_tablas(tournament_id):
        season_id = get_current_season_id(tournament_id)
        url = f"https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/standings/total"
        response = requests.get(url)
        return response.json()

    
    def parse_tablas(data):
        rows = []
        standings = data['standings'][0]['rows']
        for team in standings:
            rows.append({
                'position': team['position'],
                'team': team['team']['name'],
                'played': team['matches'],
                'wins': team['wins'],
                'draws': team['draws'],
                'losses': team['losses'],
                'goals_for': team['scoresFor'],
                'goals_against': team['scoresAgainst'],
                'points': team['points']
            })
        return pd.DataFrame(rows)
    data = get_tablas(155)  l
    df = parse_tablas(data)
    print(df)
    tabla = df.to_dict(orient='records')  

    return render(request, 'index.html', {'info': info, 'tabla': tabla})
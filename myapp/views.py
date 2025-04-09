from django.shortcuts import render
import ScraperFC as sfc
import datetime

def home(request):
    sofascore = sfc.Sofascore()

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

    return render(request, 'index.html', {'info': info})

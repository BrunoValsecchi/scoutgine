from django import template
from django.shortcuts import render
from .models import EstadisticasEquipo

register = template.Library()

@register.filter
def obtener_stats_equipo(obj, label):
    # Map label to field name
    label_to_field = {
        'Rating': 'fotmob_rating',
        'Goles por partido': 'goals_per_match',
        'Menos goles recibidos': 'goals_conceded_per_match',
        'Posesión (%)': 'average_possession',
        'Vallas invictas': 'clean_sheets',
        'xG': 'expected_goals_xg',
        'Tiros al arco/partido': 'shots_on_target_per_match',
        'Grandes chances': 'big_chances',
        'Grandes chances falladas': 'big_chances_missed',
        'Pases precisos/partido': 'accurate_passes_per_match',
        'Pases largos precisos/partido': 'accurate_long_balls_per_match',
        'Centros precisos/partido': 'accurate_crosses_per_match',
        'Penales a favor': 'penalties_awarded',
        'Toques en área rival': 'touches_in_opposition_box',
        'Corners': 'corners',
        'xG concedido': 'xg_concedido',
        'Intercepciones/partido': 'interceptions_per_match',
        'Entradas exitosas/partido': 'successful_tackles_per_match',
        'Despejes/partido': 'clearances_per_match',
        'Recuperaciones en 1/3 final/partido': 'possession_won_final_3rd_per_match',
        'Atajadas/partido': 'saves_per_match',
        'Faltas/partido': 'fouls_per_match',
        'Amarillas': 'yellow_cards',
        'Rojas': 'red_cards',
    }
    field = label_to_field.get(label)
    return getattr(obj, field, '')

def stats_equipos(request):
    estadisticas = [
        ('fotmob_rating', 'Rating'),
        ('goals_per_match', 'Goles por partido'),
        ('goals_conceded_per_match', 'Menos goles recibidos'),
        ('average_possession', 'Posesión (%)'),
        ('clean_sheets', 'Vallas invictas'),
        ('expected_goals_xg', 'xG'),
        ('shots_on_target_per_match', 'Tiros al arco/partido'),
        ('big_chances', 'Grandes chances'),
        ('big_chances_missed', 'Grandes chances falladas'),
        ('accurate_passes_per_match', 'Pases precisos/partido'),
        ('accurate_long_balls_per_match', 'Pases largos precisos/partido'),
        ('accurate_crosses_per_match', 'Centros precisos/partido'),
        ('penalties_awarded', 'Penales a favor'),
        ('touches_in_opposition_box', 'Toques en área rival'),
        ('corners', 'Corners'),
        ('xg_concedido', 'xG concedido'),
        ('interceptions_per_match', 'Intercepciones/partido'),
        ('successful_tackles_per_match', 'Entradas exitosas/partido'),
        ('clearances_per_match', 'Despejes/partido'),
        ('possession_won_final_3rd_per_match', 'Recuperaciones en 1/3 final/partido'),
        ('saves_per_match', 'Atajadas/partido'),
        ('fouls_per_match', 'Faltas/partido'),
        ('yellow_cards', 'Amarillas'),
        ('red_cards', 'Rojas'),
    ]

    top3_por_estadistica = {}
    for field, label in estadisticas:
        # Para estadísticas donde "menos es mejor"
        if field in ['goals_conceded_per_match', 'big_chances_missed', 'xg_concedido', 'fouls_per_match', 'yellow_cards', 'red_cards']:
            equipos = EstadisticasEquipo.objects.exclude(**{field: None}).order_by(field)[:3]
        else:
            equipos = EstadisticasEquipo.objects.exclude(**{field: None}).order_by(f'-{field}')[:3]
        top3_por_estadistica[label] = [
            {
                "nombre": equipo.equipo.nombre,
                "valor": obtener_stats_equipo(equipo, field)
            }
            for equipo in equipos
        ]
    return render(request, "partials/statsequipo.html", {
        "top3_por_estadistica": top3_por_estadistica
    })
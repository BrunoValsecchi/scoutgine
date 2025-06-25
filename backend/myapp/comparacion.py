from django.shortcuts import render
from .models import Equipo, EstadisticasEquipo
import json

GRUPOS_STATS = {
    "Ofensivos": [
        ("Goles por partido", "goals_per_match"),
        ("Tiros al arco por partido", "shots_on_target_per_match"),
        ("Ocasiones claras", "big_chances"),
        ("Ocasiones claras falladas", "big_chances_missed"),
        ("Goles esperados (xG)", "expected_goals_xg"),
        ("Penales a favor", "penalties_awarded"),
    ],
    "Defensivos": [
        ("Goles concedidos por partido", "goals_conceded_per_match"),
        ("Vallas invictas", "clean_sheets"),
        ("xG concedido", "expected_goals_conceded_xgc"),
        ("Intercepciones por partido", "interceptions_per_match"),
        ("Entradas exitosas por partido", "tackles_won_per_match"),
        ("Despejes por partido", "clearances_per_match"),
        ("Recuperaciones en el último tercio", "recoveries_final_third"),
        ("Atajadas por partido", "saves_per_match"),
    ],
    "Creación": [
        ("Pases precisos por partido", "accurate_passes_per_match"),
        ("Pases largos precisos por partido", "accurate_long_balls_per_match"),
        ("Centros precisos por partido", "accurate_crosses_per_match"),
        ("Toques en el área rival", "touches_in_opposition_box"),
        ("Tiros de esquina", "corners_taken"),
    ],
    "Generales": [
        ("Rating", "average_rating"),
        ("Posesión promedio", "average_possession"),
        ("Faltas por partido", "fouls_per_match"),
        ("Tarjetas amarillas", "yellow_cards"),
        ("Tarjetas rojas", "red_cards"),
    ]
}

def comparacion(request):
    equipos = Equipo.objects.all().order_by('nombre')
    
    # Preparar datos de equipos con estadísticas para JSON
    equipos_data = []
    for equipo in equipos:
        stats = EstadisticasEquipo.objects.filter(equipo=equipo).first()
        equipo_dict = {
            'id': equipo.id,
            'nombre': equipo.nombre,
            'nombre_corto': equipo.nombre_corto or equipo.nombre[:15],
        }
        
        # Agregar todas las estadísticas al diccionario
        if stats:
            for grupo_stats in GRUPOS_STATS.values():
                for label, field in grupo_stats:
                    value = getattr(stats, field, 0)
                    equipo_dict[field] = float(value) if value else 0
        else:
            # Si no tiene estadísticas, llenar con 0
            for grupo_stats in GRUPOS_STATS.values():
                for label, field in grupo_stats:
                    equipo_dict[field] = 0
                    
        equipos_data.append(equipo_dict)

    context = {
        "equipos": equipos,
        "equipos_data": json.dumps(equipos_data),
        "GRUPOS_STATS": GRUPOS_STATS,
        "GRUPOS_STATS_JSON": json.dumps(GRUPOS_STATS),
    }
    return render(request, "comparacion.html", context)
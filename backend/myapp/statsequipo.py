from django.shortcuts import render
from django.http import JsonResponse
from .models import EstadisticasEquipo

def obtener_stats_equipo(obj, field):
    valor = getattr(obj, field, '')
    return valor

def stats_equipos(request):

    
    # Verificar si es una petición AJAX para vista completa
    is_ajax = request.GET.get('format') == 'json'
    estadistica_param = request.GET.get('estadistica')
    
 
    
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
        ('xg_conceded', 'xG concedido'),
        ('interceptions_per_match', 'Intercepciones/partido'),
        ('successful_tackles_per_match', 'Entradas exitosas/partido'),
        ('clearances_per_match', 'Despejes/partido'),
        ('possession_won_final_3rd_per_match', 'Recuperaciones en 1/3 final/partido'),
        ('saves_per_match', 'Atajadas/partido'),
        ('fouls_per_match', 'Faltas/partido'),
        ('yellow_cards', 'Amarillas'),
        ('red_cards', 'Rojas'),
    ]
    
    
    if is_ajax and estadistica_param:
        
        # Encontrar la estadística solicitada
        estadistica_info = next((stat for stat in estadisticas if stat[0] == estadistica_param), None)
        
        if not estadistica_info:
            return JsonResponse({"error": "Estadística no encontrada"}, status=400)
        
        field, label = estadistica_info
        
        # Estadísticas donde menor es mejor
        if field in ['goals_conceded_per_match', 'big_chances_missed', 'xg_conceded', 'fouls_per_match', 'yellow_cards', 'red_cards']:
            equipos = EstadisticasEquipo.objects.exclude(**{field: None}).order_by(field)[:30]
        else:
            equipos = EstadisticasEquipo.objects.exclude(**{field: None}).order_by(f'-{field}')[:30]
        
        
        equipos_lista = []
        for i, equipo in enumerate(equipos, 1):
            try:
                nombre = equipo.equipo.nombre if hasattr(equipo, 'equipo') and hasattr(equipo.equipo, 'nombre') else str(equipo.equipo)
                valor = getattr(equipo, field, 0)
                equipos_lista.append({"nombre": nombre, "valor": valor})
            except Exception as e:
                print(f"❌ Error procesando equipo {i}: {e}")
        
        return JsonResponse({
            "equipos": equipos_lista,
            "label": label,
            "field": field
        })
    
    # Vista resumen normal (Top 3)
    top3_por_estadistica = {}
    
    for field, label in estadisticas:
        
        if field in ['goals_conceded_per_match', 'big_chances_missed', 'xg_conceded', 'fouls_per_match', 'yellow_cards', 'red_cards']:
            equipos = EstadisticasEquipo.objects.exclude(**{field: None}).order_by(field)[:3]
        else:
            equipos = EstadisticasEquipo.objects.exclude(**{field: None}).order_by(f'-{field}')[:3]
        
        
        equipos_lista = []
        for equipo in equipos:
            nombre = equipo.equipo.nombre if hasattr(equipo, 'equipo') and hasattr(equipo.equipo, 'nombre') else str(equipo.equipo)
            valor = obtener_stats_equipo(equipo, field)
            equipos_lista.append({"nombre": nombre, "valor": valor})
        
        top3_por_estadistica[label] = equipos_lista

    

    return render(request, "partials/statsequipo.html", {
        "top3_por_estadistica": top3_por_estadistica
    })
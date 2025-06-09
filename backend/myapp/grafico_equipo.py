from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Equipo, EstadisticasEquipo
import numpy as np

RADAR_GROUPS = {
    "ofensivos": [
        "Goles por partido", "Tiros al arco por partido", "Ocasiones claras",
        "Ocasiones claras falladas", "Goles esperados (xG)", "Penales a favor"
    ],
    "defensivos": [
        "Goles concedidos por partido", "Vallas invictas", "xG concedido",
        "Intercepciones por partido", "Entradas exitosas por partido",
        "Despejes por partido", "Recuperaciones en el último tercio", "Atajadas por partido"
    ],
    "creacion": [
        "Pases precisos por partido", "Pases largos precisos por partido",
        "Centros precisos por partido", "Toques en el área rival", "Tiros de esquina"
    ],
    "generales": [
        "Rating", "Posesión promedio", "Faltas por partido", "Tarjetas amarillas", "Tarjetas rojas"
    ]
}

STAT_MAPPING = {
    'Rating': 'fotmob_rating',
    'Posesión promedio': 'average_possession', 
    'Faltas por partido': 'fouls_per_match',
    'Tarjetas amarillas': 'yellow_cards',
    'Tarjetas rojas': 'red_cards',
    'Goles por partido': 'goals_per_match',
    'Goles esperados (xG)': 'expected_goals_xg',
    'Tiros al arco por partido': 'shots_on_target_per_match',
    'Ocasiones claras': 'big_chances',
    'Ocasiones claras falladas': 'big_chances_missed',
    'Penales a favor': 'penalties_awarded',
    'Goles concedidos por partido': 'goals_conceded_per_match',
    'Vallas invictas': 'clean_sheets',
    'xG concedido': 'xg_concedido',
    'Intercepciones por partido': 'interceptions_per_match',
    'Entradas exitosas por partido': 'successful_tackles_per_match',
    'Despejes por partido': 'clearances_per_match',
    'Recuperaciones en el último tercio': 'possession_won_final_3rd_per_match',
    'Atajadas por partido': 'saves_per_match',
    'Pases precisos por partido': 'accurate_passes_per_match',
    'Pases largos precisos por partido': 'accurate_long_balls_per_match',
    'Centros precisos por partido': 'accurate_crosses_per_match',
    'Toques en el área rival': 'touches_in_opposition_box',
    'Tiros de esquina': 'corners',
}

STATS_MENOS_ES_MEJOR = [
    "Goles concedidos por partido", "Vallas invictas", "xG concedido",
    "Intercepciones por partido", "Entradas exitosas por partido",
    "Despejes por partido", "Recuperaciones en el último tercio", "Atajadas por partido",
    "Faltas por partido", "Tarjetas amarillas", "Tarjetas rojas"
]

def grafico_equipo(request, equipo_id, estadistica):
    """Página de gráfico para una estadística específica de equipo"""
    print(f"🎯 Mostrando gráfico de '{estadistica}' para equipo ID: {equipo_id}")
    
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        estadisticas_obj = EstadisticasEquipo.objects.filter(equipo=equipo).first()
        
        print(f"✅ Equipo encontrado: {equipo.nombre} (ID: {equipo.id})")
        
        field_name = STAT_MAPPING.get(estadistica)
        if not field_name or not estadisticas_obj:
            raise ValueError(f"Estadística no encontrada: {estadistica}")
            
        # Valor del equipo actual
        valor_equipo = getattr(estadisticas_obj, field_name, 0) or 0
        
        # Obtener datos de todos los equipos para comparación
        todos_equipos = EstadisticasEquipo.objects.select_related('equipo').exclude(**{field_name: None})
        
        # Datos para gráficos (puedes usarlos en tu lógica JS/ECharts)
        equipos_nombres = []
        equipos_valores = []
        
        for eq_stat in todos_equipos:
            valor = getattr(eq_stat, field_name, 0) or 0
            equipos_nombres.append(eq_stat.equipo.nombre_corto or eq_stat.equipo.nombre[:15])
            equipos_valores.append(float(valor))
        
        # Promedio general
        promedio = sum(equipos_valores) / len(equipos_valores) if equipos_valores else 0
        
        # Posición del equipo en el ranking
        valores_ordenados = sorted(equipos_valores, reverse=True)
        try:
            posicion = valores_ordenados.index(float(valor_equipo)) + 1
        except ValueError:
            posicion = len(valores_ordenados) + 1
        
        context = {
            'equipo': equipo,
            'stat_name': estadistica,
            'valor_equipo': valor_equipo,
            'promedio': round(promedio, 2),
            'posicion': posicion,
            'total_equipos': len(equipos_valores),
            'equipos_nombres': equipos_nombres,
            'equipos_valores': equipos_valores,
            'title': f'{estadistica} - {equipo.nombre}',
        }
        
        print(f"✅ Estadística: {estadistica} = {valor_equipo}")
        print(f"📊 Posición: {posicion}/{len(equipos_valores)}")
        return render(request, 'estadistica_detalle.html', context)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            equipo = get_object_or_404(Equipo, id=equipo_id)
        except:
            equipo = {'id': equipo_id, 'nombre': 'Equipo no encontrado'}
            
        context = {
            'equipo': equipo,
            'error': f'Error al cargar la estadística: {estadistica}',
            'title': 'Error'
        }
        return render(request, 'estadistica_detalle.html', context)

def calcular_percentil(valor, lista):
    if not lista:
        return 0
    return round(100 * (np.sum(np.array(lista) < valor) / len(lista)), 2)

def ajax_radar_equipo(request):
    equipo_id = request.GET.get('equipo_id')
    grupo = request.GET.get('grupo', 'ofensivos')
    labels = RADAR_GROUPS.get(grupo, [])
    equipo = Equipo.objects.get(id=equipo_id)
    stats_obj = EstadisticasEquipo.objects.filter(equipo=equipo).first()
    all_stats = EstadisticasEquipo.objects.all()
    equipo_percentiles = []
    mediana_percentiles = []
    for label in labels:
        field = STAT_MAPPING[label]
        valores = [getattr(e, field, 0) for e in all_stats if getattr(e, field, None) not in [None, '']]
        valores = [float(v) for v in valores if v is not None]
        valor_equipo = getattr(stats_obj, field, 0) or 0
        try:
            valor_equipo = float(valor_equipo)
        except Exception:
            valor_equipo = 0
        percentil_equipo = calcular_percentil(valor_equipo, valores)
        # Invertir percentil si menos es mejor
        if label in STATS_MENOS_ES_MEJOR:
            percentil_equipo = 100 - percentil_equipo
        equipo_percentiles.append(percentil_equipo)
        mediana = float(np.median(valores)) if valores else 0
        percentil_mediana = calcular_percentil(mediana, valores)
        if label in STATS_MENOS_ES_MEJOR:
            percentil_mediana = 100 - percentil_mediana
        mediana_percentiles.append(percentil_mediana)
    return JsonResponse({
        "labels": labels,
        "equipo": equipo_percentiles,
        "promedio": mediana_percentiles,
        "max": 100
    })

def ajax_boxplot_estadistica(request):
    stat_id = request.GET.get('stat_id')
    equipo_id = request.GET.get('equipo_id')
    # Busca el nombre de la estadística a partir del id (puede ser el nombre en español)
    field = STAT_MAPPING.get(stat_id)
    if not field:
        return JsonResponse({'success': False, 'error': 'Estadística no válida'})
    all_stats = EstadisticasEquipo.objects.all()
    valores = [getattr(e, field, None) for e in all_stats if getattr(e, field, None) not in [None, '']]
    valores = [float(v) for v in valores if v is not None]
    valores.sort()
    if not valores:
        return JsonResponse({'success': False, 'error': 'Sin datos'})
    # Boxplot: min, Q1, median, Q3, max
    q1 = np.percentile(valores, 25)
    q2 = np.percentile(valores, 50)
    q3 = np.percentile(valores, 75)
    box = [min(valores), q1, q2, q3, max(valores)]
    valor_equipo = None
    if equipo_id:
        stats_obj = EstadisticasEquipo.objects.filter(equipo_id=equipo_id).first()
        if stats_obj:
            valor_equipo = getattr(stats_obj, field, None)
            if valor_equipo is not None:
                valor_equipo = float(valor_equipo)
    return JsonResponse({
        'success': True,
        'stat': stat_id,
        'box': box,
        'valores': valores,
        'valor_equipo': valor_equipo,
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import EstadisticasJugador, Jugador
import json
import random
import numpy as np

# Puedes poner esto como constantes en tu models.py o en un archivo utils.py

STATS_OFENSIVAS = [
    'goals', 'expected_goals_xg', 'shots', 'shots_on_target', 'assists',
    'expected_assists_xa', 'penalties_awarded', 'touches_in_opposition_box',
    'successful_dribbles', 'dribble_success'
]

STATS_DEFENSIVAS = [
    'saves', 'save_percentage', 'goals_conceded', 'goals_prevented', 'clean_sheets',
    'error_led_to_goal', 'high_claim', 'tackles_won', 'tackles_won_percentage',
    'interceptions', 'blocked', 'recoveries', 'possession_won_final_3rd',
    'dribbled_past', 'fouls_committed', 'yellow_cards', 'red_cards', 'aerial_duels_won',
    'aerial_duels_won_percentage', 'duels_won', 'duels_won_percentage', 'dispossessed'
]

STATS_CREACION = [
    'successful_passes', 'pass_accuracy_outfield', 'accurate_long_balls_outfield',
    'long_ball_accuracy_outfield', 'chances_created', 'successful_crosses',
    'cross_accuracy', 'touches', 'fouls_won'
]

STATS_ARQUERO = [
    'saves', 'save_percentage', 'goals_conceded', 'goals_prevented', 'clean_sheets',
    'error_led_to_goal', 'high_claim', 'pass_accuracy', 'accurate_long_balls',
    'long_ball_accuracy'
]

def grafico_jugador_view(request, jugador_id, estadistica):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    
    # Calcular estadísticas para las cards
    stat_value, promedio, percentil = calcular_estadisticas_cards(jugador, estadistica)
    
    datos_grafico = obtener_datos_estadistica(jugador, estadistica)
    
    context = {
        'jugador': jugador,
        'estadistica': estadistica,
        'datos_json': json.dumps(datos_grafico),
        'stat_value': stat_value,
        'promedio': promedio,
        'percentil': percentil,
    }
    return render(request, 'estadistica_jugador.html', context)

def calcular_estadisticas_cards(jugador, estadistica):
    """
    Calcula las estadísticas para mostrar en las cards del hero:
    - Valor actual del jugador
    - Promedio de la liga
    - Percentil del jugador
    """
    
    # Mapeo de nombres de estadística a campos del modelo
    mapeo_estadisticas = {
        'Goles': 'goals',
        'Asistencias': 'assists',
        'Tiros al arco': 'shots_on_target',
        'Tiros totales': 'shots',
        'Goles esperados (xG)': 'expected_goals_xg',
        'Penales a favor': 'penalties_awarded',
        'Ocasiones claras falladas': 'big_chances_missed',
        'Goles concedidos': 'goals_conceded',
        'Vallas invictas': 'clean_sheets',
        'xG concedido': 'expected_goals_conceded_xgc',
        'Entradas exitosas': 'tackles_won',
        'Intercepciones': 'interceptions',
        'Despejes': 'blocked',
        'Recuperaciones último tercio': 'recoveries',
        'Atajadas': 'saves',
        'Pases precisos por partido': 'successful_passes',
        'Precisión de pases': 'pass_accuracy_outfield',
        'Pases largos precisos': 'accurate_long_balls_outfield',
        'Centros precisos': 'successful_crosses',
        'Ocasiones creadas': 'chances_created',
        'Toques en área rival': 'touches_in_opposition_box',
        'Tiros de esquina': 'corners_taken',
        'Rating': 'average_rating',
        'Partidos jugados': 'appearances',
        'Minutos jugados': 'minutes_played',
        'Posesión promedio': 'possession_percentage',
        'Toques totales': 'touches',
        'Duelos ganados': 'duels_won_percentage',
        'Duelos aéreos ganados': 'aerial_duels_won_percentage',
        'Faltas por partido': 'fouls_committed',
        'Tarjetas amarillas': 'yellow_cards',
        'Tarjetas rojas': 'red_cards',
    }
    
    campo_bd = mapeo_estadisticas.get(estadistica)
    
    if not campo_bd:
        print(f"❌ Estadística '{estadistica}' no encontrada en el mapeo")
        return None, None, None
    
    try:
        # 1. Obtener valor actual del jugador
        stat_value = None
        try:
            jugador_stats = EstadisticasJugador.objects.get(jugador=jugador)
            stat_value = getattr(jugador_stats, campo_bd, None)
            if stat_value is not None:
                if isinstance(stat_value, float):
                    stat_value = round(stat_value, 2)
                else:
                    stat_value = int(stat_value)
            print(f"📊 Valor del jugador: {stat_value}")
        except EstadisticasJugador.DoesNotExist:
            print(f"❌ No se encontraron estadísticas para el jugador {jugador.nombre}")
        
        # 2. Calcular promedio de la liga
        promedio = None
        try:
            stats_liga = EstadisticasJugador.objects.exclude(**{f'{campo_bd}__isnull': True})
            valores = [getattr(stat, campo_bd) for stat in stats_liga if getattr(stat, campo_bd) is not None]
            
            if valores:
                promedio = sum(valores) / len(valores)
                if isinstance(promedio, float):
                    promedio = round(promedio, 2)
                else:
                    promedio = int(promedio)
                print(f"📊 Promedio liga: {promedio}")
        except Exception as e:
            print(f"❌ Error calculando promedio: {e}")
        
        # 3. Calcular percentil
        percentil = None
        if stat_value is not None:
            try:
                stats_liga = EstadisticasJugador.objects.exclude(**{f'{campo_bd}__isnull': True})
                valores = [getattr(stat, campo_bd) for stat in stats_liga if getattr(stat, campo_bd) is not None]
                
                if valores:
                    valores_menores = [v for v in valores if v < stat_value]
                    percentil = round((len(valores_menores) / len(valores)) * 100, 1)
                    print(f"📊 Percentil: {percentil}%")
            except Exception as e:
                print(f"❌ Error calculando percentil: {e}")
        
        return stat_value, promedio, percentil
        
    except Exception as e:
        print(f"❌ Error general en calcular_estadisticas_cards: {e}")
        return None, None, None

def obtener_datos_estadistica(jugador, estadistica):
    mapeo_estadisticas = {
        'Goles': 'goals',
        'Asistencias': 'assists',
        'Tiros al arco': 'shots_on_target',
        'Tiros totales': 'shots',
        'Goles esperados (xG)': 'expected_goals_xg',
        'Penales a favor': 'penalties_awarded',
        'Ocasiones claras falladas': 'big_chances_missed',
        'Goles concedidos': 'goals_conceded',
        'Vallas invictas': 'clean_sheets',
        'xG concedido': 'expected_goals_conceded_xgc',
        'Entradas exitosas': 'tackles_won',
        'Intercepciones': 'interceptions',
        'Despejes': 'blocked',
        'Recuperaciones último tercio': 'recoveries',
        'Atajadas': 'saves',
        'Pases precisos por partido': 'successful_passes',
        'Precisión de pases': 'pass_accuracy_outfield',
        'Pases largos precisos': 'accurate_long_balls_outfield',
        'Centros precisos': 'successful_crosses',
        'Ocasiones creadas': 'chances_created',
        'Toques en área rival': 'touches_in_opposition_box',
        'Tiros de esquina': 'corners_taken',
        'Rating': 'average_rating',
        'Partidos jugados': 'appearances',
        'Minutos jugados': 'minutes_played',
        'Posesión promedio': 'possession_percentage',
        'Toques totales': 'touches',
        'Duelos ganados': 'duels_won_percentage',
        'Duelos aéreos ganados': 'aerial_duels_won_percentage',
        'Faltas por partido': 'fouls_committed',
        'Tarjetas amarillas': 'yellow_cards',
        'Tarjetas rojas': 'red_cards',
    }
    campo = mapeo_estadisticas.get(estadistica)
    if not campo:
        return {'labels': [], 'data': [], 'error': f'Estadística "{estadistica}" no encontrada'}
    stats_jugador = EstadisticasJugador.objects.filter(jugador=jugador).first()
    if stats_jugador and hasattr(stats_jugador, campo):
        valor_actual = getattr(stats_jugador, campo, 0)
        labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        data = generar_evolucion_ejemplo(valor_actual or 0, len(labels))
        return {
            'labels': labels,
            'data': data,
            'estadistica': estadistica,
            'jugador': jugador.nombre,
            'valor_actual': float(valor_actual) if valor_actual else 0,
            'error': None
        }
    else:
        return generar_datos_ejemplo(estadistica, jugador)

def generar_evolucion_ejemplo(valor_base, num_puntos):
    if not valor_base:
        valor_base = 1
    datos = []
    valor_actual = valor_base
    for i in range(num_puntos):
        variacion = random.uniform(-0.2, 0.2)
        valor_actual = max(0, valor_actual * (1 + variacion))
        if valor_base >= 10:
            datos.append(round(valor_actual, 1))
        else:
            datos.append(round(valor_actual, 2))
    return datos

def generar_datos_ejemplo(estadistica, jugador):
    import random
    labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    if 'Rating' in estadistica:
        data = [round(random.uniform(6.0, 8.5), 2) for _ in range(12)]
    elif 'Goles' in estadistica:
        data = [random.randint(0, 3) for _ in range(12)]
    elif 'Pases' in estadistica or 'precisos' in estadistica.lower():
        data = [round(random.uniform(20, 80), 1) for _ in range(12)]
    elif 'Precisión' in estadistica or '%' in estadistica:
        data = [round(random.uniform(60, 95), 1) for _ in range(12)]
    elif 'Tarjetas' in estadistica:
        data = [random.randint(0, 2) for _ in range(12)]
    else:
        data = [round(random.uniform(0, 15), 1) for _ in range(12)]
    return {
        'labels': labels,
        'data': data,
        'estadistica': estadistica,
        'jugador': jugador.nombre,
        'valor_actual': data[-1] if data else 0,
        'error': None,
        'es_ejemplo': True
    }

# --- Radar AJAX endpoint ---
def ajax_radar_jugador(request):
    jugador_id = request.GET.get('jugador_id')
    grupo = request.GET.get('grupo', 'ofensivos')
    posicion = request.GET.get('posicion')  # Nueva: posición seleccionada

    if not jugador_id:
        return JsonResponse({'success': False, 'error': 'Falta jugador_id'})

    GRUPOS = {
        'ofensivos': STATS_OFENSIVAS,
        'defensivos': STATS_DEFENSIVAS,
        'creacion': STATS_CREACION,
        'arquero': STATS_ARQUERO,
    }
    campos = GRUPOS.get(grupo, STATS_OFENSIVAS)
    labels_nombres = [campo.replace('_', ' ').capitalize() for campo in campos]

    try:
        jugador = Jugador.objects.get(id=jugador_id)
        jugador_stats = EstadisticasJugador.objects.get(jugador_id=jugador_id)
    except (Jugador.DoesNotExist, EstadisticasJugador.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Jugador no encontrado'})

    # Si el jugador tiene varias posiciones, usa la seleccionada o la primera
    posiciones_jugador = [p.strip() for p in jugador.posicion.split(',')]
    posicion_base = posicion if posicion in posiciones_jugador else posiciones_jugador[0]

    percentiles_jugador = []

    def calcular_percentil(valores, valor_jugador):
        if not valores or valor_jugador is None:
            return 0
        return int(round(100 * (np.sum(np.array(valores) < valor_jugador) / len(valores))))

    for campo in campos:
        # Solo jugadores con esa posición (en cualquier parte de la cadena)
        jugadores_misma_pos = Jugador.objects.filter(posicion__icontains=posicion_base)
        stats_misma_pos = EstadisticasJugador.objects.filter(jugador__in=jugadores_misma_pos).exclude(**{f"{campo}__isnull": True})
        valores = list(stats_misma_pos.values_list(campo, flat=True))
        valor_jugador = getattr(jugador_stats, campo, None)
        percentil = calcular_percentil(valores, valor_jugador)
        percentiles_jugador.append(percentil)

    percentiles_promedio = [50 for _ in campos]

    return JsonResponse({
        'success': True,
        'labels': labels_nombres,
        'max': 100,
        'jugador': percentiles_jugador,
        'promedio': percentiles_promedio,
        'posicion': posicion_base,
        'posiciones_jugador': posiciones_jugador,
    })

# --- Ranking, Evolución, Percentil AJAX endpoints ---
def ajax_ranking_jugadores(request):
    stat = request.GET.get('stat')
    if not stat:
        return JsonResponse({'success': False, 'error': 'Falta estadística'})
    jugadores = EstadisticasJugador.objects.exclude(**{f"{stat}__isnull": True}).select_related('jugador')
    top = sorted(jugadores, key=lambda j: getattr(j, stat, 0), reverse=True)[:10]
    data = [{
        'nombre': j.jugador.nombre,
        'equipo': j.jugador.equipo.nombre if j.jugador.equipo else '',
        'valor': getattr(j, stat, 0)
    } for j in top]
    return JsonResponse({'success': True, 'ranking': data})

def ajax_evolucion_jugador(request):
    jugador_id = request.GET.get('jugador_id')
    stat = request.GET.get('stat')
    if not jugador_id or not stat:
        return JsonResponse({'success': False, 'error': 'Faltan datos'})
    try:
        est = EstadisticasJugador.objects.get(jugador_id=jugador_id)
        base = getattr(est, stat, 0)
        evolucion = [round(base * (1 + random.uniform(-0.15, 0.15)), 2) for _ in range(6)]
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
        return JsonResponse({'success': True, 'labels': meses, 'data': evolucion})
    except EstadisticasJugador.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Jugador no encontrado'})

def ajax_percentil_jugador(request):
    jugador_id = request.GET.get('jugador_id')
    stat = request.GET.get('stat')
    if not jugador_id or not stat:
        return JsonResponse({'success': False, 'error': 'Faltan datos'})
    jugadores = EstadisticasJugador.objects.exclude(**{f"{stat}__isnull": True})
    valores = sorted([getattr(j, stat, 0) for j in jugadores])
    try:
        est = EstadisticasJugador.objects.get(jugador_id=jugador_id)
        valor = getattr(est, stat, 0)
    except EstadisticasJugador.DoesNotExist:
        valor = 0
    percentiles = [25, 50, 75, 90]
    valores_percentiles = [valores[int(len(valores)*p/100)] if valores else 0 for p in percentiles]
    return JsonResponse({
        'success': True,
        'percentiles': percentiles,
        'valores_percentiles': valores_percentiles,
        'valor_jugador': valor
    })

def calcular_percentil(valores, valor):
    """Calcula el percentil de un valor en una lista de valores."""
    if not valores or valor is None:
        return 0
    valores = sorted(valores)
    below = sum(1 for v in valores if v < valor)
    percentil = below / len(valores) * 100
    return int(round(percentil))

def ajax_grafico_dispersion_jugador(request):
    """
    Devuelve datos para scatter plot de jugadores según dos estadísticas, filtrando por posición.
    """
    stat_x = request.GET.get('stat_x')
    stat_y = request.GET.get('stat_y')
    posicion = request.GET.get('posicion')
    jugador_id = request.GET.get('jugador_id')

    if not stat_x or not posicion:
        return JsonResponse({'success': False, 'error': 'Faltan parámetros obligatorios'})

    # Campos numéricos disponibles para el eje Y (todos los campos de estadísticas)
    campos_numericos = [
        'goals', 'expected_goals_xg', 'shots', 'shots_on_target', 'assists',
        'penalties_awarded', 'goals_conceded', 'clean_sheets', 'tackles_won',
        'interceptions', 'blocked', 'recoveries', 'saves', 'successful_passes',
        'pass_accuracy_outfield', 'accurate_long_balls_outfield', 'successful_crosses',
        'chances_created', 'touches_in_opposition_box', 'touches', 
        'duels_won_percentage', 'aerial_duels_won_percentage', 'fouls_committed',
        'yellow_cards', 'red_cards'
    ]
    
    # Si no se especifica stat_y, usar la primera disponible diferente a stat_x
    if not stat_y or stat_y not in campos_numericos:
        stat_y = next((campo for campo in campos_numericos if campo != stat_x), 'assists')

    # Filtrar jugadores por posición (usando el campo posicion del modelo Jugador)
    jugadores_posicion = Jugador.objects.filter(posicion__icontains=posicion)
    jugadores_ids = list(jugadores_posicion.values_list('id', flat=True))
    
    # Obtener estadísticas de esos jugadores
    stats_qs = EstadisticasJugador.objects.filter(
        jugador_id__in=jugadores_ids
    ).exclude(**{f"{stat_x}__isnull": True}).exclude(**{f"{stat_y}__isnull": True}).select_related('jugador')

    data = []
    jugador_actual = None
    
    for stat in stats_qs:
        x_val = getattr(stat, stat_x, None)
        y_val = getattr(stat, stat_y, None)
        
        if x_val is not None and y_val is not None:
            punto = {
                'nombre': stat.jugador.nombre,
                'x': float(x_val),
                'y': float(y_val),
                'jugador_id': stat.jugador.id,
            }
            if jugador_id and int(jugador_id) == stat.jugador.id:
                jugador_actual = punto
            data.append(punto)

    return JsonResponse({
        'success': True,
        'data': data,
        'stat_x': stat_x,
        'stat_y': stat_y,
        'campos_y': campos_numericos,
        'jugador_actual': jugador_actual,
        'posicion': posicion,
        'total_jugadores': len(data)
    })

def api_jugador_posiciones(request, jugador_id):
    """Devuelve las posiciones de un jugador"""
    try:
        jugador = Jugador.objects.get(id=jugador_id)
        posiciones = [p.strip() for p in jugador.posicion.split(',')]
        return JsonResponse({'success': True, 'posiciones': posiciones})
    except Jugador.DoesNotExist:
        return JsonResponse({'success': False, 'posiciones': []})

def ajax_boxplot_jugador(request):
    """
    Devuelve datos para boxplot de una estadística específica de jugadores.
    """
    jugador_id = request.GET.get('jugador_id')
    estadistica = request.GET.get('estadistica')
    posicion = request.GET.get('posicion')
    
    if not jugador_id or not estadistica:
        return JsonResponse({'success': False, 'error': 'Faltan parámetros obligatorios'})

    # Mapeo de nombres de estadística a campos del modelo
    mapeo_estadisticas = {
        'Goles': 'goals',
        'Goles esperados (xG)': 'expected_goals_xg',
        'Tiros al arco': 'shots_on_target',
        'Tiros totales': 'shots',
        'Asistencias': 'assists',
        'Penales a favor': 'penalties_awarded',
        'Ocasiones claras falladas': 'big_chances_missed',
        'Goles concedidos': 'goals_conceded',
        'Vallas invictas': 'clean_sheets',
        'xG concedido': 'expected_goals_conceded_xgc',
        'Entradas exitosas': 'tackles_won',
        'Intercepciones': 'interceptions',
        'Despejes': 'blocked',
        'Recuperaciones último tercio': 'recoveries',
        'Atajadas': 'saves',
        'Pases precisos por partido': 'successful_passes',
        'Precisión de pases': 'pass_accuracy_outfield',
        'Pases largos precisos': 'accurate_long_balls_outfield',
        'Centros precisos': 'successful_crosses',
        'Ocasiones creadas': 'chances_created',
        'Toques en área rival': 'touches_in_opposition_box',
        'Tiros de esquina': 'corners_taken',
        'Rating': 'average_rating',
        'Partidos jugados': 'appearances',
        'Minutos jugados': 'minutes_played',
        'Posesión promedio': 'possession_percentage',
        'Toques totales': 'touches',
        'Duelos ganados': 'duels_won_percentage',
        'Duelos aéreos ganados': 'aerial_duels_won_percentage',
        'Faltas por partido': 'fouls_committed',
        'Tarjetas amarillas': 'yellow_cards',
        'Tarjetas rojas': 'red_cards',
    }
    
    campo_bd = mapeo_estadisticas.get(estadistica, 'goals')
    
    try:
        jugador = Jugador.objects.get(id=jugador_id)
        
        # Si no se especifica posición, usar la primera del jugador
        if not posicion:
            posiciones_jugador = [p.strip() for p in jugador.posicion.split(',')]
            posicion = posiciones_jugador[0] if posiciones_jugador else 'ST'
        
        # Filtrar jugadores por posición
        jugadores_posicion = Jugador.objects.filter(posicion__icontains=posicion)
        stats_qs = EstadisticasJugador.objects.filter(
            jugador__in=jugadores_posicion
        ).exclude(**{f"{campo_bd}__isnull": True})
        
        # Obtener todos los valores de la estadística
        valores = [float(getattr(stat, campo_bd, 0)) for stat in stats_qs]
        valores = sorted([v for v in valores if v is not None])
        
        if len(valores) < 5:
            return JsonResponse({
                'success': False, 
                'error': f'No hay suficientes datos para {estadistica} en posición {posicion}'
            })
        
        # Calcular estadísticas para el boxplot
        import numpy as np
        q1 = np.percentile(valores, 25)
        median = np.percentile(valores, 50)
        q3 = np.percentile(valores, 75)
        iqr = q3 - q1
        lower_whisker = max(min(valores), q1 - 1.5 * iqr)
        upper_whisker = min(max(valores), q3 + 1.5 * iqr)
        
        # Valor del jugador actual
        try:
            jugador_stats = EstadisticasJugador.objects.get(jugador=jugador)
            valor_jugador = float(getattr(jugador_stats, campo_bd, 0))
        except EstadisticasJugador.DoesNotExist:
            valor_jugador = None
        
        return JsonResponse({
            'success': True,
            'stat': estadistica,
            'posicion': posicion,
            'box': [lower_whisker, q1, median, q3, upper_whisker],
            'valor_jugador': valor_jugador,
            'total_jugadores': len(valores),
            'jugador_nombre': jugador.nombre
        })
        
    except Jugador.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Jugador no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
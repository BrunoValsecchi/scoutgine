from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Jugador, EstadisticasJugador  # Cambiar JugadorStats por EstadisticasJugador
import json

def grafico_jugador_view(request, jugador_id, estadistica):
    """
    Vista para mostrar el gráfico de una estadística específica de un jugador
    """
    try:
        jugador = get_object_or_404(Jugador, id=jugador_id)
        
        # Obtener datos históricos de la estadística
        datos_grafico = obtener_datos_estadistica(jugador, estadistica)
        
        context = {
            'jugador': jugador,
            'estadistica': estadistica,
            'datos_json': json.dumps(datos_grafico),  # Para pasar al JS
        }
        
        return render(request, 'estadistica_jugador.html', context)
        
    except Exception as e:
        # En caso de error, redirige a la página del jugador
        return redirect('jugador_detalle', jugador_id=jugador_id)

def obtener_datos_estadistica(jugador, estadistica):
    """
    Función que obtiene los datos históricos de una estadística específica
    """
    # Mapeo de nombres de estadísticas a campos del modelo EstadisticasJugador
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
        return {
            'labels': [],
            'data': [],
            'error': f'Estadística "{estadistica}" no encontrada'
        }
    
    try:
        # Obtener estadísticas del jugador
        # Como parece que solo tienes una estadística por jugador, no histórica
        stats_jugador = EstadisticasJugador.objects.filter(jugador=jugador).first()
        
        if stats_jugador and hasattr(stats_jugador, campo):
            # Como no tienes datos históricos, generar datos de ejemplo
            valor_actual = getattr(stats_jugador, campo, 0)
            
            # Generar datos de ejemplo para mostrar evolución
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
        
    except Exception as e:
        # Si hay error, generar datos de ejemplo
        return generar_datos_ejemplo(estadistica, jugador)

def generar_evolucion_ejemplo(valor_base, num_puntos):
    """
    Genera una evolución de ejemplo basada en un valor base
    """
    import random
    
    if not valor_base:
        valor_base = 1
    
    datos = []
    valor_actual = valor_base
    
    for i in range(num_puntos):
        # Variación aleatoria del ±20%
        variacion = random.uniform(-0.2, 0.2)
        valor_actual = max(0, valor_actual * (1 + variacion))
        
        # Redondear según el tipo de estadística
        if valor_base >= 10:
            datos.append(round(valor_actual, 1))
        else:
            datos.append(round(valor_actual, 2))
    
    return datos

def generar_datos_ejemplo(estadistica, jugador):
    """
    Genera datos de ejemplo para el gráfico cuando no hay datos
    """
    import random
    
    labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Generar datos de ejemplo basados en el tipo de estadística
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
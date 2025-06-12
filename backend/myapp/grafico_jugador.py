from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Jugador, EstadisticasJugador
import json

def radar_comparacion_view(request):
    """
    Vista para mostrar el radar de comparación de jugadores por posición
    """
    posiciones = [
        ('GK', 'Arquero'),
        ('CB', 'Defensor Central'),
        ('LB', 'Lateral Izquierdo'),
        ('RB', 'Lateral Derecho'),
        ('CMD', 'Mediocampista Central'),
        ('DM', 'Mediocampista Defensivo'),
        ('RM', 'Mediocampista Derecho'),
        ('LM', 'Mediocampista Izquierdo'),
        ('AM', 'Mediocampista Ofensivo'),
        ('LW', 'Extremo Izquierdo'),
        ('RW', 'Extremo Derecho'),
        ('ST', 'Delantero'),
    ]
    
    context = {
        'posiciones': posiciones,
    }
    
    return render(request, 'radar_comparacion.html', context)

def obtener_jugadores_por_posicion(request):
    """
    API para obtener jugadores por posición
    """
    posicion = request.GET.get('posicion')
    
    if not posicion:
        return JsonResponse({'error': 'Posición requerida'}, status=400)
    
    # Buscar jugadores que contengan esa posición en su campo posicion
    jugadores = Jugador.objects.filter(
        posicion__icontains=posicion,
        estadisticasjugador__isnull=False
    ).select_related('equipo').prefetch_related('estadisticasjugador_set')
    
    jugadores_data = []
    for jugador in jugadores:
        try:
            stats = jugador.estadisticasjugador_set.first()
            if stats:
                jugadores_data.append({
                    'id': jugador.id,
                    'nombre': jugador.nombre,
                    'equipo': jugador.equipo.nombre,
                    'posicion': jugador.posicion,
                    'edad': jugador.edad or 0,
                })
        except:
            continue
    
    return JsonResponse({'jugadores': jugadores_data})

def obtener_datos_radar(request):
    """
    API para obtener datos del radar de jugadores seleccionados
    """
    jugadores_ids = request.GET.getlist('jugadores')
    posicion = request.GET.get('posicion')
    
    if not jugadores_ids or not posicion:
        return JsonResponse({'error': 'Jugadores y posición requeridos'}, status=400)
    
    # Obtener estadísticas según la posición
    stats_config = obtener_config_estadisticas_por_posicion(posicion)
    
    jugadores_data = []
    
    for jugador_id in jugadores_ids:
        try:
            jugador = Jugador.objects.get(id=jugador_id)
            stats = EstadisticasJugador.objects.filter(jugador=jugador).first()
            
            if stats:
                datos_jugador = {
                    'nombre': jugador.nombre,
                    'equipo': jugador.equipo.nombre,
                    'color': obtener_color_jugador(len(jugadores_data)),
                    'datos': []
                }
                
                for stat in stats_config['estadisticas']:
                    valor = getattr(stats, stat['campo'], 0) or 0
                    # Normalizar a escala 0-100
                    valor_normalizado = normalizar_valor(valor, stat['max_esperado'])
                    datos_jugador['datos'].append(valor_normalizado)
                
                jugadores_data.append(datos_jugador)
                
        except Jugador.DoesNotExist:
            continue
    
    return JsonResponse({
        'jugadores': jugadores_data,
        'labels': [stat['label'] for stat in stats_config['estadisticas']],
        'posicion': posicion
    })

def obtener_config_estadisticas_por_posicion(posicion):
    """
    Devuelve las estadísticas relevantes para cada posición
    """
    configs = {
        'GK': {
            'estadisticas': [
                {'campo': 'saves', 'label': 'Atajadas', 'max_esperado': 5},
                {'campo': 'save_percentage', 'label': 'Efectividad', 'max_esperado': 80},
                {'campo': 'clean_sheets', 'label': 'Vallas invictas', 'max_esperado': 15},
                {'campo': 'pass_accuracy', 'label': 'Precisión pases', 'max_esperado': 85},
                {'campo': 'accurate_long_balls', 'label': 'Pases largos', 'max_esperado': 10},
                {'campo': 'goals_prevented', 'label': 'Goles evitados', 'max_esperado': 3},
            ]
        },
        'CB': {
            'estadisticas': [
                {'campo': 'tackles_won', 'label': 'Entradas', 'max_esperado': 3},
                {'campo': 'interceptions', 'label': 'Intercepciones', 'max_esperado': 5},
                {'campo': 'aerial_duels_won_percentage', 'label': 'Duelos aéreos', 'max_esperado': 80},
                {'campo': 'blocked', 'label': 'Despejes', 'max_esperado': 5},
                {'campo': 'pass_accuracy_outfield', 'label': 'Precisión pases', 'max_esperado': 90},
                {'campo': 'accurate_long_balls_outfield', 'label': 'Pases largos', 'max_esperado': 8},
            ]
        },
        'LB': {
            'estadisticas': [
                {'campo': 'tackles_won', 'label': 'Entradas', 'max_esperado': 3},
                {'campo': 'successful_crosses', 'label': 'Centros', 'max_esperado': 3},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.3},
                {'campo': 'pass_accuracy_outfield', 'label': 'Precisión pases', 'max_esperado': 85},
                {'campo': 'interceptions', 'label': 'Intercepciones', 'max_esperado': 4},
                {'campo': 'duels_won_percentage', 'label': 'Duelos ganados', 'max_esperado': 65},
            ]
        },
        'RB': {
            'estadisticas': [
                {'campo': 'tackles_won', 'label': 'Entradas', 'max_esperado': 3},
                {'campo': 'successful_crosses', 'label': 'Centros', 'max_esperado': 3},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.3},
                {'campo': 'pass_accuracy_outfield', 'label': 'Precisión pases', 'max_esperado': 85},
                {'campo': 'interceptions', 'label': 'Intercepciones', 'max_esperado': 4},
                {'campo': 'duels_won_percentage', 'label': 'Duelos ganados', 'max_esperado': 65},
            ]
        },
        'CMD': {
            'estadisticas': [
                {'campo': 'successful_passes', 'label': 'Pases exitosos', 'max_esperado': 50},
                {'campo': 'pass_accuracy_outfield', 'label': 'Precisión pases', 'max_esperado': 90},
                {'campo': 'chances_created', 'label': 'Ocasiones creadas', 'max_esperado': 3},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.4},
                {'campo': 'tackles_won', 'label': 'Entradas', 'max_esperado': 2},
                {'campo': 'interceptions', 'label': 'Intercepciones', 'max_esperado': 3},
            ]
        },
        'DM': {
            'estadisticas': [
                {'campo': 'tackles_won', 'label': 'Entradas', 'max_esperado': 4},
                {'campo': 'interceptions', 'label': 'Intercepciones', 'max_esperado': 5},
                {'campo': 'recoveries', 'label': 'Recuperaciones', 'max_esperado': 8},
                {'campo': 'pass_accuracy_outfield', 'label': 'Precisión pases', 'max_esperado': 88},
                {'campo': 'duels_won_percentage', 'label': 'Duelos ganados', 'max_esperado': 65},
                {'campo': 'fouls_committed', 'label': 'Faltas (inverso)', 'max_esperado': 3},
            ]
        },
        'RM': {
            'estadisticas': [
                {'campo': 'successful_crosses', 'label': 'Centros', 'max_esperado': 2},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.4},
                {'campo': 'chances_created', 'label': 'Ocasiones creadas', 'max_esperado': 2},
                {'campo': 'successful_dribbles', 'label': 'Dribles', 'max_esperado': 3},
                {'campo': 'pass_accuracy_outfield', 'label': 'Precisión pases', 'max_esperado': 80},
                {'campo': 'duels_won_percentage', 'label': 'Duelos ganados', 'max_esperado': 60},
            ]
        },
        'LM': {
            'estadisticas': [
                {'campo': 'successful_crosses', 'label': 'Centros', 'max_esperado': 2},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.4},
                {'campo': 'chances_created', 'label': 'Ocasiones creadas', 'max_esperado': 2},
                {'campo': 'successful_dribbles', 'label': 'Dribles', 'max_esperado': 3},
                {'campo': 'pass_accuracy_outfield', 'label': 'Precisión pases', 'max_esperado': 80},
                {'campo': 'duels_won_percentage', 'label': 'Duelos ganados', 'max_esperado': 60},
            ]
        },
        'AM': {
            'estadisticas': [
                {'campo': 'goals', 'label': 'Goles', 'max_esperado': 0.5},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.6},
                {'campo': 'chances_created', 'label': 'Ocasiones creadas', 'max_esperado': 4},
                {'campo': 'successful_dribbles', 'label': 'Dribles', 'max_esperado': 3},
                {'campo': 'shots', 'label': 'Tiros', 'max_esperado': 3},
                {'campo': 'touches_in_opposition_box', 'label': 'Toques área rival', 'max_esperado': 5},
            ]
        },
        'LW': {
            'estadisticas': [
                {'campo': 'goals', 'label': 'Goles', 'max_esperado': 0.4},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.5},
                {'campo': 'successful_crosses', 'label': 'Centros', 'max_esperado': 2},
                {'campo': 'successful_dribbles', 'label': 'Dribles', 'max_esperado': 4},
                {'campo': 'shots', 'label': 'Tiros', 'max_esperado': 3},
                {'campo': 'duels_won_percentage', 'label': 'Duelos ganados', 'max_esperado': 55},
            ]
        },
        'RW': {
            'estadisticas': [
                {'campo': 'goals', 'label': 'Goles', 'max_esperado': 0.4},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.5},
                {'campo': 'successful_crosses', 'label': 'Centros', 'max_esperado': 2},
                {'campo': 'successful_dribbles', 'label': 'Dribles', 'max_esperado': 4},
                {'campo': 'shots', 'label': 'Tiros', 'max_esperado': 3},
                {'campo': 'duels_won_percentage', 'label': 'Duelos ganados', 'max_esperado': 55},
            ]
        },
        'ST': {
            'estadisticas': [
                {'campo': 'goals', 'label': 'Goles', 'max_esperado': 0.8},
                {'campo': 'expected_goals_xg', 'label': 'xG', 'max_esperado': 0.7},
                {'campo': 'shots', 'label': 'Tiros', 'max_esperado': 4},
                {'campo': 'shots_on_target', 'label': 'Tiros al arco', 'max_esperado': 2},
                {'campo': 'assists', 'label': 'Asistencias', 'max_esperado': 0.3},
                {'campo': 'touches_in_opposition_box', 'label': 'Toques área rival', 'max_esperado': 8},
            ]
        },
    }
    
    return configs.get(posicion, configs['CMD'])  # Default a CMD si no encuentra

def normalizar_valor(valor, max_esperado):
    """
    Normaliza un valor a escala 0-100
    """
    if max_esperado == 0:
        return 0
    
    # Convertir a porcentaje con un máximo
    porcentaje = (float(valor) / max_esperado) * 100
    return min(100, max(0, porcentaje))

def obtener_color_jugador(index):
    """
    Devuelve colores para diferenciar jugadores en el radar
    """
    colores = [
        '#FF6384',  # Rosa
        '#36A2EB',  # Azul
        '#FFCE56',  # Amarillo
        '#4BC0C0',  # Verde agua
        '#9966FF',  # Violeta
        '#FF9F40',  # Naranja
        '#FF6384',  # Rosa (repetir si hay más de 6)
        '#C9CBCF',  # Gris
    ]
    return colores[index % len(colores)]
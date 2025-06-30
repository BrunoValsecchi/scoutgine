from .models import EstadisticasJugador, Jugador
from django.db import connection
from django.db.models import Q
import json

# ✅ DEFINICIÓN DE PERFILES CON ESTADÍSTICAS PRIORIZADAS
PERFILES_JUGADORES = {
    # 🧤 ARQUEROS
    "arquero_tradicional": {
        "posiciones": ["Arquero", "GK", "Goalkeeper"],
        "stats_principales": {
            "saves": 3.0,           # Atajadas (MUY IMPORTANTE)
            "save_percentage": 2.5,  # % de atajadas
            "clean_sheets": 2.0,     # Vallas invictas
            "goals_conceded": -2.0,  # Menos goles = mejor (negativo)
            "punches": 1.5,          # Salidas a puño
            "catches": 1.5           # Atrapadas
        },
        "stats_secundarias": {
            "passes_completed": 0.5,
            "long_balls_accurate": 0.3
        },
        "descripcion": "Arquero tradicional enfocado en atajar y posicionarse"
    },
    
    "arquero_moderno": {
        "posiciones": ["Arquero", "GK", "Goalkeeper"],
        "stats_principales": {
            "saves": 2.5,
            "clean_sheets": 2.0,
            "passes_completed": 2.0,      # Participa en salida
            "long_balls_accurate": 1.8,   # Pases largos precisos
            "distribution_accuracy": 1.5,  # Precisión en distribución
            "sweeper_clearances": 2.2     # Sale del área
        },
        "stats_secundarias": {
            "goals_conceded": -1.5,
            "punches": 1.0
        },
        "descripcion": "Arquero moderno que participa en la salida y sale del área"
    },

    # 🛡️ DEFENSORES
    "lateral_defensivo": {
        "posiciones": ["Defensor", "Defender", "RB", "LB", "Lateral"],
        "stats_principales": {
            "tackles_won": 3.0,           # Entradas exitosas
            "interceptions": 2.5,         # Intercepciones
            "clearances": 2.0,            # Despejes
            "duels_won": 2.2,            # Duelos ganados
            "blocks": 1.8,               # Bloqueos
            "fouls_committed": -1.5       # Menos faltas = mejor
        },
        "stats_secundarias": {
            "passes_completed": 1.0,
            "crosses_attempted": 0.5
        },
        "descripcion": "Lateral defensivo que prioriza marca y orden"
    },
    
    "lateral_ofensivo": {
        "posiciones": ["Defensor", "Defender", "RB", "LB", "Lateral"],
        "stats_principales": {
            "crosses_accurate": 3.0,      # Centros precisos
            "assists": 2.5,              # Asistencias
            "key_passes": 2.0,           # Pases clave
            "dribbles_successful": 1.8,   # Regates exitosos
            "final_third_entries": 2.2    # Llegadas al área rival
        },
        "stats_secundarias": {
            "tackles_won": 1.5,
            "interceptions": 1.2,
            "distance_covered": 1.0
        },
        "descripcion": "Lateral ofensivo que se proyecta al ataque"
    },
    
    "defensor_central_marcador": {
        "posiciones": ["Defensor", "Defender", "CB", "Centro Back"],
        "stats_principales": {
            "tackles_won": 3.0,
            "duels_won": 2.8,
            "aerial_duels_won": 2.5,     # Duelos aéreos
            "clearances": 2.2,
            "blocks": 2.0,
            "interceptions": 1.8
        },
        "stats_secundarias": {
            "fouls_committed": -1.0,
            "passes_completed": 1.0
        },
        "descripcion": "Defensor marcador fuerte en duelos uno contra uno"
    },
    
    "defensor_central_libero": {
        "posiciones": ["Defensor", "Defender", "CB", "Centro Back"],
        "stats_principales": {
            "passes_completed": 3.0,      # Salida limpia
            "long_balls_accurate": 2.5,   # Pases largos
            "interceptions": 2.8,         # Anticipación
            "pass_accuracy": 2.2,         # Precisión de pase
            "progressive_passes": 2.0      # Pases progresivos
        },
        "stats_secundarias": {
            "tackles_won": 1.5,
            "aerial_duels_won": 1.8,
            "clearances": 1.2
        },
        "descripcion": "Defensor líbero técnico con buena salida"
    },

    # ⚙️ MEDIOCAMPISTAS
    "pivote_destructivo": {
        "posiciones": ["Mediocampista", "Midfielder", "DM", "CM"],
        "stats_principales": {
            "tackles_won": 3.0,
            "interceptions": 2.8,
            "balls_recovered": 2.5,       # Recuperaciones
            "duels_won": 2.2,
            "fouls_committed": 1.0,       # Faltas tácticas permitidas
            "yellow_cards": 0.5           # Parte del juego
        },
        "stats_secundarias": {
            "passes_completed": 1.8,
            "pass_accuracy": 1.5
        },
        "descripcion": "Pivote destructivo especializado en cortar el juego"
    },
    
    "pivote_organizador": {
        "posiciones": ["Mediocampista", "Midfielder", "DM", "CM"],
        "stats_principales": {
            "passes_completed": 3.0,
            "pass_accuracy": 2.8,
            "short_passes_accurate": 2.5,
            "long_balls_accurate": 2.0,
            "progressive_passes": 1.8
        },
        "stats_secundarias": {
            "interceptions": 2.0,
            "tackles_won": 1.5,
            "key_passes": 1.2
        },
        "descripcion": "Pivote organizador que controla el juego con pases simples"
    },
    
    "box_to_box": {
        "posiciones": ["Mediocampista", "Midfielder", "CM"],
        "stats_principales": {
            "distance_covered": 3.0,      # Recorrido (versátil)
            "tackles_won": 2.2,
            "key_passes": 2.0,
            "shots": 1.8,
            "assists": 1.8,
            "interceptions": 2.0
        },
        "stats_secundarias": {
            "passes_completed": 2.0,
            "goals": 1.5,
            "duels_won": 1.5
        },
        "descripcion": "Mediocampista box-to-box versátil de área a área"
    },
    
    "organizador_central": {
        "posiciones": ["Mediocampista", "Midfielder", "CM"],
        "stats_principales": {
            "key_passes": 3.0,           # Pases clave
            "assists": 2.5,
            "pass_accuracy": 2.8,
            "progressive_passes": 2.2,
            "through_balls": 2.0         # Pases filtrados
        },
        "stats_secundarias": {
            "passes_completed": 2.5,
            "long_balls_accurate": 1.5,
            "shots": 1.0
        },
        "descripcion": "Organizador que controla el ritmo del juego"
    },
    
    "enganche_clasico": {
        "posiciones": ["Mediocampista", "Midfielder", "AM"],
        "stats_principales": {
            "key_passes": 3.5,           # MUY IMPORTANTE
            "assists": 3.0,
            "through_balls": 2.8,
            "chances_created": 2.5,       # Ocasiones creadas
            "pass_accuracy": 2.0
        },
        "stats_secundarias": {
            "goals": 1.5,
            "shots": 1.2,
            "dribbles_successful": 1.8
        },
        "descripcion": "Enganche clásico creador de juego y último pase"
    },
    
    "mediapunta_llegador": {
        "posiciones": ["Mediocampista", "Midfielder", "AM"],
        "stats_principales": {
            "goals": 3.0,               # Definición
            "shots": 2.5,
            "shots_on_target": 2.8,
            "penalty_area_entries": 2.2, # Llegadas al área
            "assists": 2.0
        },
        "stats_secundarias": {
            "key_passes": 2.0,
            "dribbles_successful": 1.5,
            "distance_covered": 1.2
        },
        "descripcion": "Mediapunta que llega al área y define"
    },

    # 🎯 EXTREMOS
    "extremo_desborde": {
        "posiciones": ["Delantero", "Attacker", "LW", "RW"],
        "stats_principales": {
            "dribbles_successful": 3.5,   # Regate (MUY IMPORTANTE)
            "crosses_accurate": 2.8,      # Centros precisos
            "sprint_speed": 2.5,          # Velocidad
            "final_third_entries": 2.2,
            "duels_won": 2.0
        },
        "stats_secundarias": {
            "assists": 2.0,
            "goals": 1.5,
            "distance_covered": 1.8
        },
        "descripcion": "Extremo de desborde con velocidad y regate"
    },
    
    "extremo_inverso": {
        "posiciones": ["Delantero", "Attacker", "LW", "RW"],
        "stats_principales": {
            "goals": 3.0,               # Definición (pierna cambiada)
            "shots": 2.8,
            "shots_on_target": 2.5,
            "dribbles_successful": 2.2,
            "cut_inside_attempts": 2.0   # Jugadas hacia adentro
        },
        "stats_secundarias": {
            "assists": 1.8,
            "key_passes": 1.5,
            "crosses_accurate": 1.0
        },
        "descripcion": "Extremo inverso que busca el remate a pierna cambiada"
    },

    # 🔥 DELANTEROS
    "delantero_area": {
        "posiciones": ["Delantero", "Attacker", "ST", "CF"],
        "stats_principales": {
            "goals": 3.5,               # Goles (MUY IMPORTANTE)
            "shots_on_target": 3.0,     # Tiros al arco
            "penalty_area_touches": 2.8, # Toques en el área
            "aerial_duels_won": 2.5,    # Juego aéreo
            "shot_accuracy": 2.2
        },
        "stats_secundarias": {
            "assists": 1.5,
            "key_passes": 1.0,
            "hold_up_play": 2.0
        },
        "descripcion": "Delantero de área especializado en definir"
    },
    
    "delantero_movil": {
        "posiciones": ["Delantero", "Attacker", "ST", "CF"],
        "stats_principales": {
            "goals": 2.8,
            "assists": 2.5,             # Se asocia
            "key_passes": 2.2,
            "dribbles_successful": 2.0,
            "distance_covered": 2.2,     # Movilidad
            "link_up_play": 2.5         # Juego asociativo
        },
        "stats_secundarias": {
            "shots": 2.0,
            "duels_won": 1.5,
            "passes_completed": 1.8
        },
        "descripcion": "Delantero móvil que se asocia y genera juego"
    },
    
    "falso_nueve": {
        "posiciones": ["Delantero", "Attacker", "ST", "CF"],
        "stats_principales": {
            "key_passes": 3.0,          # Creación desde posición de 9
            "assists": 2.8,
            "pass_accuracy": 2.5,
            "drop_back_frequency": 2.2,  # Se retrasa
            "space_creation": 2.0        # Genera espacios
        },
        "stats_secundarias": {
            "goals": 2.0,
            "dribbles_successful": 1.8,
            "shots": 1.5
        },
        "descripcion": "Falso 9 que se retrasa y genera espacios"
    }
}


def recomendar_jugadores_por_perfil(perfil_nombre, limite=10, equipo_excluir=None):
    """
    Recomienda jugadores según un perfil específico
    """
    
    if perfil_nombre not in PERFILES_JUGADORES:
        return []
    
    perfil = PERFILES_JUGADORES[perfil_nombre]
    
    # ✅ 1. FILTRAR JUGADORES POR POSICIÓN
    posiciones_query = Q()
    for posicion in perfil["posiciones"]:
        posiciones_query |= Q(posicion__icontains=posicion)
    
    jugadores_query = Jugador.objects.filter(posiciones_query)
    
    if equipo_excluir:
        jugadores_query = jugadores_query.exclude(equipo_id=equipo_excluir)
    
    jugadores = list(jugadores_query)
    
    if not jugadores:
        return []
    
    # ✅ 2. OBTENER ESTADÍSTICAS DE TODOS LOS JUGADORES
    jugador_ids = [j.id for j in jugadores]
    
    stats_dict = {}
    try:
        stats_queryset = EstadisticasJugador.objects.filter(jugador_id__in=jugador_ids)
        for stat in stats_queryset:
            stats_dict[stat.jugador_id] = stat
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        return []
    
    # ✅ 3. CALCULAR PUNTUACIÓN PARA CADA JUGADOR
    jugadores_puntuados = []
    
    for jugador in jugadores:
        if jugador.id not in stats_dict:
            continue
            
        stats = stats_dict[jugador.id]
        puntuacion = calcular_puntuacion_perfil(stats, perfil)
        
        if puntuacion > 0:  # Solo incluir jugadores con puntuación positiva
            jugadores_puntuados.append({
                'jugador': jugador,
                'puntuacion': puntuacion,
                'perfil': perfil_nombre,
                'descripcion_perfil': perfil['descripcion'],
                'stats_destacadas': obtener_stats_destacadas(stats, perfil)
            })
    
    # ✅ 4. ORDENAR POR PUNTUACIÓN Y LIMITAR
    jugadores_puntuados.sort(key=lambda x: x['puntuacion'], reverse=True)
    
    return jugadores_puntuados[:limite]


def calcular_puntuacion_perfil(stats, perfil):
    """
    Calcula la puntuación de un jugador según un perfil específico
    """
    puntuacion_total = 0
    total_peso = 0
    
    # ✅ ESTADÍSTICAS PRINCIPALES (mayor peso)
    for stat_name, peso in perfil["stats_principales"].items():
        valor = getattr(stats, stat_name, None)
        if valor is not None:
            if peso < 0:  # Para estadísticas donde menor es mejor
                puntuacion_total += (100 - min(valor, 100)) * abs(peso)
            else:
                puntuacion_total += min(valor, 100) * peso
            total_peso += abs(peso)
    
    # ✅ ESTADÍSTICAS SECUNDARIAS (menor peso)
    for stat_name, peso in perfil.get("stats_secundarias", {}).items():
        valor = getattr(stats, stat_name, None)
        if valor is not None:
            if peso < 0:
                puntuacion_total += (100 - min(valor, 100)) * abs(peso)
            else:
                puntuacion_total += min(valor, 100) * peso
            total_peso += abs(peso)
    
    # ✅ CALCULAR PUNTUACIÓN PROMEDIO PONDERADA
    if total_peso > 0:
        puntuacion_promedio = puntuacion_total / total_peso
        return round(puntuacion_promedio, 1)
    
    return 0


def obtener_stats_destacadas(stats, perfil):
    """
    Obtiene las estadísticas más destacadas del jugador según el perfil
    """
    stats_destacadas = {}
    
    # Tomar las 3 estadísticas principales más importantes
    stats_principales = sorted(perfil["stats_principales"].items(), 
                             key=lambda x: abs(x[1]), reverse=True)[:3]
    
    for stat_name, peso in stats_principales:
        valor = getattr(stats, stat_name, None)
        if valor is not None:
            stats_destacadas[stat_name] = {
                'valor': valor,
                'peso': peso,
                'nombre_friendly': formatear_nombre_stat(stat_name)
            }
    
    return stats_destacadas


def formatear_nombre_stat(stat_name):
    """
    Convierte nombres de estadísticas a formato amigable
    """
    traducciones = {
        'goals': 'Goles',
        'assists': 'Asistencias', 
        'shots': 'Tiros',
        'shots_on_target': 'Tiros al arco',
        'key_passes': 'Pases clave',
        'passes_completed': 'Pases completados',
        'pass_accuracy': 'Precisión de pase',
        'tackles_won': 'Entradas exitosas',
        'interceptions': 'Intercepciones',
        'dribbles_successful': 'Regates exitosos',
        'crosses_accurate': 'Centros precisos',
        'clearances': 'Despejes',
        'saves': 'Atajadas',
        'clean_sheets': 'Vallas invictas',
        'aerial_duels_won': 'Duelos aéreos ganados',
        'distance_covered': 'Distancia recorrida',
        'duels_won': 'Duelos ganados',
        'through_balls': 'Pases filtrados',
        'chances_created': 'Ocasiones creadas',
        'progressive_passes': 'Pases progresivos',
        'long_balls_accurate': 'Pases largos precisos'
    }
    
    return traducciones.get(stat_name, stat_name.replace('_', ' ').title())


def obtener_perfiles_disponibles():
    """
    Devuelve todos los perfiles disponibles organizados por posición
    """
    perfiles_organizados = {
        "🧤 Arqueros": [],
        "🛡️ Defensores": [],
        "⚙️ Mediocampistas": [],
        "🎯 Extremos": [],
        "🔥 Delanteros": []
    }
    
    for perfil_key, perfil_data in PERFILES_JUGADORES.items():
        descripcion = perfil_data['descripcion']
        
        if any(pos in perfil_data['posiciones'] for pos in ['Arquero', 'GK']):
            perfiles_organizados["🧤 Arqueros"].append({
                'key': perfil_key,
                'nombre': perfil_key.replace('_', ' ').title(),
                'descripcion': descripcion
            })
        elif any(pos in perfil_data['posiciones'] for pos in ['Defensor', 'Defender', 'RB', 'LB', 'CB']):
            perfiles_organizados["🛡️ Defensores"].append({
                'key': perfil_key,
                'nombre': perfil_key.replace('_', ' ').title(),
                'descripcion': descripcion
            })
        elif any(pos in perfil_data['posiciones'] for pos in ['Mediocampista', 'Midfielder', 'DM', 'CM', 'AM']):
            perfiles_organizados["⚙️ Mediocampistas"].append({
                'key': perfil_key,
                'nombre': perfil_key.replace('_', ' ').title(),
                'descripcion': descripcion
            })
        elif any(pos in perfil_data['posiciones'] for pos in ['LW', 'RW']) and 'ST' not in perfil_data['posiciones']:
            perfiles_organizados["🎯 Extremos"].append({
                'key': perfil_key,
                'nombre': perfil_key.replace('_', ' ').title(),
                'descripcion': descripcion
            })
        else:
            perfiles_organizados["🔥 Delanteros"].append({
                'key': perfil_key,
                'nombre': perfil_key.replace('_', ' ').title(),
                'descripcion': descripcion
            })
    
    return perfiles_organizados
from django.shortcuts import render
from .models import Equipo, Jugador, EstadisticasEquipo
import json

GRUPOS_STATS_EQUIPOS = {
    "Ofensivos": [
        ("Goles por partido", "goals_per_match"),
        ("Tiros al arco por partido", "shots_on_target_per_match"),
        ("Ocasiones claras", "big_chances"),
        ("Ocasiones claras falladas", "big_chances_missed"),
        ("Goles esperados (xG)", "expected_goals_xg"),
        ("Penales a favor", "penalties_awarded"),
    ],
    "Defensivos": [
        ("Goles concededs por partido", "goals_conceded_per_match"),
        ("Vallas invictas", "clean_sheets"),
        ("xG conceded", "xg_conceded"),
        ("Intercepciones por partido", "interceptions_per_match"),
        ("Entradas exitosas por partido", "successful_tackles_per_match"),
        ("Despejes por partido", "clearances_per_match"),
        ("Recuperaciones en el último tercio", "possession_won_final_3rd_per_match"),
        ("Atajadas por partido", "saves_per_match"),
    ],
    "Creación": [
        ("Pases precisos por partido", "accurate_passes_per_match"),
        ("Pases largos precisos por partido", "accurate_long_balls_per_match"),
        ("Centros precisos por partido", "accurate_crosses_per_match"),
        ("Toques en el área rival", "touches_in_opposition_box"),
        ("Tiros de esquina", "corners"),
    ],
    "Generales": [
        ("Rating", "fotmob_rating"),
        ("Posesión promedio", "average_possession"),
        ("Faltas por partido", "fouls_per_match"),
        ("Tarjetas amarillas", "yellow_cards"),
        ("Tarjetas rojas", "red_cards"),
    ]
}

GRUPOS_STATS_JUGADORES = {
    "Arqueros": [
        ("Atajadas", "saves"),
        ("Porcentaje de atajadas", "save_percentage"),
        ("Goles prevenidos", "goals_prevented"),
        ("Vallas invictas", "clean_sheets"),
        ("Salidas en alto", "high_claim"),
        ("Goles recibidos", "goals_conceded"),
    ],
    "Ofensivos": [
        ("Goles", "goals"),
        ("xG", "expected_goals_xg"),
        ("xG en el arco", "xg_on_target_xgot"),
        ("xG sin penales", "non_penalty_xg"),
        ("Disparos", "shots"),
        ("Disparos al arco", "shots_on_target"),
        ("Asistencias", "assists"),
        ("xA", "expected_assists_xa"),
        ("Chances creadas", "chances_created"),
    ],
    "Pases": [
        ("Pases exitosos", "successful_passes"),
        ("Precisión de pase", "pass_accuracy"),
        ("Precisión de pase (campo)", "pass_accuracy_outfield"),
        ("Pases largos precisos", "accurate_long_balls"),
        ("Precisión pases largos", "long_ball_accuracy"),
        ("Centros exitosos", "successful_crosses"),
        ("Precisión de centros", "cross_accuracy"),
    ],
    "Dribbling": [
        ("Regates exitosos", "successful_dribbles"),
        ("Éxito en regates", "dribble_success"),
        ("Toques", "touches"),
        ("Toques en área rival", "touches_in_opposition_box"),
    ],
    "Defensivos": [
        ("Entradas ganadas", "tackles_won"),
        ("Porcentaje entradas ganadas", "tackles_won_percentage"),
        ("Duelos ganados", "duels_won"),
        ("Porcentaje duelos ganados", "duels_won_percentage"),
        ("Duelos aéreos ganados", "aerial_duels_won"),
        ("Porcentaje duelos aéreos", "aerial_duels_won_percentage"),
        ("Intercepciones", "interceptions"),
        ("Bloqueos", "blocked"),
        ("Recuperaciones", "recoveries"),
        ("Recuperaciones en 1/3 final", "possession_won_final_3rd"),
    ],
    "Disciplina": [
        ("Faltas recibidas", "fouls_won"),
        ("Faltas cometidas", "fouls_committed"),
        ("Penales provocados", "penalties_awarded"),
        ("Pérdidas de balón", "dispossessed"),
        ("Regateado", "dribbled_past"),
        ("Tarjetas amarillas", "yellow_cards"),
        ("Tarjetas rojas", "red_cards"),
        ("Errores que llevaron a gol", "error_led_to_goal"),
    ]
}

# ✅ AGREGAR PARA COMPATIBILIDAD CON views.py
GRUPOS_STATS = GRUPOS_STATS_EQUIPOS

def comparacion(request):
    print("🚀 Iniciando función comparación OPTIMIZADA...")
    
    try:
        # ✅ CARGAR EQUIPOS (optimización: solo campos necesarios)
        equipos_query = Equipo.objects.only('id', 'nombre', 'nombre_corto').order_by('nombre')
        equipos = []
        equipos_data = []
        
        print(f"📊 Cargando {equipos_query.count()} equipos desde la BD...")
        
        for equipo in equipos_query:
            # Para el template (solo básico)
            equipos.append({
                'id': equipo.id,
                'nombre': equipo.nombre
            })
            
            # ✅ BUSCAR ESTADÍSTICAS DE FORMA OPTIMIZADA
            try:
                stats = EstadisticasEquipo.objects.filter(equipo=equipo).first()
                
                if stats:
                    # ✅ CONVERTIR DATOS REALES A FORMATO NECESARIO
                    equipo_stats = {
                        'id': equipo.id,
                        'nombre': equipo.nombre,
                        'nombre_corto': equipo.nombre_corto or equipo.nombre[:15],
                        
                        # ✅ CAMPOS OFENSIVOS
                        'goals_per_match': float(stats.goals_per_match or 0),
                        'shots_on_target_per_match': float(stats.shots_on_target_per_match or 0),
                        'big_chances': int(stats.big_chances or 0),
                        'big_chances_missed': int(stats.big_chances_missed or 0),
                        'expected_goals_xg': float(stats.expected_goals_xg or 0),
                        'penalties_awarded': int(stats.penalties_awarded or 0),
                        
                        # ✅ CAMPOS DEFENSIVOS
                        'goals_conceded_per_match': float(stats.goals_conceded_per_match or 0),
                        'clean_sheets': int(stats.clean_sheets or 0),
                        'xg_conceded': float(getattr(stats, 'xg_conceded', 0) or 0),
                        'interceptions_per_match': int(getattr(stats, 'interceptions_per_match', 0) or 0),
                        'successful_tackles_per_match': float(getattr(stats, 'successful_tackles_per_match', 0) or 0),
                        'clearances_per_match': float(getattr(stats, 'clearances_per_match', 0) or 0),
                        'possession_won_final_3rd_per_match': float(getattr(stats, 'possession_won_final_3rd_per_match', 0) or 0),
                        'saves_per_match': float(getattr(stats, 'saves_per_match', 0) or 0),
                        
                        # ✅ CAMPOS DE CREACIÓN
                        'accurate_passes_per_match': float(getattr(stats, 'accurate_passes_per_match', 0) or 0),
                        'accurate_long_balls_per_match': float(getattr(stats, 'accurate_long_balls_per_match', 0) or 0),
                        'accurate_crosses_per_match': float(getattr(stats, 'accurate_crosses_per_match', 0) or 0),
                        'touches_in_opposition_box': int(getattr(stats, 'touches_in_opposition_box', 0) or 0),
                        'corners': int(getattr(stats, 'corners', 0) or 0),
                        
                        # ✅ CAMPOS GENERALES
                        'fotmob_rating': float(getattr(stats, 'fotmob_rating', 0) or 0),
                        'average_possession': _convertir_posesion(getattr(stats, 'average_possession', 0)),
                        'fouls_per_match': float(getattr(stats, 'fouls_per_match', 0) or 0),
                        'yellow_cards': int(getattr(stats, 'yellow_cards', 0) or 0),
                        'red_cards': int(getattr(stats, 'red_cards', 0) or 0),
                    }
                    
                else:
                    # ✅ VALORES POR DEFECTO SI NO HAY ESTADÍSTICAS
                    equipo_stats = {
                        'id': equipo.id,
                        'nombre': equipo.nombre,
                        'nombre_corto': equipo.nombre_corto or equipo.nombre[:15],
                        'goals_per_match': 0.0,
                        'shots_on_target_per_match': 0.0,
                        'big_chances': 0,
                        'big_chances_missed': 0,
                        'expected_goals_xg': 0.0,
                        'penalties_awarded': 0,
                        'goals_conceded_per_match': 0.0,
                        'clean_sheets': 0,
                        'xg_conceded': 0.0,
                        'interceptions_per_match': 0,
                        'successful_tackles_per_match': 0.0,
                        'clearances_per_match': 0.0,
                        'possession_won_final_3rd_per_match': 0.0,
                        'saves_per_match': 0.0,
                        'accurate_passes_per_match': 0.0,
                        'accurate_long_balls_per_match': 0.0,
                        'accurate_crosses_per_match': 0.0,
                        'touches_in_opposition_box': 0,
                        'corners': 0,
                        'fotmob_rating': 0.0,
                        'average_possession': 0.0,
                        'fouls_per_match': 0.0,
                        'yellow_cards': 0,
                        'red_cards': 0,
                    }
                    
            except Exception as e:
                print(f"❌ Error obteniendo estadísticas para {equipo.nombre}: {e}")
                continue
            
            equipos_data.append(equipo_stats)
        
        print(f"📊 Equipos procesados: {len(equipos_data)}")
        
        # ✅ CALCULAR PERCENTILES DE FORMA OPTIMIZADA
        print("📊 Calculando percentiles...")
        
        # Recopilar todos los valores por campo de una vez
        valores_por_campo = {}
        for grupo in GRUPOS_STATS_EQUIPOS.values():
            for nombre, campo in grupo:
                valores_por_campo[campo] = [equipo[campo] for equipo in equipos_data if equipo[campo] is not None]
        
        # Agregar percentiles a cada equipo
        for equipo_data in equipos_data:
            for campo, todos_valores in valores_por_campo.items():
                if todos_valores:  # Solo si hay valores
                    valor_original = equipo_data[campo]
                    percentil = calcular_percentil(valor_original, todos_valores)
                    equipo_data[f"{campo}_percentil"] = percentil
                else:
                    equipo_data[f"{campo}_percentil"] = 50  # Default
        
        # ✅ CARGAR TODOS LOS JUGADORES CON ESTADÍSTICAS
        print("👥 Cargando TODOS los jugadores CON ESTADÍSTICAS...")
        
        from .models import EstadisticasJugador
        
        # ✅ CONSULTA OPTIMIZADA CON ESTADÍSTICAS
        jugadores_query = Jugador.objects.select_related('equipo').only(
            'id', 'nombre', 'equipo__id', 'equipo__nombre', 'posicion'
        ).filter(
            equipo__isnull=False  # ✅ SOLO JUGADORES CON EQUIPO VÁLIDO
        ).order_by('equipo__nombre', 'nombre')
        
        # ✅ DEBUG: Ver estructura ANTES de procesar
        total_jugadores = jugadores_query.count()
        print(f"📊 Total de jugadores con equipo en BD: {total_jugadores}")
        
        # ✅ CARGAR TODAS LAS ESTADÍSTICAS DE JUGADORES DE UNA VEZ
        estadisticas_jugadores = {}
        try:
            estadisticas_query = EstadisticasJugador.objects.select_related('jugador').all()
            print(f"📊 Cargando {estadisticas_query.count()} estadísticas de jugadores...")
            
            for stat in estadisticas_query:
                estadisticas_jugadores[stat.jugador.id] = stat
                
            print(f"📊 Estadísticas de jugadores cargadas: {len(estadisticas_jugadores)}")
            
        except Exception as e:
            print(f"❌ Error cargando estadísticas de jugadores: {e}")
            estadisticas_jugadores = {}
        
        primer_jugador = jugadores_query.first()
        if primer_jugador:
            print(f"🔍 DEBUG JUGADOR EJEMPLO:")
            print(f"   ID: {primer_jugador.id}")
            print(f"   Nombre: {primer_jugador.nombre}")
            print(f"   Equipo: {primer_jugador.equipo}")
            print(f"   Equipo ID: {primer_jugador.equipo.id if primer_jugador.equipo else 'None'}")
            print(f"   Posición: {primer_jugador.posicion}")
            print(f"   Tiene estadísticas: {primer_jugador.id in estadisticas_jugadores}")
        
        # ✅ PROCESAR TODOS LOS JUGADORES CON ESTADÍSTICAS
        jugadores = []
        jugadores_data = []
        jugadores_por_equipo = {}
        
        print(f"👥 Procesando TODOS los {total_jugadores} jugadores...")
        
        for jugador in jugadores_query:
            # Para el template (básico)
            jugadores.append({
                'id': jugador.id,
                'nombre': jugador.nombre,
                'equipo': {'nombre': jugador.equipo.nombre if jugador.equipo else 'Sin equipo'}
            })
            
            # ✅ OBTENER ESTADÍSTICAS SI EXISTEN
            stats = estadisticas_jugadores.get(jugador.id)
            
            # ✅ PARA JAVASCRIPT CON DATOS COMPLETOS Y ESTADÍSTICAS
            jugador_data = {
                'id': jugador.id,
                'nombre': jugador.nombre,
                'equipo': jugador.equipo.nombre if jugador.equipo else 'Sin equipo',
                'equipo_id': jugador.equipo.id if jugador.equipo else None,
                'posicion': jugador.posicion or 'N/A',
            }
            
            # ✅ AGREGAR ESTADÍSTICAS SI EXISTEN
            if stats:
                # ESTADÍSTICAS DE ARQUERO
                jugador_data.update({
                    'saves': float(stats.saves or 0),
                    'save_percentage': float(stats.save_percentage or 0),
                    'goals_prevented': float(stats.goals_prevented or 0),
                    'clean_sheets': int(stats.clean_sheets or 0),
                    'high_claim': int(stats.high_claim or 0),
                    'goals_conceded': int(stats.goals_conceded or 0),
                    
                    # ESTADÍSTICAS OFENSIVAS
                    'goals': int(stats.goals or 0),
                    'expected_goals_xg': float(stats.expected_goals_xg or 0),
                    'xg_on_target_xgot': float(stats.xg_on_target_xgot or 0),
                    'non_penalty_xg': float(stats.non_penalty_xg or 0),
                    'shots': int(stats.shots or 0),
                    'shots_on_target': int(stats.shots_on_target or 0),
                    'assists': int(stats.assists or 0),
                    'expected_assists_xa': float(stats.expected_assists_xa or 0),
                    'chances_created': int(stats.chances_created or 0),
                    
                    # ESTADÍSTICAS DE PASE
                    'successful_passes': int(stats.successful_passes or 0),
                    'pass_accuracy': float(stats.pass_accuracy or 0),
                    'pass_accuracy_outfield': float(stats.pass_accuracy_outfield or 0),
                    'accurate_long_balls': int(stats.accurate_long_balls or 0),
                    'long_ball_accuracy': float(stats.long_ball_accuracy or 0),
                    'successful_crosses': int(stats.successful_crosses or 0),
                    'cross_accuracy': float(stats.cross_accuracy or 0),
                    
                    # ESTADÍSTICAS DE DRIBBLING
                    'successful_dribbles': int(stats.successful_dribbles or 0),
                    'dribble_success': float(stats.dribble_success or 0),
                    'touches': int(stats.touches or 0),
                    'touches_in_opposition_box': int(stats.touches_in_opposition_box or 0),
                    
                    # ESTADÍSTICAS DEFENSIVAS
                    'tackles_won': int(stats.tackles_won or 0),
                    'tackles_won_percentage': float(stats.tackles_won_percentage or 0),
                    'duels_won': int(stats.duels_won or 0),
                    'duels_won_percentage': float(stats.duels_won_percentage or 0),
                    'aerial_duels_won': int(stats.aerial_duels_won or 0),
                    'aerial_duels_won_percentage': float(stats.aerial_duels_won_percentage or 0),
                    'interceptions': int(stats.interceptions or 0),
                    'blocked': int(stats.blocked or 0),
                    'recoveries': int(stats.recoveries or 0),
                    'possession_won_final_3rd': int(stats.possession_won_final_3rd or 0),
                    
                    # ESTADÍSTICAS DISCIPLINARIAS
                    'fouls_won': int(stats.fouls_won or 0),
                    'fouls_committed': int(stats.fouls_committed or 0),
                    'penalties_awarded': int(stats.penalties_awarded or 0),
                    'dispossessed': int(stats.dispossessed or 0),
                    'dribbled_past': int(stats.dribbled_past or 0),
                    'yellow_cards': int(stats.yellow_cards or 0),
                    'red_cards': int(stats.red_cards or 0),
                    'error_led_to_goal': int(stats.error_led_to_goal or 0),
                })
            else:
                # ✅ ESTADÍSTICAS EN CERO SI NO TIENE DATOS
                jugador_data.update({
                    # ESTADÍSTICAS DE ARQUERO
                    'saves': 0, 'save_percentage': 0, 'goals_prevented': 0,
                    'clean_sheets': 0, 'high_claim': 0, 'goals_conceded': 0,
                    
                    # ESTADÍSTICAS OFENSIVAS
                    'goals': 0, 'expected_goals_xg': 0, 'xg_on_target_xgot': 0,
                    'non_penalty_xg': 0, 'shots': 0, 'shots_on_target': 0,
                    'assists': 0, 'expected_assists_xa': 0, 'chances_created': 0,
                    
                    # ESTADÍSTICAS DE PASE
                    'successful_passes': 0, 'pass_accuracy': 0, 'pass_accuracy_outfield': 0,
                    'accurate_long_balls': 0, 'long_ball_accuracy': 0,
                    'successful_crosses': 0, 'cross_accuracy': 0,
                    
                    # ESTADÍSTICAS DE DRIBBLING
                    'successful_dribbles': 0, 'dribble_success': 0,
                    'touches': 0, 'touches_in_opposition_box': 0,
                    
                    # ESTADÍSTICAS DEFENSIVAS
                    'tackles_won': 0, 'tackles_won_percentage': 0, 'duels_won': 0,
                    'duels_won_percentage': 0, 'aerial_duels_won': 0,
                    'aerial_duels_won_percentage': 0, 'interceptions': 0,
                    'blocked': 0, 'recoveries': 0, 'possession_won_final_3rd': 0,
                    
                    # ESTADÍSTICAS DISCIPLINARIAS
                    'fouls_won': 0, 'fouls_committed': 0, 'penalties_awarded': 0,
                    'dispossessed': 0, 'dribbled_past': 0, 'yellow_cards': 0,
                    'red_cards': 0, 'error_led_to_goal': 0,
                })
            
            jugadores_data.append(jugador_data)
            
            # ✅ CONTAR POR EQUIPO PARA DEBUG COMPLETO
            if jugador.equipo:
                equipo_id = jugador.equipo.id
                equipo_nombre = jugador.equipo.nombre
                
                if equipo_id not in jugadores_por_equipo:
                    jugadores_por_equipo[equipo_id] = {
                        'nombre': equipo_nombre,
                        'jugadores': [],
                        'posiciones': set(),
                        'jugadores_cb': [],
                        'con_estadisticas': 0
                    }
                
                jugadores_por_equipo[equipo_id]['jugadores'].append({
                    'nombre': jugador.nombre,
                    'posicion': jugador.posicion,
                    'id': jugador.id,
                    'tiene_stats': stats is not None
                })
                
                if stats:
                    jugadores_por_equipo[equipo_id]['con_estadisticas'] += 1
                
                if jugador.posicion:
                    jugadores_por_equipo[equipo_id]['posiciones'].add(jugador.posicion)
                    
                    # ✅ IDENTIFICAR JUGADORES CB ESPECÍFICAMENTE
                    if 'CB' in (jugador.posicion or ''):
                        jugadores_por_equipo[equipo_id]['jugadores_cb'].append({
                            'nombre': jugador.nombre,
                            'posicion': jugador.posicion,
                            'id': jugador.id,
                            'tiene_stats': stats is not None
                        })
        
        # ✅ CALCULAR PERCENTILES PARA JUGADORES
        print("📊 Calculando percentiles para jugadores...")
        
        # ✅ SOLO CALCULAR CON JUGADORES QUE TIENEN ESTADÍSTICAS
        jugadores_con_stats = [j for j in jugadores_data if j['id'] in estadisticas_jugadores]
        
        # Recopilar todos los valores por campo de jugadores
        valores_jugadores_por_campo = {}
        for grupo in GRUPOS_STATS_JUGADORES.values():
            for nombre, campo in grupo:
                valores_jugadores_por_campo[campo] = [
                    jugador[campo] for jugador in jugadores_con_stats 
                    if jugador[campo] is not None and jugador[campo] > 0
                ]
        
        # Agregar percentiles a cada jugador
        for jugador_data in jugadores_data:
            for campo, todos_valores in valores_jugadores_por_campo.items():
                if todos_valores and jugador_data[campo] > 0:
                    valor_original = jugador_data[campo]
                    percentil = calcular_percentil(valor_original, todos_valores)
                    jugador_data[f"{campo}_percentil"] = percentil
                else:
                    jugador_data[f"{campo}_percentil"] = 50  # Default
        
        print(f"👥 Jugadores procesados: {len(jugadores_data)}")
        print(f"👥 Jugadores con estadísticas: {len(jugadores_con_stats)}")
        
        # ✅ DEBUG ESPECÍFICO PARA INDEPENDIENTE (ID 16)
        if 16 in jugadores_por_equipo:
            independiente_data = jugadores_por_equipo[16]
            print(f"\n🔍 ANÁLISIS COMPLETO DE INDEPENDIENTE (ID: 16):")
            print(f"   Nombre: {independiente_data['nombre']}")
            print(f"   Total jugadores: {len(independiente_data['jugadores'])}")
            print(f"   Jugadores con estadísticas: {independiente_data['con_estadisticas']}")
            print(f"   Jugadores CB encontrados: {len(independiente_data['jugadores_cb'])}")
            
            print(f"   📋 TODOS LOS JUGADORES CB:")
            for jugador_cb in independiente_data['jugadores_cb']:
                stats_text = "✅ Con stats" if jugador_cb['tiene_stats'] else "❌ Sin stats"
                print(f"     - {jugador_cb['nombre']} ({jugador_cb['posicion']}) [ID: {jugador_cb['id']}] - {stats_text}")
        
        # ✅ ESTADÍSTICAS FINALES
        jugadores_con_equipo = [j for j in jugadores_data if j['equipo_id'] is not None]
        jugadores_sin_equipo = [j for j in jugadores_data if j['equipo_id'] is None]
        
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   Equipos: {len(equipos)}")
        print(f"   Jugadores con equipo válido: {len(jugadores_con_equipo)}")
        print(f"   Jugadores sin equipo: {len(jugadores_sin_equipo)}")
        print(f"   Total jugadores en JavaScript: {len(jugadores_data)}")
        print(f"   Jugadores con estadísticas cargadas: {len(jugadores_con_stats)}")

        # ✅ PREPARAR CONTEXTO OPTIMIZADO
        context = {
            "equipos": equipos,
            "jugadores": jugadores,
            "equipos_data": json.dumps(equipos_data, ensure_ascii=False),
            "jugadores_data": json.dumps(jugadores_data, ensure_ascii=False),
            "GRUPOS_STATS_EQUIPOS": GRUPOS_STATS_EQUIPOS,
            "GRUPOS_STATS_JUGADORES": GRUPOS_STATS_JUGADORES,
            "GRUPOS_STATS_EQUIPOS_JSON": json.dumps(GRUPOS_STATS_EQUIPOS, ensure_ascii=False),
            "GRUPOS_STATS_JUGADORES_JSON": json.dumps(GRUPOS_STATS_JUGADORES, ensure_ascii=False),
        }
        
        print(f"✅ Contexto final preparado con estadísticas de jugadores")
        return render(request, "comparacion.html", context)

    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        
        # ✅ CONTEXTO DE ERROR MÍNIMO
        context = {
            "equipos": [],
            "jugadores": [],
            "equipos_data": "[]",
            "jugadores_data": "[]",
            "GRUPOS_STATS_EQUIPOS": GRUPOS_STATS_EQUIPOS,
            "GRUPOS_STATS_JUGADORES": GRUPOS_STATS_JUGADORES,
            "GRUPOS_STATS_EQUIPOS_JSON": json.dumps(GRUPOS_STATS_EQUIPOS, ensure_ascii=False),
            "GRUPOS_STATS_JUGADORES_JSON": json.dumps(GRUPOS_STATS_JUGADORES, ensure_ascii=False),
            "error": str(e)
        }
        
        return render(request, "comparacion.html", context)

def calcular_percentil(valor, todos_los_valores):
    """
    Calcula el percentil de un valor respecto a una lista de valores
    """
    if not todos_los_valores or valor is None:
        return 50
    
    try:
        # Filtrar valores válidos
        valores_validos = [v for v in todos_los_valores if v is not None]
        if not valores_validos:
            return 50
        
        # Contar valores menores
        menores = sum(1 for v in valores_validos if v < valor)
        percentil = (menores / len(valores_validos)) * 100
        
        # Redondear y limitar entre 1 y 99
        return max(1, min(99, round(percentil)))
        
    except Exception:
        return 50

def _convertir_posesion(posesion_str):
    """
    Convierte el string de posesión "65%" a float 65.0
    """
    if not posesion_str:
        return 0.0
    
    try:
        # Remover el símbolo % si existe
        posesion_clean = str(posesion_str).replace('%', '').strip()
        return float(posesion_clean)
    except (ValueError, AttributeError):
        return 0.0

# ✅ Mantener compatibilidad con imports antiguos
GRUPOS_STATS = GRUPOS_STATS_EQUIPOS  # Para compatibilidad hacia atrás
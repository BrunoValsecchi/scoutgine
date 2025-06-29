from django.shortcuts import render
from django.db.models import Q
from .models import EstadisticasJugador

def stats_jugadores(request):
    """Vista optimizada para estadísticas de jugadores"""
    
    # ✅ UNA SOLA QUERY OPTIMIZADA CON SELECT_RELATED
    jugadores_stats = EstadisticasJugador.objects.select_related('jugador', 'jugador__equipo').all()
    
    total_jugadores = jugadores_stats.count()
    if total_jugadores == 0:
        return render(request, "partials/statsjugadores.html", {
            "top3_por_estadistica": {},
            "error": "No hay datos de estadísticas de jugadores"
        })
    
    # ✅ ESTADÍSTICAS OPTIMIZADAS - Solo las más importantes
    estadisticas = [
        # 🏆 TOP STATS (15) - Las más consultadas
        ('goals', 'Goles'),
        ('assists', 'Asistencias'), 
        ('expected_goals_xg', 'xG'),
        ('shots_on_target', 'Disparos al arco'),
        ('successful_passes', 'Pases exitosos'),
        ('pass_accuracy', 'Precisión de pase'),
        ('successful_dribbles', 'Regates exitosos'),
        ('tackles_won', 'Entradas ganadas'),
        ('interceptions', 'Intercepciones'),
        ('duels_won', 'Duelos ganados'),
        ('saves', 'Atajadas'),
        ('clean_sheets', 'Vallas invictas'),
        ('yellow_cards', 'Tarjetas amarillas'),
        ('fouls_committed', 'Faltas cometidas'),
        ('chances_created', 'Chances creadas'),
        
        # 📊 STATS ADICIONALES (20) - Completar hasta 35 total
        ('expected_assists_xa', 'xA'),
        ('shots', 'Disparos'),
        ('accurate_long_balls', 'Pases largos precisos'),
        ('successful_crosses', 'Centros exitosos'),
        ('touches_in_opposition_box', 'Toques en área rival'),
        ('aerial_duels_won', 'Duelos aéreos ganados'),
        ('blocked', 'Bloqueos'),
        ('recoveries', 'Recuperaciones'),
        ('fouls_won', 'Faltas recibidas'),
        ('dispossessed', 'Pérdidas de balón'),
        ('save_percentage', 'Porcentaje de atajadas'),
        ('goals_prevented', 'Goles prevenidos'),
        ('cross_accuracy', 'Precisión de centros'),
        ('dribble_success', 'Éxito en regates'),
        ('tackles_won_percentage', 'Porcentaje entradas ganadas'),
        ('duels_won_percentage', 'Porcentaje duelos ganados'),
        ('aerial_duels_won_percentage', 'Porcentaje duelos aéreos'),
        ('red_cards', 'Tarjetas rojas'),
        ('error_led_to_goal', 'Errores que llevaron a gol'),
        ('goals_conceded', 'Goles recibidos'),
    ]
    
    # ✅ CAMPOS DONDE MENOR ES MEJOR (para ordenar ascendente)
    campos_menor_mejor = {
        'goals_conceded', 'error_led_to_goal', 'fouls_committed', 
        'dispossessed', 'dribbled_past', 'yellow_cards', 'red_cards'
    }
    
    top3_por_estadistica = {}
    
    # ✅ PROCESAMIENTO OPTIMIZADO SIN PRINTS EXCESIVOS
    for field, label in estadisticas:
        try:
            # Filtrar jugadores con datos válidos para este campo
            jugadores_validos = [
                j for j in jugadores_stats 
                if hasattr(j, field) and getattr(j, field) is not None and getattr(j, field) != 0
            ]
            
            if not jugadores_validos:
                top3_por_estadistica[label] = []
                continue
            
            # ✅ ORDENAMIENTO OPTIMIZADO EN MEMORIA
            if field in campos_menor_mejor:
                # Menor es mejor (ascendente)
                jugadores_ordenados = sorted(jugadores_validos, key=lambda x: getattr(x, field))
            else:
                # Mayor es mejor (descendente)  
                jugadores_ordenados = sorted(jugadores_validos, key=lambda x: getattr(x, field), reverse=True)
            
            # ✅ TOMAR TOP 3 Y FORMATEAR
            top3 = []
            for jugador in jugadores_ordenados[:3]:
                try:
                    valor = getattr(jugador, field)
                    
                    # ✅ FORMATEO INTELIGENTE
                    if isinstance(valor, float):
                        if field in ['pass_accuracy', 'save_percentage', 'cross_accuracy', 'dribble_success', 
                                   'tackles_won_percentage', 'duels_won_percentage', 'aerial_duels_won_percentage']:
                            valor_formato = f"{valor:.1f}%"
                        else:
                            valor_formato = f"{valor:.1f}"
                    else:
                        valor_formato = str(valor)
                    
                    jugador_data = {
                        "nombre": jugador.jugador.nombre,
                        "valor": valor_formato,
                        "equipo": jugador.jugador.equipo.nombre if jugador.jugador.equipo else 'Sin equipo',
                        "posicion": jugador.tipo or 'N/A'
                    }
                    top3.append(jugador_data)
                    
                except Exception:
                    continue
            
            top3_por_estadistica[label] = top3
            
        except Exception:
            top3_por_estadistica[label] = []
    
    # ✅ LOGGING MÍNIMO
    stats_con_datos = len([k for k, v in top3_por_estadistica.items() if len(v) > 0])
    print(f"✅ Stats jugadores: {stats_con_datos}/{len(estadisticas)} estadísticas con datos")
    
    return render(request, "partials/statsjugadores.html", {
        "top3_por_estadistica": top3_por_estadistica
    })


def obtener_stats_jugador_resumen():
    """Función auxiliar para obtener solo las 8 estadísticas principales"""
    
    jugadores_stats = EstadisticasJugador.objects.select_related('jugador', 'jugador__equipo').all()
    
    if not jugadores_stats:
        return {}
    
    # ✅ SOLO LAS 8 MÁS IMPORTANTES PARA RESUMEN
    estadisticas_resumen = [
        ('goals', 'Goles'),
        ('assists', 'Asistencias'),
        ('expected_goals_xg', 'xG'),
        ('shots_on_target', 'Disparos al arco'),
        ('successful_passes', 'Pases exitosos'),
        ('tackles_won', 'Entradas ganadas'),
        ('saves', 'Atajadas'),
        ('yellow_cards', 'Tarjetas amarillas'),
    ]
    
    top3_por_estadistica = {}
    
    for field, label in estadisticas_resumen:
        try:
            jugadores_validos = [
                j for j in jugadores_stats 
                if getattr(j, field, None) is not None and getattr(j, field, 0) != 0
            ]
            
            if not jugadores_validos:
                continue
            
            if field == 'yellow_cards':
                jugadores_ordenados = sorted(jugadores_validos, key=lambda x: getattr(x, field))
            else:
                jugadores_ordenados = sorted(jugadores_validos, key=lambda x: getattr(x, field), reverse=True)
            
            top3 = []
            for jugador in jugadores_ordenados[:3]:
                valor = getattr(jugador, field)
                valor_formato = f"{valor:.1f}" if isinstance(valor, float) else str(valor)
                
                top3.append({
                    "nombre": jugador.jugador.nombre,
                    "valor": valor_formato,
                    "equipo": jugador.jugador.equipo.nombre if jugador.jugador.equipo else 'Sin equipo',
                    "posicion": jugador.tipo or 'N/A'
                })
            
            top3_por_estadistica[label] = top3
        except Exception:
            continue
    
    return top3_por_estadistica
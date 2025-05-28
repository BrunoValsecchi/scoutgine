from django.shortcuts import render
from .models import EstadisticasJugador

def obtener_stats_jugador(obj, field):
    valor = getattr(obj, field, '')
    print(f"  - {obj.jugador.nombre}: {field} = {valor}")
    return valor

def stats_jugadores(request):
    print("=" * 50)
    print("🔥 FUNCIÓN STATS_JUGADORES EJECUTADA")
    print("=" * 50)
    
    # Verificar si hay datos en la tabla
    total_jugadores = EstadisticasJugador.objects.count()
    print(f"📊 Total de EstadisticasJugador en BD: {total_jugadores}")
    
    if total_jugadores == 0:
        print("⚠️  NO HAY DATOS DE JUGADORES EN LA BASE DE DATOS")
        return render(request, "partials/statsjugadores.html", {
            "top3_por_estadistica": {},
            "error": "No hay datos de estadísticas de jugadores"
        })
    
    # Verificar algunos datos de ejemplo
    print("\n🔍 PRIMEROS 5 JUGADORES:")
    for i, jugador in enumerate(EstadisticasJugador.objects.all()[:5], 1):
        print(f"  {i}. {jugador.jugador.nombre} ({jugador.tipo})")
        print(f"     - Goles: {jugador.goals}")
        print(f"     - Asistencias: {jugador.assists}")
        print(f"     - Disparos: {jugador.shots}")
    
    # TODAS LAS ESTADÍSTICAS DEL MODELO
    estadisticas = [
        # Estadísticas de Arquero
        ('saves', 'Atajadas'),
        ('save_percentage', 'Porcentaje de atajadas'),
        ('goals_prevented', 'Goles prevenidos'),
        ('clean_sheets', 'Vallas invictas'),
        ('high_claim', 'Salidas en alto'),
        
        # Estadísticas Ofensivas
        ('goals', 'Goles'),
        ('expected_goals_xg', 'xG'),
        ('xg_on_target_xgot', 'xG en el arco'),
        ('non_penalty_xg', 'xG sin penales'),
        ('shots', 'Disparos'),
        ('shots_on_target', 'Disparos al arco'),
        ('assists', 'Asistencias'),
        ('expected_assists_xa', 'xA'),
        ('chances_created', 'Chances creadas'),
        
        # Estadísticas de Pase
        ('successful_passes', 'Pases exitosos'),
        ('pass_accuracy', 'Precisión de pase'),
        ('pass_accuracy_outfield', 'Precisión de pase (campo)'),
        ('accurate_long_balls', 'Pases largos precisos'),
        ('long_ball_accuracy', 'Precisión pases largos'),
        ('accurate_long_balls_outfield', 'Pases largos precisos (campo)'),
        ('long_ball_accuracy_outfield', 'Precisión pases largos (campo)'),
        ('successful_crosses', 'Centros exitosos'),
        ('cross_accuracy', 'Precisión de centros'),
        
        # Estadísticas de Dribbling y Toques
        ('successful_dribbles', 'Regates exitosos'),
        ('dribble_success', 'Éxito en regates'),
        ('touches', 'Toques'),
        ('touches_in_opposition_box', 'Toques en área rival'),
        
        # Estadísticas Defensivas
        ('tackles_won', 'Entradas ganadas'),
        ('tackles_won_percentage', 'Porcentaje entradas ganadas'),
        ('duels_won', 'Duelos ganados'),
        ('duels_won_percentage', 'Porcentaje duelos ganados'),
        ('aerial_duels_won', 'Duelos aéreos ganados'),
        ('aerial_duels_won_percentage', 'Porcentaje duelos aéreos'),
        ('interceptions', 'Intercepciones'),
        ('blocked', 'Bloqueos'),
        ('recoveries', 'Recuperaciones'),
        ('possession_won_final_3rd', 'Recuperaciones en 1/3 final'),
        
        # Estadísticas Disciplinarias y Otros
        ('fouls_won', 'Faltas recibidas'),
        ('fouls_committed', 'Faltas cometidas'),
        ('penalties_awarded', 'Penales provocados'),
        ('dispossessed', 'Pérdidas de balón'),
        ('dribbled_past', 'Regateado'),
        ('yellow_cards', 'Tarjetas amarillas'),
        ('red_cards', 'Tarjetas rojas'),
        ('error_led_to_goal', 'Errores que llevaron a gol'),
        ('goals_conceded', 'Goles recibidos'),
    ]
    
    print(f"\n📈 PROCESANDO {len(estadisticas)} ESTADÍSTICAS:")
    print(f"Lista de estadísticas: {[stat[0] for stat in estadisticas]}")

    top3_por_estadistica = {}
    
    for field, label in estadisticas:
        print(f"\n{'='*60}")
        print(f"🔄 Procesando: {label} ({field})")
        print(f"{'='*60}")
        
        try:
            # Verificar si el campo existe en el modelo
            if not hasattr(EstadisticasJugador, field):
                print(f"❌ CAMPO {field} NO EXISTE EN EL MODELO")
                continue
            
            # Contar total de registros con este campo no nulo
            total_con_campo = EstadisticasJugador.objects.exclude(**{field: None}).count()
            print(f"📊 Total registros con {field} no nulo: {total_con_campo}")
            
            if total_con_campo == 0:
                print(f"⚠️  No hay datos para {field}")
                top3_por_estadistica[label] = []
                continue
            
            # Estadísticas donde MENOR es mejor
            if field in ['goals_conceded', 'error_led_to_goal', 'fouls_committed', 'dispossessed', 'dribbled_past', 'yellow_cards', 'red_cards']:
                print(f"  📉 Ordenando de MENOR a MAYOR para {field}")
                jugadores = EstadisticasJugador.objects.exclude(**{field: None}).exclude(**{field: 0}).order_by(field)[:3]
            else:
                # Estadísticas donde MAYOR es mejor
                print(f"  📈 Ordenando de MAYOR a MENOR para {field}")
                jugadores = EstadisticasJugador.objects.exclude(**{field: None}).exclude(**{field: 0}).order_by(f'-{field}')[:3]
            
            print(f"  🎯 {jugadores.count()} jugadores encontrados después del filtro")
            
            # Debug: mostrar valores antes del filtro
            print(f"  🔍 VALORES ENCONTRADOS PARA {field}:")
            valores_debug = EstadisticasJugador.objects.exclude(**{field: None}).values_list('jugador__nombre', field)[:10]
            for nombre, valor in valores_debug:
                print(f"    - {nombre}: {valor}")
            
            jugadores_lista = []
            for i, jugador in enumerate(jugadores, 1):
                try:
                    nombre = jugador.jugador.nombre
                    equipo = jugador.jugador.equipo.nombre if hasattr(jugador.jugador, 'equipo') and jugador.jugador.equipo else 'Sin equipo'
                    posicion = jugador.tipo
                    valor = getattr(jugador, field, 0)
                    
                    print(f"    🏃 Procesando jugador {i}: {nombre}")
                    print(f"      - Equipo: {equipo}")
                    print(f"      - Posición: {posicion}")
                    print(f"      - Valor {field}: {valor}")
                    
                    # Solo agregar si el valor no es None o 0
                    if valor is not None and valor != 0:
                        jugador_data = {
                            "nombre": nombre, 
                            "valor": valor,
                            "equipo": equipo,
                            "posicion": posicion
                        }
                        jugadores_lista.append(jugador_data)
                        print(f"      ✅ Agregado: {nombre} ({equipo}) - {valor}")
                    else:
                        print(f"      ❌ Descartado por valor inválido: {valor}")
                    
                except Exception as e:
                    print(f"    ❌ Error procesando jugador {i}: {e}")
                    import traceback
                    traceback.print_exc()
            
            top3_por_estadistica[label] = jugadores_lista
            print(f"  ✅ {len(jugadores_lista)} jugadores agregados a '{label}'")
            
            # Debug final para esta estadística
            print(f"  📋 RESULTADO FINAL para {label}:")
            for j, jug in enumerate(jugadores_lista, 1):
                print(f"    {j}. {jug['nombre']} - {jug['valor']}")
            
        except Exception as e:
            print(f"  ❌ ERROR GENERAL en {field}: {e}")
            import traceback
            traceback.print_exc()
            top3_por_estadistica[label] = []

    print(f"\n{'='*60}")
    print(f"📋 RESUMEN FINAL:")
    print(f"{'='*60}")
    print(f"  📊 Total estadísticas procesadas: {len(top3_por_estadistica)}")
    
    estadisticas_con_datos = 0
    estadisticas_sin_datos = 0
    
    for k, v in top3_por_estadistica.items():
        if len(v) > 0:
            print(f"    ✅ {k}: {len(v)} jugadores")
            estadisticas_con_datos += 1
        else:
            print(f"    ❌ {k}: sin datos")
            estadisticas_sin_datos += 1
    
    print(f"\n  📈 Estadísticas con datos: {estadisticas_con_datos}")
    print(f"  📉 Estadísticas sin datos: {estadisticas_sin_datos}")

    print(f"\n🎯 ENVIANDO DATOS AL TEMPLATE...")
    print(f"Diccionario final tiene {len(top3_por_estadistica)} elementos")
    print("=" * 50)
    
    return render(request, "partials/statsjugadores.html", {
        "top3_por_estadistica": top3_por_estadistica
    })
from django.shortcuts import render
from django.http import JsonResponse
from .models import EstadisticasEquipo

def stats_equipos(request):
    """Vista para estadísticas de equipos"""
    print("🔄 stats_equipos ejecutado")
    
    # ✅ SI ES PETICIÓN AJAX (Vista Completa)
    if request.GET.get('format') == 'json':
        estadistica = request.GET.get('estadistica')
        print(f"📊 Petición AJAX para: {estadistica}")
        
        if not estadistica:
            return JsonResponse({"error": "No se especificó estadística"})
        
        # ✅ MAPEO COMPLETO DE TODOS LOS 25 CAMPOS DEL MODELO
        campos = {
            # Generales (5)
            'fotmob_rating': 'Rating FotMob',
            'goals_per_match': 'Goles por partido',
            'goals_conceded_per_match': 'Goles recibidos por partido',
            'average_possession': 'Posesión promedio (%)',
            'clean_sheets': 'Vallas invictas',
            
            # Ataque (7)
            'expected_goals_xg': 'Goles esperados (xG)',
            'shots_on_target_per_match': 'Tiros al arco por partido',
            'big_chances': 'Grandes oportunidades',
            'big_chances_missed': 'Grandes oportunidades perdidas',
            'penalties_awarded': 'Penales a favor',
            'touches_in_opposition_box': 'Toques en área rival',
            'corners': 'Córners',
            
            # Pases (3)
            'accurate_passes_per_match': 'Pases precisos por partido',
            'accurate_long_balls_per_match': 'Pases largos precisos por partido',
            'accurate_crosses_per_match': 'Centros precisos por partido',
            
            # Defensa (7)
            'xg_conceded': 'xG concedidos',
            'interceptions_per_match': 'Intercepciones por partido',
            'successful_tackles_per_match': 'Tackles exitosos por partido',
            'clearances_per_match': 'Despejes por partido',
            'possession_won_final_3rd_per_match': 'Recuperaciones en campo rival',
            'saves_per_match': 'Atajadas por partido',
            
            # Disciplina (3)
            'fouls_per_match': 'Faltas por partido',
            'yellow_cards': 'Tarjetas amarillas',
            'red_cards': 'Tarjetas rojas',
        }
        
        if estadistica not in campos:
            return JsonResponse({"error": f"Campo {estadistica} no válido. Disponibles: {list(campos.keys())}"})
        
        # Consulta para AJAX
        try:
            equipos_stats = EstadisticasEquipo.objects.select_related('equipo').all()
            equipos_lista = []
            
            for eq_stat in equipos_stats:
                valor = getattr(eq_stat, estadistica, None)
                
                # Verificar que el valor no sea None, vacío o cero
                if valor is not None and valor != '' and str(valor) != '0' and str(valor) != '0.0':
                    try:
                        # Manejar diferentes tipos de datos
                        if isinstance(valor, str):
                            # Para campos como average_possession que pueden tener '%'
                            valor_numerico = float(valor.replace('%', '').replace(',', '.'))
                        else:
                            valor_numerico = float(valor)
                        
                        # Solo incluir valores positivos válidos
                        if valor_numerico > 0:
                            # Formatear según el tipo de estadística
                            if "possession" in estadistica:
                                formato = f"{valor_numerico:.1f}%"
                            elif estadistica in ['yellow_cards', 'red_cards', 'clean_sheets', 'big_chances', 
                                               'big_chances_missed', 'penalties_awarded', 'touches_in_opposition_box', 
                                               'corners', 'interceptions_per_match']:
                                formato = f"{int(valor_numerico)}"  # Enteros
                            else:
                                formato = f"{valor_numerico:.1f}"  # Decimales con 1 decimal
                            
                            equipos_lista.append({
                                'nombre': eq_stat.equipo.nombre,
                                'valor': valor_numerico,
                                'valor_formatted': formato
                            })
                    except (ValueError, TypeError) as e:
                        print(f"⚠️ Error procesando {eq_stat.equipo.nombre} - {estadistica}: {valor} -> {e}")
                        continue
            
            # Ordenar por valor (descendente para la mayoría, ascendente para stats "malas")
            stats_ascendentes = ['goals_conceded_per_match', 'xg_conceded', 'fouls_per_match', 
                               'yellow_cards', 'red_cards', 'big_chances_missed']
            reverse_order = estadistica not in stats_ascendentes
            
            equipos_lista.sort(key=lambda x: x['valor'], reverse=reverse_order)
            
            print(f"✅ AJAX: {estadistica} -> {len(equipos_lista)} equipos con datos válidos")
            if equipos_lista:
                print("🥇 Top 3:", [f'{eq["nombre"]}: {eq["valor_formatted"]}' for eq in equipos_lista[:3]])            
            return JsonResponse({
                'equipos': equipos_lista,
                'label': campos[estadistica],
                'total': len(equipos_lista)
            })
            
        except Exception as e:
            print(f"❌ Error AJAX: {e}")
            return JsonResponse({"error": str(e)})
    
    # ✅ VISTA NORMAL (Vista Resumen) - TOP 3 POR ESTADÍSTICAS PRINCIPALES
    print("🏠 Generando Vista Resumen con TOP 3")
    
    # Solo las estadísticas más importantes para la vista resumen (8 estadísticas clave)
    campos_resumen = {
        # Generales (5)
            'fotmob_rating': 'Rating FotMob',
            'goals_per_match': 'Goles por partido',
            'goals_conceded_per_match': 'Goles recibidos por partido',
            'average_possession': 'Posesión promedio (%)',
            'clean_sheets': 'Vallas invictas',
            
            # Ataque (7)
            'expected_goals_xg': 'Goles esperados (xG)',
            'shots_on_target_per_match': 'Tiros al arco por partido',
            'big_chances': 'Grandes oportunidades',
            'big_chances_missed': 'Grandes oportunidades perdidas',
            'penalties_awarded': 'Penales a favor',
            'touches_in_opposition_box': 'Toques en área rival',
            'corners': 'Córners',
            
            # Pases (3)
            'accurate_passes_per_match': 'Pases precisos por partido',
            'accurate_long_balls_per_match': 'Pases largos precisos por partido',
            'accurate_crosses_per_match': 'Centros precisos por partido',
            
            # Defensa (7)
            'xg_conceded': 'xG concedidos',
            'interceptions_per_match': 'Intercepciones por partido',
            'successful_tackles_per_match': 'Tackles exitosos por partido',
            'clearances_per_match': 'Despejes por partido',
            'possession_won_final_3rd_per_match': 'Recuperaciones en campo rival',
            'saves_per_match': 'Atajadas por partido',
            
            # Disciplina (3)
            'fouls_per_match': 'Faltas por partido',
            'yellow_cards': 'Tarjetas amarillas',
            'red_cards': 'Tarjetas rojas',
    }
    
    top3_por_estadistica = {}
    
    for campo, label in campos_resumen.items():
        print(f"🔍 Procesando campo: {campo} ({label})")
        
        try:
            equipos_stats = EstadisticasEquipo.objects.select_related('equipo').all()
            equipos_con_datos = []
            
            for eq_stat in equipos_stats:
                valor = getattr(eq_stat, campo, None)
                
                # Verificar que el valor sea válido
                if valor is not None and valor != '' and str(valor) != '0' and str(valor) != '0.0':
                    try:
                        if isinstance(valor, str):
                            valor_numerico = float(valor.replace('%', '').replace(',', '.'))
                        else:
                            valor_numerico = float(valor)
                        
                        # Solo valores positivos
                        if valor_numerico > 0:
                            # Formatear según el tipo
                            if "possession" in campo:
                                formato = f"{valor_numerico:.1f}%"
                            elif campo in ['clean_sheets']:
                                formato = f"{int(valor_numerico)}"
                            else:
                                formato = f"{valor_numerico:.1f}"
                            
                            equipos_con_datos.append({
                                'nombre': eq_stat.equipo.nombre,
                                'valor': formato,
                                'valor_numerico': valor_numerico
                            })
                    except (ValueError, TypeError):
                        continue
            
            # Ordenar por valor numérico y tomar top 3
            equipos_con_datos.sort(key=lambda x: x['valor_numerico'], reverse=True)
            top3 = equipos_con_datos[:3]
            
            print(f"✅ {label}: {len(top3)} equipos en top 3")
            for i, equipo in enumerate(top3):
                print(f"  {i+1}. {equipo['nombre']}: {equipo['valor']}")
            
            top3_por_estadistica[label] = top3
            
        except Exception as e:
            print(f"❌ Error en {label}: {e}")
            top3_por_estadistica[label] = []
    
    print(f"🎯 Total estadísticas procesadas: {len(top3_por_estadistica)}")
    
    # Enviar datos al template
    context = {
        "top3_por_estadistica": top3_por_estadistica
    }
    
    print("📄 Renderizando template con context")
    
    return render(request, "partials/statsequipo.html", context)


def obtener_stats_resumen():
    """Función auxiliar para obtener TOP 3 por estadística (para usar en otras vistas)"""
    print("🔄 obtener_stats_resumen ejecutado")
    
    # Solo estadísticas principales para resumen
    campos = {
        # Generales (5)
            'fotmob_rating': 'Rating FotMob',
            'goals_per_match': 'Goles por partido',
            'goals_conceded_per_match': 'Goles recibidos por partido',
            'average_possession': 'Posesión promedio (%)',
            'clean_sheets': 'Vallas invictas',
            
            # Ataque (7)
            'expected_goals_xg': 'Goles esperados (xG)',
            'shots_on_target_per_match': 'Tiros al arco por partido',
            'big_chances': 'Grandes oportunidades',
            'big_chances_missed': 'Grandes oportunidades perdidas',
            'penalties_awarded': 'Penales a favor',
            'touches_in_opposition_box': 'Toques en área rival',
            'corners': 'Córners',
            
            # Pases (3)
            'accurate_passes_per_match': 'Pases precisos por partido',
            'accurate_long_balls_per_match': 'Pases largos precisos por partido',
            'accurate_crosses_per_match': 'Centros precisos por partido',
            
            # Defensa (7)
            'xg_conceded': 'xG concedidos',
            'interceptions_per_match': 'Intercepciones por partido',
            'successful_tackles_per_match': 'Tackles exitosos por partido',
            'clearances_per_match': 'Despejes por partido',
            'possession_won_final_3rd_per_match': 'Recuperaciones en campo rival',
            'saves_per_match': 'Atajadas por partido',
            
            # Disciplina (3)
            'fouls_per_match': 'Faltas por partido',
            'yellow_cards': 'Tarjetas amarillas',
            'red_cards': 'Tarjetas rojas',
    }
    
    top3_por_estadistica = {}
    
    for campo, label in campos.items():
        try:
            equipos_stats = EstadisticasEquipo.objects.select_related('equipo').all()
            equipos_con_datos = []
            
            for eq_stat in equipos_stats:
                valor = getattr(eq_stat, campo, None)
                
                if valor is not None and valor != '' and str(valor) != '0' and str(valor) != '0.0':
                    try:
                        if isinstance(valor, str):
                            valor_numerico = float(valor.replace('%', '').replace(',', '.'))
                        else:
                            valor_numerico = float(valor)
                        
                        if valor_numerico > 0:
                            if "possession" in campo:
                                formato = f"{valor_numerico:.1f}%"
                            elif campo in ['clean_sheets']:
                                formato = f"{int(valor_numerico)}"
                            else:
                                formato = f"{valor_numerico:.1f}"
                            
                            equipos_con_datos.append({
                                'nombre': eq_stat.equipo.nombre,
                                'valor': formato,
                                'valor_numerico': valor_numerico
                            })
                    except (ValueError, TypeError):
                        continue
            
            equipos_con_datos.sort(key=lambda x: x['valor_numerico'], reverse=True)
            top3 = equipos_con_datos[:3]
            
            top3_por_estadistica[label] = top3
            
        except Exception as e:
            print(f"❌ Error en {label}: {e}")
            top3_por_estadistica[label] = []
    
    return top3_por_estadistica
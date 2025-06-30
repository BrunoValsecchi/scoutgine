from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Posicion, Equipo, EstadisticasEquipo, Jugador
import json
import random
import numpy as np
from .estadistica_jugador import grafico_jugador_view
from .comparacion import GRUPOS_STATS, GRUPOS_STATS_EQUIPOS, GRUPOS_STATS_JUGADORES# ============================================================================
# VISTAS PRINCIPALES
# ============================================================================

def home(request):
    return render(request, "index.html")

def grafico(request):
    return render(request, "grafico.html")

def menu(request):
    return render(request, "menu.html")

def equipo(request):
    """Página principal de equipos"""
    try:
        from .equipo import equipo as equipo_func
        return equipo_func(request)
    except Exception as e:
        return render(request, "equipo.html", {'error': str(e)})

def equipo_detalle(request, equipo_id):
    """Vista para mostrar un equipo individual"""
    try:
        from .equipo import equipo_detalle as equipo_detalle_func
        return equipo_detalle_func(request, equipo_id)
    except Exception as e:
        return render(request, "equipo_detalle.html", {'error': str(e)})

def ligas(request):
    from .ligas import ligas as ligas_func
    return ligas_func(request)

import numpy as np

def comparacion(request):
    # ✅ Usar la función de comparacion.py en lugar de duplicar lógica
    from .comparacion import comparacion as comparacion_func
    return comparacion_func(request)


def stats_jugadores(request):
    from .statsjugadores import stats_jugadores as stats_jugadores_func
    return stats_jugadores_func(request)

def jugadores(request):
    from .jugadores import jugadores as jugadores_func
    return jugadores_func(request)

def jugador_detalle(request, jugador_id):
    from .detalle_jugador import jugador_detalle as jugador_detalle_func
    return jugador_detalle_func(request, jugador_id)

def posiciones(request):
    from .posiciones import posiciones as posiciones_func
    return posiciones_func(request)
def grafico_jugador(request, jugador_id, estadistica):
    # Tu lógica aquí
    pass
def buscar(request):
    from .buscar import buscar as buscar_func
    return buscar_func(request)

def index(request):
    from .index import index as index_func
    return index_func(request)
def jugador_detalle(request, jugador_id):
    from .detalle_jugador import jugador_detalle as jugador_detalle_func
    return jugador_detalle_func(request, jugador_id)
# ============================================================================
# API ENDPOINTS
# ============================================================================

def posiciones_api(request):
    """API para obtener datos de posiciones"""
    torneos = {
        'apertura_a': Posicion.objects.filter(torneo_id=34),
        'apertura_b': Posicion.objects.filter(torneo_id=49),
        'clausura_a': Posicion.objects.filter(torneo_id=4),
        'clausura_b': Posicion.objects.filter(torneo_id=19)
    }
    
    data = {key: list(torneo.values()) for key, torneo in torneos.items()}
    return JsonResponse(data)

# ============================================================================
# GRÁFICOS DE ESTADÍSTICAS
# ============================================================================

def grafico_equipo(request, equipo_id, stat_name):
    """Vista para mostrar gráfico de estadística específica de un equipo"""
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        
        # Decodificar el nombre de la estadística desde la URL
        from urllib.parse import unquote
        stat_name = unquote(stat_name)
        
        # ✅ Inicializar variables correctamente
        stat_value = None
        posicion = None
        total_equipos = 0
        equipos_valores = []
        promedio = 0
        
        # Mapeo de nombres de estadísticas a campos de base de datos
        STAT_MAPPING = {
            "Goles por partido": "goals_per_match",
            "Tiros al arco por partido": "shots_on_target_per_match",
            "Ocasiones claras": "big_chances",
            "Ocasiones claras falladas": "big_chances_missed",
            "Goles esperados (xG)": "expected_goals_xg",
            "Penales a favor": "penalties_awarded",
            "Goles concedidos por partido": "goals_conceded_per_match",
            "Vallas invictas": "clean_sheets",
            "xG concedido": "expected_goals_conceded_xgc",
            "Intercepciones por partido": "interceptions_per_match",
            "Entradas exitosas por partido": "tackles_won_per_match",
            "Despejes por partido": "clearances_per_match",
            "Recuperaciones en el último tercio": "recoveries_final_third",
            "Atajadas por partido": "saves_per_match",
            "Pases precisos por partido": "accurate_passes_per_match",
            "Pases largos precisos por partido": "accurate_long_balls_per_match",
            "Centros precisos por partido": "accurate_crosses_per_match",
            "Toques en el área rival": "touches_in_opposition_box",
            "Tiros de esquina": "corners_taken",
            "Rating": "average_rating",
            "Posesión promedio": "average_possession",
            "Faltas por partido": "fouls_per_match",
            "Tarjetas amarillas": "yellow_cards",
            "Tarjetas rojas": "red_cards",
        }
        
        # Obtener el campo de base de datos correspondiente
        campo_bd = STAT_MAPPING.get(stat_name)
        if not campo_bd:
            print(f"❌ Estadística no encontrada: {stat_name}")
            return render(request, 'estadistica_detalle.html', {
                'equipo': equipo,
                'stat_name': stat_name,
                'title': f"{stat_name} - {equipo.nombre}",
                'error': f"Estadística '{stat_name}' no encontrada",
                'stat_value': None,
                'posicion': None,
                'total_equipos': 0,
                'promedio': 0,
            })
        
        try:
            # Obtener estadísticas del equipo
            equipo_stats = EstadisticasEquipo.objects.filter(equipo=equipo).first()
            
            if equipo_stats:
                # ✅ Obtener valor de forma segura
                raw_value = getattr(equipo_stats, campo_bd, None)
                if raw_value is not None:
                    try:
                        stat_value = float(raw_value)
                        if isinstance(raw_value, float):
                            stat_value = round(stat_value, 2)
                        else:
                            stat_value = int(stat_value)
                    except (ValueError, TypeError):
                        stat_value = 0
                        print(f"⚠️ Error convertiendo valor: {raw_value}")
                
                print(f"📊 Valor del equipo {equipo.nombre}: {stat_value}")
            else:
                print(f"❌ No hay estadísticas para el equipo {equipo.nombre}")
        
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas del equipo: {e}")
            stat_value = None
        
        # Obtener valores de todos los equipos para comparación
        try:
            all_stats = EstadisticasEquipo.objects.all()
            equipos_valores = []
            
            for stats in all_stats:
                try:
                    valor = getattr(stats, campo_bd, None)
                    if valor is not None:
                        equipos_valores.append(float(valor))
                except (ValueError, TypeError, AttributeError):
                    continue
            
            total_equipos = len(equipos_valores)
            
            # Calcular promedio
            if equipos_valores:
                promedio = round(sum(equipos_valores) / len(equipos_valores), 2)
            
            # Calcular posición si tenemos el valor del equipo
            if stat_value is not None and equipos_valores:
                valores_ordenados = sorted(equipos_valores, reverse=True)
                try:
                    posicion = valores_ordenados.index(float(stat_value)) + 1
                except ValueError:
                    # Si el valor exacto no está, encontrar la posición aproximada
                    posicion = sum(1 for v in valores_ordenados if v > stat_value) + 1
            
            print(f"📊 Estadísticas: valor={stat_value}, posición={posicion}/{total_equipos}, promedio={promedio}")
        
        except Exception as e:
            print(f"❌ Error calculando comparaciones: {e}")
            equipos_valores = []
            total_equipos = 0
            promedio = 0
            posicion = None
        
        # ✅ Preparar contexto completo para estadistica_detalle.html
        context = {
            'equipo': equipo,
            'stat_name': stat_name,
            'title': f"{stat_name} - {equipo.nombre}",
            'stat_value': stat_value,
            'posicion': posicion,
            'total_equipos': total_equipos,
            'promedio': promedio,
            'error': None if stat_value is not None else f"No hay datos para {stat_name}",
        }
        
        print(f"✅ Contexto final: {stat_name} = {stat_value}, pos: {posicion}")
        return render(request, 'estadistica_detalle.html', context)  # ✅ Usar el template correcto
        
    except Exception as e:
        print(f"❌ Error general en grafico_equipo: {e}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'estadistica_detalle.html', {
            'equipo': equipo if 'equipo' in locals() else None,
            'stat_name': stat_name if 'stat_name' in locals() else 'Estadística',
            'title': f"Error - {stat_name if 'stat_name' in locals() else 'Estadística'}",
            'stat_value': None,
            'posicion': None,
            'total_equipos': 0,
            'promedio': 0,
            'error': f"Error cargando estadística: {str(e)}",
        })
def generar_graficos_completos(equipo, estadistica, valor_equipo, equipos_nombres, equipos_valores, estadisticas_obj):
    """Genera todos los gráficos para la estadística"""
    from pyecharts.charts import Bar, Line, Gauge
    from pyecharts import options as opts
    
    # Determinar color según tipo
    if 'goles' in estadistica.lower() or 'tiros' in estadistica.lower():
        color = "#ff6b6b"
    elif 'defens' in estadistica.lower() or 'vallas' in estadistica.lower():
        color = "#4ecdc4"
    elif 'pases' in estadistica.lower() or 'posesión' in estadistica.lower():
        color = "#45b7d1"
    else:
        color = "#67aaff"
    
    graficos = {}
    
    # 1. RANKING TOP 10
    try:
        top_equipos = sorted(zip(equipos_nombres, equipos_valores), key=lambda x: x[1], reverse=True)[:10]
        nombres_top = [nombre for nombre, _ in top_equipos]
        valores_top = [valor for _, valor in top_equipos]
        
        ranking_chart = (
            Bar(init_opts=opts.InitOpts(width="100%", height="350px", theme="dark"))
            .add_xaxis(nombres_top)
            .add_yaxis("", valores_top, color=color)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"🏆 Top 10 - {estadistica}",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#e3e6ee", font_size=14)
                ),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45, color="#a6b6d9")),
                yaxis_opts=opts.AxisOpts(name=estadistica, name_textstyle_opts=opts.TextStyleOpts(color="#a6b6d9"))
            )
        )
        graficos['ranking_chart'] = mark_safe(ranking_chart.render_embed())
    except:
        pass
    
    # 2. EVOLUCIÓN TEMPORAL
    try:
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
        evolucion = []
        base = valor_equipo
        
        for _ in range(6):
            variacion = random.uniform(-0.1, 0.1)
            nuevo_valor = base * (1 + variacion)
            evolucion.append(round(nuevo_valor, 2))
            base = nuevo_valor
        
        promedio_liga = sum(equipos_valores) / len(equipos_valores)
        
        evolucion_chart = (
            Line(init_opts=opts.InitOpts(width="100%", height="350px", theme="dark"))
            .add_xaxis(meses)
            .add_yaxis(f"{equipo.nombre}", evolucion, color=color, is_smooth=True)
            .add_yaxis("Promedio Liga", [promedio_liga] * 6, color="#666666", is_smooth=True)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"📈 Evolución - {estadistica}",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#e3e6ee", font_size=14)
                )
            )
        )
        graficos['evolucion_chart'] = mark_safe(evolucion_chart.render_embed())
    except:
        pass
    
    # 3. PERCENTILES
    try:
        valores_ordenados = sorted(equipos_valores)
        percentiles = [25, 50, 75, 90]
        valores_percentiles = []
        
        for p in percentiles:
            index = int(len(valores_ordenados) * p / 100)
            if index < len(valores_ordenados):
                valores_percentiles.append(valores_ordenados[index])
            else:
                valores_percentiles.append(valores_ordenados[-1])
        
        percentil_chart = (
            Bar(init_opts=opts.InitOpts(width="100%", height="350px", theme="dark"))
            .add_xaxis([f"P{p}" for p in percentiles])
            .add_yaxis("Liga", valores_percentiles, color="#95a5a6")
            .add_yaxis(equipo.nombre, [valor_equipo] * 4, color=color)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"🎯 Distribución - {estadistica}",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#e3e6ee", font_size=14)
                )
            )
        )
        graficos['percentil_chart'] = mark_safe(percentil_chart.render_embed())
    except:
        pass
    
    # 4. ANÁLISIS CONTEXTUAL
    try:
        categorias = ["Últimos 5", "Casa", "Visitante", "1ª Mitad", "2ª Mitad"]
        datos_simulados = [valor_equipo * (1 + random.uniform(-0.2, 0.2)) for _ in categorias]
        promedio_liga = sum(equipos_valores) / len(equipos_valores)
        
        barras_chart = (
            Bar(init_opts=opts.InitOpts(width="100%", height="350px", theme="dark"))
            .add_xaxis(categorias)
            .add_yaxis(f"{equipo.nombre}", datos_simulados, color=color)
            .add_yaxis("Promedio Liga", [promedio_liga] * len(categorias), color="#666666")
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"📊 Análisis Contextual - {estadistica}",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#e3e6ee", font_size=14)
                ),
                legend_opts=opts.LegendOpts(pos_top="10%")
            )
        )
        graficos['barras_chart'] = mark_safe(barras_chart.render_embed())
    except:
        pass
    
    # 5. MEDIDOR DE RENDIMIENTO
    try:
        valores_ordenados = sorted(equipos_valores, reverse=True)
        try:
            posicion = valores_ordenados.index(valor_equipo)
            percentil = ((len(valores_ordenados) - posicion) / len(valores_ordenados)) * 100
        except ValueError:
            percentil = 50
        
        gauge_chart = (
            Gauge(init_opts=opts.InitOpts(width="100%", height="350px", theme="dark"))
            .add(
                "",
                [("Rendimiento", round(percentil, 1))],
                radius="70%",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=[(0.3, "#ff6b6b"), (0.7, "#ffd700"), (1, "#4ecdc4")], width=20
                    )
                )
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"🎯 Percentil - {estadistica}",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#e3e6ee", font_size=14)
                )
            )
        )
        graficos['gauge_chart'] = mark_safe(gauge_chart.render_embed())
    except:
        pass
    
    # 6. COMPARACIÓN CON RIVALES
    try:
        # Equipos similares (±30% del valor)
        equipos_similares = []
        for nombre, valor in zip(equipos_nombres, equipos_valores):
            if abs(valor - valor_equipo) <= valor_equipo * 0.3:
                equipos_similares.append((nombre, valor))
        
        equipos_similares = equipos_similares[:5]
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
        
        comparacion_chart = Line(init_opts=opts.InitOpts(width="100%", height="350px", theme="dark"))
        comparacion_chart.add_xaxis(meses)
        
        # Equipo principal
        tendencia = [valor_equipo * (1 + random.uniform(-0.1, 0.1)) for _ in range(6)]
        comparacion_chart.add_yaxis(f"{equipo.nombre} ⭐", tendencia, color=color, is_smooth=True, symbol_size=8)
        
        # Rivales
        colores = ["#ff6b6b", "#4ecdc4", "#ffd700", "#95a5a6"]
        for i, (nombre_rival, valor_rival) in enumerate(equipos_similares[:4]):
            if nombre_rival != (equipo.nombre_corto or equipo.nombre[:15]):
                tendencia_rival = [valor_rival * (1 + random.uniform(-0.1, 0.1)) for _ in range(6)]
                comparacion_chart.add_yaxis(
                    nombre_rival, tendencia_rival, 
                    color=colores[i % len(colores)], is_smooth=True, symbol_size=6
                )
        
        comparacion_chart.set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"📈 vs Rivales Directos",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#e3e6ee", font_size=14)
            ),
            legend_opts=opts.LegendOpts(pos_top="12%")
        )
        graficos['comparacion_chart'] = mark_safe(comparacion_chart.render_embed())
    except:
        pass
    
    return graficos

# ============================================================================
# AJAX ENDPOINTS
# ============================================================================

@csrf_exempt  # Solo para pruebas, luego usa CSRF correctamente
def ajax_grafico_dispersion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            equipo_id = data.get('equipo_id')
            stat_principal = data.get('stat_principal')
            stat_comparacion = data.get('stat_comparacion', 'Rating')
            
            print(f"🔍 AJAX Dispersión - Principal: {stat_principal}, Comparación: {stat_comparacion}")
            
            # MAPEO COMPLETO DE ESTADÍSTICAS
            STAT_MAPPING = {
                'Rating': 'fotmob_rating',
                'Goles por partido': 'goals_per_match',
                'Goles concedidos por partido': 'goals_conceded_per_match',
                'Posesión promedio': 'average_possession',
                'Vallas invictas': 'clean_sheets',
                'Goles esperados (xG)': 'expected_goals_xg',
                'Tiros al arco por partido': 'shots_on_target_per_match',
                'Ocasiones claras': 'big_chances',
                'Ocasiones claras falladas': 'big_chances_missed',
                'xG concedido': 'xg_concedido',
                'Intercepciones por partido': 'interceptions_per_match',
                'Entradas exitosas por partido': 'successful_tackles_per_match',
                'Despejes por partido': 'clearances_per_match',
                'Atajadas por partido': 'saves_per_match',
                'Faltas por partido': 'fouls_per_match',
                'Tarjetas amarillas': 'yellow_cards',
                'Tarjetas rojas': 'red_cards',
                'Pases precisos por partido': 'accurate_passes_per_match',
                'Pases largos precisos por partido': 'accurate_long_balls_per_match',
                'Centros precisos por partido': 'accurate_crosses_per_match',
                'Toques en el área rival': 'touches_in_opposition_box',
                'Tiros de esquina': 'corners',
                'Recuperaciones en el último tercio': 'possession_won_final_3rd_per_match',
                'Penales a favor': 'penalties_awarded',
            }
            
            field_principal = STAT_MAPPING.get(stat_principal)
            field_comparacion = STAT_MAPPING.get(stat_comparacion)
            
            print(f"🔍 Fields - Principal: {field_principal}, Comparación: {field_comparacion}")
            
            if not field_principal:
                return JsonResponse({
                    'success': False, 
                    'error': f'Estadística principal no válida: {stat_principal}'
                })
                
            if not field_comparacion:
                return JsonResponse({
                    'success': False, 
                    'error': f'Estadística de comparación no válida: {stat_comparacion}'
                })
            
            # Obtener datos de todos los equipos
            equipos_data = []
            todos_equipos = EstadisticasEquipo.objects.select_related('equipo').all()
            
            print(f"🔍 Total equipos en BD: {todos_equipos.count()}")
            
            for eq_stat in todos_equipos:
                val_principal = getattr(eq_stat, field_principal, None)
                val_comparacion = getattr(eq_stat, field_comparacion, None)
                
                if val_principal is not None and val_comparacion is not None:
                    try:
                        equipos_data.append({
                            'nombre': eq_stat.equipo.nombre_corto or eq_stat.equipo.nombre[:15],
                            'stat_principal': float(val_principal),
                            'stat_comparacion': float(val_comparacion),
                            'es_actual': eq_stat.equipo.id == int(equipo_id)
                        })
                    except (ValueError, TypeError):
                        continue
            
            print(f"🔍 Equipos con datos válidos: {len(equipos_data)}")
            
            if not equipos_data:
                return JsonResponse({
                    'success': False, 
                    'error': f'No se encontraron datos para {stat_principal} vs {stat_comparacion}'
                })
            
            # Calcular promedios
            promedio_principal = sum(eq['stat_principal'] for eq in equipos_data) / len(equipos_data)
            promedio_comparacion = sum(eq['stat_comparacion'] for eq in equipos_data) / len(equipos_data)
            
            print(f"✅ Dispersión exitosa: {len(equipos_data)} equipos")
            
            return JsonResponse({
                'success': True,
                'chart_data': {
                    'equipos': equipos_data,
                    'promedio_principal': round(promedio_principal, 2),
                    'promedio_comparacion': round(promedio_comparacion, 2)
                }
            })
            
        except Exception as e:
            print(f"❌ Error AJAX dispersión: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@require_POST  
def ajax_analisis_correlacion(request):
    """Vista AJAX para análisis de correlación"""
    try:
        # Datos simulados
        correlaciones = [
            {'stat': 'Victorias', 'correlacion': 0.75},
            {'stat': 'Goles Favor', 'correlacion': 0.68},
            {'stat': 'Posesión', 'correlacion': 0.45},
            {'stat': 'Goles Contra', 'correlacion': -0.62},
            {'stat': 'Tarjetas', 'correlacion': -0.23}
        ]
        
        return JsonResponse({'success': True, 'correlaciones': correlaciones})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def get_stats_data(stat_name, equipo_id=None):
    STAT_MAPPING = {
        'Rating': 'fotmob_rating',
        'Goles por partido': 'goals_per_match',
        'Goles concedidos por partido': 'goals_conceded_per_match',
        'Posesión promedio': 'average_possession',
        'Vallas invictas': 'clean_sheets',
        'Goles esperados (xG)': 'expected_goals_xg',
        'Tiros al arco por partido': 'shots_on_target_per_match',
        'Ocasiones claras': 'big_chances',
        'Ocasiones claras falladas': 'big_chances_missed',
        'xG concedido': 'xg_concedido',
        'Intercepciones por partido': 'interceptions_per_match',
        'Entradas exitosas por partido': 'successful_tackles_per_match',
        'Despejes por partido': 'clearances_per_match',
        'Atajadas por partido': 'saves_per_match',
        'Faltas por partido': 'fouls_per_match',
        'Tarjetas amarillas': 'yellow_cards',
        'Tarjetas rojas': 'red_cards',
        'Pases precisos por partido': 'accurate_passes_per_match',
        'Pases largos precisos por partido': 'accurate_long_balls_per_match',
        'Centros precisos por partido': 'accurate_crosses_per_match',
        'Toques en el área rival': 'touches_in_opposition_box',
        'Tiros de esquina': 'corners',
        'Recuperaciones en el último tercio': 'possession_won_final_3rd_per_match',
        'Penales a favor': 'penalties_awarded',
    }
    field_name = STAT_MAPPING.get(stat_name)
    if not field_name:
        return [], None

    equipos_stats = EstadisticasEquipo.objects.select_related('equipo').exclude(**{f"{field_name}__isnull": True})
    equipos_valores = []
    valor_equipo = None
    for eq_stat in equipos_stats:
        valor = getattr(eq_stat, field_name, None)
        if valor is not None:
            equipos_valores.append(float(valor))
            if equipo_id and str(eq_stat.equipo.id) == str(equipo_id):
                valor_equipo = float(valor)
    return equipos_valores, valor_equipo
def ajax_boxplot_estadistica(request):
    stat_id = request.GET.get('stat_id')
    equipo_id = request.GET.get('equipo_id')
    equipos_valores, valor_equipo = get_stats_data(stat_id, equipo_id)
    if not equipos_valores:
        return JsonResponse({'success': False, 'error': 'Sin datos'})
    # Boxplot: min, Q1, median, Q3, max
    q1 = np.percentile(equipos_valores, 25)
    q2 = np.percentile(equipos_valores, 50)
    q3 = np.percentile(equipos_valores, 75)
    box = [min(equipos_valores), q1, q2, q3, max(equipos_valores)]
    return JsonResponse({
        'success': True,
        'stat': stat_id,
        'box': box,
        'valores': equipos_valores,
        'valor_equipo': valor_equipo,
    })

def estadistica_jugador(request, jugador_id, estadistica):
    try:
        jugador = get_object_or_404(Jugador, id=jugador_id)
        
        # Obtener el valor actual del jugador para esta estadística
        stat_value = None
        if hasattr(jugador, estadistica):
            stat_value = getattr(jugador, estadistica)
            # Formatear el valor si es necesario
            if stat_value is not None:
                if isinstance(stat_value, float):
                    stat_value = round(stat_value, 2)
        
        # Calcular promedio de la liga para esta estadística
        promedio = None
        if hasattr(Jugador, estadistica):
            valores = Jugador.objects.exclude(**{f'{estadistica}__isnull': True}).values_list(estadistica, flat=True)
            if valores:
                promedio = round(sum(valores) / len(valores), 2)
        
        # Calcular percentil
        percentil = None
        if stat_value is not None:
            valores = list(Jugador.objects.exclude(**{f'{estadistica}__isnull': True}).values_list(estadistica, flat=True))
            if valores:
                valores_menores = [v for v in valores if v < stat_value]
                percentil = round((len(valores_menores) / len(valores)) * 100, 1)
        
        # Obtener posiciones para selectores
        posiciones = Jugador.objects.values_list('posicion', flat=True).distinct()
        posiciones = [p for p in posiciones if p]
        
        context = {
            'jugador': jugador,
            'estadistica': estadistica,
            'stat_value': stat_value,
            'promedio': promedio,
            'percentil': percentil,
            'posiciones': posiciones,
        }
        
        return render(request, 'estadistica_jugador.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar estadística: {str(e)}')
        return redirect('jugador_detalle', jugador_id=jugador_id)
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .recomendacion import (
    recomendar_jugadores_por_perfil, 
    obtener_perfiles_disponibles,
    PERFILES_JUGADORES
)
from .models import Equipo

def recomendacion(request):
    """Página principal de recomendación de jugadores"""
    perfiles = obtener_perfiles_disponibles()
    
    context = {
        'perfiles': perfiles,
        'title': 'Recomendación de Jugadores por Perfil',
        'equipos': Equipo.objects.all().order_by('nombre')
    }
    
    return render(request, 'recomendacion.html', context)


def ajax_recomendar_jugadores(request):
    """AJAX para obtener recomendaciones"""
    perfil = request.GET.get('perfil')
    limite = int(request.GET.get('limite', 10))
    equipo_excluir = request.GET.get('equipo_excluir')
    
    if not perfil or perfil not in PERFILES_JUGADORES:
        return JsonResponse({'error': 'Perfil no válido'}, status=400)
    
    equipo_excluir_id = None
    if equipo_excluir and equipo_excluir.isdigit():
        equipo_excluir_id = int(equipo_excluir)
    
    try:
        recomendaciones = recomendar_jugadores_por_perfil(
            perfil, limite, equipo_excluir_id
        )
        
        # Formatear respuesta para JSON
        jugadores_json = []
        for rec in recomendaciones:
            jugador = rec['jugador']
            jugadores_json.append({
                'id': jugador.id,
                'nombre': jugador.nombre,
                'posicion': jugador.posicion,
                'equipo': jugador.equipo.nombre if jugador.equipo else 'Sin equipo',
                'equipo_logo': jugador.equipo.logo if jugador.equipo and jugador.equipo.logo else None,
                'edad': jugador.edad,
                'pais': jugador.pais,
                'puntuacion': rec['puntuacion'],
                'perfil': rec['perfil'],
                'descripcion_perfil': rec['descripcion_perfil'],
                'stats_destacadas': rec['stats_destacadas']
            })
        
        return JsonResponse({
            'jugadores': jugadores_json,
            'total': len(jugadores_json),
            'perfil_info': {
                'nombre': perfil,
                'descripcion': PERFILES_JUGADORES[perfil]['descripcion']
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


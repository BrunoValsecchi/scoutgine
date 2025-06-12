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

# ============================================================================
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

def stats_equipos(request):
    from .statsequipo import stats_equipos as stats_equipos_func
    return stats_equipos_func(request)

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
    """Vista para mostrar gráfico individual de una estadística"""
    print(f"🎯 Gráfico: equipo {equipo_id}, stat: {stat_name}")
    
    try:
        # Verificar disponibilidad de PyECharts
        try:
            from pyecharts.charts import Line, Bar, Gauge
            from pyecharts import options as opts
            pyecharts_available = True
        except ImportError:
            pyecharts_available = False
            print("⚠️ PyECharts no disponible")
        
        equipo = get_object_or_404(Equipo, id=equipo_id)
        estadisticas_obj = EstadisticasEquipo.objects.filter(equipo=equipo).first()
        
        # Mapeo de estadísticas
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
        
        # Obtener valor de la estadística
        stat_value = None
        field_name = STAT_MAPPING.get(stat_name)
        
        if estadisticas_obj and field_name:
            stat_value = getattr(estadisticas_obj, field_name, None)
        
        # Obtener datos de todos los equipos
        equipos_nombres = []
        equipos_valores = []
        
        if field_name:
            todos_equipos = EstadisticasEquipo.objects.select_related('equipo').exclude(**{f"{field_name}__isnull": True})
            
            for eq_stat in todos_equipos:
                valor = getattr(eq_stat, field_name, 0)
                if valor is not None:
                    nombre = eq_stat.equipo.nombre_corto or eq_stat.equipo.nombre[:15]
                    equipos_nombres.append(nombre)
                    equipos_valores.append(float(valor))
        
        # Calcular métricas
        promedio = sum(equipos_valores) / len(equipos_valores) if equipos_valores else 0
        
        # Calcular posición
        if stat_value and equipos_valores:
            valores_ordenados = sorted(equipos_valores, reverse=True)
            try:
                posicion = valores_ordenados.index(float(stat_value)) + 1
            except ValueError:
                posicion = len(valores_ordenados) + 1
        else:
            posicion = "N/A"
        
        # Generar gráficos
        graficos = {}
        if pyecharts_available and stat_value and equipos_valores:
            graficos = generar_graficos_completos(
                equipo, stat_name, float(stat_value), 
                equipos_nombres, equipos_valores, estadisticas_obj
            )
        
        context = {
            'equipo': equipo,
            'stat_name': stat_name,
            'stat_value': stat_value,
            'promedio': round(promedio, 2) if promedio else "N/A",
            'posicion': posicion,
            'title': f'{stat_name} - {equipo.nombre}',
            'error': None if stat_value else f"No hay datos para {stat_name}",
            **graficos
        }
        
        print(f"✅ Datos: {stat_name} = {stat_value}, pos: {posicion}")
        return render(request, 'estadistica_detalle.html', context)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        context = {
            'error': str(e),
            'title': 'Error - Gráfico',
            'equipo': {'id': equipo_id, 'nombre': 'Error'},
            'stat_name': stat_name
        }
        return render(request, 'estadistica_detalle.html', context)

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


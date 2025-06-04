from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from .models import Equipo, EstadisticasEquipo
from pyecharts.charts import Line, Bar, Pie, Scatter
from pyecharts import options as opts
import random

def grafico_equipo(request, equipo_id, estadistica):
    """Página de gráfico para una estadística específica de equipo"""
    print(f"🎯 Mostrando gráfico de '{estadistica}' para equipo ID: {equipo_id}")
    
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        estadisticas_obj = EstadisticasEquipo.objects.filter(equipo=equipo).first()
        
        print(f"✅ Equipo encontrado: {equipo.nombre} (ID: {equipo.id})")
        
        # Mapeo de nombres de estadísticas a campos del modelo
        stat_mapping = {
            'Rating': 'fotmob_rating',
            'Posesión promedio': 'average_possession', 
            'Faltas por partido': 'fouls_per_match',
            'Tarjetas amarillas': 'yellow_cards',
            'Tarjetas rojas': 'red_cards',
            'Goles por partido': 'goals_per_match',
            'Goles esperados (xG)': 'expected_goals_xg',
            'Tiros al arco por partido': 'shots_on_target_per_match',
            'Ocasiones claras': 'big_chances',
            'Ocasiones claras falladas': 'big_chances_missed',
            'Penales a favor': 'penalties_awarded',
            'Goles concedidos por partido': 'goals_conceded_per_match',
            'Vallas invictas': 'clean_sheets',
            'xG concedido': 'xg_concedido',
            'Intercepciones por partido': 'interceptions_per_match',
            'Entradas exitosas por partido': 'successful_tackles_per_match',
            'Despejes por partido': 'clearances_per_match',
            'Recuperaciones en el último tercio': 'possession_won_final_3rd_per_match',
            'Atajadas por partido': 'saves_per_match',
            'Pases precisos por partido': 'accurate_passes_per_match',
            'Pases largos precisos por partido': 'accurate_long_balls_per_match',
            'Centros precisos por partido': 'accurate_crosses_per_match',
            'Toques en el área rival': 'touches_in_opposition_box',
            'Tiros de esquina': 'corners',
        }
        
        field_name = stat_mapping.get(estadistica)
        if not field_name or not estadisticas_obj:
            raise ValueError(f"Estadística no encontrada: {estadistica}")
            
        # Valor del equipo actual
        valor_equipo = getattr(estadisticas_obj, field_name, 0) or 0
        
        # Obtener datos de todos los equipos para comparación
        todos_equipos = EstadisticasEquipo.objects.select_related('equipo').exclude(**{field_name: None})
        
        # Datos para gráficos
        equipos_nombres = []
        equipos_valores = []
        
        for eq_stat in todos_equipos:
            valor = getattr(eq_stat, field_name, 0) or 0
            equipos_nombres.append(eq_stat.equipo.nombre_corto or eq_stat.equipo.nombre[:15])
            equipos_valores.append(float(valor))
        
        # Promedio general
        promedio = sum(equipos_valores) / len(equipos_valores) if equipos_valores else 0
        
        # Posición del equipo en el ranking
        valores_ordenados = sorted(equipos_valores, reverse=True)
        try:
            posicion = valores_ordenados.index(float(valor_equipo)) + 1
        except ValueError:
            posicion = len(valores_ordenados) + 1
            
        context = {
            'equipo': equipo,  # ← IMPORTANTE: Pasamos el objeto equipo completo
            'stat_name': estadistica,
            'valor_equipo': valor_equipo,
            'promedio': round(promedio, 2),
            'posicion': posicion,
            'total_equipos': len(equipos_valores),
            'equipos_nombres': equipos_nombres,
            'equipos_valores': equipos_valores,
            'title': f'{estadistica} - {equipo.nombre}',
        }
        
        print(f"✅ Estadística: {estadistica} = {valor_equipo}")
        print(f"📊 Posición: {posicion}/{len(equipos_valores)}")
        return render(request, 'estadistica_detalle.html', context)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Incluso en caso de error, pasamos un objeto equipo básico
        try:
            equipo = get_object_or_404(Equipo, id=equipo_id)
        except:
            equipo = {'id': equipo_id, 'nombre': 'Equipo no encontrado'}
            
        context = {
            'equipo': equipo,
            'error': f'Error al cargar la estadística: {estadistica}',
            'title': 'Error'
        }
        return render(request, 'estadistica_detalle.html', context)

def generar_graficos_estadistica(equipo, estadistica, valor_equipo, campo_original):
    """Genera diferentes tipos de gráficos para una estadística"""
    
    # Datos de ejemplo (reemplaza con datos reales de otros equipos)
    equipos_liga = ["Boca", "River", "Racing", "Independiente", "San Lorenzo", "Huracán"]
    valores_liga = [random.uniform(valor_equipo * 0.7, valor_equipo * 1.3) for _ in range(6)]
    valores_liga[0] = valor_equipo  # El primer valor es del equipo actual
    
    # 1. Gráfico de barras comparativo
    bar_chart = (
        Bar(init_opts=opts.InitOpts(width="600px", height="400px", theme="dark"))
        .add_xaxis(equipos_liga)
        .add_yaxis(estadistica, valores_liga, color="#67aaff")
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{estadistica} - Comparación Liga",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#b8c3d9")
            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
            yaxis_opts=opts.AxisOpts(name=estadistica)
        )
    )
    
    # 2. Gráfico de línea temporal (simulado)
    fechas = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
    valores_temporales = [random.uniform(valor_equipo * 0.8, valor_equipo * 1.2) for _ in range(6)]
    
    line_chart = (
        Line(init_opts=opts.InitOpts(width="600px", height="400px", theme="dark"))
        .add_xaxis(fechas)
        .add_yaxis(estadistica, valores_temporales, color="#ff6b6b")
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{estadistica} - Evolución Temporal",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#b8c3d9")
            )
        )
    )
    
    # 3. Gráfico de dispersión vs otras estadísticas
    scatter_data = [[random.uniform(0, 100), random.uniform(0, 100)] for _ in range(20)]
    scatter_data[0] = [valor_equipo, random.uniform(50, 80)]  # Punto del equipo
    
    scatter_chart = (
        Scatter(init_opts=opts.InitOpts(width="600px", height="400px", theme="dark"))
        .add_yaxis(f"{estadistica} vs Otras", scatter_data, color="#4ecdc4")
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{estadistica} - Análisis Correlación",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#b8c3d9")
            )
        )
    )
    
    return {
        'bar_chart_html': mark_safe(bar_chart.render_embed()),
        'line_chart_html': mark_safe(line_chart.render_embed()),
        'scatter_chart_html': mark_safe(scatter_chart.render_embed()),
    }
import logging
from django.shortcuts import render
from django.http import JsonResponse
from .models import Posicion, Torneo, Equipo

logger = logging.getLogger(__name__)

def ligas(request):
    logger.debug('Vista ligas llamada')
    try:
        # Agrupar por nombre y zona (todas las temporadas juntas)
        torneos = Torneo.objects.all().order_by('nombre', 'zona')
        zonas_dict = {}
        for torneo in torneos:
            key = f"{torneo.nombre} - {torneo.zona}" if torneo.zona else torneo.nombre
            if key not in zonas_dict:
                zonas_dict[key] = {
                    'nombre': torneo.nombre,
                    'zona': torneo.zona,
                    'posiciones': []
                }
            posiciones = Posicion.objects.filter(torneo=torneo).select_related('equipo').order_by('posicion')
            for pos in posiciones:
                equipo_nombre = pos.equipo.nombre if pos.equipo else 'Sin equipo'
                zonas_dict[key]['posiciones'].append({
                    'posicion': pos.posicion,
                    'equipo': equipo_nombre,
                    'pj': pos.partidos_jugados,
                    'pg': pos.partidos_ganados,
                    'pe': pos.partidos_empatados,
                    'pp': pos.partidos_perdidos,
                    'gf': pos.goles_a_favor,
                    'gc': pos.goles_en_contra,
                    'dif': pos.goles_a_favor - pos.goles_en_contra,
                    'pts': (pos.partidos_ganados * 3) + pos.partidos_empatados
                })
        # Quitar duplicados de equipos por zona (por si un equipo aparece en varias temporadas)
        for zona in zonas_dict.values():
            equipos_vistos = set()
            posiciones_unicas = []
            for pos in zona['posiciones']:
                if pos['equipo'] not in equipos_vistos:
                    posiciones_unicas.append(pos)
                    equipos_vistos.add(pos['equipo'])
            zona['posiciones'] = sorted(posiciones_unicas, key=lambda x: x['posicion'])
        
        # ✅ AGREGAR DATOS DE STATS EQUIPOS
        from .statsequipo import obtener_stats_resumen  # Crear esta función
        
        try:
            top3_por_estadistica = obtener_stats_resumen()
            print(f"🏆 Datos stats agregados a ligas: {len(top3_por_estadistica)} estadísticas")
        except Exception as e:
            print(f"❌ Error al obtener stats: {e}")
            top3_por_estadistica = {}
        
        context = {
            'torneos': zonas_dict,
            'stats_equipos_data': top3_por_estadistica,  # ← CAMBIO AQUÍ
        }
        return render(request, "ligas.html", context)
    except Exception as e:
        import traceback
        traceback.print_exc()
        context = {
            'torneos': {},
            'error': f'Error: {str(e)}'
        }
        return render(request, "ligas.html", context)

def ligas_api(request):
    try:
        apertura_a = list(Posicion.objects.filter(
            torneo_id=34
        ).select_related('equipo').order_by('posicion').values(
            'posicion', 'equipo__nombre', 'partidos_jugados',
            'partidos_ganados', 'partidos_empatados', 'partidos_perdidos',
            'goles_a_favor', 'goles_en_contra'
        ))
        
        
        # Procesar datos para API
        for item in apertura_a:
            item['dif'] = item['goles_a_favor'] - item['goles_en_contra']
            item['pts'] = (item['partidos_ganados'] * 3) + item['partidos_empatados']
        
        data = {
            'apertura_a': apertura_a,
            'status': 'success'
        }
        
        return JsonResponse(data)
        for zona_key, zona in zonas_dict.items():
            for pos in zona['posiciones']:
                print(f"  - {pos['equipo']}")
    except Exception as e:
        logger.error(f'Error in ligas_api: {e}')
        return JsonResponse({'error': str(e)}, status=500)


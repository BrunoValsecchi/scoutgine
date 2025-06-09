from django.shortcuts import render, get_object_or_404
from .models import Equipo, Jugador, EstadisticasEquipo

def equipo(request):
    """Página simple de equipos con logos desde la base de datos"""
    print("🔥 Página de equipos - Solo logos y links desde BD")
    try:
        equipos_bd = Equipo.objects.all().order_by('nombre')
        total_equipos = equipos_bd.count()
        print(f"📊 Total equipos en BD: {total_equipos}")
        equipos = []
        equipos_con_logo = 0
        for equipo_bd in equipos_bd:
            logo_url = equipo_bd.logo if equipo_bd.logo else None
            if logo_url:
                equipos_con_logo += 1
            equipo_info = {
                'id': equipo_bd.id,
                'nombre': equipo_bd.nombre,
                'nombre_corto': equipo_bd.nombre_corto or equipo_bd.nombre[:15],
                'logo': logo_url,
                'liga': equipo_bd.liga
            }
            equipos.append(equipo_info)
            print(f"✅ {equipo_bd.nombre} - Logo: {'✓' if logo_url else '✗'}")
        context = {
            'equipos': equipos,
            'total_equipos': total_equipos,
            'equipos_con_logo': equipos_con_logo,
            'title': 'Equipos del Fútbol Argentino'
        }
        print(f"🎯 {equipos_con_logo}/{total_equipos} equipos con logo")
        return render(request, "equipo.html", context)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        context = {
            'equipos': [],
            'total_equipos': 0,
            'title': 'Error - Equipos',
            'error': str(e)
        }
        return render(request, "equipo.html", context)

def equipo_detalle(request, equipo_id):
    """Página de detalle de un equipo específico con plantilla"""
    print(f"🔍 Mostrando detalle del equipo ID: {equipo_id}")
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        
        # 🔥 IMPORT PROTEGIDO DE WIKIPEDIA
        wikipedia_info = {'resumen': '', 'url': '', 'fundacion': '', 'estadio': '', 'error': None}
        try:
            from .wikipedia_info import obtener_info_wikipedia
            print(f"🔎 Buscando Wikipedia para: {equipo.nombre}")
            wikipedia_info = obtener_info_wikipedia(equipo)
            print(f"📝 Wikipedia resultado: {wikipedia_info}")
            print(f"📝 Resumen existe: {bool(wikipedia_info.get('resumen'))}")
        except Exception as wiki_error:
            print(f"⚠️ Error con Wikipedia: {wiki_error}")
            import traceback
            traceback.print_exc()
            wikipedia_info['error'] = str(wiki_error)
        
        orden_posiciones = [
            "ENTRENADOR", "COACH", "GK", "CB", "RB", "LB", "DEFENDER", "DM", "CM", "LM", "RM", "AM", "MIDFIELDER", "LW", "RW", "ST", "STRIKER"
        ]
        jugadores = list(Jugador.objects.filter(equipo=equipo))
        def orden_jugador(j):
            pos = (j.posicion or "").split(",")[0].strip().upper()
            try:
                idx = orden_posiciones.index(pos)
            except ValueError:
                idx = len(orden_posiciones)
            return idx, j.nombre.lower()
        jugadores_ordenados = sorted(jugadores, key=orden_jugador)
        total_jugadores = len(jugadores_ordenados)
        estadisticas_obj = EstadisticasEquipo.objects.filter(equipo=equipo).first()
        estadisticas = {}
        traducciones = {
            'fotmob_rating': 'Rating',
            'goals_per_match': 'Goles por partido',
            'goals_conceded_per_match': 'Goles concedidos por partido',
            'average_possession': 'Posesión promedio',
            'clean_sheets': 'Vallas invictas',
            'expected_goals_xg': 'Goles esperados (xG)',
            'shots_on_target_per_match': 'Tiros al arco por partido',
            'big_chances': 'Ocasiones claras',
            'big_chances_missed': 'Ocasiones claras falladas',
            'accurate_passes_per_match': 'Pases precisos por partido',
            'accurate_long_balls_per_match': 'Pases largos precisos por partido',
            'accurate_crosses_per_match': 'Centros precisos por partido',
            'penalties_awarded': 'Penales a favor',
            'touches_in_opposition_box': 'Toques en el área rival',
            'corners': 'Tiros de esquina',
            'xg_conceded': 'xG concedido',
            'interceptions_per_match': 'Intercepciones por partido',
            'successful_tackles_per_match': 'Entradas exitosas por partido',
            'clearances_per_match': 'Despejes por partido',
            'possession_won_final_3rd_per_match': 'Recuperaciones en el último tercio',
            'saves_per_match': 'Atajadas por partido',
            'fouls_per_match': 'Faltas por partido',
            'yellow_cards': 'Tarjetas amarillas',
            'red_cards': 'Tarjetas rojas',
        }
        if estadisticas_obj:
            exclude = ['id', 'equipo']
            for field in estadisticas_obj._meta.fields:
                name = field.name
                if name not in exclude:
                    value = getattr(estadisticas_obj, name)
                    if value is not None:
                        label = traducciones.get(name, name.replace("_", " ").capitalize())
                        estadisticas[label] = value
        context = {
            'equipo': equipo,
            'jugadores': jugadores_ordenados,
            'total_jugadores': total_jugadores,
            'title': f'{equipo.nombre} - Plantilla',
            'estadisticas': estadisticas,
            'wikipedia_info': wikipedia_info,  # ← AGREGAR ESTA LÍNEA
        }
        print(f"✅ Equipo: {equipo.nombre}")
        print(f"👥 Total jugadores: {total_jugadores}")
        print(f"📝 Wikipedia: {'✓' if wikipedia_info.get('resumen') else '✗'}")
        return render(request, 'equipo_detalle.html', context)
    except Exception as e:
        print(f"❌ Error obteniendo equipo {equipo_id}: {e}")
        import traceback
        traceback.print_exc()
        context = {
            'error': 'Equipo no encontrado',
            'title': 'Error'
        }
        return render(request, 'equipo_detalle.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Equipo

def equipo(request):
    """Página simple de equipos con logos desde la base de datos"""
    
    print("🔥 Página de equipos - Solo logos y links desde BD")
    
    try:
        # Obtener equipos desde la base de datos
        equipos_bd = Equipo.objects.all().order_by('nombre')
        total_equipos = equipos_bd.count()
        
        print(f"📊 Total equipos en BD: {total_equipos}")
        
        if total_equipos == 0:
            context = {
                'equipos': [],
                'total_equipos': 0,
                'title': 'Equipos del Fútbol Argentino',
                'error': 'No hay equipos en la base de datos.'
            }
            return render(request, "equipo.html", context)
        
        # Preparar equipos para template
        equipos = []
        equipos_con_logo = 0
        
        for equipo_bd in equipos_bd:
            # Usar el logo desde la BD (campo 'logo')
            logo_url = equipo_bd.logo if equipo_bd.logo else None
            
            if logo_url:
                equipos_con_logo += 1
            
            equipo_info = {
                'id': equipo_bd.id,
                'nombre': equipo_bd.nombre,
                'nombre_corto': equipo_bd.nombre_corto or equipo_bd.nombre[:15],
                'logo': logo_url,  # 👈 CAMBIADO: usar 'logo' en lugar de 'logo_url'
                'liga': equipo_bd.liga
            }
            equipos.append(equipo_info)
            
            # Log para debugging
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
    """Página de detalle de un equipo específico"""
    
    print(f"🔍 Mostrando detalle del equipo ID: {equipo_id}")
    
    try:
        equipo = get_object_or_404(Equipo, id=equipo_id)
        
        context = {
            'equipo': equipo,
            'title': f'{equipo.nombre} - Detalle'
        }
        
        print(f"✅ Equipo encontrado: {equipo.nombre}")
        return render(request, 'equipo_detalle.html', context)
        
    except Exception as e:
        print(f"❌ Error obteniendo equipo {equipo_id}: {e}")
        context = {
            'error': 'Equipo no encontrado',
            'title': 'Error'
        }
        return render(request, 'equipo_detalle.html', context)

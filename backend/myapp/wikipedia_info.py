import wikipedia
import re
from django.core.cache import cache
from .models import Equipo

# Configurar Wikipedia en español
wikipedia.set_lang("es")

def limpiar_texto(texto):
    """Limpia el texto de Wikipedia removiendo referencias y caracteres extraños"""
    if not texto:
        return ""
    
    # Remover referencias como [1], [2], etc.
    texto = re.sub(r'\[\d+\]', '', texto)
    
    # Remover múltiples espacios
    texto = re.sub(r'\s+', ' ', texto)
    

    return texto.strip()

def obtener_info_wikipedia(equipo):
    """Obtiene información de Wikipedia para un equipo específico"""
    # Usar cache para evitar consultas repetidas
    cache_key = f"wikipedia_{equipo.id}"
    cached_info = cache.get(cache_key)
    
    if cached_info:
        print(f"📋 Info de {equipo.nombre} desde cache")
        return cached_info
    
    print(f"🔍 Buscando info de {equipo.nombre} en Wikipedia...")
    
    # Mapeo de nombres de equipos para mejores búsquedas
    busquedas = [
        equipo.nombre,
        f"Club Atlético {equipo.nombre}",
        f"Club {equipo.nombre}",
        f"{equipo.nombre} fútbol",
        f"{equipo.nombre} Argentina"
    ]
    
    # Busquedas específicas para equipos conocidos
    mapeo_equipos = {
        'Boca Juniors': 'Club Atlético Boca Juniors',
        'River Plate': 'Club Atlético River Plate',
        'Racing Club': 'Racing Club de Avellaneda',
        'Independiente': 'Club Atlético Independiente',
        'San Lorenzo': 'Club Atlético San Lorenzo de Almagro',
        'Estudiantes': 'Estudiantes de La Plata',
        'Gimnasia': 'Club de Gimnasia y Esgrima La Plata',
        'Lanús': 'Club Atlético Lanús',
        'Banfield': 'Club Atlético Banfield',
        'Huracán': 'Club Atlético Huracán',
        'Vélez': 'Club Atlético Vélez Sarsfield',
        'Newells': "Newell's Old Boys",
        'Rosario Central': 'Club Atlético Rosario Central',
        'Talleres': 'Club Atlético Talleres',
        'Belgrano': 'Club Atlético Belgrano',
        'Godoy Cruz': 'Club Deportivo Godoy Cruz Antonio Tomba',
        'Platense': 'Club Atlético Platense',
        'Arsenal': 'Arsenal de Sarandí',
        'Tigre': 'Club Atlético Tigre',
        'Defensa y Justicia': 'Club Social y Deportivo Defensa y Justicia',
        'Colón': 'Club Atlético Colón',
        'Unión': 'Club Atlético Unión',
        'Central Córdoba': 'Club Atlético Central Córdoba',
        'Sarmiento': 'Club Atlético Sarmiento',
        'Aldosivi': 'Club Atlético Aldosivi',
        'Patronato': 'Club Atlético Patronato',
    }
    
    # Agregar búsqueda específica si existe en el mapeo
    nombre_simple = equipo.nombre.replace('Club Atlético ', '').replace('Club ', '')
    if nombre_simple in mapeo_equipos:
        busquedas.insert(0, mapeo_equipos[nombre_simple])
    
    info_equipo = {
        'resumen': '',
        'url': '',
        'fundacion': '',
        'estadio': '',
        'error': None
    }
    
    for busqueda in busquedas:
        try:
            print(f"🔎 Intentando: {busqueda}")
            
            # Buscar páginas relacionadas
            resultados = wikipedia.search(busqueda, results=3)
            
            if not resultados:
                continue
                
            # Intentar obtener la página principal
            pagina = wikipedia.page(resultados[0])
            
            # Verificar que sea relevante (contiene palabras clave de fútbol)
            if any(keyword in pagina.content.lower() for keyword in ['fútbol', 'football', 'club', 'equipo', 'argentina', 'liga']):
                info_equipo['resumen'] = limpiar_texto(pagina.summary)
                info_equipo['url'] = pagina.url
                
                # Extraer información adicional del contenido
                contenido = pagina.content.lower()
                
                # Buscar año de fundación
                fundacion_match = re.search(r'fundad[oa].{0,20}(\d{4})', contenido)
                if fundacion_match:
                    info_equipo['fundacion'] = fundacion_match.group(1)
                
                # Buscar estadio
                estadio_match = re.search(r'estadio.{0,50}([A-ZÁÉÍÓÚ][a-záéíóú\s]+)', contenido)
                if estadio_match:
                    estadio = estadio_match.group(1).strip()
                    if len(estadio) < 50:  # Evitar texto muy largo
                        info_equipo['estadio'] = estadio
                
                print(f"✅ Info encontrada para {equipo.nombre}")
                break
                
        except wikipedia.exceptions.DisambiguationError as e:
            # Si hay desambiguación, intentar con la primera opción
            try:
                if e.options:
                    pagina = wikipedia.page(e.options[0])
                    info_equipo['resumen'] = limpiar_texto(pagina.summary)
                    info_equipo['url'] = pagina.url
                    print(f"✅ Info encontrada (desambiguación) para {equipo.nombre}")
                    break
            except:
                continue
                
        except wikipedia.exceptions.PageError:
            continue
            
        except Exception as e:
            print(f"❌ Error con {busqueda}: {e}")
            continue
    
    if not info_equipo['resumen']:
        info_equipo['error'] = f"No se encontró información de Wikipedia para {equipo.nombre}"
        print(f"❌ No se encontró info para {equipo.nombre}")
    
    # Guardar en cache por 1 día
    cache.set(cache_key, info_equipo, 86400)
    
    return info_equipo

def obtener_info_todos_equipos():
    """Obtiene información de Wikipedia para todos los equipos"""
    equipos = Equipo.objects.all()
    resultados = {}
    
    for equipo in equipos:
        print(f"\n🔄 Procesando {equipo.nombre}...")
        info = obtener_info_wikipedia(equipo)
        resultados[equipo.id] = info
    
    return resultados
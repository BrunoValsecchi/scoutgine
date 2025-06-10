from django.shortcuts import render, get_object_or_404
from .models import Jugador, Equipo
import wikipedia
import re

def limpiar_nombre(nombre):
    """
    Limpia el nombre del jugador para buscar en Wikipedia
    """
    # Elimina todo lo que esté después de palabras clave de lesión
    palabras_lesion = [
        'injured', 'injury', 'muscle', 'ankle', 'knee', 'sprained', 
        'hamstring', 'back', 'foot', 'shoulder', 'hip', 'groin', 'calf'
    ]
    
    nombre_limpio = nombre.strip()
    
    # Busca cualquier palabra de lesión y elimina todo lo que sigue
    for palabra in palabras_lesion:
        patron = rf'\s+{palabra}.*$'
        nombre_limpio = re.sub(patron, '', nombre_limpio, flags=re.IGNORECASE)
    
    # Elimina fechas y otros patrones comunes
    patrones_extra = [
        r'\s+-\s+(Late|Early|Mid|A few).*$',  # Fechas y períodos
        r'\s+\(.*\).*$',  # Paréntesis
    ]
    
    for patron in patrones_extra:
        nombre_limpio = re.sub(patron, '', nombre_limpio, flags=re.IGNORECASE)
    
    return nombre_limpio.strip()

def limpiar_contenido_wikipedia(contenido):
    """
    Limpia el contenido de Wikipedia eliminando referencias y limitando texto
    """
    # Eliminar referencias como [1], [11], [123], etc.
    contenido = re.sub(r'\[[\d]+\]', '', contenido)
    
    # Eliminar símbolos extraños como ​
    contenido = re.sub(r'​', '', contenido)
    
    # Tomar solo los primeros 3-4 párrafos (aproximadamente 800-1000 caracteres)
    parrafos = contenido.split('\n\n')
    
    # Filtrar párrafos muy cortos y tomar los primeros contenidos sustanciales
    parrafos_buenos = []
    caracteres_totales = 0
    
    for parrafo in parrafos:
        parrafo = parrafo.strip()
        # Saltar párrafos muy cortos, títulos de sección (==), o líneas vacías
        if len(parrafo) < 50 or parrafo.startswith('==') or parrafo.startswith('==='):
            continue
            
        parrafos_buenos.append(parrafo)
        caracteres_totales += len(parrafo)
        
        # Limitar a aproximadamente 1000 caracteres
        if caracteres_totales > 1000 or len(parrafos_buenos) >= 3:
            break
    
    # Unir los párrafos seleccionados
    resultado = '\n\n'.join(parrafos_buenos)
    
    # Si queda muy largo, cortar en la última oración completa
    if len(resultado) > 1200:
        oraciones = resultado.split('.')
        resultado_corto = ''
        for oracion in oraciones[:-1]:  # Excluir la última oración incompleta
            if len(resultado_corto + oracion + '.') <= 1000:
                resultado_corto += oracion + '.'
            else:
                break
        resultado = resultado_corto
    
    return resultado.strip()

def jugador_detalle(request, jugador_id):
    jugador = get_object_or_404(Jugador, id=jugador_id)
    equipo = jugador.equipo if hasattr(jugador, 'equipo') else None

    # Limpiar el nombre para mostrar y para Wikipedia
    nombre_limpio = limpiar_nombre(jugador.nombre)
    
    contenido = ""
    try:
        wikipedia.set_lang("es")
        print(f"🔍 Nombre original: '{jugador.nombre}' → Limpio: '{nombre_limpio}'")
        page = wikipedia.page(nombre_limpio)
        contenido_bruto = page.content
        contenido = limpiar_contenido_wikipedia(contenido_bruto)
        print(f"✅ Wikipedia encontrada y limpiada para: '{nombre_limpio}'")
    except Exception as e:
        print(f"❌ Error Wikipedia para '{nombre_limpio}': {e}")
        contenido = "No se encontró información en Wikipedia para este jugador."

    return render(request, "jugador_detalle.html", {
        "jugador": jugador,
        "equipo": equipo,
        "nombre_limpio": nombre_limpio,
        "contenido": contenido,
    })
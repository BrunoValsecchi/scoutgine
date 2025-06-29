from .models import EstadisticasJugador, Jugador

def calcular_estrellas_por_grupo_inteligente(jugador, grupos_stats):
    """
    Calcula estrellas por grupo considerando posición del jugador
    
    Args:
        jugador (Jugador): Objeto jugador con posición
        grupos_stats (dict): Grupos de estadísticas GRUPOS_STATS_JUGADORES
        
    Returns:
        dict: Estrellas por grupo + rating general ponderado
    """
    
    # ✅ OBTENER POSICIÓN PRINCIPAL DEL JUGADOR
    posicion_principal = obtener_posicion_principal(jugador.posicion)
    print(f"🔍 Jugador: {jugador.nombre} - Posición: {posicion_principal}")
    
    # ✅ OBTENER ESTADÍSTICAS DEL JUGADOR
    try:
        jugador_stats = EstadisticasJugador.objects.get(jugador=jugador)
    except EstadisticasJugador.DoesNotExist:
        print(f"❌ No hay estadísticas para {jugador.nombre}")
        return crear_resultado_vacio()
    
    # ✅ FILTRAR GRUPOS SEGÚN POSICIÓN
    grupos_filtrados = filtrar_grupos_por_posicion(grupos_stats, posicion_principal)
    
    # ✅ OBTENER PESOS POR POSICIÓN
    pesos_grupos = obtener_pesos_por_posicion(posicion_principal)
    
    resultado = {}
    suma_ponderada = 0
    suma_pesos = 0
    
    for grupo_nombre, estadisticas in grupos_filtrados.items():
        # ✅ CALCULAR PERCENTILES COMPARANDO SOLO CON MISMA POSICIÓN
        percentiles_grupo = []
        
        for nombre_stat, campo in estadisticas:
            percentil = calcular_percentil_por_posicion(
                jugador_stats, campo, posicion_principal
            )
            if percentil is not None:
                percentiles_grupo.append(percentil)
        
        # ✅ PROMEDIO DEL GRUPO
        if percentiles_grupo:
            percentil_promedio = sum(percentiles_grupo) / len(percentiles_grupo)
        else:
            percentil_promedio = 50
        
        # ✅ CONVERTIR A ESTRELLAS
        estrellas = percentil_a_estrellas(percentil_promedio)
        simbolo = generar_simbolo_estrellas(estrellas)
        
        resultado[grupo_nombre] = {
            'estrellas': estrellas,
            'simbolo': simbolo,
            'percentil_promedio': round(percentil_promedio, 1),
            'stats_count': len(percentiles_grupo),
        }
        
        # ✅ SUMAR PARA PROMEDIO PONDERADO
        peso = pesos_grupos.get(grupo_nombre, 1.0)
        suma_ponderada += percentil_promedio * peso
        suma_pesos += peso
        
        print(f"   {grupo_nombre}: {estrellas} estrellas (peso: {peso})")
    
    # ✅ CALCULAR RATING GENERAL PONDERADO
    if suma_pesos > 0:
        percentil_general = suma_ponderada / suma_pesos
    else:
        percentil_general = 50
    
    estrellas_general = percentil_a_estrellas(percentil_general)
    simbolo_general = generar_simbolo_estrellas(estrellas_general)
    
    # ✅ AGREGAR RATING GENERAL AL RESULTADO
    resultado['_general'] = {
        'rating_general': estrellas_general,
        'simbolo_general': simbolo_general,
        'percentil_general': round(percentil_general, 1),
        'posicion': posicion_principal,
        'grupos_evaluados': list(grupos_filtrados.keys())
    }
    
    print(f"🌟 Rating final: {estrellas_general} estrellas ({percentil_general:.1f}%)")
    
    return resultado


def obtener_posicion_principal(posicion_str):
    """
    Extrae la posición principal del jugador
    
    Args:
        posicion_str (str): String de posición del jugador ("Arquero", "Defensor", etc.)
        
    Returns:
        str: Posición principal normalizada
    """
    if not posicion_str:
        return "Mediocampista"
    
    # ✅ MAPEO DE POSICIONES
    mapeo_posiciones = {
        'Arquero': 'Arquero',
        'GK': 'Arquero',
        'Goalkeeper': 'Arquero',
        
        'Defensor': 'Defensor',
        'Defender': 'Defensor',
        'CB': 'Defensor',
        'RB': 'Defensor',
        'LB': 'Defensor',
        'Centro Back': 'Defensor',
        'Lateral': 'Defensor',
        
        'Mediocampista': 'Mediocampista',
        'Midfielder': 'Mediocampista',
        'DM': 'Mediocampista',
        'CM': 'Mediocampista',
        'AM': 'Mediocampista',
        'RM': 'Mediocampista',
        'LM': 'Mediocampista',
        'Medio': 'Mediocampista',
        
        'Delantero': 'Delantero',
        'Attacker': 'Delantero',
        'ST': 'Delantero',
        'CF': 'Delantero',
        'LW': 'Delantero',
        'RW': 'Delantero',
        'Forward': 'Delantero',
    }
    
    # ✅ BUSCAR POSICIÓN EN EL MAPEO
    posicion_limpia = posicion_str.split(',')[0].strip()
    
    for clave, valor in mapeo_posiciones.items():
        if clave.lower() in posicion_limpia.lower():
            return valor
    
    # ✅ DEFAULT: Mediocampista si no encuentra
    return "Mediocampista"


def filtrar_grupos_por_posicion(grupos_stats, posicion):
    """
    Filtra grupos de estadísticas según la posición del jugador
    
    Args:
        grupos_stats (dict): Todos los grupos de estadísticas
        posicion (str): Posición del jugador
        
    Returns:
        dict: Grupos filtrados para la posición
    """
    
    if posicion == "Arquero":
        # ✅ ARQUEROS: Solo estadísticas de arquero
        return {
            "Arqueros": grupos_stats.get("Arqueros", [])
        }
    
    elif posicion == "Defensor":
        # ✅ DEFENSORES: Defensivos + un poco de Pases
        return {
            "Defensivos": grupos_stats.get("Defensivos", []),
            "Pases": grupos_stats.get("Pases", []),
            "Disciplina": grupos_stats.get("Disciplina", [])
        }
    
    elif posicion == "Mediocampista":
        # ✅ MEDIOCAMPISTAS: Balanceado (todos menos arqueros)
        grupos_filtrados = {}
        for grupo, stats in grupos_stats.items():
            if grupo != "Arqueros":
                grupos_filtrados[grupo] = stats
        return grupos_filtrados
    
    elif posicion == "Delantero":
        # ✅ DELANTEROS: Ofensivos + Dribbling + un poco de otros
        return {
            "Ofensivos": grupos_stats.get("Ofensivos", []),
            "Dribbling": grupos_stats.get("Dribbling", []),
            "Pases": grupos_stats.get("Pases", []),
            "Disciplina": grupos_stats.get("Disciplina", [])
        }
    
    # ✅ DEFAULT: Todos excepto arqueros
    grupos_filtrados = {}
    for grupo, stats in grupos_stats.items():
        if grupo != "Arqueros":
            grupos_filtrados[grupo] = stats
    return grupos_filtrados


def obtener_pesos_por_posicion(posicion):
    """
    Obtiene pesos de importancia por grupo según posición
    
    Args:
        posicion (str): Posición del jugador
        
    Returns:
        dict: Pesos por grupo (mayor peso = más importante)
    """
    
    if posicion == "Arquero":
        return {
            "Arqueros": 1.0
        }
    
    elif posicion == "Defensor":
        return {
            "Defensivos": 2.0,    # MÁS IMPORTANTE
            "Pases": 1.0,         # IMPORTANTE
            "Disciplina": 1.5,    # BASTANTE IMPORTANTE
            "Ofensivos": 0.3,     # POCO IMPORTANTE
            "Dribbling": 0.5      # POCO IMPORTANTE
        }
    
    elif posicion == "Mediocampista":
        return {
            "Pases": 2.0,         # MÁS IMPORTANTE
            "Ofensivos": 1.5,     # IMPORTANTE
            "Defensivos": 1.5,    # IMPORTANTE
            "Dribbling": 1.2,     # IMPORTANTE
            "Disciplina": 1.0     # NORMAL
        }
    
    elif posicion == "Delantero":
        return {
            "Ofensivos": 2.5,     # MUY IMPORTANTE
            "Dribbling": 1.8,     # MÁS IMPORTANTE
            "Pases": 0.8,         # MENOS IMPORTANTE
            "Defensivos": 0.2,    # POCO IMPORTANTE
            "Disciplina": 1.0     # NORMAL
        }
    
    # ✅ DEFAULT: Pesos balanceados
    return {
        "Ofensivos": 1.0,
        "Defensivos": 1.0,
        "Pases": 1.0,
        "Dribbling": 1.0,
        "Disciplina": 1.0
    }


def calcular_percentil_por_posicion(jugador_stats, campo, posicion):
    """
    Calcula percentil comparando solo con jugadores de la misma posición
    
    Args:
        jugador_stats (EstadisticasJugador): Stats del jugador
        campo (str): Campo de estadística
        posicion (str): Posición para comparar
        
    Returns:
        float: Percentil (0-100) o None si no hay datos
    """
    
    # ✅ OBTENER VALOR DEL JUGADOR
    valor_jugador = getattr(jugador_stats, campo, None)
    if valor_jugador is None:
        return None
    
    # ✅ CAMPOS DONDE MENOR ES MEJOR
    campos_menor_mejor = {
        'goals_conceded', 'fouls_committed', 'dispossessed', 
        'dribbled_past', 'yellow_cards', 'red_cards', 'error_led_to_goal'
    }
    
    # ✅ OBTENER JUGADORES DE LA MISMA POSICIÓN
    jugadores_misma_posicion = Jugador.objects.filter(
        posicion__icontains=posicion
    )
    
    # ✅ OBTENER VALORES DE LA ESTADÍSTICA PARA ESOS JUGADORES
    stats_misma_posicion = EstadisticasJugador.objects.filter(
        jugador__in=jugadores_misma_posicion
    ).exclude(**{f"{campo}__isnull": True})
    
    valores = []
    for stat in stats_misma_posicion:
        valor = getattr(stat, campo, None)
        if valor is not None:
            valores.append(float(valor))
    
    if len(valores) < 5:  # Mínimo 5 jugadores para comparar
        return None
    
    # ✅ CALCULAR PERCENTIL
    if campo in campos_menor_mejor:
        # Para stats donde menor es mejor, invertir
        menores = sum(1 for v in valores if v > valor_jugador)
    else:
        # Para stats donde mayor es mejor
        menores = sum(1 for v in valores if v < valor_jugador)
    
    percentil = (menores / len(valores)) * 100
    
    return round(percentil, 1)


def crear_resultado_vacio():
    """Crea resultado vacío cuando no hay datos"""
    return {
        '_general': {
            'rating_general': 2.5,
            'simbolo_general': '⭐⭐✨☆☆',
            'percentil_general': 50.0,
            'posicion': 'Sin datos',
            'grupos_evaluados': []
        }
    }


# ✅ FUNCIÓN PRINCIPAL PARA USAR EN OTROS ARCHIVOS
def obtener_estrellas_jugador_completo(jugador, grupos_stats_jugadores):
    """
    Función principal optimizada para obtener estrellas de un jugador
    
    Args:
        jugador (Jugador): Objeto jugador
        grupos_stats_jugadores (dict): GRUPOS_STATS_JUGADORES
        
    Returns:
        dict: Rating completo del jugador
    """
    resultado = calcular_estrellas_por_grupo_inteligente(jugador, grupos_stats_jugadores)
    
    # ✅ EXTRAER DATOS GENERALES
    general_data = resultado.pop('_general', {})
    
    return {
        'rating_general': general_data.get('rating_general', 2.5),
        'simbolo_general': general_data.get('simbolo_general', '⭐⭐✨☆☆'),
        'percentil_general': general_data.get('percentil_general', 50.0),
        'posicion': general_data.get('posicion', 'Sin datos'),
        'grupos': resultado,
        'grupos_evaluados': general_data.get('grupos_evaluados', [])
    }


# ✅ FUNCIONES AUXILIARES (mantener las existentes)
def percentil_a_estrellas(percentil):
    """Convierte percentil (0-100) a estrellas (0.5-5.0)"""
    if percentil <= 5:
        return 0.5
    elif percentil <= 15:
        return 1.0
    elif percentil <= 25:
        return 1.5
    elif percentil <= 35:
        return 2.0
    elif percentil <= 45:
        return 2.5
    elif percentil <= 55:
        return 3.0
    elif percentil <= 70:
        return 3.5
    elif percentil <= 85:
        return 4.0
    elif percentil <= 95:
        return 4.5
    else:
        return 5.0


def generar_simbolo_estrellas(estrellas):
    """Genera símbolo visual de estrellas"""
    estrellas_enteras = int(estrellas)
    tiene_media = (estrellas % 1) == 0.5
    
    simbolo = "⭐" * estrellas_enteras
    
    if tiene_media:
        simbolo += "✨"
    
    estrellas_vacias = 5 - estrellas_enteras - (1 if tiene_media else 0)
    simbolo += "☆" * estrellas_vacias
    
    return simbolo


def formatear_numero(numero):
    """Formatear números para mostrar en templates"""
    if numero is None:
        return "N/A"
    if isinstance(numero, float):
        return f"{numero:.1f}"
    return str(numero)


def obtener_color_rating(rating):
    """Obtener color según rating/percentil"""
    if rating >= 85:
        return "#27ae60"  # Verde excelente
    elif rating >= 70:
        return "#2ecc71"  # Verde bueno
    elif rating >= 55:
        return "#f39c12"  # Naranja promedio
    elif rating >= 35:
        return "#e67e22"  # Naranja bajo
    else:
        return "#e74c3c"  # Rojo malo


# ✅ FUNCIÓN DE TEST MEJORADA
def test_estrellas_inteligente():
    """Test con datos reales de la base de datos"""
    
    # Obtener un jugador real para probar
    try:
        jugador = Jugador.objects.first()
        if not jugador:
            print("❌ No hay jugadores en la base de datos")
            return
        
        # Importar grupos desde comparacion.py
        from .comparacion import GRUPOS_STATS_JUGADORES
        
        # Calcular estrellas
        resultado = obtener_estrellas_jugador_completo(jugador, GRUPOS_STATS_JUGADORES)
        
        print(f"\n🌟 RATING DE {jugador.nombre}:")
        print(f"   Posición: {resultado['posicion']}")
        print(f"   General: {resultado['rating_general']} {resultado['simbolo_general']}")
        print(f"   Percentil: {resultado['percentil_general']}%")
        print(f"   Grupos evaluados: {', '.join(resultado['grupos_evaluados'])}")
        
        print(f"\n📊 POR GRUPOS:")
        for grupo, datos in resultado['grupos'].items():
            print(f"   {grupo}: {datos['estrellas']} {datos['simbolo']} ({datos['percentil_promedio']}%)")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_estrellas_inteligente()
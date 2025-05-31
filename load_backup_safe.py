import pandas as pd
import re

def fix_backup():
    r"""
    Arregla el backup agregando el campo 'tipo' con valor \N entre url y saves
    """
    # Leer el archivo
    with open('datos.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Encontrar la línea COPY
    copy_line_index = None
    for i, line in enumerate(lines):
        if line.startswith('COPY'):
            copy_line_index = i
            break
    
    if copy_line_index is None:
        print("❌ No se encontró la línea COPY")
        return
    
    # Analizar la primera línea de datos para entender la estructura real
    data_start = copy_line_index + 1
    first_data_line = None
    for i in range(data_start, len(lines)):
        if lines[i].strip() and not lines[i].startswith('\\.'):
            first_data_line = lines[i].strip()
            break
    
    if not first_data_line:
        print("❌ No se encontraron datos")
        return
    
    # Contar las columnas en los datos reales
    data_parts = first_data_line.split('\t')
    print(f"🔍 Número de columnas en los datos: {len(data_parts)}")
    print(f"📝 Primeras 5 columnas: {data_parts[:5]}")
    print(f"📝 Últimas 5 columnas: {data_parts[-5:]}")
    
    # La estructura correcta según el modelo Django (incluyendo tipo):
    correct_columns = [
        'id', 'url', 'tipo', 'saves', 'save_percentage', 'goals_conceded', 'goals_prevented', 
        'clean_sheets', 'error_led_to_goal', 'high_claim', 'pass_accuracy', 
        'accurate_long_balls', 'long_ball_accuracy', 'goals', 'expected_goals_xg', 
        'xg_on_target_xgot', 'non_penalty_xg', 'shots', 'shots_on_target', 
        'assists', 'expected_assists_xa', 'successful_passes', 'pass_accuracy_outfield', 
        'accurate_long_balls_outfield', 'long_ball_accuracy_outfield', 'chances_created', 
        'successful_crosses', 'cross_accuracy', 'successful_dribbles', 'dribble_success', 
        'touches', 'touches_in_opposition_box', 'dispossessed', 'fouls_won', 
        'penalties_awarded', 'tackles_won', 'tackles_won_percentage', 'duels_won', 
        'duels_won_percentage', 'aerial_duels_won', 'aerial_duels_won_percentage', 
        'interceptions', 'blocked', 'fouls_committed', 'recoveries', 
        'possession_won_final_3rd', 'dribbled_past', 'yellow_cards', 'red_cards', 
        'jugador_id'
    ]
    
    # Crear nueva línea COPY
    new_copy_line = f"COPY public.myapp_estadisticasjugador ({', '.join(correct_columns)}) FROM stdin;\n"
    
    # Reorganizar los datos
    new_lines = [new_copy_line]
    
    for i in range(data_start, len(lines)):
        line = lines[i].strip()
        if not line or line == '\\.':
            new_lines.append(line + '\n')
            continue
        
        # Procesar línea de datos
        parts = line.split('\t')
        if len(parts) >= 48:  # Verificar que tenemos suficientes columnas
            # Estructura actual: id, url, saves, save_percentage, ..., jugador_id
            # Estructura nueva: id, url, tipo, saves, save_percentage, ..., jugador_id
            
            new_parts = [
                parts[0],  # id
                parts[1],  # url
                '\\N',     # tipo (agregar \N aquí) - usar doble backslash
            ]
            
            # Agregar el resto de las estadísticas (desde saves en adelante)
            # parts[2:] son saves, save_percentage, etc.
            new_parts.extend(parts[2:])
            
            # Ahora tenemos 49 columnas: id, url, tipo, saves, ..., jugador_id
            new_lines.append('\t'.join(new_parts) + '\n')
        else:
            print(f"⚠️ Línea con {len(parts)} columnas (esperadas 48+): {line[:100]}...")
    
    # Agregar línea de terminación
    if not new_lines[-1].strip() == '\\.':
        new_lines.append('\\.\n')
    
    # Guardar archivo corregido
    with open('datos_fixed.csv', 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    
    print("✅ Archivo corregido guardado como 'datos_fixed.csv'")
    print(f"🔄 Nueva línea COPY: {new_copy_line.strip()}")
    
    # Mostrar ejemplo de la primera línea de datos
    if len(new_lines) > 1:
        example_line = new_lines[1].strip()
        example_parts = example_line.split('\t')
        print(f"📝 Ejemplo de línea corregida ({len(example_parts)} columnas):")
        print(f"   ID: {example_parts[0]}")
        print(f"   URL: {example_parts[1]}")
        print(f"   Tipo: {example_parts[2]}")  # Debería mostrar \N
        print(f"   Saves: {example_parts[3]}")
        print(f"   Jugador ID (final): {example_parts[-1]}")

# Ejecutar
fix_backup()
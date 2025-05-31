import os
import django
import re
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scoutgine.settings')
django.setup()

from myapp.models import Posicion, Equipo, Torneo

def verificar_datos_existentes():
    """
    Verifica los datos existentes SIN BORRAR NADA
    """
    print("🔍 VERIFICANDO DATOS EXISTENTES...")
    print("=" * 50)
    
    # Contar datos existentes
    posiciones_count = Posicion.objects.count()
    equipos_count = Equipo.objects.count()
    torneos_count = Torneo.objects.count()
    
    print(f"📊 Posiciones existentes: {posiciones_count}")
    print(f"🏆 Equipos existentes: {equipos_count}")
    print(f"🏆 Torneos existentes: {torneos_count}")
    
    print("\n💡 NO SE BORRARÁ NADA - Solo se añadirán nuevos datos")

def parse_posiciones_csv(csv_path):
    """
    Parsea el archivo CSV de posiciones manejando espacios extra.
    """
    print(f"📄 Leyendo archivo de posiciones: {csv_path}")
    
    with open(csv_path, encoding='utf-8') as f:
        lines = f.readlines()
    
    data_lines = []
    in_data = False
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        if line.startswith('COPY public.myapp_posicion'):
            in_data = True
            print("📊 Encontrada línea COPY de posiciones, comenzando a leer...")
            continue
            
        if line == '\\.':
            print("✅ Fin de datos de posiciones encontrado")
            break
            
        if in_data and line:
            # Usar regex para separar por espacios múltiples o tabulaciones
            fields = re.split(r'\s+', line)
            
            # Debugging: mostrar los primeros campos para ver el formato
            if line_num <= 5:
                print(f"🔍 Línea {line_num}: {len(fields)} campos")
                print(f"    Campos: {fields}")
            
            processed_fields = []
            for i, field in enumerate(fields):
                try:
                    # Campos numéricos
                    if field == '\\N' or field == 'NULL' or field == '':
                        processed_fields.append(None)
                    else:
                        processed_fields.append(int(field))
                            
                except ValueError as e:
                    print(f"⚠️  Error convirtiendo campo {i} ({field}): {e}")
                    processed_fields.append(None)
            
            if len(processed_fields) >= 10:  # Verificar que tengamos todos los campos
                data_lines.append(tuple(processed_fields))
            else:
                print(f"⚠️  Línea {line_num} descartada: esperados 10 campos, encontrados {len(processed_fields)}")
    
    print(f"📊 {len(data_lines)} posiciones procesadas")
    return data_lines

def insert_posiciones(data):
    """
    Inserta las posiciones usando Django ORM - EVITA DUPLICADOS.
    """
    print(f"\n🚀 Añadiendo posiciones usando Django ORM...")
    
    try:
        success_count = 0
        error_count = 0
        duplicates_count = 0
        
        for i, row in enumerate(data, 1):
            try:
                if len(row) < 10:
                    print(f"⚠️  Fila {i}: Longitud incorrecta ({len(row)} campos)")
                    error_count += 1
                    continue
                
                posicion_id = row[0]
                posicion = row[1]
                partidos_jugados = row[2]
                partidos_ganados = row[3]
                partidos_empatados = row[4]
                partidos_perdidos = row[5]
                goles_a_favor = row[6]
                goles_en_contra = row[7]
                equipo_id = row[8]
                torneo_id = row[9]
                
                # Debugging para las primeras filas
                if i <= 5:
                    print(f"🔍 Fila {i}: ID={posicion_id}, Pos={posicion}, PJ={partidos_jugados}, Equipo={equipo_id}, Torneo={torneo_id}")
                
                # Verificar si la posición ya existe
                if Posicion.objects.filter(id=posicion_id).exists():
                    duplicates_count += 1
                    continue
                
                # Verificar que el equipo existe
                try:
                    equipo = Equipo.objects.get(id=equipo_id) if equipo_id and equipo_id != 0 else None
                except Equipo.DoesNotExist:
                    if equipo_id != 0:  # Solo mostrar error si no es 0
                        print(f"⚠️  Fila {i}: Equipo ID {equipo_id} no existe")
                    equipo = None
                
                # Verificar que el torneo existe
                try:
                    torneo = Torneo.objects.get(id=torneo_id) if torneo_id and torneo_id != 0 else None
                except Torneo.DoesNotExist:
                    if torneo_id != 0:  # Solo mostrar error si no es 0
                        print(f"⚠️  Fila {i}: Torneo ID {torneo_id} no existe")
                    torneo = None
                
                # Crear la posición
                posicion_obj = Posicion.objects.create(
                    id=posicion_id,
                    posicion=posicion,
                    partidos_jugados=partidos_jugados,
                    partidos_ganados=partidos_ganados,
                    partidos_empatados=partidos_empatados,
                    partidos_perdidos=partidos_perdidos,
                    goles_a_favor=goles_a_favor,
                    goles_en_contra=goles_en_contra,
                    equipo=equipo,
                    torneo=torneo
                )
                
                success_count += 1
                
                if success_count <= 5:
                    equipo_nombre = equipo.nombre if equipo else "Sin equipo"
                    torneo_nombre = torneo.nombre if torneo else "Sin torneo"
                    print(f"✅ Inserción exitosa #{success_count}: Pos {posicion} - {equipo_nombre} en {torneo_nombre}")
                
            except Exception as e:
                print(f"⚠️  Error en fila {i}: {e}")
                error_count += 1
        
        print(f"✅ {success_count} posiciones AÑADIDAS")
        print(f"🔄 {duplicates_count} posiciones ya existían (ignoradas)")
        print(f"❌ {error_count} errores")
        
        count = Posicion.objects.count()
        print(f"📊 Total de posiciones en la BD: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def verificar_datos_finales():
    print("\n🔍 VERIFICACIÓN FINAL DE DATOS")
    print("=" * 50)
    
    posiciones = Posicion.objects.select_related('equipo', 'torneo').all()
    print(f"📊 Total de posiciones: {posiciones.count()}")
    
    # Agrupar por torneo
    torneos_con_posiciones = {}
    for pos in posiciones:
        torneo_nombre = pos.torneo.nombre if pos.torneo else "Sin torneo"
        if torneo_nombre not in torneos_con_posiciones:
            torneos_con_posiciones[torneo_nombre] = []
        torneos_con_posiciones[torneo_nombre].append(pos)
    
    for torneo_nombre, posiciones_torneo in torneos_con_posiciones.items():
        print(f"\n🏆 {torneo_nombre} ({len(posiciones_torneo)} posiciones):")
        for pos in sorted(posiciones_torneo, key=lambda x: x.posicion)[:5]:
            equipo_nombre = pos.equipo.nombre if pos.equipo else "Sin equipo"
            print(f"  • Pos {pos.posicion}: {equipo_nombre} ({pos.partidos_jugados} PJ, {pos.goles_a_favor}-{pos.goles_en_contra})")

def main():
    print("🚀 CARGADOR DE POSICIONES")
    print("💡 Solo se añadirán datos nuevos, sin borrar nada")
    print("=" * 70)
    
    # PASO 1: VERIFICAR DATOS EXISTENTES
    verificar_datos_existentes()
    
    # PASO 2: Procesar posiciones
    csv_path_posiciones = Path(__file__).parent / "datos.csv"
    if csv_path_posiciones.exists():
        print("\n💡 Añadiendo posiciones...")
        data = parse_posiciones_csv(csv_path_posiciones)
        if data:
            insert_posiciones(data)
        else:
            print("⚠️  No se encontraron datos de posiciones")
    else:
        print(f"❌ Archivo de posiciones no encontrado: {csv_path_posiciones}")
    
    # PASO 3: Verificar resultados finales
    verificar_datos_finales()
    
    print("\n✨ Proceso completado!")

if __name__ == "__main__":
    main()
"""
Script para cargar datos completos del departamento del Quindío
Incluye: ubicaciones (departamento, municipios, zonas, puestos, mesas) y usuarios (coordinadores y testigos)
Ejecutar: python scripts/init/cargar_quindio_completo.py
"""
import csv
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from backend.app import create_app
    from backend.database import db
    from backend.models.location import Location
    from backend.models.user import User
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)

def cargar_quindio_completo():
    """Cargar datos completos del Quindío desde CSV"""
    print("=" * 80)
    print("CARGANDO DATOS COMPLETOS DEL DEPARTAMENTO DEL QUINDÍO")
    print("=" * 80)
    print()
    
    # Verificar que existe el archivo CSV
    csv_file = 'data/divipola.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Error: No se encontró el archivo {csv_file}")
        return
    
    app = create_app()
    
    with app.app_context():
        print("📊 Conectando a la base de datos...")
        print()
        
        # PASO 1: CARGAR UBICACIONES DEL QUINDÍO
        print("🗺️  PASO 1: CARGANDO UBICACIONES DEL QUINDÍO")
        print("-" * 80)
        
        # Leer CSV y filtrar solo Quindío
        print(f"📖 Leyendo archivo {csv_file}...")
        quindio_rows = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['departamento'].strip().upper() == 'QUINDIO':
                    quindio_rows.append(row)
        
        print(f"✅ {len(quindio_rows)} registros del Quindío encontrados")
        print()
        
        if not quindio_rows:
            print("❌ No se encontraron datos del Quindío en el archivo CSV")
            return
        
        # Procesar ubicaciones jerárquicamente
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
        mesas_creadas = 0
        errores = []
        
        print("🔄 Procesando ubicaciones del Quindío...")
        
        for idx, row in enumerate(quindio_rows, 1):
            try:
                dd = row['dd'].strip().zfill(2)
                mm = row['mm'].strip().zfill(2)
                zz = row['zz'].strip().zfill(2)
                pp = row['pp'].strip().zfill(2)
                mesa_num = row['mesa'].strip().zfill(2)
                
                depto_nombre = row['departamento'].strip()
                muni_nombre = row['municipio'].strip()
                puesto_nombre = row['puesto'].strip()
                mesa_nombre = row['mesa_nombre'].strip()
                
                # Códigos completos
                depto_codigo = dd
                muni_codigo = f"{dd}{mm}"
                zona_codigo = f"{dd}{mm}{zz}"
                puesto_codigo = f"{dd}{mm}{zz}{pp}"
                mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa_num}"
                
                # 1. Crear/obtener departamento
                if depto_codigo not in departamentos:
                    dept_existente = Location.query.filter_by(
                        departamento_codigo=depto_codigo,
                        tipo='departamento'
                    ).first()
                    
                    if dept_existente:
                        departamentos[depto_codigo] = dept_existente.id
                    else:
                        dept = Location(
                            departamento_codigo=depto_codigo,
                            departamento_nombre=depto_nombre,
                            nombre_completo=depto_nombre,
                            tipo='departamento',
                            activo=True
                        )
                        db.session.add(dept)
                        db.session.flush()
                        departamentos[depto_codigo] = dept.id
                        print(f"  ✅ Departamento creado: {depto_nombre} ({depto_codigo})")
                
                depto_id = departamentos[depto_codigo]
                
                # 2. Crear/obtener municipio
                if muni_codigo not in municipios:
                    muni_existente = Location.query.filter_by(
                        municipio_codigo=muni_codigo,
                        tipo='municipio'
                    ).first()
                    
                    if muni_existente:
                        municipios[muni_codigo] = muni_existente.id
                    else:
                        nombre_completo = f"{depto_nombre} - {muni_nombre}"
                        muni = Location(
                            departamento_codigo=depto_codigo,
                            municipio_codigo=muni_codigo,
                            departamento_nombre=depto_nombre,
                            municipio_nombre=muni_nombre,
                            nombre_completo=nombre_completo,
                            tipo='municipio',
                            parent_id=depto_id,
                            activo=True
                        )
                        db.session.add(muni)
                        db.session.flush()
                        municipios[muni_codigo] = muni.id
                        print(f"  ✅ Municipio creado: {muni_nombre} ({muni_codigo})")
                
                muni_id = municipios[muni_codigo]
                
                # 3. Crear/obtener zona
                if zona_codigo not in zonas:
                    zona_existente = Location.query.filter_by(
                        zona_codigo=zona_codigo,
                        tipo='zona'
                    ).first()
                    
                    if zona_existente:
                        zonas[zona_codigo] = zona_existente.id
                    else:
                        zona_nombre = f"Zona {zz}"
                        nombre_completo = f"{depto_nombre} - {muni_nombre} - {zona_nombre}"
                        zona = Location(
                            departamento_codigo=depto_codigo,
                            municipio_codigo=muni_codigo,
                            zona_codigo=zona_codigo,
                            departamento_nombre=depto_nombre,
                            municipio_nombre=muni_nombre,
                            nombre_completo=nombre_completo,
                            tipo='zona',
                            parent_id=muni_id,
                            activo=True
                        )
                        db.session.add(zona)
                        db.session.flush()
                        zonas[zona_codigo] = zona.id
                        print(f"  ✅ Zona creada: {zona_nombre} ({zona_codigo})")
                
                zona_id = zonas[zona_codigo]
                
                # 4. Crear/obtener puesto
                if puesto_codigo not in puestos:
                    puesto_existente = Location.query.filter_by(
                        puesto_codigo=puesto_codigo,
                        tipo='puesto'
                    ).first()
                    
                    if puesto_existente:
                        puestos[puesto_codigo] = puesto_existente.id
                    else:
                        # Extraer datos adicionales
                        comuna = row.get('comuna', '').strip()
                        direccion = row.get('direccion', '').strip()
                        latitud = row.get('LATITUD', '').strip()
                        longitud = row.get('LONGITUD', '').strip()
                        
                        nombre_completo = f"{depto_nombre} - {muni_nombre} - {puesto_nombre}"
                        
                        puesto = Location(
                            departamento_codigo=depto_codigo,
                            municipio_codigo=muni_codigo,
                            zona_codigo=zona_codigo,
                            puesto_codigo=puesto_codigo,
                            departamento_nombre=depto_nombre,
                            municipio_nombre=muni_nombre,
                            puesto_nombre=puesto_nombre,
                            nombre_completo=nombre_completo,
                            tipo='puesto',
                            parent_id=zona_id,
                            direccion=direccion or None,
                            latitud=float(latitud) if latitud else None,
                            longitud=float(longitud) if longitud else None,
                            comuna=comuna or None,
                            activo=True
                        )
                        db.session.add(puesto)
                        db.session.flush()
                        puestos[puesto_codigo] = puesto.id
                        print(f"  ✅ Puesto creado: {puesto_nombre} ({puesto_codigo})")
                
                puesto_id = puestos[puesto_codigo]
                
                # 5. Crear mesa
                mesa_existente = Location.query.filter_by(
                    mesa_codigo=mesa_codigo,
                    tipo='mesa'
                ).first()
                
                if not mesa_existente:
                    mujeres = int(row.get('mujeres_mesa', 0) or 0)
                    hombres = int(row.get('hombres_mesa', 0) or 0)
                    total_votantes = int(row.get('total_mesa', 0) or 0)
                    
                    nombre_completo = f"{depto_nombre} - {muni_nombre} - {mesa_nombre}"
                    
                    mesa = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        puesto_codigo=puesto_codigo,
                        mesa_codigo=mesa_codigo,
                        departamento_nombre=depto_nombre,
                        municipio_nombre=muni_nombre,
                        puesto_nombre=puesto_nombre,
                        mesa_nombre=mesa_nombre,
                        nombre_completo=nombre_completo,
                        tipo='mesa',
                        parent_id=puesto_id,
                        total_votantes_registrados=total_votantes,
                        mujeres=mujeres,
                        hombres=hombres,
                        activo=True
                    )
                    db.session.add(mesa)
                    mesas_creadas += 1
                
                if idx % 100 == 0:
                    print(f"  Procesados {idx}/{len(quindio_rows)} registros...")
                    db.session.commit()  # Commit parcial cada 100 registros
                
            except Exception as e:
                errores.append(f"Fila {idx}: {str(e)}")
                print(f"  ⚠️  Error en fila {idx}: {str(e)}")
        
        # Commit de ubicaciones
        print()
        print("💾 Guardando ubicaciones en la base de datos...")
        db.session.commit()
        print("✅ Ubicaciones guardadas exitosamente")
        print()
        
        # PASO 2: CREAR USUARIOS DEL QUINDÍO
        print("👥 PASO 2: CREANDO USUARIOS DEL QUINDÍO")
        print("-" * 80)
        
        # Obtener ubicaciones creadas
        departamento = Location.query.filter_by(
            departamento_codigo=list(departamentos.keys())[0],
            tipo='departamento'
        ).first()
        
        municipios_objs = Location.query.filter_by(
            departamento_codigo=list(departamentos.keys())[0],
            tipo='municipio'
        ).all()
        
        puestos_objs = Location.query.filter_by(
            departamento_codigo=list(departamentos.keys())[0],
            tipo='puesto'
        ).all()
        
        mesas_objs = Location.query.filter_by(
            departamento_codigo=list(departamentos.keys())[0],
            tipo='mesa'
        ).all()
        
        print(f"📍 Ubicaciones disponibles:")
        print(f"   • Departamento: {departamento.nombre_completo}")
        print(f"   • Municipios: {len(municipios_objs)}")
        print(f"   • Puestos: {len(puestos_objs)}")
        print(f"   • Mesas: {len(mesas_objs)}")
        print()
        
        # 2.1 Crear Coordinador Departamental
        print("2.1 Creando Coordinador Departamental...")
        coord_depto = User.query.filter_by(
            rol='coordinador_departamental',
            ubicacion_id=departamento.id
        ).first()
        
        if not coord_depto:
            coord_depto = User(
                nombre='QUINDIO',
                rol='coordinador_departamental',
                ubicacion_id=departamento.id,
                activo=True,
                es_usuario_basico=False
            )
            coord_depto.set_password('test123')
            db.session.add(coord_depto)
            print(f"✅ Creado: QUINDIO (Coordinador Departamental)")
        else:
            print(f"ℹ️  Ya existe: {coord_depto.nombre}")
        
        # 2.2 Crear Coordinadores Municipales
        print("\n2.2 Creando Coordinadores Municipales...")
        coords_muni_creados = 0
        for municipio in municipios_objs:
            nombre_usuario = municipio.municipio_nombre.upper().replace(' ', '_')
            
            coord_muni = User.query.filter_by(
                rol='coordinador_municipal',
                ubicacion_id=municipio.id
            ).first()
            
            if not coord_muni:
                coord_muni = User(
                    nombre=nombre_usuario,
                    rol='coordinador_municipal',
                    ubicacion_id=municipio.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_muni.set_password('test123')
                db.session.add(coord_muni)
                coords_muni_creados += 1
                print(f"✅ Creado: {nombre_usuario} ({municipio.municipio_nombre})")
        
        # 2.3 Crear Coordinadores de Puesto
        print(f"\n2.3 Creando Coordinadores de Puesto...")
        coords_puesto_creados = 0
        for puesto in puestos_objs:
            municipio_nombre = puesto.municipio_nombre.upper().replace(' ', '_')
            nombre_usuario = f"{municipio_nombre}_P{puesto.puesto_codigo[-2:]}"
            
            coord_puesto = User.query.filter_by(
                rol='coordinador_puesto',
                ubicacion_id=puesto.id
            ).first()
            
            if not coord_puesto:
                coord_puesto = User(
                    nombre=nombre_usuario,
                    rol='coordinador_puesto',
                    ubicacion_id=puesto.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_puesto.set_password('test123')
                db.session.add(coord_puesto)
                coords_puesto_creados += 1
                
                if coords_puesto_creados <= 5:  # Mostrar solo los primeros 5
                    print(f"✅ Creado: {nombre_usuario}")
        
        if coords_puesto_creados > 5:
            print(f"   ... y {coords_puesto_creados - 5} más")
        
        # 2.4 Crear Testigos Electorales
        print(f"\n2.4 Creando Testigos Electorales...")
        testigos_creados = 0
        for mesa in mesas_objs:
            # Generar cédula única para cada testigo
            cedula = f"{mesa.mesa_codigo}001"  # Usar código de mesa + 001
            
            # Nombre de usuario basado en ubicación
            municipio_nombre = mesa.municipio_nombre.upper().replace(' ', '_')
            nombre_usuario = f"testigo_{cedula}"
            
            testigo = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=mesa.id
            ).first()
            
            if not testigo:
                testigo = User(
                    nombre=nombre_usuario,
                    cedula=cedula,
                    rol='testigo_electoral',
                    ubicacion_id=mesa.id,
                    activo=True,
                    es_usuario_basico=False
                )
                testigo.set_password('test123')
                db.session.add(testigo)
                testigos_creados += 1
                
                if testigos_creados <= 5:  # Mostrar solo los primeros 5
                    print(f"✅ Creado: {nombre_usuario} (Cédula: {cedula})")
        
        if testigos_creados > 5:
            print(f"   ... y {testigos_creados - 5} más")
        
        # Commit de usuarios
        print()
        print("💾 Guardando usuarios en la base de datos...")
        db.session.commit()
        print("✅ Usuarios guardados exitosamente")
        print()
        
        # RESUMEN FINAL
        print("=" * 80)
        print("RESUMEN DE CARGA DEL QUINDÍO")
        print("=" * 80)
        print()
        print("📊 UBICACIONES:")
        print(f"   • Departamentos: {len(departamentos)}")
        print(f"   • Municipios: {len(municipios)}")
        print(f"   • Zonas: {len(zonas)}")
        print(f"   • Puestos: {len(puestos)}")
        print(f"   • Mesas creadas: {mesas_creadas}")
        print()
        print("👥 USUARIOS:")
        print(f"   • Coordinador Departamental: 1")
        print(f"   • Coordinadores Municipales: {coords_muni_creados}")
        print(f"   • Coordinadores de Puesto: {coords_puesto_creados}")
        print(f"   • Testigos Electorales: {testigos_creados}")
        print()
        print(f"📈 TOTAL REGISTROS PROCESADOS: {len(quindio_rows)}")
        print(f"📈 TOTAL USUARIOS CREADOS: {1 + coords_muni_creados + coords_puesto_creados + testigos_creados}")
        print()
        if errores:
            print(f"⚠️  ERRORES: {len(errores)}")
            for error in errores[:5]:  # Mostrar solo los primeros 5
                print(f"   - {error}")
            if len(errores) > 5:
                print(f"   ... y {len(errores) - 5} errores más")
        else:
            print("✅ SIN ERRORES")
        print()
        print("🔐 CONTRASEÑAS:")
        print("   • Todos los usuarios: test123")
        print()
        print("⚠️  IMPORTANTE:")
        print("   • Cada usuario está vinculado a su ubicación geográfica")
        print("   • Los testigos tienen cédulas únicas generadas automáticamente")
        print("   • El sistema está listo para usar con datos del Quindío")
        print()
        print("=" * 80)

if __name__ == '__main__':
    cargar_quindio_completo()
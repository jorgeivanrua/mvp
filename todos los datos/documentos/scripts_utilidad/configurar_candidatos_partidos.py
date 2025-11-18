"""
Configurar candidatos y partidos para el sistema electoral
"""
from backend.database import db
from backend.models.configuracion_electoral import Partido, Candidato, TipoEleccion
from backend.app import create_app

app = create_app()

def configurar_sistema():
    with app.app_context():
        print("\n" + "="*70)
        print("CONFIGURACIÓN DE CANDIDATOS Y PARTIDOS")
        print("="*70)
        
        # 1. Crear tipo de elección
        print("\n1️⃣  Creando tipo de elección...")
        tipo_eleccion = TipoEleccion.query.filter_by(codigo="ALCALDIA_MUNICIPAL").first()
        
        if not tipo_eleccion:
            tipo_eleccion = TipoEleccion(
                codigo="ALCALDIA_MUNICIPAL",
                nombre="Alcaldía Municipal",
                descripcion="Elección de Alcalde Municipal",
                es_uninominal=True,
                permite_lista_cerrada=False,
                permite_lista_abierta=False,
                permite_coaliciones=True,
                activo=True,
                orden=1
            )
            db.session.add(tipo_eleccion)
            db.session.commit()
            print(f"✅ Tipo de elección creado: {tipo_eleccion.nombre}")
        else:
            print(f"✅ Tipo de elección ya existe: {tipo_eleccion.nombre}")
        
        # 2. Crear partidos políticos
        print("\n2️⃣  Creando partidos políticos...")
        
        partidos_data = [
            {
                "codigo": "PLC",
                "nombre": "Partido Liberal Colombiano",
                "nombre_corto": "Liberal",
                "color": "#FF0000",
                "orden": 1
            },
            {
                "codigo": "PCC",
                "nombre": "Partido Conservador Colombiano",
                "nombre_corto": "Conservador",
                "color": "#0000FF",
                "orden": 2
            },
            {
                "codigo": "PV",
                "nombre": "Partido Verde",
                "nombre_corto": "Verde",
                "color": "#00FF00",
                "orden": 3
            },
            {
                "codigo": "CD",
                "nombre": "Centro Democrático",
                "nombre_corto": "Centro Democrático",
                "color": "#FFA500",
                "orden": 4
            },
            {
                "codigo": "PH",
                "nombre": "Pacto Histórico",
                "nombre_corto": "Pacto Histórico",
                "color": "#800080",
                "orden": 5
            }
        ]
        
        partidos_creados = []
        for partido_data in partidos_data:
            partido = Partido.query.filter_by(codigo=partido_data["codigo"]).first()
            
            if not partido:
                partido = Partido(
                    codigo=partido_data["codigo"],
                    nombre=partido_data["nombre"],
                    nombre_corto=partido_data["nombre_corto"],
                    color=partido_data["color"],
                    orden=partido_data["orden"],
                    activo=True
                )
                db.session.add(partido)
                partidos_creados.append(partido)
                print(f"✅ Partido creado: {partido.codigo} - {partido.nombre}")
            else:
                partidos_creados.append(partido)
                print(f"✅ Partido ya existe: {partido.codigo} - {partido.nombre}")
        
        db.session.commit()
        
        # 3. Crear candidatos
        print("\n3️⃣  Creando candidatos...")
        
        candidatos_data = [
            {
                "codigo": "CAND_001",
                "nombre": "Juan Carlos Rodríguez",
                "partido_codigo": "PLC",
                "numero_lista": 1
            },
            {
                "codigo": "CAND_002",
                "nombre": "María Fernanda Gómez",
                "partido_codigo": "PCC",
                "numero_lista": 2
            },
            {
                "codigo": "CAND_003",
                "nombre": "Pedro Antonio Martínez",
                "partido_codigo": "PV",
                "numero_lista": 3
            },
            {
                "codigo": "CAND_004",
                "nombre": "Ana Lucía Ramírez",
                "partido_codigo": "CD",
                "numero_lista": 4
            },
            {
                "codigo": "CAND_005",
                "nombre": "Carlos Eduardo López",
                "partido_codigo": "PH",
                "numero_lista": 5
            }
        ]
        
        candidatos_creados = []
        for candidato_data in candidatos_data:
            # Buscar partido
            partido = Partido.query.filter_by(codigo=candidato_data["partido_codigo"]).first()
            
            if not partido:
                print(f"❌ Partido no encontrado: {candidato_data['partido_codigo']}")
                continue
            
            # Verificar si el candidato ya existe
            candidato = Candidato.query.filter_by(
                codigo=candidato_data["codigo"]
            ).first()
            
            if not candidato:
                candidato = Candidato(
                    codigo=candidato_data["codigo"],
                    nombre_completo=candidato_data["nombre"],
                    partido_id=partido.id,
                    tipo_eleccion_id=tipo_eleccion.id,
                    numero_lista=candidato_data["numero_lista"],
                    es_cabeza_lista=True,
                    activo=True,
                    orden=candidato_data["numero_lista"]
                )
                db.session.add(candidato)
                candidatos_creados.append(candidato)
                print(f"✅ Candidato creado: {candidato.nombre_completo} ({partido.codigo})")
            else:
                candidatos_creados.append(candidato)
                print(f"✅ Candidato ya existe: {candidato.nombre_completo}")
        
        db.session.commit()
        
        # 4. Resumen
        print("\n" + "="*70)
        print("RESUMEN DE CONFIGURACIÓN")
        print("="*70)
        
        total_partidos = Partido.query.filter_by(activo=True).count()
        total_candidatos = Candidato.query.filter_by(activo=True).count()
        total_tipos = TipoEleccion.query.filter_by(activo=True).count()
        
        print(f"\n✅ Tipos de Elección: {total_tipos}")
        print(f"✅ Partidos Políticos: {total_partidos}")
        print(f"✅ Candidatos: {total_candidatos}")
        
        print("\n📋 PARTIDOS CONFIGURADOS:")
        partidos = Partido.query.filter_by(activo=True).all()
        for partido in partidos:
            candidatos_partido = Candidato.query.filter_by(
                partido_id=partido.id,
                activo=True
            ).count()
            print(f"  - {partido.codigo}: {partido.nombre} ({candidatos_partido} candidatos)")
        
        print("\n👥 CANDIDATOS CONFIGURADOS:")
        candidatos = Candidato.query.filter_by(activo=True).all()
        for candidato in candidatos:
            partido = Partido.query.get(candidato.partido_id)
            print(f"  - #{candidato.numero_lista}: {candidato.nombre_completo} ({partido.codigo})")
        
        print("\n" + "="*70)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("="*70)
        print("\n🎯 Ahora puedes:")
        print("  1. Login como Super Admin (test123)")
        print("  2. Ir al dashboard de Super Admin")
        print("  3. Ver partidos y candidatos configurados")
        print("  4. Los coordinadores pueden usar el formulario E14")
        print("\n" + "="*70)

if __name__ == '__main__':
    configurar_sistema()

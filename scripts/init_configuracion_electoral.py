"""
Script para inicializar configuración electoral
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import (
    TipoEleccion, Partido, Coalicion, PartidoCoalicion, Candidato
)


def init_configuracion():
    """Inicializar configuración electoral con datos de ejemplo"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n>> Creando tablas de configuración electoral...")
        
        # Crear tablas
        db.create_all()
        print("✓ Tablas creadas")
        
        # Limpiar datos existentes
        print("\n>> Limpiando datos existentes...")
        Candidato.query.delete()
        PartidoCoalicion.query.delete()
        Coalicion.query.delete()
        Partido.query.delete()
        TipoEleccion.query.delete()
        db.session.commit()
        print("✓ Datos limpiados")
        
        # Crear tipos de elección
        print("\n>> Creando tipos de elección...")
        tipos = [
            TipoEleccion(codigo='senado', nombre='Senado de la República', orden=1),
            TipoEleccion(codigo='camara', nombre='Cámara de Representantes', orden=2),
            TipoEleccion(codigo='asamblea', nombre='Asamblea Departamental', orden=3),
            TipoEleccion(codigo='concejo', nombre='Concejo Municipal', orden=4),
            TipoEleccion(codigo='jal', nombre='Juntas Administradoras Locales (JAL)', orden=5),
            TipoEleccion(codigo='ediles', nombre='Ediles', orden=6),
        ]
        
        for tipo in tipos:
            db.session.add(tipo)
        
        db.session.commit()
        print(f"✓ {len(tipos)} tipos de elección creados")
        
        # Crear partidos
        print("\n>> Creando partidos políticos...")
        partidos_data = [
            {'codigo': 'LIBERAL', 'nombre': 'Partido Liberal Colombiano', 'nombre_corto': 'Liberal', 'color': '#FF0000', 'orden': 1},
            {'codigo': 'CONSERVADOR', 'nombre': 'Partido Conservador Colombiano', 'nombre_corto': 'Conservador', 'color': '#0000FF', 'orden': 2},
            {'codigo': 'VERDE', 'nombre': 'Partido Alianza Verde', 'nombre_corto': 'Verde', 'color': '#00FF00', 'orden': 3},
            {'codigo': 'CAMBIO_RADICAL', 'nombre': 'Partido Cambio Radical', 'nombre_corto': 'Cambio Radical', 'color': '#FFA500', 'orden': 4},
            {'codigo': 'CENTRO_DEMOCRATICO', 'nombre': 'Centro Democrático', 'nombre_corto': 'Centro Democrático', 'color': '#000080', 'orden': 5},
            {'codigo': 'POLO', 'nombre': 'Polo Democrático Alternativo', 'nombre_corto': 'Polo', 'color': '#FFFF00', 'orden': 6},
            {'codigo': 'MIRA', 'nombre': 'Movimiento Independiente de Renovación Absoluta', 'nombre_corto': 'MIRA', 'color': '#800080', 'orden': 7},
            {'codigo': 'COMUNES', 'nombre': 'Comunes', 'nombre_corto': 'Comunes', 'color': '#FF69B4', 'orden': 8},
            {'codigo': 'PACTO_HISTORICO', 'nombre': 'Pacto Histórico', 'nombre_corto': 'Pacto Histórico', 'color': '#8B0000', 'orden': 9},
            {'codigo': 'COLOMBIA_HUMANA', 'nombre': 'Colombia Humana', 'nombre_corto': 'Colombia Humana', 'color': '#4B0082', 'orden': 10},
        ]
        
        partidos = []
        for data in partidos_data:
            partido = Partido(**data)
            db.session.add(partido)
            partidos.append(partido)
        
        db.session.commit()
        print(f"✓ {len(partidos)} partidos creados")
        
        # Crear candidatos de ejemplo
        print("\n>> Creando candidatos de ejemplo...")
        tipo_concejo = TipoEleccion.query.filter_by(codigo='concejo').first()
        
        candidatos_data = [
            {'codigo': 'CAND001', 'nombre_completo': 'Juan Pérez García', 'numero_lista': 1, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 1},
            {'codigo': 'CAND002', 'nombre_completo': 'María López Rodríguez', 'numero_lista': 2, 'partido_id': partidos[0].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 2},
            {'codigo': 'CAND003', 'nombre_completo': 'Carlos Martínez Silva', 'numero_lista': 1, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 3},
            {'codigo': 'CAND004', 'nombre_completo': 'Ana Gómez Torres', 'numero_lista': 2, 'partido_id': partidos[1].id, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 4},
            {'codigo': 'CAND005', 'nombre_completo': 'Pedro Sánchez Díaz', 'es_independiente': True, 'tipo_eleccion_id': tipo_concejo.id, 'orden': 5},
        ]
        
        for data in candidatos_data:
            candidato = Candidato(**data)
            db.session.add(candidato)
        
        db.session.commit()
        print(f"✓ {len(candidatos_data)} candidatos creados")
        
        # Crear coalición de ejemplo
        print("\n>> Creando coalición de ejemplo...")
        coalicion = Coalicion(
            codigo='COALICION_CENTRO',
            nombre='Coalición por el Centro',
            descripcion='Coalición de partidos de centro'
        )
        db.session.add(coalicion)
        db.session.flush()
        
        # Agregar partidos a la coalición
        pc1 = PartidoCoalicion(partido_id=partidos[3].id, coalicion_id=coalicion.id)
        pc2 = PartidoCoalicion(partido_id=partidos[4].id, coalicion_id=coalicion.id)
        db.session.add(pc1)
        db.session.add(pc2)
        
        db.session.commit()
        print("✓ 1 coalición creada")
        
        print("\n" + "="*60)
        print("CONFIGURACIÓN ELECTORAL INICIALIZADA EXITOSAMENTE")
        print("="*60)
        print(f"\n✓ Tipos de Elección: {len(tipos)}")
        print(f"✓ Partidos: {len(partidos)}")
        print(f"✓ Candidatos: {len(candidatos_data)}")
        print(f"✓ Coaliciones: 1")
        print("\n" + "="*60)


if __name__ == '__main__':
    init_configuracion()

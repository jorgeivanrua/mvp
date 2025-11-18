#!/usr/bin/env python3
"""
Script para agregar más tipos de elecciones a la base de datos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import TipoEleccion

def agregar_tipos_elecciones():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("AGREGANDO NUEVOS TIPOS DE ELECCIONES")
        print("=" * 60)
        
        # Obtener el orden máximo actual
        max_orden = db.session.query(db.func.max(TipoEleccion.orden)).scalar() or 0
        
        nuevos_tipos = [
            {
                'codigo': 'GOBERNACION',
                'nombre': 'Gobernación',
                'descripcion': 'Elección de Gobernador Departamental',
                'es_uninominal': True,
                'permite_lista_cerrada': False,
                'permite_lista_abierta': False,
                'permite_coaliciones': True,
                'orden': max_orden + 1
            },
            {
                'codigo': 'ASAMBLEA',
                'nombre': 'Asamblea Departamental',
                'descripcion': 'Elección de Diputados a la Asamblea Departamental',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': True,
                'orden': max_orden + 2
            },
            {
                'codigo': 'CONCEJO',
                'nombre': 'Concejo Municipal',
                'descripcion': 'Elección de Concejales Municipales',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': True,
                'orden': max_orden + 3
            },
            {
                'codigo': 'JAL',
                'nombre': 'JAL - Juntas Administradoras Locales',
                'descripcion': 'Elección de miembros de Juntas Administradoras Locales',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': False,
                'orden': max_orden + 4
            },
            {
                'codigo': 'CONCEJO_JUVENTUD',
                'nombre': 'Concejo de Juventudes',
                'descripcion': 'Elección de Concejo Municipal de Juventud',
                'es_uninominal': False,
                'permite_lista_cerrada': True,
                'permite_lista_abierta': True,
                'permite_coaliciones': False,
                'orden': max_orden + 5
            }
        ]
        
        agregados = 0
        actualizados = 0
        
        for tipo_data in nuevos_tipos:
            # Verificar si ya existe
            tipo_existente = TipoEleccion.query.filter_by(codigo=tipo_data['codigo']).first()
            
            if tipo_existente:
                # Actualizar
                print(f"\n📝 Actualizando: {tipo_data['nombre']}")
                tipo_existente.nombre = tipo_data['nombre']
                tipo_existente.descripcion = tipo_data['descripcion']
                tipo_existente.es_uninominal = tipo_data['es_uninominal']
                tipo_existente.permite_lista_cerrada = tipo_data['permite_lista_cerrada']
                tipo_existente.permite_lista_abierta = tipo_data['permite_lista_abierta']
                tipo_existente.permite_coaliciones = tipo_data['permite_coaliciones']
                tipo_existente.activo = True
                actualizados += 1
            else:
                # Crear nuevo
                print(f"\n✅ Agregando: {tipo_data['nombre']}")
                nuevo_tipo = TipoEleccion(
                    codigo=tipo_data['codigo'],
                    nombre=tipo_data['nombre'],
                    descripcion=tipo_data['descripcion'],
                    es_uninominal=tipo_data['es_uninominal'],
                    permite_lista_cerrada=tipo_data['permite_lista_cerrada'],
                    permite_lista_abierta=tipo_data['permite_lista_abierta'],
                    permite_coaliciones=tipo_data['permite_coaliciones'],
                    activo=True,
                    orden=tipo_data['orden']
                )
                db.session.add(nuevo_tipo)
                agregados += 1
            
            print(f"   Código: {tipo_data['codigo']}")
            print(f"   Tipo: {'Uninominal' if tipo_data['es_uninominal'] else 'Por listas'}")
            print(f"   Permite coaliciones: {'Sí' if tipo_data['permite_coaliciones'] else 'No'}")
        
        # Guardar cambios
        db.session.commit()
        
        print("\n" + "=" * 60)
        print("RESUMEN:")
        print(f"  ✅ Tipos agregados: {agregados}")
        print(f"  📝 Tipos actualizados: {actualizados}")
        print("=" * 60)
        
        # Mostrar todos los tipos de elección
        print("\n📋 TODOS LOS TIPOS DE ELECCIÓN EN EL SISTEMA:")
        todos_tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.orden).all()
        for tipo in todos_tipos:
            tipo_str = "Uninominal" if tipo.es_uninominal else "Por listas"
            print(f"  {tipo.orden}. {tipo.nombre} ({tipo_str})")
        
        print("\n✅ Proceso completado exitosamente")

if __name__ == '__main__':
    agregar_tipos_elecciones()

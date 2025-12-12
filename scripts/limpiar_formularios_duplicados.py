#!/usr/bin/env python3
"""
Script para limpiar formularios E-14 duplicados
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import db
from backend.models.formulario_e14 import FormularioE14
from backend.app import create_app

def limpiar_formularios_duplicados():
    """Eliminar formularios duplicados, dejando solo el más reciente por mesa y tipo de elección"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Buscando formularios duplicados...")
        
        # Obtener todos los formularios
        formularios = FormularioE14.query.order_by(
            FormularioE14.mesa_id,
            FormularioE14.tipo_eleccion_id,
            FormularioE14.created_at.desc()
        ).all()
        
        # Agrupar por mesa y tipo de elección
        grupos = {}
        for form in formularios:
            key = (form.mesa_id, form.tipo_eleccion_id)
            if key not in grupos:
                grupos[key] = []
            grupos[key].append(form)
        
        # Encontrar duplicados
        duplicados_encontrados = 0
        formularios_a_eliminar = []
        
        for key, forms in grupos.items():
            if len(forms) > 1:
                mesa_id, tipo_id = key
                print(f"\n📋 Mesa {mesa_id}, Tipo Elección {tipo_id}: {len(forms)} formularios")
                
                # Mantener el más reciente, eliminar los demás
                mas_reciente = forms[0]
                duplicados = forms[1:]
                
                print(f"  ✅ Mantener: ID {mas_reciente.id} (creado: {mas_reciente.created_at}, testigo: {mas_reciente.testigo_id})")
                
                for dup in duplicados:
                    print(f"  ❌ Eliminar: ID {dup.id} (creado: {dup.created_at}, testigo: {dup.testigo_id})")
                    formularios_a_eliminar.append(dup)
                    duplicados_encontrados += 1
        
        if duplicados_encontrados == 0:
            print("\n✅ No se encontraron formularios duplicados")
            return
        
        print(f"\n⚠️  Se encontraron {duplicados_encontrados} formularios duplicados")
        respuesta = input("¿Desea eliminarlos? (s/n): ")
        
        if respuesta.lower() == 's':
            for form in formularios_a_eliminar:
                print(f"  🗑️  Eliminando formulario ID {form.id}...")
                db.session.delete(form)
            
            db.session.commit()
            print(f"\n✅ {duplicados_encontrados} formularios duplicados eliminados exitosamente")
        else:
            print("\n❌ Operación cancelada")

def listar_todos_formularios():
    """Listar todos los formularios en la base de datos"""
    app = create_app()
    
    with app.app_context():
        formularios = FormularioE14.query.order_by(FormularioE14.created_at.desc()).all()
        
        print(f"\n📊 Total de formularios: {len(formularios)}\n")
        
        for form in formularios:
            print(f"ID: {form.id}")
            print(f"  Mesa: {form.mesa_id}")
            print(f"  Testigo: {form.testigo_id}")
            print(f"  Tipo Elección: {form.tipo_eleccion_id}")
            print(f"  Estado: {form.estado}")
            print(f"  Creado: {form.created_at}")
            print(f"  Total Votos: {form.total_votos}")
            print()

def eliminar_todos_formularios():
    """Eliminar TODOS los formularios (usar con precaución)"""
    app = create_app()
    
    with app.app_context():
        count = FormularioE14.query.count()
        
        if count == 0:
            print("✅ No hay formularios para eliminar")
            return
        
        print(f"⚠️  ADVERTENCIA: Se eliminarán {count} formularios")
        respuesta = input("¿Está SEGURO de que desea eliminar TODOS los formularios? (escriba 'SI' para confirmar): ")
        
        if respuesta == 'SI':
            FormularioE14.query.delete()
            db.session.commit()
            print(f"✅ {count} formularios eliminados exitosamente")
        else:
            print("❌ Operación cancelada")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gestión de formularios E-14')
    parser.add_argument('accion', choices=['limpiar', 'listar', 'eliminar-todos'],
                       help='Acción a realizar')
    
    args = parser.parse_args()
    
    if args.accion == 'limpiar':
        limpiar_formularios_duplicados()
    elif args.accion == 'listar':
        listar_todos_formularios()
    elif args.accion == 'eliminar-todos':
        eliminar_todos_formularios()

#!/usr/bin/env python3
"""
Eliminar testigos creados manualmente
Solo mantener usuarios que vienen de DIVIPOLA
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User

def eliminar_testigos_manuales():
    """Eliminar testigos creados manualmente"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("ELIMINANDO TESTIGOS CREADOS MANUALMENTE")
        print("=" * 80)
        
        # Primero, eliminar todos los formularios E-14
        from backend.models.formulario_e14 import FormularioE14
        
        formularios = FormularioE14.query.all()
        if formularios:
            print(f"\n⚠️  Encontrados {len(formularios)} formularios E-14")
            print("Eliminando formularios E-14...")
            for form in formularios:
                db.session.delete(form)
            db.session.commit()
            print(f"✅ {len(formularios)} formularios E-14 eliminados")
        
        # Buscar testigos con nombres específicos que fueron creados manualmente
        testigos_manuales = [
            'Testigo Electoral Puesto 01',
            'Testigo Mesa 01',
            'Testigo Mesa 02',
            'Testigo Mesa 03',
            'testigo.puesto01',
            'testigo.mesa01',
            'testigo.mesa02',
            'testigo.mesa03'
        ]
        
        eliminados = 0
        
        for nombre in testigos_manuales:
            # Buscar por nombre exacto
            testigo = User.query.filter_by(nombre=nombre).first()
            if testigo:
                print(f"\n❌ Eliminando: {testigo.nombre} (ID: {testigo.id}, Rol: {testigo.rol})")
                db.session.delete(testigo)
                eliminados += 1
        
        # También buscar testigos con rol 'testigo' o 'testigo_electoral'
        testigos_rol = User.query.filter(
            (User.rol == 'testigo') | (User.rol == 'testigo_electoral')
        ).all()
        
        print(f"\n\nTestigos encontrados por rol: {len(testigos_rol)}")
        for testigo in testigos_rol:
            if testigo.nombre not in testigos_manuales:
                print(f"  ⚠️  Testigo adicional encontrado: {testigo.nombre} (ID: {testigo.id})")
                respuesta = input(f"    ¿Eliminar este testigo? (s/n): ")
                if respuesta.lower() == 's':
                    db.session.delete(testigo)
                    eliminados += 1
                    print(f"    ❌ Eliminado")
        
        if eliminados > 0:
            db.session.commit()
            print(f"\n✅ {eliminados} testigos eliminados exitosamente")
        else:
            print("\n✅ No se encontraron testigos para eliminar")
        
        # Verificar usuarios restantes
        print("\n" + "=" * 80)
        print("USUARIOS RESTANTES EN EL SISTEMA")
        print("=" * 80)
        
        usuarios = User.query.all()
        print(f"\nTotal usuarios: {len(usuarios)}\n")
        
        roles = {}
        for user in usuarios:
            if user.rol not in roles:
                roles[user.rol] = []
            roles[user.rol].append(user)
        
        for rol, users in sorted(roles.items()):
            print(f"{rol.upper()}: {len(users)} usuarios")
            for user in users:
                print(f"  - {user.nombre}")

if __name__ == '__main__':
    eliminar_testigos_manuales()

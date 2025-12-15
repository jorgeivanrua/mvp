#!/usr/bin/env python3
"""
Script para crear usuario coordinador de puesto para pruebas del modal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db
from werkzeug.security import generate_password_hash

def crear_coordinador_puesto():
    app = create_app()
    
    with app.app_context():
        try:
            # Buscar el puesto donde está el formulario ID 1
            print("🔍 Buscando datos del formulario...")
            
            # Verificar si ya existe el usuario
            usuario_existente = User.query.filter_by(nombre='COORD_PUESTO_TEST').first()
            if usuario_existente:
                print(f"✅ Usuario ya existe: {usuario_existente.nombre} (ID: {usuario_existente.id})")
                print(f"   Rol: {usuario_existente.rol}")
                print(f"   Ubicación ID: {usuario_existente.ubicacion_id}")
                print(f"   Activo: {usuario_existente.activo}")
                return usuario_existente
            
            # Buscar un puesto disponible
            puesto = Location.query.filter_by(tipo='puesto').first()
            if not puesto:
                print("❌ No se encontró ningún puesto en la base de datos")
                return None
            
            print(f"📍 Puesto encontrado: {puesto.nombre_completo} (ID: {puesto.id})")
            
            # Crear el usuario coordinador
            nuevo_usuario = User(
                nombre='COORD_PUESTO_TEST',
                cedula='99999999',
                password_hash=generate_password_hash('test123'),
                rol='coordinador_puesto',
                ubicacion_id=puesto.id,
                activo=True
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            print("✅ Usuario coordinador creado exitosamente:")
            print(f"   Nombre: {nuevo_usuario.nombre}")
            print(f"   Cédula: {nuevo_usuario.cedula}")
            print(f"   Contraseña: test123")
            print(f"   Rol: {nuevo_usuario.rol}")
            print(f"   Puesto: {puesto.nombre_completo}")
            print(f"   ID Usuario: {nuevo_usuario.id}")
            print(f"   ID Ubicación: {nuevo_usuario.ubicacion_id}")
            
            return nuevo_usuario
            
        except Exception as e:
            print(f"❌ Error creando usuario: {e}")
            db.session.rollback()
            return None

if __name__ == "__main__":
    crear_coordinador_puesto()
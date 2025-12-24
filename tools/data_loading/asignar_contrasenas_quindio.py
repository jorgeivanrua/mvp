#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para asignar contraseñas a usuarios de Quindío
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
sys.path.insert(0, 'd:\\Software\\mvp')

from backend.app import create_app
from backend.models.user import User
from backend.database import db

app = create_app()

with app.app_context():
    print("ASIGNANDO CONTRASEÑAS A USUARIOS DE QUINDIO")
    print("="*80)
    
    # Contraseña por defecto para todos los usuarios
    password_default = "test123"
    
    usuarios = User.query.filter_by(activo=True).all()
    
    actualizados = 0
    for usuario in usuarios:
        # No tocar Super Admin y Monitoreo
        if usuario.nombre in ['Super Admin', 'Monitoreo']:
            continue
        
        # Asignar contraseña
        usuario.set_password(password_default)
        actualizados += 1
    
    db.session.commit()
    
    print(f"Contraseñas asignadas: {actualizados} usuarios")
    print(f"Contraseña: {password_default}")
    print()
    print("USUARIOS CONFIGURADOS PARA LOGIN:")
    print("-"*80)
    
    usuarios_login = [
        ("Super Admin", "admin123"),
        ("Monitoreo", "test123"),
        ("ARMENIA_P01", password_default),
        ("ARMENIA_P02", password_default),
        ("ARMENIA_P03", password_default),
    ]
    
    for nombre, pwd in usuarios_login:
        print(f"  {nombre:30} : {pwd}")
    
    print()
    print("✅ Configuración completada")

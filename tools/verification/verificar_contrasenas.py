#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
sys.path.insert(0, 'd:\\Software\\mvp')

from backend.app import create_app
from backend.models.user import User

app = create_app()
with app.app_context():
    usuarios_prueba = ['Super Admin', 'ARMENIA_P01', 'ARMENIA_P02', 'ARMENIA']
    print("\nVERIFICACION DE CONTRASEÑAS:")
    print("="*80)
    
    for nombre in usuarios_prueba:
        u = User.query.filter_by(nombre=nombre).first()
        if u:
            pwd_ok = u.verify_password('test123')
            print(f"{nombre:30} - Existe: SI, test123: {'OK' if pwd_ok else 'FALLA'}")
        else:
            print(f"{nombre:30} - Existe: NO")
    
    print()
    # Actualizar si falta algo
    for u in User.query.filter_by(activo=True).all():
        if u.nombre not in ['Super Admin', 'Monitoreo']:
            if not u.verify_password('test123'):
                u.set_password('test123')
    
    from backend.database import db
    db.session.commit()
    print("Contraseñas verificadas y actualizadas!")

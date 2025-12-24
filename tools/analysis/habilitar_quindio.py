#!/usr/bin/env python3
"""
Script para habilitar Quindío en departamentos_config
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.departamento_config import DepartamentoConfig
from backend.models.location import Location
from datetime import datetime

def habilitar_quindio():
    app = create_app()
    
    with app.app_context():
        print("[*] Habilitando Quindío en departamentos_config...")
        
        # Contar ubicaciones de Quindío
        total_ubicaciones = Location.query.filter_by(
            departamento_codigo='26',
            activo=True
        ).count()
        
        municipios = Location.query.filter_by(
            departamento_codigo='26',
            tipo='municipio',
            activo=True
        ).count()
        
        puestos = Location.query.filter_by(
            departamento_codigo='26',
            tipo='puesto',
            activo=True
        ).count()
        
        mesas = Location.query.filter_by(
            departamento_codigo='26',
            tipo='mesa',
            activo=True
        ).count()
        
        print(f"    - Total ubicaciones: {total_ubicaciones}")
        print(f"    - Municipios: {municipios}")
        print(f"    - Puestos: {puestos}")
        print(f"    - Mesas: {mesas}")
        print()
        
        # Verificar si ya existe
        existing = DepartamentoConfig.query.filter_by(
            departamento_codigo='26'
        ).first()
        
        if existing:
            print(f"[*] Quindío ya existe. Actualizando...")
            existing.habilitado = True
            existing.es_principal = True
            existing.habilitado_at = datetime.utcnow()
            existing.auto_crear_usuarios = True
            existing.auto_cargar_ubicaciones = True
            existing.total_municipios = municipios
            existing.total_puestos = puestos
            existing.total_mesas = mesas
        else:
            print(f"[*] Creando nueva configuración para Quindío...")
            config = DepartamentoConfig(
                departamento_codigo='26',
                departamento_nombre='Quindío',
                habilitado=True,
                es_principal=True,
                auto_crear_usuarios=True,
                auto_cargar_ubicaciones=True,
                total_municipios=municipios,
                total_puestos=puestos,
                total_mesas=mesas,
                habilitado_at=datetime.utcnow()
            )
            db.session.add(config)
        
        db.session.commit()
        
        print()
        print("[OK] Quindío habilitado correctamente")
        print("    - Código: 26")
        print("    - Nombre: Quindío")
        print("    - Principal: SÍ")
        print("    - Habilitado: SÍ")

if __name__ == '__main__':
    habilitar_quindio()

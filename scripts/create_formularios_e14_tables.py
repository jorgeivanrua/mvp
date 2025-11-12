"""
Script para crear las tablas de Formularios E-14
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato, Coalicion, PartidoCoalicion
from backend.models.location import Location
from backend.models.user import User

def create_tables():
    """Crear las tablas de formularios E-14"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Creando tablas de Formularios E-14...")
        
        # Crear las tablas
        db.create_all()
        
        print("✅ Tablas creadas exitosamente:")
        print("   - formularios_e14")
        print("   - votos_partidos")
        print("   - votos_candidatos")
        print("\n✨ Sistema de Formularios E-14 listo para usar!")

if __name__ == '__main__':
    create_tables()

"""
Script para actualizar los logos de los partidos políticos en la BD
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import db
from backend.models.configuracion_electoral import Partido
from backend.app import create_app

# URLs de logos de partidos políticos colombianos
LOGOS_PARTIDOS = {
    # Partidos principales
    'PARTIDO LIBERAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
    'PARTIDO CONSERVADOR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
    'CENTRO DEMOCRÁTICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png',
    'PACTO HISTÓRICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Logo_Pacto_Hist%C3%B3rico.svg/200px-Logo_Pacto_Hist%C3%B3rico.svg.png',
    'CAMBIO RADICAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png',
    'PARTIDO DE LA U': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png',
    'ALIANZA VERDE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png',
    'POLO DEMOCRÁTICO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png',
    'MIRA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MIRA_logo.svg/200px-MIRA_logo.svg.png',
    'COMUNES': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Comunes_logo.svg/200px-Comunes_logo.svg.png',
    
    # Variaciones de nombres
    'LIBERAL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Colombian_Liberal_Party_logo.svg/200px-Colombian_Liberal_Party_logo.svg.png',
    'CONSERVADOR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Colombian_Conservative_Party_logo.svg/200px-Colombian_Conservative_Party_logo.svg.png',
    'CD': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Democratic_Center_%28Colombia%29_logo.svg/200px-Democratic_Center_%28Colombia%29_logo.svg.png',
    'CR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Radical_Change_logo.svg/200px-Radical_Change_logo.svg.png',
    'LA U': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Social_Party_of_National_Unity_logo.svg/200px-Social_Party_of_National_Unity_logo.svg.png',
    'VERDE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Green_Alliance_%28Colombia%29_logo.svg/200px-Green_Alliance_%28Colombia%29_logo.svg.png',
    'POLO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alternative_Democratic_Pole_logo.svg/200px-Alternative_Democratic_Pole_logo.svg.png',
}

def actualizar_logos():
    """Actualizar logos de partidos en la BD"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Consultando partidos en la base de datos...\n")
        
        partidos = Partido.query.all()
        
        if not partidos:
            print("❌ No hay partidos en la base de datos")
            return
        
        print(f"📊 Encontrados {len(partidos)} partidos:\n")
        
        actualizados = 0
        sin_logo = 0
        
        for partido in partidos:
            print(f"  {partido.id}. {partido.nombre} ({partido.nombre_corto or 'Sin sigla'})")
            print(f"     Logo actual: {partido.logo_url or 'Sin logo'}")
            
            # Buscar logo por nombre o nombre_corto
            logo_url = None
            
            # Intentar con nombre completo
            nombre_upper = partido.nombre.upper()
            if nombre_upper in LOGOS_PARTIDOS:
                logo_url = LOGOS_PARTIDOS[nombre_upper]
            
            # Intentar con nombre_corto
            if not logo_url and partido.nombre_corto:
                nombre_corto_upper = partido.nombre_corto.upper()
                if nombre_corto_upper in LOGOS_PARTIDOS:
                    logo_url = LOGOS_PARTIDOS[nombre_corto_upper]
            
            # Intentar búsqueda parcial
            if not logo_url:
                for key in LOGOS_PARTIDOS.keys():
                    if key in nombre_upper or nombre_upper in key:
                        logo_url = LOGOS_PARTIDOS[key]
                        break
            
            if logo_url:
                partido.logo_url = logo_url
                actualizados += 1
                print(f"     ✅ Logo actualizado: {logo_url}")
            else:
                sin_logo += 1
                print(f"     ⚠️  No se encontró logo para este partido")
            
            print()
        
        # Guardar cambios
        try:
            db.session.commit()
            print(f"\n✅ Actualización completada:")
            print(f"   - {actualizados} partidos con logo actualizado")
            print(f"   - {sin_logo} partidos sin logo encontrado")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al guardar cambios: {str(e)}")

if __name__ == '__main__':
    actualizar_logos()

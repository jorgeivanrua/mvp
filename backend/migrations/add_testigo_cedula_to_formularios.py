"""
Migración: Agregar campo testigo_cedula a formularios_e14
Fecha: 2025-12-12
Propósito: Usar cédula como identificador único consistente para testigos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database import db
from backend.models.formulario_e14 import FormularioE14
from backend.models.user import User
from backend.app import create_app


def aplicar_migracion():
    """Aplicar migración para agregar testigo_cedula a formularios_e14"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Iniciando migración: Agregar testigo_cedula a formularios_e14...")
            
            # 1. Verificar si la columna ya existe
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('formularios_e14')]
            
            if 'testigo_cedula' in columns:
                print("✅ La columna testigo_cedula ya existe")
            else:
                print("📝 Agregando columna testigo_cedula...")
                # Agregar la columna
                db.engine.execute('ALTER TABLE formularios_e14 ADD COLUMN testigo_cedula VARCHAR(20)')
                print("✅ Columna testigo_cedula agregada")
            
            # 2. Poblar los datos de cédula para formularios existentes
            print("📊 Poblando datos de cédula para formularios existentes...")
            
            formularios_sin_cedula = FormularioE14.query.filter(
                FormularioE14.testigo_cedula.is_(None)
            ).all()
            
            print(f"📋 Encontrados {len(formularios_sin_cedula)} formularios sin cédula")
            
            actualizados = 0
            for formulario in formularios_sin_cedula:
                # Obtener la cédula del testigo
                testigo = User.query.get(formulario.testigo_id)
                if testigo and testigo.cedula:
                    formulario.testigo_cedula = testigo.cedula
                    actualizados += 1
                    
                    if actualizados % 100 == 0:
                        print(f"  📝 Procesados {actualizados} formularios...")
                        db.session.commit()
            
            # Commit final
            db.session.commit()
            
            print(f"✅ Migración completada:")
            print(f"   - {actualizados} formularios actualizados con cédula")
            
            # 3. Crear índice para mejorar rendimiento
            try:
                print("📊 Creando índice para testigo_cedula...")
                db.engine.execute('CREATE INDEX IF NOT EXISTS idx_formularios_testigo_cedula ON formularios_e14(testigo_cedula)')
                print("✅ Índice creado")
            except Exception as e:
                print(f"⚠️  Advertencia creando índice: {e}")
            
            # 4. Verificar integridad
            print("🔍 Verificando integridad de datos...")
            
            total_formularios = FormularioE14.query.count()
            formularios_con_cedula = FormularioE14.query.filter(
                FormularioE14.testigo_cedula.isnot(None)
            ).count()
            
            print(f"📊 Resumen:")
            print(f"   - Total formularios: {total_formularios}")
            print(f"   - Con cédula: {formularios_con_cedula}")
            print(f"   - Sin cédula: {total_formularios - formularios_con_cedula}")
            
            if formularios_con_cedula == total_formularios:
                print("✅ Todos los formularios tienen cédula asignada")
            else:
                print("⚠️  Algunos formularios no tienen cédula (testigos sin cédula)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en migración: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    if aplicar_migracion():
        print("🎉 Migración completada exitosamente")
    else:
        print("💥 Migración falló")
        sys.exit(1)
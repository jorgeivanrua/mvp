"""
Migración: Agregar tabla para múltiples fotos de formularios E-14
"""
from backend.database import db
from backend.models.formulario_fotos import FormularioFoto


def aplicar_migracion():
    """
    Crear tabla formulario_fotos para manejar múltiples fotos por formulario
    """
    try:
        print("[MIGRACIÓN] Creando tabla formulario_fotos...")
        
        # Crear tabla
        db.create_all()
        
        print("[MIGRACIÓN] ✅ Tabla formulario_fotos creada exitosamente")
        
        # Migrar fotos existentes del campo imagen_url
        from backend.models.formulario_e14 import FormularioE14
        
        formularios_con_imagen = FormularioE14.query.filter(
            FormularioE14.imagen_url.isnot(None),
            FormularioE14.imagen_url != ''
        ).all()
        
        print(f"[MIGRACIÓN] Migrando {len(formularios_con_imagen)} fotos existentes...")
        
        for formulario in formularios_con_imagen:
            # Crear registro de foto para la imagen existente
            foto = FormularioFoto(
                formulario_id=formulario.id,
                nombre_archivo=f"formulario_{formulario.id}_foto_1.jpg",
                url=formulario.imagen_url,
                hash_archivo=formulario.imagen_hash,
                orden=1,
                es_principal=True,
                validada=formulario.estado == 'validado',
                validada_por_id=formulario.validado_por_id,
                validada_at=formulario.validado_at,
                subida_por_id=formulario.testigo_id,
                created_at=formulario.created_at
            )
            db.session.add(foto)
        
        db.session.commit()
        
        print(f"[MIGRACIÓN] ✅ {len(formularios_con_imagen)} fotos migradas exitosamente")
        print("[MIGRACIÓN] ✅ Migración completada")
        
        return True
        
    except Exception as e:
        print(f"[MIGRACIÓN] ❌ Error: {str(e)}")
        db.session.rollback()
        return False


if __name__ == '__main__':
    aplicar_migracion()
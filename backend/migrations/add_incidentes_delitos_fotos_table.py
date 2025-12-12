"""
Migración: Agregar tabla para múltiples fotos de incidentes y delitos
"""
from backend.database import db
from backend.models.incidentes_delitos_fotos import IncidenteDelitoFoto


def aplicar_migracion():
    """
    Crear tabla incidentes_delitos_fotos para manejar múltiples fotos por reporte
    """
    try:
        print("[MIGRACIÓN] Creando tabla incidentes_delitos_fotos...")
        
        # Crear tabla
        db.create_all()
        
        print("[MIGRACIÓN] ✅ Tabla incidentes_delitos_fotos creada exitosamente")
        
        # Migrar evidencias existentes del campo evidencia_url
        from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
        
        # Migrar incidentes con evidencia
        incidentes_con_evidencia = IncidenteElectoral.query.filter(
            IncidenteElectoral.evidencia_url.isnot(None),
            IncidenteElectoral.evidencia_url != ''
        ).all()
        
        print(f"[MIGRACIÓN] Migrando {len(incidentes_con_evidencia)} evidencias de incidentes...")
        
        for incidente in incidentes_con_evidencia:
            # Crear registro de foto para la evidencia existente
            foto = IncidenteDelitoFoto(
                incidente_id=incidente.id,
                nombre_archivo=f"incidente_{incidente.id}_evidencia_1.jpg",
                url=incidente.evidencia_url,
                orden=1,
                es_principal=True,
                categoria='general',
                tipo_evidencia='directa',
                relevancia='alta',
                descripcion=f"Evidencia del incidente: {incidente.titulo}",
                subida_por_id=incidente.reportado_por_id,
                created_at=incidente.created_at
            )
            db.session.add(foto)
        
        # Migrar delitos con evidencia
        delitos_con_evidencia = DelitoElectoral.query.filter(
            DelitoElectoral.evidencia_url.isnot(None),
            DelitoElectoral.evidencia_url != ''
        ).all()
        
        print(f"[MIGRACIÓN] Migrando {len(delitos_con_evidencia)} evidencias de delitos...")
        
        for delito in delitos_con_evidencia:
            # Crear registro de foto para la evidencia existente
            foto = IncidenteDelitoFoto(
                delito_id=delito.id,
                nombre_archivo=f"delito_{delito.id}_evidencia_1.jpg",
                url=delito.evidencia_url,
                orden=1,
                es_principal=True,
                categoria='general',
                tipo_evidencia='directa',
                relevancia='critica',  # Los delitos tienen relevancia crítica por defecto
                descripcion=f"Evidencia del delito: {delito.titulo}",
                subida_por_id=delito.reportado_por_id,
                created_at=delito.created_at
            )
            db.session.add(foto)
        
        db.session.commit()
        
        total_migradas = len(incidentes_con_evidencia) + len(delitos_con_evidencia)
        print(f"[MIGRACIÓN] ✅ {total_migradas} evidencias migradas exitosamente")
        print("[MIGRACIÓN] ✅ Migración completada")
        
        return True
        
    except Exception as e:
        print(f"[MIGRACIÓN] ❌ Error: {str(e)}")
        db.session.rollback()
        return False


if __name__ == '__main__':
    aplicar_migracion()
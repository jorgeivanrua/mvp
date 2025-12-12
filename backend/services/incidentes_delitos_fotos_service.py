"""
Servicio para manejo de fotos de incidentes y delitos electorales
"""
import os
import hashlib
import uuid
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from backend.database import db
from backend.models.incidentes_delitos_fotos import IncidenteDelitoFoto
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
from backend.utils.exceptions import ValidationException, NotFoundException


class IncidentesDelitosFotosService:
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB (más grande para evidencias)
    
    @staticmethod
    def _allowed_file(filename):
        """Verificar si el archivo es permitido"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in IncidentesDelitosFotosService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def _calculate_hash(file_data):
        """Calcular hash SHA-256 del archivo"""
        return hashlib.sha256(file_data).hexdigest()
    
    @staticmethod
    def _generate_filename(tipo_reporte, reporte_id, original_filename):
        """Generar nombre único para el archivo"""
        ext = original_filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{tipo_reporte}_{reporte_id}_{timestamp}_{unique_id}.{ext}"
    
    @staticmethod
    def subir_foto(tipo_reporte, reporte_id, file, descripcion=None, categoria='general', 
                   tipo_evidencia='directa', relevancia='media', usuario_id=None):
        """
        Subir una foto para un incidente o delito
        
        Args:
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del incidente o delito
            file: Archivo de imagen
            descripcion: Descripción de la evidencia
            categoria: Categoría de la evidencia
            tipo_evidencia: Tipo de evidencia
            relevancia: Nivel de relevancia
            usuario_id: ID del usuario que sube la foto
            
        Returns:
            dict: Información de la foto subida
        """
        try:
            # Validar tipo de reporte
            if tipo_reporte not in ['incidente', 'delito']:
                raise ValidationException({'tipo_reporte': ['Tipo de reporte inválido']})
            
            # Validar que el reporte existe
            if tipo_reporte == 'incidente':
                reporte = IncidenteElectoral.query.get(reporte_id)
                if not reporte:
                    raise NotFoundException('Incidente no encontrado')
            else:
                reporte = DelitoElectoral.query.get(reporte_id)
                if not reporte:
                    raise NotFoundException('Delito no encontrado')
            
            # Validar archivo
            if not file or file.filename == '':
                raise ValidationException({'file': ['No se seleccionó archivo']})
            
            if not IncidentesDelitosFotosService._allowed_file(file.filename):
                raise ValidationException({
                    'file': [f'Tipo de archivo no permitido. Use: {", ".join(IncidentesDelitosFotosService.ALLOWED_EXTENSIONS)}']
                })
            
            # Leer datos del archivo
            file_data = file.read()
            file.seek(0)  # Resetear puntero
            
            # Validar tamaño
            if len(file_data) > IncidentesDelitosFotosService.MAX_FILE_SIZE:
                raise ValidationException({
                    'file': [f'Archivo muy grande. Máximo {IncidentesDelitosFotosService.MAX_FILE_SIZE // (1024*1024)}MB']
                })
            
            # Generar nombre único
            filename = IncidentesDelitosFotosService._generate_filename(tipo_reporte, reporte_id, file.filename)
            
            # Calcular hash
            file_hash = IncidentesDelitosFotosService._calculate_hash(file_data)
            
            # Verificar si ya existe una foto con el mismo hash para este reporte
            query_params = {'hash_archivo': file_hash}
            if tipo_reporte == 'incidente':
                query_params['incidente_id'] = reporte_id
            else:
                query_params['delito_id'] = reporte_id
            
            foto_existente = IncidenteDelitoFoto.query.filter_by(**query_params).first()
            
            if foto_existente:
                raise ValidationException({'file': ['Esta foto ya fue subida anteriormente']})
            
            # Crear directorio si no existe
            upload_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'evidencias')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Guardar archivo
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            
            # Determinar orden
            query_params_orden = {}
            if tipo_reporte == 'incidente':
                query_params_orden['incidente_id'] = reporte_id
            else:
                query_params_orden['delito_id'] = reporte_id
            
            max_orden = db.session.query(db.func.max(IncidenteDelitoFoto.orden)).filter_by(
                **query_params_orden
            ).scalar() or 0
            
            # Determinar si es principal (primera foto)
            es_principal = IncidenteDelitoFoto.query.filter_by(
                **query_params_orden, es_principal=True
            ).first() is None
            
            # Crear registro en BD
            foto_data = {
                'nombre_archivo': filename,
                'url': f'/uploads/evidencias/{filename}',
                'hash_archivo': file_hash,
                'tamaño_bytes': len(file_data),
                'tipo_mime': file.content_type,
                'orden': max_orden + 1,
                'descripcion': descripcion,
                'categoria': categoria,
                'tipo_evidencia': tipo_evidencia,
                'relevancia': relevancia,
                'es_principal': es_principal,
                'subida_por_id': usuario_id
            }
            
            if tipo_reporte == 'incidente':
                foto_data['incidente_id'] = reporte_id
            else:
                foto_data['delito_id'] = reporte_id
            
            foto = IncidenteDelitoFoto(**foto_data)
            
            db.session.add(foto)
            db.session.commit()
            
            return {
                'success': True,
                'foto': foto.to_dict(),
                'message': 'Evidencia fotográfica subida exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'file': [f'Error al subir evidencia: {str(e)}']})
    
    @staticmethod
    def obtener_fotos(tipo_reporte, reporte_id):
        """
        Obtener todas las fotos de un incidente o delito
        
        Args:
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del reporte
            
        Returns:
            list: Lista de fotos
        """
        query_params = {}
        if tipo_reporte == 'incidente':
            query_params['incidente_id'] = reporte_id
        else:
            query_params['delito_id'] = reporte_id
        
        fotos = IncidenteDelitoFoto.query.filter_by(
            **query_params
        ).order_by(IncidenteDelitoFoto.orden).all()
        
        return [foto.to_dict() for foto in fotos]
    
    @staticmethod
    def eliminar_foto(foto_id, usuario_id=None):
        """
        Eliminar una foto de evidencia
        
        Args:
            foto_id: ID de la foto
            usuario_id: ID del usuario (para validación)
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            foto = IncidenteDelitoFoto.query.get(foto_id)
            if not foto:
                raise NotFoundException('Foto no encontrada')
            
            # Validar permisos (solo el que subió la foto o coordinadores/auditores pueden eliminar)
            if usuario_id and foto.subida_por_id != usuario_id:
                from backend.models.user import User
                usuario = User.query.get(usuario_id)
                if not usuario or usuario.rol not in ['coordinador_puesto', 'coordinador_municipal', 
                                                     'coordinador_departamental', 'auditor_electoral', 'super_admin']:
                    raise ValidationException({'permission': ['No tiene permisos para eliminar esta evidencia']})
            
            # Eliminar archivo físico
            if foto.url.startswith('/uploads/'):
                filepath = os.path.join(current_app.root_path, '..', foto.url[1:])
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            # Si era la foto principal, asignar otra como principal
            if foto.es_principal:
                query_params = {}
                if foto.incidente_id:
                    query_params['incidente_id'] = foto.incidente_id
                else:
                    query_params['delito_id'] = foto.delito_id
                
                siguiente_foto = IncidenteDelitoFoto.query.filter(
                    IncidenteDelitoFoto.id != foto.id
                ).filter_by(**query_params).order_by(IncidenteDelitoFoto.orden).first()
                
                if siguiente_foto:
                    siguiente_foto.es_principal = True
            
            # Eliminar registro
            db.session.delete(foto)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Evidencia eliminada exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al eliminar evidencia: {str(e)}']})
    
    @staticmethod
    def validar_foto(foto_id, validada, comentario=None, usuario_id=None):
        """
        Validar o rechazar una foto de evidencia
        
        Args:
            foto_id: ID de la foto
            validada: True para validar, False para rechazar
            comentario: Comentario de validación
            usuario_id: ID del usuario que valida
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            foto = IncidenteDelitoFoto.query.get(foto_id)
            if not foto:
                raise NotFoundException('Foto no encontrada')
            
            foto.validada = validada
            foto.validada_por_id = usuario_id
            foto.validada_at = datetime.utcnow()
            foto.comentario_validacion = comentario
            
            db.session.commit()
            
            return {
                'success': True,
                'foto': foto.to_dict(),
                'message': 'Evidencia validada' if validada else 'Evidencia rechazada'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al validar evidencia: {str(e)}']})
    
    @staticmethod
    def establecer_principal(foto_id, usuario_id=None):
        """
        Establecer una foto como principal
        
        Args:
            foto_id: ID de la foto
            usuario_id: ID del usuario
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            foto = IncidenteDelitoFoto.query.get(foto_id)
            if not foto:
                raise NotFoundException('Foto no encontrada')
            
            # Quitar principal de otras fotos del mismo reporte
            query_params = {}
            if foto.incidente_id:
                query_params['incidente_id'] = foto.incidente_id
            else:
                query_params['delito_id'] = foto.delito_id
            
            IncidenteDelitoFoto.query.filter_by(
                **query_params, es_principal=True
            ).update({'es_principal': False})
            
            # Establecer como principal
            foto.es_principal = True
            
            db.session.commit()
            
            return {
                'success': True,
                'foto': foto.to_dict(),
                'message': 'Evidencia establecida como principal'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al establecer evidencia principal: {str(e)}']})
    
    @staticmethod
    def actualizar_metadatos(foto_id, descripcion=None, categoria=None, tipo_evidencia=None, 
                           relevancia=None, usuario_id=None):
        """
        Actualizar metadatos de una foto
        
        Args:
            foto_id: ID de la foto
            descripcion: Nueva descripción
            categoria: Nueva categoría
            tipo_evidencia: Nuevo tipo de evidencia
            relevancia: Nueva relevancia
            usuario_id: ID del usuario
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            foto = IncidenteDelitoFoto.query.get(foto_id)
            if not foto:
                raise NotFoundException('Foto no encontrada')
            
            # Actualizar campos si se proporcionan
            if descripcion is not None:
                foto.descripcion = descripcion
            if categoria is not None:
                foto.categoria = categoria
            if tipo_evidencia is not None:
                foto.tipo_evidencia = tipo_evidencia
            if relevancia is not None:
                foto.relevancia = relevancia
            
            db.session.commit()
            
            return {
                'success': True,
                'foto': foto.to_dict(),
                'message': 'Metadatos actualizados exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al actualizar metadatos: {str(e)}']})
    
    @staticmethod
    def obtener_estadisticas_fotos(tipo_reporte, reporte_id):
        """
        Obtener estadísticas de fotos de un reporte
        
        Args:
            tipo_reporte: 'incidente' o 'delito'
            reporte_id: ID del reporte
            
        Returns:
            dict: Estadísticas de fotos
        """
        query_params = {}
        if tipo_reporte == 'incidente':
            query_params['incidente_id'] = reporte_id
        else:
            query_params['delito_id'] = reporte_id
        
        fotos = IncidenteDelitoFoto.query.filter_by(**query_params).all()
        
        total_fotos = len(fotos)
        fotos_validadas = len([f for f in fotos if f.validada])
        
        # Estadísticas por categoría
        categorias = {}
        for foto in fotos:
            cat = foto.categoria or 'general'
            categorias[cat] = categorias.get(cat, 0) + 1
        
        # Estadísticas por relevancia
        relevancias = {}
        for foto in fotos:
            rel = foto.relevancia or 'media'
            relevancias[rel] = relevancias.get(rel, 0) + 1
        
        return {
            'total_fotos': total_fotos,
            'fotos_validadas': fotos_validadas,
            'fotos_pendientes': total_fotos - fotos_validadas,
            'porcentaje_validadas': round((fotos_validadas / total_fotos * 100), 2) if total_fotos > 0 else 0,
            'por_categoria': categorias,
            'por_relevancia': relevancias,
            'tiene_foto_principal': any(f.es_principal for f in fotos)
        }
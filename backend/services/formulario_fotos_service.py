"""
Servicio para manejo de fotos de formularios E-14
"""
import os
import hashlib
import uuid
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from backend.database import db
from backend.models.formulario_fotos import FormularioFoto
from backend.models.formulario_e14 import FormularioE14
from backend.utils.exceptions import ValidationException, NotFoundException


class FormularioFotosService:
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def _allowed_file(filename):
        """Verificar si el archivo es permitido"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FormularioFotosService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def _calculate_hash(file_data):
        """Calcular hash SHA-256 del archivo"""
        return hashlib.sha256(file_data).hexdigest()
    
    @staticmethod
    def _generate_filename(formulario_id, original_filename):
        """Generar nombre único para el archivo"""
        ext = original_filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"formulario_{formulario_id}_{timestamp}_{unique_id}.{ext}"
    
    @staticmethod
    def subir_foto(formulario_id, file, descripcion=None, usuario_id=None):
        """
        Subir una foto para un formulario
        
        Args:
            formulario_id: ID del formulario
            file: Archivo de imagen
            descripcion: Descripción opcional
            usuario_id: ID del usuario que sube la foto
            
        Returns:
            dict: Información de la foto subida
        """
        try:
            # Validar formulario
            formulario = FormularioE14.query.get(formulario_id)
            if not formulario:
                raise NotFoundException('Formulario no encontrado')
            
            # Validar archivo
            if not file or file.filename == '':
                raise ValidationException({'file': ['No se seleccionó archivo']})
            
            if not FormularioFotosService._allowed_file(file.filename):
                raise ValidationException({
                    'file': [f'Tipo de archivo no permitido. Use: {", ".join(FormularioFotosService.ALLOWED_EXTENSIONS)}']
                })
            
            # Leer datos del archivo
            file_data = file.read()
            file.seek(0)  # Resetear puntero
            
            # Validar tamaño
            if len(file_data) > FormularioFotosService.MAX_FILE_SIZE:
                raise ValidationException({
                    'file': [f'Archivo muy grande. Máximo {FormularioFotosService.MAX_FILE_SIZE // (1024*1024)}MB']
                })
            
            # Generar nombre único
            filename = FormularioFotosService._generate_filename(formulario_id, file.filename)
            
            # Calcular hash
            file_hash = FormularioFotosService._calculate_hash(file_data)
            
            # Verificar si ya existe una foto con el mismo hash
            foto_existente = FormularioFoto.query.filter_by(
                formulario_id=formulario_id,
                hash_archivo=file_hash
            ).first()
            
            if foto_existente:
                raise ValidationException({'file': ['Esta foto ya fue subida anteriormente']})
            
            # Crear directorio si no existe
            upload_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'formularios')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Guardar archivo
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            
            # Determinar orden
            max_orden = db.session.query(db.func.max(FormularioFoto.orden)).filter_by(
                formulario_id=formulario_id
            ).scalar() or 0
            
            # Determinar si es principal (primera foto)
            es_principal = FormularioFoto.query.filter_by(
                formulario_id=formulario_id,
                es_principal=True
            ).first() is None
            
            # Crear registro en BD
            foto = FormularioFoto(
                formulario_id=formulario_id,
                nombre_archivo=filename,
                url=f'/uploads/formularios/{filename}',
                hash_archivo=file_hash,
                tamaño_bytes=len(file_data),
                tipo_mime=file.content_type,
                orden=max_orden + 1,
                descripcion=descripcion,
                es_principal=es_principal,
                subida_por_id=usuario_id
            )
            
            db.session.add(foto)
            db.session.commit()
            
            return {
                'success': True,
                'foto': foto.to_dict(),
                'message': 'Foto subida exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'file': [f'Error al subir foto: {str(e)}']})
    
    @staticmethod
    def obtener_fotos(formulario_id):
        """
        Obtener todas las fotos de un formulario
        
        Args:
            formulario_id: ID del formulario
            
        Returns:
            list: Lista de fotos
        """
        fotos = FormularioFoto.query.filter_by(
            formulario_id=formulario_id
        ).order_by(FormularioFoto.orden).all()
        
        return [foto.to_dict() for foto in fotos]
    
    @staticmethod
    def eliminar_foto(foto_id, usuario_id=None):
        """
        Eliminar una foto
        
        Args:
            foto_id: ID de la foto
            usuario_id: ID del usuario (para validación)
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            foto = FormularioFoto.query.get(foto_id)
            if not foto:
                raise NotFoundException('Foto no encontrada')
            
            # Validar permisos (solo el que subió la foto o coordinador puede eliminar)
            if usuario_id and foto.subida_por_id != usuario_id:
                from backend.models.user import User
                usuario = User.query.get(usuario_id)
                if not usuario or 'coordinador' not in usuario.rol:
                    raise ValidationException({'permission': ['No tiene permisos para eliminar esta foto']})
            
            # Eliminar archivo físico
            if foto.url.startswith('/uploads/'):
                filepath = os.path.join(current_app.root_path, '..', foto.url[1:])
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            # Si era la foto principal, asignar otra como principal
            if foto.es_principal:
                siguiente_foto = FormularioFoto.query.filter(
                    FormularioFoto.formulario_id == foto.formulario_id,
                    FormularioFoto.id != foto.id
                ).order_by(FormularioFoto.orden).first()
                
                if siguiente_foto:
                    siguiente_foto.es_principal = True
            
            # Eliminar registro
            db.session.delete(foto)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Foto eliminada exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al eliminar foto: {str(e)}']})
    
    @staticmethod
    def validar_foto(foto_id, validada, comentario=None, usuario_id=None):
        """
        Validar o rechazar una foto
        
        Args:
            foto_id: ID de la foto
            validada: True para validar, False para rechazar
            comentario: Comentario de validación
            usuario_id: ID del usuario que valida
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            foto = FormularioFoto.query.get(foto_id)
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
                'message': 'Foto validada' if validada else 'Foto rechazada'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al validar foto: {str(e)}']})
    
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
            foto = FormularioFoto.query.get(foto_id)
            if not foto:
                raise NotFoundException('Foto no encontrada')
            
            # Quitar principal de otras fotos del mismo formulario
            FormularioFoto.query.filter_by(
                formulario_id=foto.formulario_id,
                es_principal=True
            ).update({'es_principal': False})
            
            # Establecer como principal
            foto.es_principal = True
            
            db.session.commit()
            
            return {
                'success': True,
                'foto': foto.to_dict(),
                'message': 'Foto establecida como principal'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al establecer foto principal: {str(e)}']})
    
    @staticmethod
    def reordenar_fotos(formulario_id, orden_fotos, usuario_id=None):
        """
        Reordenar fotos de un formulario
        
        Args:
            formulario_id: ID del formulario
            orden_fotos: Lista de IDs en el nuevo orden
            usuario_id: ID del usuario
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Validar que todas las fotos pertenezcan al formulario
            fotos = FormularioFoto.query.filter(
                FormularioFoto.formulario_id == formulario_id,
                FormularioFoto.id.in_(orden_fotos)
            ).all()
            
            if len(fotos) != len(orden_fotos):
                raise ValidationException({'orden': ['IDs de fotos inválidos']})
            
            # Actualizar orden
            for i, foto_id in enumerate(orden_fotos, 1):
                FormularioFoto.query.filter_by(id=foto_id).update({'orden': i})
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Fotos reordenadas exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationException, NotFoundException)):
                raise
            raise ValidationException({'error': [f'Error al reordenar fotos: {str(e)}']})
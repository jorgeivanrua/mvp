"""
Modelo para fotos múltiples de incidentes y delitos electorales
"""
from backend.database import db
from datetime import datetime


class IncidenteDelitoFoto(db.Model):
    """Fotos de incidentes y delitos electorales"""
    __tablename__ = 'incidentes_delitos_fotos'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con reporte (puede ser incidente o delito)
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidentes_electorales.id'), nullable=True)
    delito_id = db.Column(db.Integer, db.ForeignKey('delitos_electorales.id'), nullable=True)
    
    # Información de la foto
    nombre_archivo = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    hash_archivo = db.Column(db.String(64))  # SHA-256 para integridad
    tamaño_bytes = db.Column(db.Integer)
    tipo_mime = db.Column(db.String(100))
    
    # Metadatos de la imagen
    ancho = db.Column(db.Integer)
    alto = db.Column(db.Integer)
    
    # Metadatos de captura
    latitud_captura = db.Column(db.Float)
    longitud_captura = db.Column(db.Float)
    fecha_captura = db.Column(db.DateTime)
    dispositivo = db.Column(db.String(200))
    
    # Organización
    orden = db.Column(db.Integer, default=1)  # Orden de las fotos
    descripcion = db.Column(db.String(255))  # Descripción de la evidencia
    es_principal = db.Column(db.Boolean, default=False)  # Foto principal
    categoria = db.Column(db.String(50))  # Categoría de evidencia
    
    # Estado de validación
    validada = db.Column(db.Boolean, default=False)
    validada_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    validada_at = db.Column(db.DateTime)
    comentario_validacion = db.Column(db.Text)
    
    # Clasificación de evidencia
    tipo_evidencia = db.Column(db.String(50))  # 'directa', 'indirecta', 'contextual'
    relevancia = db.Column(db.String(20), default='media')  # 'baja', 'media', 'alta', 'critica'
    
    # Auditoría
    subida_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    incidente = db.relationship('IncidenteElectoral', backref='fotos_evidencia')
    delito = db.relationship('DelitoElectoral', backref='fotos_evidencia')
    subida_por = db.relationship('User', foreign_keys=[subida_por_id], backref='fotos_evidencia_subidas')
    validada_por = db.relationship('User', foreign_keys=[validada_por_id], backref='fotos_evidencia_validadas')
    
    # Categorías de evidencia
    CATEGORIAS = {
        'general': 'Evidencia general',
        'personas': 'Personas involucradas',
        'documentos': 'Documentos',
        'ubicacion': 'Ubicación del hecho',
        'material_electoral': 'Material electoral',
        'daños': 'Daños o alteraciones',
        'multitud': 'Multitudes o aglomeraciones',
        'autoridades': 'Presencia de autoridades',
        'otros': 'Otros'
    }
    
    # Tipos de evidencia
    TIPOS_EVIDENCIA = {
        'directa': 'Evidencia directa del hecho',
        'indirecta': 'Evidencia indirecta o circunstancial',
        'contextual': 'Evidencia de contexto'
    }
    
    # Niveles de relevancia
    RELEVANCIAS = {
        'baja': 'Baja relevancia',
        'media': 'Media relevancia',
        'alta': 'Alta relevancia',
        'critica': 'Relevancia crítica'
    }
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'incidente_id': self.incidente_id,
            'delito_id': self.delito_id,
            'nombre_archivo': self.nombre_archivo,
            'url': self.url,
            'hash_archivo': self.hash_archivo,
            'tamaño_bytes': self.tamaño_bytes,
            'tipo_mime': self.tipo_mime,
            'ancho': self.ancho,
            'alto': self.alto,
            'latitud_captura': self.latitud_captura,
            'longitud_captura': self.longitud_captura,
            'fecha_captura': self.fecha_captura.isoformat() if self.fecha_captura else None,
            'dispositivo': self.dispositivo,
            'orden': self.orden,
            'descripcion': self.descripcion,
            'es_principal': self.es_principal,
            'categoria': self.categoria,
            'categoria_label': self.CATEGORIAS.get(self.categoria, self.categoria),
            'validada': self.validada,
            'validada_por_id': self.validada_por_id,
            'validada_at': self.validada_at.isoformat() if self.validada_at else None,
            'comentario_validacion': self.comentario_validacion,
            'tipo_evidencia': self.tipo_evidencia,
            'tipo_evidencia_label': self.TIPOS_EVIDENCIA.get(self.tipo_evidencia, self.tipo_evidencia),
            'relevancia': self.relevancia,
            'relevancia_label': self.RELEVANCIAS.get(self.relevancia, self.relevancia),
            'subida_por_id': self.subida_por_id,
            'subida_por_nombre': self.subida_por.nombre if self.subida_por else None,
            'validada_por_nombre': self.validada_por.nombre if self.validada_por else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<IncidenteDelitoFoto {self.id}: {self.nombre_archivo}>'
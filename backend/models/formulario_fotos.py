"""
Modelo para fotos de formularios E-14
"""
from backend.database import db
from datetime import datetime


class FormularioFoto(db.Model):
    """Fotos de formularios E-14"""
    __tablename__ = 'formulario_fotos'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    
    # Información de la foto
    nombre_archivo = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    hash_archivo = db.Column(db.String(64))  # SHA-256 para integridad
    tamaño_bytes = db.Column(db.Integer)
    tipo_mime = db.Column(db.String(100))
    
    # Metadatos
    orden = db.Column(db.Integer, default=1)  # Orden de las fotos
    descripcion = db.Column(db.String(255))  # Descripción opcional
    es_principal = db.Column(db.Boolean, default=False)  # Foto principal
    
    # Estado de validación
    validada = db.Column(db.Boolean, default=False)
    validada_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    validada_at = db.Column(db.DateTime)
    comentario_validacion = db.Column(db.Text)
    
    # Auditoría
    subida_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    formulario = db.relationship('FormularioE14', backref='fotos')
    subida_por = db.relationship('User', foreign_keys=[subida_por_id], backref='fotos_subidas')
    validada_por = db.relationship('User', foreign_keys=[validada_por_id], backref='fotos_validadas')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'formulario_id': self.formulario_id,
            'nombre_archivo': self.nombre_archivo,
            'url': self.url,
            'hash_archivo': self.hash_archivo,
            'tamaño_bytes': self.tamaño_bytes,
            'tipo_mime': self.tipo_mime,
            'orden': self.orden,
            'descripcion': self.descripcion,
            'es_principal': self.es_principal,
            'validada': self.validada,
            'validada_por_id': self.validada_por_id,
            'validada_at': self.validada_at.isoformat() if self.validada_at else None,
            'comentario_validacion': self.comentario_validacion,
            'subida_por_id': self.subida_por_id,
            'subida_por_nombre': self.subida_por.nombre if self.subida_por else None,
            'validada_por_nombre': self.validada_por.nombre if self.validada_por else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<FormularioFoto {self.id}: {self.nombre_archivo}>'
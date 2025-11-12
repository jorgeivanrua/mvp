"""
Modelos para Formularios E-14 (Actas de Escrutinio)
"""
from datetime import datetime
from backend.database import db

class FormularioE14(db.Model):
    """Formulario E-14 - Acta de Escrutinio"""
    __tablename__ = 'formularios_e14'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    
    # Información básica
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    hora_apertura = db.Column(db.Time, nullable=False)
    hora_cierre = db.Column(db.Time, nullable=False)
    
    # Datos de votación
    total_votantes_registrados = db.Column(db.Integer, nullable=False)
    total_votos = db.Column(db.Integer, nullable=False)
    votos_validos = db.Column(db.Integer, nullable=False)
    votos_nulos = db.Column(db.Integer, nullable=False)
    votos_blanco = db.Column(db.Integer, nullable=False)
    tarjetas_no_marcadas = db.Column(db.Integer, nullable=False)
    total_tarjetas = db.Column(db.Integer, nullable=False)
    
    # Imagen del formulario
    imagen_url = db.Column(db.String(500))
    
    # Estado y validación
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, validado, rechazado
    observaciones = db.Column(db.Text)
    validado_por = db.Column(db.Integer, db.ForeignKey('users.id'))
    fecha_validacion = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    testigo = db.relationship('User', foreign_keys=[testigo_id], backref='formularios_e14')
    validador = db.relationship('User', foreign_keys=[validado_por])
    mesa = db.relationship('Location', foreign_keys=[mesa_id])
    tipo_eleccion = db.relationship('TipoEleccion', backref='formularios')
    votos_partidos = db.relationship('VotoPartido', backref='formulario', cascade='all, delete-orphan')
    votos_candidatos = db.relationship('VotoCandidato', backref='formulario', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'testigo_id': self.testigo_id,
            'testigo_nombre': self.testigo.nombre_completo if self.testigo else None,
            'mesa_id': self.mesa_id,
            'tipo_eleccion_id': self.tipo_eleccion_id,
            'tipo_eleccion_nombre': self.tipo_eleccion.nombre if self.tipo_eleccion else None,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'hora_apertura': self.hora_apertura.strftime('%H:%M') if self.hora_apertura else None,
            'hora_cierre': self.hora_cierre.strftime('%H:%M') if self.hora_cierre else None,
            'total_votantes_registrados': self.total_votantes_registrados,
            'total_votos': self.total_votos,
            'votos_validos': self.votos_validos,
            'votos_nulos': self.votos_nulos,
            'votos_blanco': self.votos_blanco,
            'tarjetas_no_marcadas': self.tarjetas_no_marcadas,
            'total_tarjetas': self.total_tarjetas,
            'imagen_url': self.imagen_url,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'validado_por': self.validado_por,
            'fecha_validacion': self.fecha_validacion.isoformat() if self.fecha_validacion else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'votos_partidos': [vp.to_dict() for vp in self.votos_partidos],
            'votos_candidatos': [vc.to_dict() for vc in self.votos_candidatos]
        }


class VotoPartido(db.Model):
    """Votos por partido político"""
    __tablename__ = 'votos_partidos'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False, default=0)
    
    # Relaciones
    partido = db.relationship('Partido')
    
    def to_dict(self):
        return {
            'id': self.id,
            'formulario_id': self.formulario_id,
            'partido_id': self.partido_id,
            'partido_nombre': self.partido.nombre if self.partido else None,
            'partido_nombre_corto': self.partido.nombre_corto if self.partido else None,
            'votos': self.votos
        }


class VotoCandidato(db.Model):
    """Votos por candidato"""
    __tablename__ = 'votos_candidatos'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidatos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False, default=0)
    
    # Relaciones
    candidato = db.relationship('Candidato')
    
    def to_dict(self):
        return {
            'id': self.id,
            'formulario_id': self.formulario_id,
            'candidato_id': self.candidato_id,
            'candidato_nombre': self.candidato.nombre_completo if self.candidato else None,
            'candidato_numero_lista': self.candidato.numero_lista if self.candidato else None,
            'votos': self.votos
        }

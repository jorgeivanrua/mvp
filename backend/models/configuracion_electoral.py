"""
Modelos para configuración electoral
"""
from backend.database import db
from datetime import datetime


class TipoEleccion(db.Model):
    """Tipos de elección configurables"""
    __tablename__ = 'tipos_eleccion'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    es_uninominal = db.Column(db.Boolean, default=False)  # True para presidencia, gobernación, alcaldía
    permite_lista_cerrada = db.Column(db.Boolean, default=True)  # Para corporaciones
    permite_lista_abierta = db.Column(db.Boolean, default=False)  # Voto preferente
    permite_coaliciones = db.Column(db.Boolean, default=False)  # Coaliciones de partidos
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'es_uninominal': self.es_uninominal,
            'permite_lista_cerrada': self.permite_lista_cerrada,
            'permite_lista_abierta': self.permite_lista_abierta,
            'permite_coaliciones': self.permite_coaliciones,
            'activo': self.activo,
            'orden': self.orden
        }


class Partido(db.Model):
    """Partidos políticos"""
    __tablename__ = 'partidos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    nombre_corto = db.Column(db.String(50))
    logo_url = db.Column(db.String(500))
    color = db.Column(db.String(7))  # Código hexadecimal #RRGGBB
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    candidatos = db.relationship('Candidato', back_populates='partido', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'nombre_corto': self.nombre_corto,
            'logo_url': self.logo_url,
            'color': self.color,
            'activo': self.activo,
            'orden': self.orden
        }


class Coalicion(db.Model):
    """Coaliciones de partidos"""
    __tablename__ = 'coaliciones'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    partidos_coalicion = db.relationship('PartidoCoalicion', back_populates='coalicion', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'partidos': [pc.partido.to_dict() for pc in self.partidos_coalicion]
        }


class PartidoCoalicion(db.Model):
    """Relación entre partidos y coaliciones"""
    __tablename__ = 'partidos_coaliciones'
    
    id = db.Column(db.Integer, primary_key=True)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.id'), nullable=False)
    coalicion_id = db.Column(db.Integer, db.ForeignKey('coaliciones.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    partido = db.relationship('Partido', backref='coaliciones')
    coalicion = db.relationship('Coalicion', back_populates='partidos_coalicion')


class Candidato(db.Model):
    """Candidatos"""
    __tablename__ = 'candidatos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre_completo = db.Column(db.String(200), nullable=False)
    numero_lista = db.Column(db.Integer)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.id'))
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'))
    foto_url = db.Column(db.String(500))
    es_independiente = db.Column(db.Boolean, default=False)
    es_cabeza_lista = db.Column(db.Boolean, default=False)  # Para listas cerradas
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    partido = db.relationship('Partido', back_populates='candidatos')
    tipo_eleccion = db.relationship('TipoEleccion', backref='candidatos')
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre_completo': self.nombre_completo,
            'numero_lista': self.numero_lista,
            'partido_id': self.partido_id,
            'tipo_eleccion_id': self.tipo_eleccion_id,
            'foto_url': self.foto_url,
            'es_independiente': self.es_independiente,
            'es_cabeza_lista': self.es_cabeza_lista,
            'activo': self.activo,
            'orden': self.orden,
            'partido_nombre': self.partido.nombre if self.partido else None,
            'tipo_eleccion_nombre': self.tipo_eleccion.nombre if self.tipo_eleccion else None
        }

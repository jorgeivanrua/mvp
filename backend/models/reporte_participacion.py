"""
Modelo para Reporte de Participación Horaria (E-11)
"""
from backend.database import db
from datetime import datetime


class ReporteParticipacion(db.Model):
    """
    Reporte de participación horaria durante el día de votación.
    Los testigos reportan cuántas personas han votado según el formulario E-11.
    """
    __tablename__ = 'reporte_participacion'
    
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hora_reporte = db.Column(db.DateTime, nullable=False)
    personas_votadas = db.Column(db.Integer, nullable=False)
    porcentaje_participacion = db.Column(db.Float)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraint: Un testigo solo puede hacer un reporte por hora por mesa
    __table_args__ = (
        db.UniqueConstraint('mesa_id', 'hora_reporte', name='uq_mesa_hora_reporte'),
        db.Index('idx_reporte_participacion_mesa', 'mesa_id'),
        db.Index('idx_reporte_participacion_hora', 'hora_reporte'),
        db.Index('idx_reporte_participacion_testigo', 'testigo_id'),
    )
    
    def __repr__(self):
        return f'<ReporteParticipacion {self.id} - Mesa {self.mesa_id} - {self.hora_reporte}>'
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'mesa_id': self.mesa_id,
            'testigo_id': self.testigo_id,
            'hora_reporte': self.hora_reporte.isoformat() if self.hora_reporte else None,
            'personas_votadas': self.personas_votadas,
            'porcentaje_participacion': round(self.porcentaje_participacion, 2) if self.porcentaje_participacion else 0,
            'observaciones': self.observaciones,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_completo(self):
        """Convertir a diccionario con información completa"""
        from backend.models.location import Location
        from backend.models.user import User
        
        data = self.to_dict()
        
        # Agregar información de la mesa
        mesa = Location.query.get(self.mesa_id)
        if mesa:
            data['mesa'] = {
                'id': mesa.id,
                'codigo': mesa.mesa_codigo,
                'nombre': mesa.mesa_nombre,
                'puesto_nombre': mesa.puesto_nombre,
                'votantes_registrados': mesa.total_votantes_registrados or 0
            }
        
        # Agregar información del testigo
        testigo = User.query.get(self.testigo_id)
        if testigo:
            data['testigo'] = {
                'id': testigo.id,
                'nombre': testigo.nombre
            }
        
        return data

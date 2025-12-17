"""
Modelo para configuración de departamentos habilitados
"""
from datetime import datetime
from backend.database import db


class DepartamentoConfig(db.Model):
    """Configuración de departamentos habilitados en el sistema"""
    
    __tablename__ = 'departamentos_config'
    
    # Campos
    id = db.Column(db.Integer, primary_key=True)
    departamento_codigo = db.Column(db.String(10), nullable=False, unique=True, index=True)
    departamento_nombre = db.Column(db.String(100), nullable=False)
    
    # Estado
    habilitado = db.Column(db.Boolean, default=False, nullable=False)
    es_principal = db.Column(db.Boolean, default=False, nullable=False)  # Solo un departamento puede ser principal
    
    # Configuración de carga
    auto_crear_usuarios = db.Column(db.Boolean, default=True, nullable=False)
    auto_cargar_ubicaciones = db.Column(db.Boolean, default=True, nullable=False)
    
    # Estadísticas (se actualizan automáticamente)
    total_municipios = db.Column(db.Integer, default=0)
    total_puestos = db.Column(db.Integer, default=0)
    total_mesas = db.Column(db.Integer, default=0)
    total_usuarios_creados = db.Column(db.Integer, default=0)
    
    # Fechas
    habilitado_at = db.Column(db.DateTime, nullable=True)
    deshabilitado_at = db.Column(db.DateTime, nullable=True)
    ultima_carga_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def habilitar(self):
        """Habilitar este departamento"""
        self.habilitado = True
        self.habilitado_at = datetime.utcnow()
        self.deshabilitado_at = None
    
    def deshabilitar(self):
        """Deshabilitar este departamento"""
        self.habilitado = False
        self.deshabilitado_at = datetime.utcnow()
        
        # Si era principal, quitar esa marca
        if self.es_principal:
            self.es_principal = False
    
    def marcar_como_principal(self):
        """Marcar como departamento principal (solo uno puede serlo)"""
        # Quitar marca principal de otros departamentos
        DepartamentoConfig.query.filter(
            DepartamentoConfig.id != self.id
        ).update({'es_principal': False})
        
        # Marcar este como principal
        self.es_principal = True
        self.habilitar()  # Un departamento principal debe estar habilitado
    
    def actualizar_estadisticas(self):
        """Actualizar estadísticas de ubicaciones y usuarios"""
        from backend.models.location import Location
        from backend.models.user import User
        
        # Contar ubicaciones
        self.total_municipios = Location.query.filter_by(
            departamento_codigo=self.departamento_codigo,
            tipo='municipio',
            activo=True
        ).count()
        
        self.total_puestos = Location.query.filter_by(
            departamento_codigo=self.departamento_codigo,
            tipo='puesto',
            activo=True
        ).count()
        
        self.total_mesas = Location.query.filter_by(
            departamento_codigo=self.departamento_codigo,
            tipo='mesa',
            activo=True
        ).count()
        
        # Contar usuarios (excluyendo super_admin)
        ubicaciones_ids = [loc.id for loc in Location.query.filter_by(
            departamento_codigo=self.departamento_codigo,
            activo=True
        ).all()]
        
        if ubicaciones_ids:
            self.total_usuarios_creados = User.query.filter(
                User.ubicacion_id.in_(ubicaciones_ids),
                User.rol != 'super_admin',
                User.activo == True
            ).count()
        else:
            self.total_usuarios_creados = 0
    
    @classmethod
    def get_principal(cls):
        """Obtener el departamento principal activo"""
        return cls.query.filter_by(
            habilitado=True,
            es_principal=True
        ).first()
    
    @classmethod
    def get_habilitados(cls):
        """Obtener todos los departamentos habilitados"""
        return cls.query.filter_by(habilitado=True).all()
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'departamento_codigo': self.departamento_codigo,
            'departamento_nombre': self.departamento_nombre,
            'habilitado': self.habilitado,
            'es_principal': self.es_principal,
            'auto_crear_usuarios': self.auto_crear_usuarios,
            'auto_cargar_ubicaciones': self.auto_cargar_ubicaciones,
            'total_municipios': self.total_municipios,
            'total_puestos': self.total_puestos,
            'total_mesas': self.total_mesas,
            'total_usuarios_creados': self.total_usuarios_creados,
            'habilitado_at': self.habilitado_at.isoformat() if self.habilitado_at else None,
            'deshabilitado_at': self.deshabilitado_at.isoformat() if self.deshabilitado_at else None,
            'ultima_carga_at': self.ultima_carga_at.isoformat() if self.ultima_carga_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        estado = "HABILITADO" if self.habilitado else "DESHABILITADO"
        principal = " (PRINCIPAL)" if self.es_principal else ""
        return f'<DepartamentoConfig {self.departamento_nombre} - {estado}{principal}>'
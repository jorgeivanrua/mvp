"""
Modelo de Testigo Registrado por Partidos
Nuevo sistema según requerimientos de la Registraduría
"""
from datetime import datetime
from backend.database import db


class TestigoRegistrado(db.Model):
    """
    Testigos registrados por los partidos políticos
    Se registran por municipio, no por mesa específica
    """
    
    __tablename__ = 'testigos_registrados'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), nullable=False, unique=True, index=True)  # ID único
    nombre_completo = db.Column(db.String(200), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos_politicos.id'), nullable=False)
    
    # Ubicación (nivel municipio)
    departamento_codigo = db.Column(db.String(10), nullable=False)
    municipio_codigo = db.Column(db.String(10), nullable=False)
    
    # Estado del testigo
    activo = db.Column(db.Boolean, default=True, nullable=False)
    validado = db.Column(db.Boolean, default=False, nullable=False)  # Si ya se validó en alguna mesa
    
    # Información de validación
    mesa_validacion_id = db.Column(db.Integer, nullable=True)  # Mesa donde se validó
    puesto_validacion_codigo = db.Column(db.String(20), nullable=True)  # Puesto donde se validó
    fecha_validacion = db.Column(db.DateTime, nullable=True)
    
    # Usuario del sistema (se crea cuando se valida)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Metadatos
    registrado_por = db.Column(db.String(100), nullable=True)  # Quien registró al testigo
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    partido = db.relationship('PartidoPolitico', backref='testigos_registrados', lazy=True)
    usuario = db.relationship('User', backref='testigo_registrado', lazy=True)
    
    # Constraints
    __table_args__ = (
        db.Index('idx_testigo_cedula', 'cedula'),
        db.Index('idx_testigo_municipio', 'departamento_codigo', 'municipio_codigo'),
        db.Index('idx_testigo_partido', 'partido_id'),
        db.UniqueConstraint('cedula', name='uq_testigo_cedula'),
    )
    
    def validar_en_mesa(self, mesa_id, puesto_codigo):
        """
        Validar testigo en una mesa específica
        
        Args:
            mesa_id: ID de la mesa donde se valida
            puesto_codigo: Código del puesto
        """
        self.validado = True
        self.mesa_validacion_id = mesa_id
        self.puesto_validacion_codigo = puesto_codigo
        self.fecha_validacion = datetime.utcnow()
    
    def crear_usuario_sistema(self):
        """
        Crear usuario del sistema para el testigo validado
        
        Returns:
            User: Usuario creado
        """
        from backend.models.user import User
        from backend.models.location import Location
        
        if self.user_id:
            return User.query.get(self.user_id)
        
        # Buscar el puesto donde se validó
        puesto = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=self.departamento_codigo,
            municipio_codigo=self.municipio_codigo,
            puesto_codigo=self.puesto_validacion_codigo
        ).first()
        
        if not puesto:
            raise ValueError(f"No se encontró el puesto {self.puesto_validacion_codigo}")
        
        # Crear usuario
        usuario = User(
            nombre=f"testigo_{self.cedula}",
            rol='testigo_electoral',
            ubicacion_id=puesto.id,
            activo=True,
            es_usuario_basico=False
        )
        
        # Contraseña temporal basada en cédula
        usuario.set_password(f"testigo{self.cedula}")
        
        db.session.add(usuario)
        db.session.flush()  # Para obtener el ID
        
        # Vincular con el testigo registrado
        self.user_id = usuario.id
        
        return usuario
    
    def to_dict(self, include_sensitive=False):
        """
        Convertir a diccionario
        
        Args:
            include_sensitive: Incluir datos sensibles
            
        Returns:
            dict: Representación del testigo
        """
        data = {
            'id': self.id,
            'cedula': self.cedula,
            'nombre_completo': self.nombre_completo,
            'partido_id': self.partido_id,
            'departamento_codigo': self.departamento_codigo,
            'municipio_codigo': self.municipio_codigo,
            'activo': self.activo,
            'validado': self.validado,
            'fecha_validacion': self.fecha_validacion.isoformat() if self.fecha_validacion else None,
            'puesto_validacion_codigo': self.puesto_validacion_codigo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
        
        if include_sensitive:
            data.update({
                'mesa_validacion_id': self.mesa_validacion_id,
                'user_id': self.user_id,
                'registrado_por': self.registrado_por
            })
        
        # Incluir información del partido
        if self.partido:
            data['partido'] = {
                'id': self.partido.id,
                'nombre': self.partido.nombre,
                'sigla': self.partido.sigla
            }
        
        return data
    
    def __repr__(self):
        return f'<TestigoRegistrado {self.cedula}: {self.nombre_completo}>'


class LogValidacionTestigo(db.Model):
    """
    Log de intentos de validación de testigos
    Para auditoría y seguimiento
    """
    
    __tablename__ = 'log_validacion_testigos'
    
    id = db.Column(db.Integer, primary_key=True)
    cedula_ingresada = db.Column(db.String(20), nullable=False)
    nombre_ingresado = db.Column(db.String(200), nullable=True)
    
    # Resultado de la validación
    exitoso = db.Column(db.Boolean, nullable=False)
    testigo_encontrado_id = db.Column(db.Integer, db.ForeignKey('testigos_registrados.id'), nullable=True)
    
    # Contexto de la validación
    mesa_id = db.Column(db.Integer, nullable=True)
    puesto_codigo = db.Column(db.String(20), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    # Motivo del fallo (si aplica)
    motivo_fallo = db.Column(db.String(200), nullable=True)
    
    # Metadatos
    fecha_intento = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    testigo_encontrado = db.relationship('TestigoRegistrado', backref='logs_validacion', lazy=True)
    
    def __repr__(self):
        return f'<LogValidacionTestigo {self.cedula_ingresada}: {"✓" if self.exitoso else "✗"}>'

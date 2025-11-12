"""
Rutas para servir el frontend
"""
from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """Página principal - redirige al login"""
    return render_template('auth/login.html')


@frontend_bp.route('/login')
def login():
    """Página de login"""
    return render_template('auth/login.html')


@frontend_bp.route('/dashboard')
def dashboard():
    """Dashboard genérico"""
    return "<h1>Dashboard - En construcción</h1>"


@frontend_bp.route('/testigo/dashboard')
def testigo_dashboard():
    """Dashboard del testigo electoral"""
    return render_template('testigo/dashboard.html')


@frontend_bp.route('/coordinador/puesto')
def coordinador_puesto():
    """Dashboard del coordinador de puesto"""
    return render_template('coordinador/puesto.html')


@frontend_bp.route('/coordinador/municipal')
def coordinador_municipal():
    """Dashboard del coordinador municipal"""
    return render_template('admin/dashboard.html')  # Usa el mismo template del admin por ahora


@frontend_bp.route('/coordinador/departamental')
def coordinador_departamental():
    """Dashboard del coordinador departamental"""
    return render_template('admin/dashboard.html')  # Usa el mismo template del admin por ahora


@frontend_bp.route('/admin/dashboard')
def admin_dashboard():
    """Dashboard del administrador"""
    return render_template('admin/dashboard.html')


@frontend_bp.route('/admin/configuracion')
def admin_configuracion():
    """Configuración electoral"""
    return render_template('admin/configuracion.html')


@frontend_bp.route('/auditor/dashboard')
def auditor_dashboard():
    """Dashboard del auditor"""
    return render_template('admin/dashboard.html')  # Usa el mismo template del admin por ahora

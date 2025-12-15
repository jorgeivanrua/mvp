"""
Configuración global para tests
"""
import pytest
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

@pytest.fixture(scope="session")
def app():
    """Fixture de aplicación Flask para tests"""
    from backend.app import create_app
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    with app.app_context():
        yield app

@pytest.fixture(scope="session")
def client(app):
    """Cliente de test para requests HTTP"""
    return app.test_client()

@pytest.fixture(scope="session")
def db(app):
    """Base de datos de test"""
    from backend.database import db as _db
    
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture
def sample_user():
    """Usuario de ejemplo para tests"""
    return {
        "id": 1,
        "nombre": "Test User",
        "rol": "testigo_electoral",
        "cedula": "12345678",
        "activo": True
    }

@pytest.fixture
def sample_formulario():
    """Formulario de ejemplo para tests"""
    return {
        "id": 1,
        "mesa_id": 1,
        "testigo_id": 1,
        "total_votos": 100,
        "votos_validos": 95,
        "votos_nulos": 3,
        "votos_blanco": 2,
        "estado": "pendiente"
    }

@pytest.fixture
def auth_headers():
    """Headers de autenticación para tests"""
    return {
        "Authorization": "Bearer test-token",
        "Content-Type": "application/json"
    }

# Marcadores personalizados
pytest_plugins = []

def pytest_configure(config):
    """Configuración de pytest"""
    config.addinivalue_line(
        "markers", "unit: Tests unitarios que no requieren base de datos"
    )
    config.addinivalue_line(
        "markers", "integration: Tests de integración que requieren base de datos"
    )
    config.addinivalue_line(
        "markers", "slow: Tests que tardan más de 1 segundo"
    )
    config.addinivalue_line(
        "markers", "auth: Tests de autenticación y autorización"
    )

def pytest_collection_modifyitems(config, items):
    """Modificar items de test durante la recolección"""
    for item in items:
        # Agregar marcador 'unit' por defecto si está en tests/unit/
        if "tests/unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Agregar marcador 'integration' si está en tests/integration/
        elif "tests/integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
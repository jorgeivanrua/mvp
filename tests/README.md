# Tests - Sistema Electoral MVP

## 📁 Estructura de Tests

```
tests/
├── unit/                    # Tests unitarios
│   ├── test_cedula_field.py
│   ├── test_cedula_toggle.py
│   └── test_cedula_visible.py
├── integration/             # Tests de integración
│   ├── test_bulk_loading.py
│   ├── test_carga_testigos.json
│   ├── test_login_cedula.py
│   ├── test_nuevos_endpoints.py
│   └── test_urls_corregidas.py
├── frontend/                # Tests de frontend
│   └── test_login_frontend.html
└── README.md
```

## 🧪 Tipos de Tests

### **Tests Unitarios** (`tests/unit/`)
Prueban componentes individuales de forma aislada:
- **test_cedula_field.py**: Validación de campos de cédula
- **test_cedula_toggle.py**: Funcionalidad de toggle de cédula
- **test_cedula_visible.py**: Visibilidad de campos de cédula

### **Tests de Integración** (`tests/integration/`)
Prueban la interacción entre múltiples componentes:
- **test_bulk_loading.py**: Carga masiva de testigos
- **test_login_cedula.py**: Proceso completo de login con cédula
- **test_nuevos_endpoints.py**: Nuevos endpoints implementados
- **test_urls_corregidas.py**: Corrección de URLs duplicadas
- **test_carga_testigos.json**: Datos de prueba para carga de testigos

### **Tests de Frontend** (`tests/frontend/`)
Prueban funcionalidades del frontend:
- **test_login_frontend.html**: Interfaz de login

## 🚀 Ejecutar Tests

### **Todos los tests**
```bash
pytest tests/
```

### **Solo tests unitarios**
```bash
pytest tests/unit/
```

### **Solo tests de integración**
```bash
pytest tests/integration/
```

### **Test específico**
```bash
pytest tests/unit/test_cedula_field.py
```

### **Con cobertura**
```bash
pytest tests/ --cov=backend --cov-report=html
```

## 📋 Configuración

### **pytest.ini** (en raíz del proyecto)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### **Dependencias de Testing**
```txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
requests-mock>=1.10.0
```

## 🔧 Buenas Prácticas

### **Nomenclatura**
- Archivos: `test_*.py`
- Clases: `Test*`
- Funciones: `test_*`

### **Estructura de Test**
```python
def test_feature_should_do_something():
    # Arrange (preparar)
    data = {"key": "value"}
    
    # Act (ejecutar)
    result = function_to_test(data)
    
    # Assert (verificar)
    assert result == expected_value
```

### **Fixtures**
```python
@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "nombre": "Test User",
        "rol": "testigo_electoral"
    }
```

### **Mocking**
```python
@patch('backend.services.user_service.get_user')
def test_user_service(mock_get_user):
    mock_get_user.return_value = {"id": 1}
    # Test logic here
```

## 📊 Cobertura de Tests

### **Objetivo**: 80%+ de cobertura
- **Backend**: Modelos, servicios, rutas
- **Frontend**: Funciones JavaScript críticas
- **Integración**: Flujos completos de usuario

### **Áreas Críticas**
- ✅ Autenticación y autorización
- ✅ Validación de formularios E-14
- ✅ Gestión de usuarios y roles
- ✅ APIs de coordinadores
- ✅ Sincronización de datos

## 🐛 Debugging Tests

### **Ejecutar con debug**
```bash
pytest tests/ -s -vv --pdb
```

### **Solo tests fallidos**
```bash
pytest tests/ --lf
```

### **Parar en primer fallo**
```bash
pytest tests/ -x
```

## 📝 Agregar Nuevos Tests

1. **Crear archivo** en directorio apropiado
2. **Seguir nomenclatura** `test_*.py`
3. **Importar dependencias** necesarias
4. **Escribir tests** siguiendo AAA pattern
5. **Ejecutar y verificar** que pasen
6. **Documentar** casos especiales

## 🔄 CI/CD Integration

Los tests se ejecutan automáticamente en:
- **Pre-commit hooks**
- **Pull requests**
- **Deployment pipeline**
- **Scheduled runs** (nightly)

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Flask Testing](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [JavaScript Testing](https://jestjs.io/docs/getting-started)
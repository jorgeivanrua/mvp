"""
Property-based tests para modelos de Partidos y Candidatos

**Feature: mejoras-admin-mapas, Property 7: All party fields are editable**
**Feature: mejoras-admin-mapas, Property 11: All candidate fields are editable**
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from backend.models.partido_politico import PartidoPolitico
from backend.models.candidato import Candidato
from backend.models.tipo_eleccion import TipoEleccion
from backend.database import db


# Estrategias personalizadas

@st.composite
def partido_data_strategy(draw):
    """Generar datos válidos para un partido político"""
    nombre = draw(st.text(min_size=3, max_size=200, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs'), 
        blacklist_characters='\x00'
    )))
    sigla = draw(st.text(min_size=2, max_size=20, alphabet=st.characters(
        whitelist_categories=('Lu', 'Nd'),
        blacklist_characters='\x00'
    )))
    
    # Generar color hexadecimal válido
    r = draw(st.integers(min_value=0, max_value=255))
    g = draw(st.integers(min_value=0, max_value=255))
    b = draw(st.integers(min_value=0, max_value=255))
    color = f"#{r:02X}{g:02X}{b:02X}"
    
    return {
        'nombre': nombre.strip(),
        'sigla': sigla.strip(),
        'color': color,
        'descripcion': draw(st.text(max_size=500)),
        'activo': draw(st.booleans())
    }


@st.composite
def candidato_data_strategy(draw, partido_id, tipo_eleccion_id):
    """Generar datos válidos para un candidato"""
    nombre = draw(st.text(min_size=5, max_size=200, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Zs'),
        blacklist_characters='\x00'
    )))
    
    cargos = ['Presidente', 'Vicepresidente', 'Senador', 'Diputado', 
              'Gobernador', 'Alcalde', 'Concejal', 'Asambleísta']
    
    return {
        'nombre_completo': nombre.strip(),
        'partido_id': partido_id,
        'tipo_eleccion_id': tipo_eleccion_id,
        'cargo': draw(st.sampled_from(cargos)),
        'numero_lista': draw(st.integers(min_value=1, max_value=999)),
        'biografia': draw(st.text(max_size=1000)),
        'activo': draw(st.booleans())
    }


class TestPartidoPoliticoProperties:
    """Property tests para PartidoPolitico"""
    
    @given(partido_data=partido_data_strategy())
    @settings(max_examples=100)
    def test_property_7_all_party_fields_are_editable(self, app, partido_data):
        """
        **Feature: mejoras-admin-mapas, Property 7: All party fields are editable**
        **Validates: Requirements 3.3**
        
        Para cualquier partido político, todos sus campos deben ser modificables
        """
        with app.app_context():
            # Crear partido inicial
            partido = PartidoPolitico(
                nombre=f"Partido Test {partido_data['nombre'][:20]}",
                sigla=f"PT{partido_data['sigla'][:5]}",
                color='#000000'
            )
            db.session.add(partido)
            db.session.commit()
            
            partido_id = partido.id
            
            # Intentar modificar todos los campos
            partido.nombre = partido_data['nombre'][:200] if partido_data['nombre'] else 'Partido Modificado'
            partido.sigla = partido_data['sigla'][:20] if partido_data['sigla'] else 'PM'
            partido.color = partido_data['color']
            partido.descripcion = partido_data['descripcion']
            partido.activo = partido_data['activo']
            
            db.session.commit()
            
            # Verificar que los cambios se guardaron
            partido_actualizado = PartidoPolitico.query.get(partido_id)
            
            assert partido_actualizado.nombre == (partido_data['nombre'][:200] if partido_data['nombre'] else 'Partido Modificado')
            assert partido_actualizado.sigla == (partido_data['sigla'][:20] if partido_data['sigla'] else 'PM')
            assert partido_actualizado.color == partido_data['color']
            assert partido_actualizado.descripcion == partido_data['descripcion']
            assert partido_actualizado.activo == partido_data['activo']
            
            # Limpiar
            db.session.delete(partido_actualizado)
            db.session.commit()
    
    @given(color=st.text(min_size=7, max_size=7))
    @settings(max_examples=100)
    def test_color_validation(self, color):
        """Validar que solo se acepten colores hexadecimales válidos"""
        is_valid = PartidoPolitico.validar_color(color)
        
        # Si el color tiene formato #RRGGBB con dígitos hex, debe ser válido
        if color.startswith('#') and len(color) == 7:
            try:
                int(color[1:], 16)
                assert is_valid, f"Color {color} debería ser válido"
            except ValueError:
                assert not is_valid, f"Color {color} no debería ser válido"


class TestCandidatoProperties:
    """Property tests para Candidato"""
    
    @given(candidato_data=st.data())
    @settings(max_examples=100)
    def test_property_11_all_candidate_fields_are_editable(self, app, candidato_data):
        """
        **Feature: mejoras-admin-mapas, Property 11: All candidate fields are editable**
        **Validates: Requirements 4.3**
        
        Para cualquier candidato, todos sus campos deben ser modificables
        """
        with app.app_context():
            # Crear partido y tipo de elección necesarios
            partido = PartidoPolitico(
                nombre=f"Partido Test {candidato_data.draw(st.integers(min_value=1, max_value=10000))}",
                sigla=f"PT{candidato_data.draw(st.integers(min_value=1, max_value=999))}",
                color='#FF0000'
            )
            db.session.add(partido)
            
            tipo_eleccion = TipoEleccion.query.first()
            if not tipo_eleccion:
                tipo_eleccion = TipoEleccion(
                    nombre='Presidencial',
                    nivel='nacional',
                    descripcion='Elección presidencial'
                )
                db.session.add(tipo_eleccion)
            
            db.session.commit()
            
            # Generar datos del candidato
            datos = candidato_data.draw(candidato_data_strategy(
                partido_id=partido.id,
                tipo_eleccion_id=tipo_eleccion.id
            ))
            
            # Crear candidato inicial
            candidato = Candidato(
                nombre_completo='Candidato Inicial',
                partido_id=partido.id,
                tipo_eleccion_id=tipo_eleccion.id,
                cargo='Presidente'
            )
            db.session.add(candidato)
            db.session.commit()
            
            candidato_id = candidato.id
            
            # Intentar modificar todos los campos
            candidato.nombre_completo = datos['nombre_completo'][:200] if datos['nombre_completo'] else 'Candidato Modificado'
            candidato.cargo = datos['cargo']
            candidato.numero_lista = datos['numero_lista']
            candidato.biografia = datos['biografia']
            candidato.activo = datos['activo']
            
            db.session.commit()
            
            # Verificar que los cambios se guardaron
            candidato_actualizado = Candidato.query.get(candidato_id)
            
            assert candidato_actualizado.nombre_completo == (datos['nombre_completo'][:200] if datos['nombre_completo'] else 'Candidato Modificado')
            assert candidato_actualizado.cargo == datos['cargo']
            assert candidato_actualizado.numero_lista == datos['numero_lista']
            assert candidato_actualizado.biografia == datos['biografia']
            assert candidato_actualizado.activo == datos['activo']
            
            # Limpiar
            db.session.delete(candidato_actualizado)
            db.session.delete(partido)
            db.session.commit()


class TestModelRelationships:
    """Property tests para relaciones entre modelos"""
    
    @given(num_candidatos=st.integers(min_value=0, max_value=10))
    @settings(max_examples=50)
    def test_partido_candidatos_relationship(self, app, num_candidatos):
        """Verificar que la relación partido-candidatos funciona correctamente"""
        with app.app_context():
            # Crear partido
            partido = PartidoPolitico(
                nombre=f"Partido Test Rel {num_candidatos}",
                sigla=f"PTR{num_candidatos}",
                color='#00FF00'
            )
            db.session.add(partido)
            
            tipo_eleccion = TipoEleccion.query.first()
            if not tipo_eleccion:
                tipo_eleccion = TipoEleccion(
                    nombre='Presidencial',
                    nivel='nacional',
                    descripcion='Elección presidencial'
                )
                db.session.add(tipo_eleccion)
            
            db.session.commit()
            
            # Crear candidatos
            for i in range(num_candidatos):
                candidato = Candidato(
                    nombre_completo=f'Candidato {i}',
                    partido_id=partido.id,
                    tipo_eleccion_id=tipo_eleccion.id,
                    cargo='Senador'
                )
                db.session.add(candidato)
            
            db.session.commit()
            
            # Verificar relación
            partido_actualizado = PartidoPolitico.query.get(partido.id)
            assert partido_actualizado.candidatos.count() == num_candidatos
            
            # Limpiar
            for candidato in partido_actualizado.candidatos:
                db.session.delete(candidato)
            db.session.delete(partido_actualizado)
            db.session.commit()



class TestPartidoDeletionProperties:
    """Property tests para eliminación de partidos"""
    
    @given(num_candidatos=st.integers(min_value=1, max_value=10))
    @settings(max_examples=50)
    def test_property_8_party_deletion_with_candidates_fails(self, app, num_candidatos):
        """
        **Feature: mejoras-admin-mapas, Property 8: Party deletion requires no associated candidates**
        **Validates: Requirements 3.4**
        
        Para cualquier partido con candidatos asociados, la eliminación debe ser rechazada
        """
        from backend.services.partido_service import PartidoService
        
        with app.app_context():
            # Crear partido
            partido_data = {
                'nombre': f'Partido Test Del {num_candidatos}',
                'sigla': f'PTD{num_candidatos}',
                'color': '#FF0000'
            }
            partido_dict, error = PartidoService.crear_partido(partido_data)
            assert error is None
            partido_id = partido_dict['id']
            
            # Crear tipo de elección si no existe
            tipo_eleccion = TipoEleccion.query.first()
            if not tipo_eleccion:
                tipo_eleccion = TipoEleccion(
                    nombre='Presidencial',
                    nivel='nacional',
                    descripcion='Elección presidencial'
                )
                db.session.add(tipo_eleccion)
                db.session.commit()
            
            # Crear candidatos asociados
            for i in range(num_candidatos):
                candidato = Candidato(
                    nombre_completo=f'Candidato {i}',
                    partido_id=partido_id,
                    tipo_eleccion_id=tipo_eleccion.id,
                    cargo='Senador'
                )
                db.session.add(candidato)
            db.session.commit()
            
            # Intentar eliminar partido con candidatos
            success, error = PartidoService.eliminar_partido(partido_id)
            
            # La eliminación debe fallar
            assert not success
            assert error is not None
            assert 'candidato' in error.lower()
            
            # Verificar que el partido sigue existiendo
            partido = PartidoPolitico.query.get(partido_id)
            assert partido is not None
            
            # Limpiar
            for candidato in partido.candidatos:
                db.session.delete(candidato)
            db.session.delete(partido)
            db.session.commit()
    
    @given(st.integers(min_value=1, max_value=100))
    @settings(max_examples=50)
    def test_property_8_party_deletion_without_candidates_succeeds(self, app, partido_num):
        """
        **Feature: mejoras-admin-mapas, Property 8: Party deletion requires no associated candidates**
        **Validates: Requirements 3.4**
        
        Para cualquier partido sin candidatos asociados, la eliminación debe tener éxito
        """
        from backend.services.partido_service import PartidoService
        
        with app.app_context():
            # Crear partido sin candidatos
            partido_data = {
                'nombre': f'Partido Test Sin Cand {partido_num}',
                'sigla': f'PTSC{partido_num}',
                'color': '#00FF00'
            }
            partido_dict, error = PartidoService.crear_partido(partido_data)
            assert error is None
            partido_id = partido_dict['id']
            
            # Intentar eliminar partido sin candidatos
            success, error = PartidoService.eliminar_partido(partido_id)
            
            # La eliminación debe tener éxito
            assert success
            assert error is None
            
            # Verificar que el partido fue eliminado
            partido = PartidoPolitico.query.get(partido_id)
            assert partido is None


class TestLogoValidationProperties:
    """Property tests para validación de logos"""
    
    @given(
        filename=st.text(min_size=5, max_size=50),
        extension=st.sampled_from(['png', 'jpg', 'jpeg', 'webp', 'svg', 'gif', 'bmp', 'txt'])
    )
    @settings(max_examples=100)
    def test_property_9_logo_format_validation(self, filename, extension):
        """
        **Feature: mejoras-admin-mapas, Property 9: Party logo upload validation**
        **Validates: Requirements 3.5**
        
        Para cualquier archivo subido, el sistema debe validar formato y tamaño
        """
        from backend.services.partido_service import PartidoService
        from werkzeug.datastructures import FileStorage
        from io import BytesIO
        
        # Extensiones permitidas
        extensiones_permitidas = {'png', 'jpg', 'jpeg', 'webp', 'svg'}
        
        # Crear archivo mock
        archivo = FileStorage(
            stream=BytesIO(b'fake image data'),
            filename=f"{filename}.{extension}",
            content_type=f'image/{extension}'
        )
        
        # Validar
        valid, error = PartidoService.validar_logo(archivo)
        
        # Verificar resultado
        if extension in extensiones_permitidas:
            assert valid, f"Extensión {extension} debería ser válida"
        else:
            assert not valid, f"Extensión {extension} no debería ser válida"
            assert error is not None
    
    @given(tamano_mb=st.floats(min_value=0.1, max_value=10.0))
    @settings(max_examples=50)
    def test_property_9_logo_size_validation(self, tamano_mb):
        """
        **Feature: mejoras-admin-mapas, Property 9: Party logo upload validation**
        **Validates: Requirements 3.5**
        
        Para cualquier archivo, el tamaño debe estar dentro del límite (5MB)
        """
        from backend.services.partido_service import PartidoService
        from werkzeug.datastructures import FileStorage
        from io import BytesIO
        
        # Crear archivo mock con tamaño específico
        tamano_bytes = int(tamano_mb * 1024 * 1024)
        archivo = FileStorage(
            stream=BytesIO(b'x' * tamano_bytes),
            filename='logo.png',
            content_type='image/png'
        )
        
        # Validar
        valid, error = PartidoService.validar_logo(archivo)
        
        # Verificar resultado
        max_tamano_mb = 5.0
        if tamano_mb <= max_tamano_mb:
            assert valid, f"Tamaño {tamano_mb}MB debería ser válido"
        else:
            assert not valid, f"Tamaño {tamano_mb}MB no debería ser válido"
            assert error is not None
            assert 'grande' in error.lower() or 'tamaño' in error.lower()

"""
Servicio para gestión de testigos registrados
Nuevo sistema según requerimientos de Registraduría
"""
from datetime import datetime
from flask import request
from datetime import datetime, timedelta
from backend.database import db
from backend.models.testigo_registrado import TestigoRegistrado, LogValidacionTestigo
from backend.models.user import User
from backend.models.location import Location
from backend.utils.exceptions import ValidationException, AuthenticationException
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)


class TestigoService:
    """Servicio para gestión de testigos registrados"""
    
    @staticmethod
    def validar_testigo_simple_por_cedula(cedula):
        """
        Validar testigo por cédula únicamente (versión simplificada)
        
        Args:
            cedula: Número de cédula del testigo
            
        Returns:
            dict: Resultado de la validación
        """
        # Limpiar cédula (solo números)
        cedula_limpia = ''.join(filter(str.isdigit, str(cedula)))
        
        if not cedula_limpia:
            TestigoService._log_intento_validacion(
                cedula, None, False, None, None, None, "Cédula inválida"
            )
            raise ValidationException({'cedula': ['Número de cédula inválido']})
        
        if len(cedula_limpia) < 6 or len(cedula_limpia) > 12:
            TestigoService._log_intento_validacion(
                cedula_limpia, None, False, None, None, None, "Cédula fuera de rango"
            )
            raise ValidationException({'cedula': ['Número de cédula debe tener entre 6 y 12 dígitos']})
        
        # Buscar testigo registrado
        testigo = TestigoRegistrado.query.filter_by(
            cedula=cedula_limpia,
            activo=True
        ).first()
        
        if not testigo:
            TestigoService._log_intento_validacion(
                cedula_limpia, None, False, None, None, None, "Testigo no registrado"
            )
            raise AuthenticationException("Testigo no encontrado en el registro de partidos políticos")
        
        # Si no está validado, validarlo ahora (sin restricciones de puesto)
        if not testigo.validado:
            # Buscar un puesto del municipio del testigo para asignarlo
            puesto = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo=testigo.departamento_codigo,
                municipio_codigo=testigo.municipio_codigo,
                activo=True
            ).first()
            
            if not puesto:
                raise ValidationException({
                    'testigo': [f'No se encontraron puestos activos en el municipio {testigo.municipio_codigo}']
                })
            
            testigo.validar_en_mesa(None, puesto.puesto_codigo)
            
            # Crear usuario del sistema
            usuario = testigo.crear_usuario_sistema()
            
            db.session.commit()
            
            logger.info(f"Testigo validado automáticamente: {cedula_limpia} - {testigo.nombre_completo}")
        else:
            # Ya estaba validado, obtener usuario existente
            if testigo.user_id:
                usuario = User.query.get(testigo.user_id)
            else:
                # Si no tiene usuario, crearlo ahora
                usuario = testigo.crear_usuario_sistema()
                db.session.commit()
        
        # Log exitoso
        TestigoService._log_intento_validacion(
            cedula_limpia, None, True, testigo.id, None, testigo.puesto_validacion_codigo, None
        )
        
        return {
            'testigo': testigo.to_dict(),
            'usuario': usuario.to_dict() if usuario else None,
            'ya_validado': testigo.validado,
            'mensaje': 'Testigo validado exitosamente' if not testigo.validado else 'Testigo ya validado previamente'
        }
    
    @staticmethod
    def validar_testigo_por_cedula(cedula, nombre, mesa_id=None, puesto_codigo=None):
        """
        Validar testigo por cédula y nombre
        
        Args:
            cedula: Número de cédula del testigo
            nombre: Nombre del testigo (para verificación)
            mesa_id: ID de la mesa donde se valida (opcional)
            puesto_codigo: Código del puesto (opcional)
            
        Returns:
            dict: Resultado de la validación
        """
        # Limpiar cédula (solo números)
        cedula_limpia = ''.join(filter(str.isdigit, str(cedula)))
        
        if not cedula_limpia:
            TestigoService._log_intento_validacion(
                cedula, nombre, False, None, mesa_id, puesto_codigo, "Cédula inválida"
            )
            raise ValidationException({'cedula': ['Número de cédula inválido']})
        
        if len(cedula_limpia) < 6 or len(cedula_limpia) > 12:
            TestigoService._log_intento_validacion(
                cedula_limpia, nombre, False, None, mesa_id, puesto_codigo, "Cédula fuera de rango"
            )
            raise ValidationException({'cedula': ['Número de cédula debe tener entre 6 y 12 dígitos']})
        
        # Buscar testigo registrado
        testigo = TestigoRegistrado.query.filter_by(
            cedula=cedula_limpia,
            activo=True
        ).first()
        
        if not testigo:
            TestigoService._log_intento_validacion(
                cedula_limpia, nombre, False, None, mesa_id, puesto_codigo, "Testigo no registrado"
            )
            raise AuthenticationException("Testigo no encontrado en el registro de partidos políticos")
        
        # Verificar nombre (coincidencia parcial)
        if nombre and not TestigoService._verificar_nombre_similar(testigo.nombre_completo, nombre):
            TestigoService._log_intento_validacion(
                cedula_limpia, nombre, False, testigo.id, mesa_id, puesto_codigo, "Nombre no coincide"
            )
            raise AuthenticationException("El nombre no coincide con el registrado")
        
        # Verificar si ya está validado en otro puesto
        if testigo.validado and testigo.puesto_validacion_codigo != puesto_codigo:
            TestigoService._log_intento_validacion(
                cedula_limpia, nombre, False, testigo.id, mesa_id, puesto_codigo, 
                f"Ya validado en puesto {testigo.puesto_validacion_codigo}"
            )
            raise ValidationException({
                'testigo': [f'Este testigo ya fue validado en el puesto {testigo.puesto_validacion_codigo}']
            })
        
        # Si no está validado, validarlo ahora
        if not testigo.validado:
            testigo.validar_en_mesa(mesa_id, puesto_codigo)
            
            # Crear usuario del sistema
            usuario = testigo.crear_usuario_sistema()
            
            db.session.commit()
            
            logger.info(f"Testigo validado: {cedula_limpia} - {testigo.nombre_completo}")
        else:
            # Ya estaba validado en este puesto
            usuario = User.query.get(testigo.user_id)
        
        # Log exitoso
        TestigoService._log_intento_validacion(
            cedula_limpia, nombre, True, testigo.id, mesa_id, puesto_codigo, None
        )
        
        return {
            'testigo': testigo.to_dict(),
            'usuario': usuario.to_dict() if usuario else None,
            'ya_validado': testigo.validado,
            'mensaje': 'Testigo validado exitosamente' if not testigo.validado else 'Testigo ya validado previamente'
        }
    
    @staticmethod
    def _verificar_nombre_similar(nombre_registrado, nombre_ingresado):
        """
        Verificar si dos nombres son similares
        Permite coincidencias parciales para manejar variaciones
        
        Args:
            nombre_registrado: Nombre en la base de datos
            nombre_ingresado: Nombre ingresado por el usuario
            
        Returns:
            bool: True si son similares
        """
        if not nombre_ingresado:
            return True  # Si no se proporciona nombre, no validar
        
        # Normalizar nombres (minúsculas, sin acentos, sin espacios extra)
        def normalizar(texto):
            import unicodedata
            texto = texto.lower().strip()
            texto = unicodedata.normalize('NFD', texto)
            texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
            return ' '.join(texto.split())
        
        nombre_reg_norm = normalizar(nombre_registrado)
        nombre_ing_norm = normalizar(nombre_ingresado)
        
        # Verificar coincidencia exacta
        if nombre_reg_norm == nombre_ing_norm:
            return True
        
        # Verificar si el nombre ingresado está contenido en el registrado
        if nombre_ing_norm in nombre_reg_norm:
            return True
        
        # Verificar coincidencia de palabras (al menos 2 palabras en común)
        palabras_reg = set(nombre_reg_norm.split())
        palabras_ing = set(nombre_ing_norm.split())
        
        coincidencias = len(palabras_reg.intersection(palabras_ing))
        
        # Si hay al menos 2 palabras en común, considerar válido
        return coincidencias >= 2
    
    @staticmethod
    def _log_intento_validacion(cedula, nombre, exitoso, testigo_id, mesa_id, puesto_codigo, motivo_fallo):
        """
        Registrar intento de validación para auditoría
        
        Args:
            cedula: Cédula ingresada
            nombre: Nombre ingresado
            exitoso: Si fue exitoso
            testigo_id: ID del testigo encontrado (si aplica)
            mesa_id: ID de la mesa
            puesto_codigo: Código del puesto
            motivo_fallo: Motivo del fallo (si aplica)
        """
        try:
            log = LogValidacionTestigo(
                cedula_ingresada=cedula,
                nombre_ingresado=nombre,
                exitoso=exitoso,
                testigo_encontrado_id=testigo_id,
                mesa_id=mesa_id,
                puesto_codigo=puesto_codigo,
                motivo_fallo=motivo_fallo,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get('User-Agent') if request else None
            )
            
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error logging validación: {e}")
    
    @staticmethod
    def obtener_testigos_municipio(departamento_codigo, municipio_codigo):
        """
        Obtener testigos registrados de un municipio
        
        Args:
            departamento_codigo: Código del departamento
            municipio_codigo: Código del municipio
            
        Returns:
            list: Lista de testigos
        """
        testigos = TestigoRegistrado.query.filter_by(
            departamento_codigo=departamento_codigo,
            municipio_codigo=municipio_codigo,
            activo=True
        ).order_by(TestigoRegistrado.nombre_completo).all()
        
        return [testigo.to_dict() for testigo in testigos]
    
    @staticmethod
    def obtener_testigos_validados_puesto(puesto_codigo):
        """
        Obtener testigos validados en un puesto específico
        
        Args:
            puesto_codigo: Código del puesto
            
        Returns:
            list: Lista de testigos validados
        """
        testigos = TestigoRegistrado.query.filter_by(
            puesto_validacion_codigo=puesto_codigo,
            validado=True,
            activo=True
        ).order_by(TestigoRegistrado.fecha_validacion.desc()).all()
        
        return [testigo.to_dict(include_sensitive=True) for testigo in testigos]
    
    @staticmethod
    def registrar_testigo_partido(cedula, nombre_completo, partido_id, departamento_codigo, municipio_codigo, registrado_por=None):
        """
        Registrar un nuevo testigo por parte de un partido
        
        Args:
            cedula: Número de cédula
            nombre_completo: Nombre completo del testigo
            partido_id: ID del partido político
            departamento_codigo: Código del departamento
            municipio_codigo: Código del municipio
            registrado_por: Quien registra al testigo
            
        Returns:
            TestigoRegistrado: Testigo registrado
        """
        # Limpiar cédula
        cedula_limpia = ''.join(filter(str.isdigit, str(cedula)))
        
        if not cedula_limpia or len(cedula_limpia) < 6:
            raise ValidationException({'cedula': ['Número de cédula inválido']})
        
        # Verificar que no exista
        testigo_existente = TestigoRegistrado.query.filter_by(cedula=cedula_limpia).first()
        if testigo_existente:
            raise ValidationException({'cedula': ['Ya existe un testigo registrado con esta cédula']})
        
        # Crear testigo
        testigo = TestigoRegistrado(
            cedula=cedula_limpia,
            nombre_completo=nombre_completo.strip().title(),
            partido_id=partido_id,
            departamento_codigo=departamento_codigo,
            municipio_codigo=municipio_codigo,
            registrado_por=registrado_por
        )
        
        db.session.add(testigo)
        db.session.commit()
        
        logger.info(f"Testigo registrado: {cedula_limpia} - {nombre_completo}")
        
        return testigo
    
    @staticmethod
    def obtener_estadisticas_validacion():
        """
        Obtener estadísticas de validación de testigos
        
        Returns:
            dict: Estadísticas
        """
        total_registrados = TestigoRegistrado.query.filter_by(activo=True).count()
        total_validados = TestigoRegistrado.query.filter_by(activo=True, validado=True).count()
        
        # Intentos de validación en las últimas 24 horas
        hace_24h = datetime.utcnow() - timedelta(hours=24)
        intentos_24h = LogValidacionTestigo.query.filter(
            LogValidacionTestigo.fecha_intento >= hace_24h
        ).count()
        
        exitosos_24h = LogValidacionTestigo.query.filter(
            LogValidacionTestigo.fecha_intento >= hace_24h,
            LogValidacionTestigo.exitoso == True
        ).count()
        
        return {
            'total_registrados': total_registrados,
            'total_validados': total_validados,
            'pendientes_validacion': total_registrados - total_validados,
            'porcentaje_validados': round((total_validados / total_registrados * 100), 2) if total_registrados > 0 else 0,
            'intentos_24h': intentos_24h,
            'exitosos_24h': exitosos_24h,
            'tasa_exito_24h': round((exitosos_24h / intentos_24h * 100), 2) if intentos_24h > 0 else 0
        }
    
    @staticmethod
    def cargar_testigos_masivo(departamento_codigo, municipio_codigo, testigos_data, registrado_por=None):
        """
        Cargar testigos masivamente por municipio
        
        Args:
            departamento_codigo: Código del departamento
            municipio_codigo: Código del municipio
            testigos_data: Lista de diccionarios con datos de testigos
            registrado_por: Quien registra los testigos
            
        Returns:
            dict: Resultado de la carga masiva
        """
        from backend.models.partido_politico import PartidoPolitico
        
        exitosos = 0
        errores = 0
        detalles_errores = []
        testigos_creados = []
        
        # Validar que el municipio existe
        municipio = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento_codigo,
            municipio_codigo=municipio_codigo
        ).first()
        
        if not municipio:
            raise ValidationException({
                'municipio': [f'No se encontró el municipio {departamento_codigo}-{municipio_codigo}']
            })
        
        logger.info(f"Iniciando carga masiva de {len(testigos_data)} testigos para {municipio.nombre_completo}")
        
        for i, testigo_data in enumerate(testigos_data, 1):
            try:
                # Validar campos requeridos
                if not testigo_data.get('cedula'):
                    raise ValidationException({'cedula': ['Cédula es requerida']})
                
                if not testigo_data.get('nombre_completo'):
                    raise ValidationException({'nombre_completo': ['Nombre completo es requerido']})
                
                # Limpiar cédula (remover puntos, espacios, guiones)
                cedula_limpia = ''.join(filter(str.isdigit, str(testigo_data['cedula'])))
                
                if not cedula_limpia or len(cedula_limpia) < 6:
                    raise ValidationException({'cedula': ['Número de cédula inválido']})
                
                # Usar partido por defecto (primer partido activo) o crear uno genérico
                partido_id = testigo_data.get('partido_id')
                if not partido_id:
                    # Buscar o crear partido genérico para testigos
                    partido_generico = PartidoPolitico.query.filter_by(sigla='TESTIGOS').first()
                    if not partido_generico:
                        partido_generico = PartidoPolitico(
                            nombre='Testigos Electorales',
                            sigla='TESTIGOS',
                            color='#6c757d',
                            activo=True
                        )
                        db.session.add(partido_generico)
                        db.session.flush()
                    partido_id = partido_generico.id
                
                # Verificar que no exista ya
                testigo_existente = TestigoRegistrado.query.filter_by(cedula=cedula_limpia).first()
                if testigo_existente:
                    raise ValidationException({'cedula': ['Ya existe un testigo con esta cédula']})
                
                # Crear testigo
                testigo = TestigoRegistrado(
                    cedula=cedula_limpia,
                    nombre_completo=testigo_data['nombre_completo'].strip().title(),
                    partido_id=partido_id,
                    departamento_codigo=departamento_codigo,
                    municipio_codigo=municipio_codigo,
                    registrado_por=registrado_por
                )
                
                db.session.add(testigo)
                testigos_creados.append(testigo)
                exitosos += 1
                
                # Commit cada 50 registros para evitar transacciones muy largas
                if exitosos % 50 == 0:
                    db.session.commit()
                    logger.info(f"Procesados {exitosos} testigos...")
                
            except ValidationException as e:
                errores += 1
                error_msg = '; '.join([f"{field}: {', '.join(messages)}" for field, messages in e.errors.items()])
                detalles_errores.append({
                    'fila': i,
                    'cedula': testigo_data.get('cedula', 'N/A'),
                    'nombre': testigo_data.get('nombre_completo', 'N/A'),
                    'error': error_msg
                })
                logger.warning(f"Error en fila {i}: {error_msg}")
                
            except Exception as e:
                errores += 1
                detalles_errores.append({
                    'fila': i,
                    'cedula': testigo_data.get('cedula', 'N/A'),
                    'nombre': testigo_data.get('nombre_completo', 'N/A'),
                    'error': str(e)
                })
                logger.error(f"Error inesperado en fila {i}: {e}")
        
        # Commit final
        try:
            db.session.commit()
            logger.info(f"Carga masiva completada: {exitosos} exitosos, {errores} errores")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error en commit final: {e}")
            raise ValidationException({'database': ['Error guardando los datos']})
        
        return {
            'exitosos': exitosos,
            'errores': errores,
            'total_procesados': len(testigos_data),
            'municipio': municipio.nombre_completo,
            'detalles_errores': detalles_errores[:10],  # Solo los primeros 10 errores
            'testigos_creados': [t.to_dict() for t in testigos_creados[:5]]  # Solo los primeros 5 para muestra
        }
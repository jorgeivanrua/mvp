"""
Servicio para gestión de departamentos habilitados
"""
import csv
import os
from datetime import datetime
from backend.database import db
from backend.models.departamento_config import DepartamentoConfig
from backend.models.location import Location
from backend.models.user import User


class DepartamentoService:
    """Servicio para gestionar departamentos habilitados"""
    
    @staticmethod
    def listar_departamentos_disponibles():
        """Listar todos los departamentos disponibles en el CSV"""
        csv_file = 'data/divipola.csv'
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Archivo {csv_file} no encontrado")
        
        departamentos = {}
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dd = row['dd'].strip().zfill(2)
                depto_nombre = row['departamento'].strip().upper()
                
                if dd not in departamentos:
                    departamentos[dd] = {
                        'codigo': dd,
                        'nombre': depto_nombre,
                        'municipios': set(),
                        'total_registros': 0
                    }
                
                departamentos[dd]['municipios'].add(row['municipio'].strip())
                departamentos[dd]['total_registros'] += 1
        
        # Convertir a lista y agregar conteos
        resultado = []
        for codigo, info in departamentos.items():
            resultado.append({
                'departamento_codigo': codigo,
                'departamento_nombre': info['nombre'],
                'total_municipios': len(info['municipios']),
                'total_registros': info['total_registros']
            })
        
        return sorted(resultado, key=lambda x: x['departamento_nombre'])
    
    @staticmethod
    def habilitar_departamento(departamento_codigo, es_principal=False, auto_cargar=True):
        """
        Habilitar un departamento y cargar sus datos
        
        Args:
            departamento_codigo: Código del departamento (ej: '26' para Quindío)
            es_principal: Si debe ser el departamento principal
            auto_cargar: Si debe cargar automáticamente ubicaciones y usuarios
        """
        # Verificar que el departamento existe en el CSV
        departamentos_disponibles = DepartamentoService.listar_departamentos_disponibles()
        depto_info = next((d for d in departamentos_disponibles if d['departamento_codigo'] == departamento_codigo), None)
        
        if not depto_info:
            raise ValueError(f"Departamento con código {departamento_codigo} no encontrado en DIVIPOLA")
        
        # Buscar o crear configuración
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo=departamento_codigo
        ).first()
        
        if not config:
            config = DepartamentoConfig(
                departamento_codigo=departamento_codigo,
                departamento_nombre=depto_info['departamento_nombre'],
                auto_crear_usuarios=auto_cargar,
                auto_cargar_ubicaciones=auto_cargar
            )
            db.session.add(config)
        
        # Habilitar departamento
        if es_principal:
            config.marcar_como_principal()
        else:
            config.habilitar()
        
        db.session.commit()
        
        # Cargar datos si está habilitado
        if auto_cargar:
            resultado_carga = DepartamentoService.cargar_datos_departamento(departamento_codigo)
            config.ultima_carga_at = datetime.utcnow()
            config.actualizar_estadisticas()
            db.session.commit()
            
            return {
                'config': config.to_dict(),
                'carga': resultado_carga
            }
        
        return {'config': config.to_dict()}
    
    @staticmethod
    def deshabilitar_departamento(departamento_codigo, desactivar_usuarios=True):
        """
        Deshabilitar un departamento
        
        Args:
            departamento_codigo: Código del departamento
            desactivar_usuarios: Si debe desactivar usuarios (no eliminar)
        """
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo=departamento_codigo
        ).first()
        
        if not config:
            raise ValueError(f"Configuración de departamento {departamento_codigo} no encontrada")
        
        # Deshabilitar configuración
        config.deshabilitar()
        
        if desactivar_usuarios:
            # Desactivar ubicaciones (no eliminar)
            Location.query.filter_by(
                departamento_codigo=departamento_codigo
            ).update({'activo': False})
            
            # Desactivar usuarios del departamento (no eliminar)
            ubicaciones_ids = [loc.id for loc in Location.query.filter_by(
                departamento_codigo=departamento_codigo
            ).all()]
            
            if ubicaciones_ids:
                User.query.filter(
                    User.ubicacion_id.in_(ubicaciones_ids),
                    User.rol != 'super_admin'  # No tocar super admin
                ).update({'activo': False})
        
        db.session.commit()
        
        return config.to_dict()
    
    @staticmethod
    def cargar_datos_departamento(departamento_codigo):
        """Cargar ubicaciones y usuarios de un departamento específico"""
        csv_file = 'data/divipola.csv'
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Archivo {csv_file} no encontrado")
        
        # Leer datos del departamento
        departamento_rows = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['dd'].strip().zfill(2) == departamento_codigo:
                    departamento_rows.append(row)
        
        if not departamento_rows:
            raise ValueError(f"No se encontraron datos para el departamento {departamento_codigo}")
        
        # Cargar ubicaciones
        resultado_ubicaciones = DepartamentoService._cargar_ubicaciones_departamento(departamento_rows)
        
        # Cargar usuarios
        resultado_usuarios = DepartamentoService._cargar_usuarios_departamento(departamento_codigo)
        
        return {
            'departamento_codigo': departamento_codigo,
            'departamento_nombre': departamento_rows[0]['departamento'].strip().upper(),
            'ubicaciones': resultado_ubicaciones,
            'usuarios': resultado_usuarios,
            'total_registros_procesados': len(departamento_rows)
        }
    
    @staticmethod
    def _cargar_ubicaciones_departamento(departamento_rows):
        """Cargar ubicaciones jerárquicas de un departamento"""
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
        mesas_creadas = 0
        
        for row in departamento_rows:
            dd = row['dd'].strip().zfill(2)
            mm = row['mm'].strip().zfill(2)
            zz = row['zz'].strip().zfill(2)
            pp = row['pp'].strip().zfill(2)
            mesa_num = row['mesa'].strip().zfill(2)
            
            depto_nombre = row['departamento'].strip().upper()
            muni_nombre = row['municipio'].strip()
            puesto_nombre = row['puesto'].strip()
            mesa_nombre = row['mesa_nombre'].strip()
            
            # Códigos completos
            depto_codigo = dd
            muni_codigo = f"{dd}{mm}"
            zona_codigo = f"{dd}{mm}{zz}"
            puesto_codigo = f"{dd}{mm}{zz}{pp}"
            mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa_num}"
            
            # 1. Crear/obtener departamento
            if depto_codigo not in departamentos:
                dept_existente = Location.query.filter_by(
                    departamento_codigo=depto_codigo,
                    tipo='departamento'
                ).first()
                
                if dept_existente:
                    # Reactivar si estaba deshabilitado
                    dept_existente.activo = True
                    departamentos[depto_codigo] = dept_existente.id
                else:
                    dept = Location(
                        departamento_codigo=depto_codigo,
                        departamento_nombre=depto_nombre,
                        nombre_completo=depto_nombre,
                        tipo='departamento',
                        activo=True
                    )
                    db.session.add(dept)
                    db.session.flush()
                    departamentos[depto_codigo] = dept.id
            
            depto_id = departamentos[depto_codigo]
            
            # 2. Crear/obtener municipio
            if muni_codigo not in municipios:
                muni_existente = Location.query.filter_by(
                    municipio_codigo=muni_codigo,
                    tipo='municipio'
                ).first()
                
                if muni_existente:
                    muni_existente.activo = True
                    municipios[muni_codigo] = muni_existente.id
                else:
                    nombre_completo = f"{depto_nombre} - {muni_nombre}"
                    muni = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        departamento_nombre=depto_nombre,
                        municipio_nombre=muni_nombre,
                        nombre_completo=nombre_completo,
                        tipo='municipio',
                        parent_id=depto_id,
                        activo=True
                    )
                    db.session.add(muni)
                    db.session.flush()
                    municipios[muni_codigo] = muni.id
            
            muni_id = municipios[muni_codigo]
            
            # 3. Crear/obtener zona
            if zona_codigo not in zonas:
                zona_existente = Location.query.filter_by(
                    zona_codigo=zona_codigo,
                    tipo='zona'
                ).first()
                
                if zona_existente:
                    zona_existente.activo = True
                    zonas[zona_codigo] = zona_existente.id
                else:
                    zona_nombre = f"Zona {zz}"
                    nombre_completo = f"{depto_nombre} - {muni_nombre} - {zona_nombre}"
                    zona = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        departamento_nombre=depto_nombre,
                        municipio_nombre=muni_nombre,
                        nombre_completo=nombre_completo,
                        tipo='zona',
                        parent_id=muni_id,
                        activo=True
                    )
                    db.session.add(zona)
                    db.session.flush()
                    zonas[zona_codigo] = zona.id
            
            zona_id = zonas[zona_codigo]
            
            # 4. Crear/obtener puesto
            if puesto_codigo not in puestos:
                puesto_existente = Location.query.filter_by(
                    puesto_codigo=puesto_codigo,
                    tipo='puesto'
                ).first()
                
                if puesto_existente:
                    puesto_existente.activo = True
                    puestos[puesto_codigo] = puesto_existente.id
                else:
                    comuna = row.get('comuna', '').strip()
                    direccion = row.get('direccion', '').strip()
                    latitud = row.get('LATITUD', '').strip()
                    longitud = row.get('LONGITUD', '').strip()
                    
                    nombre_completo = f"{depto_nombre} - {muni_nombre} - {puesto_nombre}"
                    
                    puesto = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        puesto_codigo=puesto_codigo,
                        departamento_nombre=depto_nombre,
                        municipio_nombre=muni_nombre,
                        puesto_nombre=puesto_nombre,
                        nombre_completo=nombre_completo,
                        tipo='puesto',
                        parent_id=zona_id,
                        direccion=direccion or None,
                        latitud=float(latitud) if latitud else None,
                        longitud=float(longitud) if longitud else None,
                        comuna=comuna or None,
                        activo=True
                    )
                    db.session.add(puesto)
                    db.session.flush()
                    puestos[puesto_codigo] = puesto.id
            
            puesto_id = puestos[puesto_codigo]
            
            # 5. Crear/obtener mesa
            mesa_existente = Location.query.filter_by(
                mesa_codigo=mesa_codigo,
                tipo='mesa'
            ).first()
            
            if mesa_existente:
                mesa_existente.activo = True
            else:
                mujeres = int(row.get('mujeres_mesa', 0) or 0)
                hombres = int(row.get('hombres_mesa', 0) or 0)
                total_votantes = int(row.get('total_mesa', 0) or 0)
                
                nombre_completo = f"{depto_nombre} - {muni_nombre} - {mesa_nombre}"
                
                mesa = Location(
                    departamento_codigo=depto_codigo,
                    municipio_codigo=muni_codigo,
                    zona_codigo=zona_codigo,
                    puesto_codigo=puesto_codigo,
                    mesa_codigo=mesa_codigo,
                    departamento_nombre=depto_nombre,
                    municipio_nombre=muni_nombre,
                    puesto_nombre=puesto_nombre,
                    mesa_nombre=mesa_nombre,
                    nombre_completo=nombre_completo,
                    tipo='mesa',
                    parent_id=puesto_id,
                    total_votantes_registrados=total_votantes,
                    mujeres=mujeres,
                    hombres=hombres,
                    activo=True
                )
                db.session.add(mesa)
                mesas_creadas += 1
        
        db.session.commit()
        
        return {
            'departamentos': len(departamentos),
            'municipios': len(municipios),
            'zonas': len(zonas),
            'puestos': len(puestos),
            'mesas_creadas': mesas_creadas
        }
    
    @staticmethod
    def _cargar_usuarios_departamento(departamento_codigo):
        """Crear usuarios para un departamento"""
        # Obtener ubicaciones del departamento
        departamento = Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            tipo='departamento',
            activo=True
        ).first()
        
        if not departamento:
            raise ValueError(f"Departamento {departamento_codigo} no encontrado")
        
        municipios = Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            tipo='municipio',
            activo=True
        ).all()
        
        puestos = Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            tipo='puesto',
            activo=True
        ).all()
        
        mesas = Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            tipo='mesa',
            activo=True
        ).all()
        
        usuarios_creados = {
            'coordinador_departamental': 0,
            'coordinador_municipal': 0,
            'coordinador_puesto': 0,
            'testigo_electoral': 0
        }
        
        # 1. Coordinador Departamental
        coord_depto = User.query.filter_by(
            rol='coordinador_departamental',
            ubicacion_id=departamento.id
        ).first()
        
        if not coord_depto:
            coord_depto = User(
                nombre=departamento.departamento_nombre,
                rol='coordinador_departamental',
                ubicacion_id=departamento.id,
                activo=True,
                es_usuario_basico=False
            )
            coord_depto.set_password('test123')
            db.session.add(coord_depto)
            usuarios_creados['coordinador_departamental'] = 1
        else:
            coord_depto.activo = True
        
        # 2. Coordinadores Municipales
        for municipio in municipios:
            coord_muni = User.query.filter_by(
                rol='coordinador_municipal',
                ubicacion_id=municipio.id
            ).first()
            
            if not coord_muni:
                nombre_usuario = municipio.municipio_nombre.upper().replace(' ', '_')
                coord_muni = User(
                    nombre=nombre_usuario,
                    rol='coordinador_municipal',
                    ubicacion_id=municipio.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_muni.set_password('test123')
                db.session.add(coord_muni)
                usuarios_creados['coordinador_municipal'] += 1
            else:
                coord_muni.activo = True
        
        # 3. Coordinadores de Puesto
        for puesto in puestos:
            coord_puesto = User.query.filter_by(
                rol='coordinador_puesto',
                ubicacion_id=puesto.id
            ).first()
            
            if not coord_puesto:
                municipio_nombre = puesto.municipio_nombre.upper().replace(' ', '_')
                nombre_usuario = f"{municipio_nombre}_P{puesto.puesto_codigo[-2:]}"
                coord_puesto = User(
                    nombre=nombre_usuario,
                    rol='coordinador_puesto',
                    ubicacion_id=puesto.id,
                    activo=True,
                    es_usuario_basico=False
                )
                coord_puesto.set_password('test123')
                db.session.add(coord_puesto)
                usuarios_creados['coordinador_puesto'] += 1
            else:
                coord_puesto.activo = True
        
        # 4. Testigos Electorales
        for mesa in mesas:
            testigo = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=mesa.id
            ).first()
            
            if not testigo:
                cedula = f"{mesa.mesa_codigo}001"
                nombre_usuario = f"testigo_{cedula}"
                testigo = User(
                    nombre=nombre_usuario,
                    cedula=cedula,
                    rol='testigo_electoral',
                    ubicacion_id=mesa.id,
                    activo=True,
                    es_usuario_basico=False
                )
                testigo.set_password('test123')
                db.session.add(testigo)
                usuarios_creados['testigo_electoral'] += 1
            else:
                testigo.activo = True
        
        db.session.commit()
        
        return usuarios_creados
    
    @staticmethod
    def obtener_estado_departamentos():
        """Obtener estado de todos los departamentos configurados"""
        configs = DepartamentoConfig.query.all()
        
        # Actualizar estadísticas
        for config in configs:
            config.actualizar_estadisticas()
        
        db.session.commit()
        
        return [config.to_dict() for config in configs]
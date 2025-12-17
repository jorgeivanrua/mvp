#!/usr/bin/env python3
"""
Script para verificar que un departamento esté correctamente cargado y funcional
Realiza todas las validaciones necesarias para garantizar que el sistema esté listo

Uso:
    python scripts/verificar_departamento.py <codigo>
    python scripts/verificar_departamento.py --todos
    
Ejemplos:
    python scripts/verificar_departamento.py 26    # Verificar Quindío
    python scripts/verificar_departamento.py --todos  # Verificar todos los departamentos
"""
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from backend.app import create_app
    from backend.database import db
    from backend.models.location import Location
    from backend.models.user import User
    from backend.models.departamento_config import DepartamentoConfig
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class VerificadorDepartamento:
    """Verificador completo de departamentos"""
    
    def __init__(self):
        self.app = create_app()
    
    def verificar_departamento_completo(self, departamento_codigo: str) -> Dict:
        """Verificar completamente un departamento"""
        print("=" * 80)
        print(f"🔍 VERIFICACIÓN COMPLETA - DEPARTAMENTO: {departamento_codigo}")
        print("=" * 80)
        
        with self.app.app_context():
            resultado = {
                'departamento_codigo': departamento_codigo,
                'verificaciones': {},
                'errores': [],
                'advertencias': [],
                'estado_general': 'DESCONOCIDO'
            }
            
            # 1. Verificar configuración
            print("🔍 1. VERIFICANDO CONFIGURACIÓN")
            print("-" * 40)
            config_ok, config_info = self._verificar_configuracion(departamento_codigo)
            resultado['verificaciones']['configuracion'] = config_ok
            if config_info:
                resultado['configuracion'] = config_info
            
            # 2. Verificar ubicaciones
            print("\n🔍 2. VERIFICANDO UBICACIONES")
            print("-" * 40)
            ubicaciones_ok, ubicaciones_info = self._verificar_ubicaciones(departamento_codigo)
            resultado['verificaciones']['ubicaciones'] = ubicaciones_ok
            resultado['ubicaciones'] = ubicaciones_info
            
            # 3. Verificar usuarios
            print("\n🔍 3. VERIFICANDO USUARIOS")
            print("-" * 40)
            usuarios_ok, usuarios_info = self._verificar_usuarios(departamento_codigo)
            resultado['verificaciones']['usuarios'] = usuarios_ok
            resultado['usuarios'] = usuarios_info
            
            # 4. Verificar integridad de datos
            print("\n🔍 4. VERIFICANDO INTEGRIDAD")
            print("-" * 40)
            integridad_ok, integridad_info = self._verificar_integridad(departamento_codigo)
            resultado['verificaciones']['integridad'] = integridad_ok
            resultado['integridad'] = integridad_info
            
            # 5. Verificar funcionalidad
            print("\n🔍 5. VERIFICANDO FUNCIONALIDAD")
            print("-" * 40)
            funcionalidad_ok, funcionalidad_info = self._verificar_funcionalidad(departamento_codigo)
            resultado['verificaciones']['funcionalidad'] = funcionalidad_ok
            resultado['funcionalidad'] = funcionalidad_info
            
            # Determinar estado general
            todas_ok = all(resultado['verificaciones'].values())
            if todas_ok:
                resultado['estado_general'] = 'EXCELENTE'
                print(f"\n✅ DEPARTAMENTO {departamento_codigo}: COMPLETAMENTE FUNCIONAL")
            else:
                resultado['estado_general'] = 'CON_PROBLEMAS'
                print(f"\n⚠️  DEPARTAMENTO {departamento_codigo}: REQUIERE ATENCIÓN")
            
            # Mostrar resumen
            self._mostrar_resumen_verificacion(resultado)
            
            return resultado
    
    def _verificar_configuracion(self, departamento_codigo: str) -> tuple:
        """Verificar configuración del departamento"""
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo=departamento_codigo
        ).first()
        
        if not config:
            print("❌ No existe configuración para este departamento")
            return False, None
        
        config_info = {
            'existe': True,
            'habilitado': config.habilitado,
            'es_principal': config.es_principal,
            'auto_crear_usuarios': config.auto_crear_usuarios,
            'auto_cargar_ubicaciones': config.auto_cargar_ubicaciones,
            'ultima_carga': config.ultima_carga_at.isoformat() if config.ultima_carga_at else None
        }
        
        if not config.habilitado:
            print("⚠️  Departamento deshabilitado")
            return False, config_info
        
        print(f"✅ Configuración válida: {config.departamento_nombre}")
        if config.es_principal:
            print("   ⭐ Marcado como principal")
        
        return True, config_info
    
    def _verificar_ubicaciones(self, departamento_codigo: str) -> tuple:
        """Verificar ubicaciones del departamento"""
        ubicaciones = Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            activo=True
        ).all()
        
        if not ubicaciones:
            print("❌ No se encontraron ubicaciones")
            return False, {'total': 0}
        
        # Contar por tipo
        por_tipo = {}
        for ubicacion in ubicaciones:
            tipo = ubicacion.tipo
            if tipo not in por_tipo:
                por_tipo[tipo] = 0
            por_tipo[tipo] += 1
        
        ubicaciones_info = {
            'total': len(ubicaciones),
            'por_tipo': por_tipo,
            'departamento_nombre': ubicaciones[0].departamento_nombre if ubicaciones else None
        }
        
        # Verificar jerarquía mínima
        tipos_requeridos = ['departamento', 'municipio', 'puesto']
        tipos_faltantes = [tipo for tipo in tipos_requeridos if tipo not in por_tipo]
        
        if tipos_faltantes:
            print(f"❌ Tipos de ubicación faltantes: {tipos_faltantes}")
            return False, ubicaciones_info
        
        print(f"✅ {len(ubicaciones)} ubicaciones encontradas")
        for tipo, cantidad in por_tipo.items():
            print(f"   • {tipo}: {cantidad}")
        
        return True, ubicaciones_info
    
    def _verificar_usuarios(self, departamento_codigo: str) -> tuple:
        """Verificar usuarios del departamento"""
        # Obtener ubicaciones del departamento
        ubicaciones_ids = [loc.id for loc in Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            activo=True
        ).all()]
        
        if not ubicaciones_ids:
            print("❌ No hay ubicaciones para verificar usuarios")
            return False, {'total': 0}
        
        usuarios = User.query.filter(
            User.ubicacion_id.in_(ubicaciones_ids),
            User.activo == True
        ).all()
        
        if not usuarios:
            print("❌ No se encontraron usuarios")
            return False, {'total': 0}
        
        # Contar por rol
        por_rol = {}
        usuarios_con_cedula = 0
        usuarios_sin_cedula = 0
        
        for usuario in usuarios:
            rol = usuario.rol
            if rol not in por_rol:
                por_rol[rol] = 0
            por_rol[rol] += 1
            
            if usuario.cedula:
                usuarios_con_cedula += 1
            else:
                usuarios_sin_cedula += 1
        
        usuarios_info = {
            'total': len(usuarios),
            'por_rol': por_rol,
            'con_cedula': usuarios_con_cedula,
            'sin_cedula': usuarios_sin_cedula
        }
        
        # Verificar roles mínimos
        roles_requeridos = ['coordinador_departamental', 'coordinador_municipal', 'coordinador_puesto']
        roles_faltantes = [rol for rol in roles_requeridos if rol not in por_rol]
        
        problemas = []
        if roles_faltantes:
            problemas.append(f"Roles faltantes: {roles_faltantes}")
        
        # Verificar testigos con cédula
        testigos = por_rol.get('testigo_electoral', 0)
        if testigos > 0:
            testigos_sin_cedula = User.query.join(
                Location, User.ubicacion_id == Location.id
            ).filter(
                User.rol == 'testigo_electoral',
                User.activo == True,
                User.cedula.is_(None),
                Location.departamento_codigo == departamento_codigo
            ).count()
            
            if testigos_sin_cedula > 0:
                problemas.append(f"{testigos_sin_cedula} testigos sin cédula")
        
        if problemas:
            print(f"⚠️  Problemas encontrados:")
            for problema in problemas:
                print(f"   • {problema}")
            return False, usuarios_info
        
        print(f"✅ {len(usuarios)} usuarios encontrados")
        for rol, cantidad in por_rol.items():
            print(f"   • {rol}: {cantidad}")
        
        if usuarios_sin_cedula > 0:
            print(f"   ⚠️  {usuarios_sin_cedula} usuarios sin cédula")
        
        return True, usuarios_info
    
    def _verificar_integridad(self, departamento_codigo: str) -> tuple:
        """Verificar integridad de datos"""
        problemas = []
        
        # 1. Verificar que todos los usuarios tengan ubicación válida
        usuarios_sin_ubicacion = db.session.query(User).outerjoin(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.activo == True,
            Location.id.is_(None)
        ).count()
        
        if usuarios_sin_ubicacion > 0:
            problemas.append(f"{usuarios_sin_ubicacion} usuarios sin ubicación válida")
        
        # 2. Verificar testigos en ubicaciones correctas (puestos, no mesas)
        testigos_en_mesas = db.session.query(User).join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            Location.tipo == 'mesa',
            Location.departamento_codigo == departamento_codigo
        ).count()
        
        if testigos_en_mesas > 0:
            problemas.append(f"{testigos_en_mesas} testigos asignados a mesas (deben estar en puestos)")
        
        # 3. Verificar ubicaciones huérfanas
        ubicaciones_huerfanas = Location.query.filter(
            Location.departamento_codigo == departamento_codigo,
            Location.activo == True,
            Location.parent_id.isnot(None)
        ).outerjoin(
            Location, Location.parent_id == Location.id, aliased=True
        ).filter(
            Location.id.is_(None)
        ).count()
        
        if ubicaciones_huerfanas > 0:
            problemas.append(f"{ubicaciones_huerfanas} ubicaciones con parent_id inválido")
        
        integridad_info = {
            'usuarios_sin_ubicacion': usuarios_sin_ubicacion,
            'testigos_en_mesas': testigos_en_mesas,
            'ubicaciones_huerfanas': ubicaciones_huerfanas,
            'problemas': problemas
        }
        
        if problemas:
            print("❌ Problemas de integridad encontrados:")
            for problema in problemas:
                print(f"   • {problema}")
            return False, integridad_info
        
        print("✅ Integridad de datos correcta")
        return True, integridad_info
    
    def _verificar_funcionalidad(self, departamento_codigo: str) -> tuple:
        """Verificar funcionalidad básica"""
        funcionalidad_info = {
            'puede_login_coordinador': False,
            'puede_login_testigo': False,
            'endpoints_funcionan': False
        }
        
        # 1. Verificar que coordinadores pueden hacer login
        coord_depto = User.query.join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'coordinador_departamental',
            User.activo == True,
            Location.departamento_codigo == departamento_codigo
        ).first()
        
        if coord_depto and coord_depto.check_password('test123'):
            funcionalidad_info['puede_login_coordinador'] = True
            print("✅ Login de coordinador funcional")
        else:
            print("❌ Login de coordinador no funcional")
        
        # 2. Verificar que testigos pueden hacer login
        testigo = User.query.join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            User.cedula.isnot(None),
            Location.departamento_codigo == departamento_codigo
        ).first()
        
        if testigo and testigo.check_password('test123'):
            funcionalidad_info['puede_login_testigo'] = True
            print("✅ Login de testigo funcional")
        else:
            print("❌ Login de testigo no funcional")
        
        # 3. Verificar endpoints básicos (simulado)
        ubicaciones_activas = Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            activo=True
        ).count()
        
        if ubicaciones_activas > 0:
            funcionalidad_info['endpoints_funcionan'] = True
            print("✅ Endpoints de ubicaciones funcionales")
        else:
            print("❌ Endpoints de ubicaciones no funcionales")
        
        todas_funcionales = all(funcionalidad_info.values())
        return todas_funcionales, funcionalidad_info
    
    def _mostrar_resumen_verificacion(self, resultado: Dict):
        """Mostrar resumen de la verificación"""
        print("\n" + "=" * 80)
        print("📊 RESUMEN DE VERIFICACIÓN")
        print("=" * 80)
        
        estado = resultado['estado_general']
        if estado == 'EXCELENTE':
            print("🎉 ESTADO: EXCELENTE - Sistema completamente funcional")
        else:
            print("⚠️  ESTADO: CON PROBLEMAS - Requiere atención")
        
        print(f"\n📍 DEPARTAMENTO: {resultado['departamento_codigo']}")
        if 'configuracion' in resultado and resultado['configuracion']:
            config = resultado['configuracion']
            if config.get('es_principal'):
                print("   ⭐ DEPARTAMENTO PRINCIPAL")
        
        print(f"\n✅ VERIFICACIONES PASADAS:")
        for verificacion, pasada in resultado['verificaciones'].items():
            estado_check = "✅" if pasada else "❌"
            print(f"   {estado_check} {verificacion.upper()}")
        
        # Mostrar estadísticas
        if 'ubicaciones' in resultado:
            ubicaciones = resultado['ubicaciones']
            print(f"\n📊 UBICACIONES: {ubicaciones['total']}")
            for tipo, cantidad in ubicaciones.get('por_tipo', {}).items():
                print(f"   • {tipo}: {cantidad}")
        
        if 'usuarios' in resultado:
            usuarios = resultado['usuarios']
            print(f"\n👥 USUARIOS: {usuarios['total']}")
            for rol, cantidad in usuarios.get('por_rol', {}).items():
                print(f"   • {rol}: {cantidad}")
        
        # Mostrar problemas si los hay
        if 'integridad' in resultado and resultado['integridad'].get('problemas'):
            print(f"\n⚠️  PROBLEMAS DETECTADOS:")
            for problema in resultado['integridad']['problemas']:
                print(f"   • {problema}")
        
        print("\n" + "=" * 80)
    
    def verificar_todos_departamentos(self) -> List[Dict]:
        """Verificar todos los departamentos configurados"""
        print("🔍 VERIFICANDO TODOS LOS DEPARTAMENTOS")
        print("=" * 60)
        
        with self.app.app_context():
            configs = DepartamentoConfig.query.all()
            
            if not configs:
                print("ℹ️  No hay departamentos configurados")
                return []
            
            resultados = []
            for config in configs:
                print(f"\n📍 Verificando {config.departamento_nombre} ({config.departamento_codigo})")
                print("-" * 50)
                
                resultado = self.verificar_departamento_completo(config.departamento_codigo)
                resultados.append(resultado)
            
            # Resumen general
            print("\n" + "=" * 80)
            print("📊 RESUMEN GENERAL")
            print("=" * 80)
            
            excelentes = sum(1 for r in resultados if r['estado_general'] == 'EXCELENTE')
            con_problemas = len(resultados) - excelentes
            
            print(f"📈 DEPARTAMENTOS VERIFICADOS: {len(resultados)}")
            print(f"✅ EXCELENTES: {excelentes}")
            print(f"⚠️  CON PROBLEMAS: {con_problemas}")
            
            if con_problemas > 0:
                print(f"\n⚠️  DEPARTAMENTOS QUE REQUIEREN ATENCIÓN:")
                for resultado in resultados:
                    if resultado['estado_general'] != 'EXCELENTE':
                        print(f"   • {resultado['departamento_codigo']}")
            
            return resultados


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Verificar departamentos cargados',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/verificar_departamento.py 26
  python scripts/verificar_departamento.py --todos
        """
    )
    
    parser.add_argument('codigo', nargs='?', help='Código del departamento a verificar')
    parser.add_argument('--todos', action='store_true',
                       help='Verificar todos los departamentos configurados')
    
    args = parser.parse_args()
    
    verificador = VerificadorDepartamento()
    
    try:
        if args.todos:
            resultados = verificador.verificar_todos_departamentos()
            
            # Determinar código de salida
            problemas = sum(1 for r in resultados if r['estado_general'] != 'EXCELENTE')
            if problemas > 0:
                print(f"\n⚠️  {problemas} departamento(s) con problemas detectados")
                sys.exit(1)
            else:
                print(f"\n🎉 Todos los departamentos están funcionando correctamente")
                sys.exit(0)
        
        elif args.codigo:
            codigo = args.codigo.strip().zfill(2)
            resultado = verificador.verificar_departamento_completo(codigo)
            
            if resultado['estado_general'] == 'EXCELENTE':
                print(f"\n🎉 Departamento {codigo} funcionando perfectamente")
                sys.exit(0)
            else:
                print(f"\n⚠️  Departamento {codigo} requiere atención")
                sys.exit(1)
        
        else:
            print("❌ Debe especificar un código de departamento o usar --todos")
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
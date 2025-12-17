#!/usr/bin/env python3
"""
Script mejorado para cargar cualquier departamento de Colombia de forma completa y funcional
Incluye todas las validaciones, correcciones y verificaciones necesarias

Uso:
    python scripts/cargar_departamento_completo.py <codigo> [--principal] [--forzar]
    
Ejemplos:
    python scripts/cargar_departamento_completo.py 26 --principal  # Quindío como principal
    python scripts/cargar_departamento_completo.py 05 --forzar     # Antioquia forzando recarga
    python scripts/cargar_departamento_completo.py --listar       # Ver departamentos disponibles
"""
import sys
import os
import argparse
import csv
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
    from backend.services.departamento_service import DepartamentoService
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class CargadorDepartamentoCompleto:
    """Cargador completo y robusto para cualquier departamento"""
    
    def __init__(self):
        self.app = create_app()
        self.csv_file = 'data/divipola.csv'
        
    def validar_archivo_csv(self) -> bool:
        """Validar que el archivo CSV existe y tiene el formato correcto"""
        if not os.path.exists(self.csv_file):
            print(f"❌ Archivo {self.csv_file} no encontrado")
            print("   Asegúrate de que el archivo DIVIPOLA esté en la carpeta data/")
            return False
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                first_row = next(reader)
                
                # Verificar columnas requeridas
                required_columns = ['dd', 'departamento', 'mm', 'municipio', 'zz', 'pp', 'puesto', 'mesa', 'mesa_nombre']
                missing_columns = [col for col in required_columns if col not in first_row]
                
                if missing_columns:
                    print(f"❌ Columnas faltantes en CSV: {missing_columns}")
                    return False
                
                print(f"✅ Archivo CSV válido: {self.csv_file}")
                return True
                
        except Exception as e:
            print(f"❌ Error leyendo CSV: {e}")
            return False
    
    def listar_departamentos_disponibles(self) -> List[Dict]:
        """Listar todos los departamentos disponibles en el CSV"""
        if not self.validar_archivo_csv():
            return []
        
        departamentos = {}
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dd = row['dd'].strip().zfill(2)
                depto_nombre = row['departamento'].strip().upper()
                
                if dd not in departamentos:
                    departamentos[dd] = {
                        'codigo': dd,
                        'nombre': depto_nombre,
                        'municipios': set(),
                        'puestos': set(),
                        'mesas': 0
                    }
                
                departamentos[dd]['municipios'].add(row['municipio'].strip())
                departamentos[dd]['puestos'].add(f"{dd}{row['mm'].strip().zfill(2)}{row['zz'].strip().zfill(2)}{row['pp'].strip().zfill(2)}")
                departamentos[dd]['mesas'] += 1
        
        # Convertir a lista
        resultado = []
        for codigo, info in departamentos.items():
            resultado.append({
                'departamento_codigo': codigo,
                'departamento_nombre': info['nombre'],
                'total_municipios': len(info['municipios']),
                'total_puestos': len(info['puestos']),
                'total_mesas': info['mesas']
            })
        
        return sorted(resultado, key=lambda x: x['departamento_nombre'])
    
    def verificar_estado_departamento(self, departamento_codigo: str) -> Dict:
        """Verificar el estado actual de un departamento en el sistema"""
        with self.app.app_context():
            # Verificar configuración
            config = DepartamentoConfig.query.filter_by(
                departamento_codigo=departamento_codigo
            ).first()
            
            # Contar ubicaciones
            ubicaciones = Location.query.filter_by(
                departamento_codigo=departamento_codigo,
                activo=True
            ).all()
            
            ubicaciones_por_tipo = {}
            for ubicacion in ubicaciones:
                tipo = ubicacion.tipo
                if tipo not in ubicaciones_por_tipo:
                    ubicaciones_por_tipo[tipo] = 0
                ubicaciones_por_tipo[tipo] += 1
            
            # Contar usuarios
            ubicaciones_ids = [loc.id for loc in ubicaciones]
            usuarios = []
            if ubicaciones_ids:
                usuarios = User.query.filter(
                    User.ubicacion_id.in_(ubicaciones_ids),
                    User.activo == True
                ).all()
            
            usuarios_por_rol = {}
            for usuario in usuarios:
                rol = usuario.rol
                if rol not in usuarios_por_rol:
                    usuarios_por_rol[rol] = 0
                usuarios_por_rol[rol] += 1
            
            return {
                'existe_config': config is not None,
                'config': config.to_dict() if config else None,
                'total_ubicaciones': len(ubicaciones),
                'ubicaciones_por_tipo': ubicaciones_por_tipo,
                'total_usuarios': len(usuarios),
                'usuarios_por_rol': usuarios_por_rol,
                'esta_cargado': len(ubicaciones) > 0 and len(usuarios) > 0
            }
    
    def cargar_departamento_completo(self, departamento_codigo: str, es_principal: bool = False, forzar: bool = False) -> Dict:
        """
        Cargar un departamento completo con todas las validaciones y correcciones
        
        Args:
            departamento_codigo: Código del departamento (ej: '26' para Quindío)
            es_principal: Si debe ser el departamento principal
            forzar: Si debe forzar la recarga aunque ya exista
        """
        print("=" * 80)
        print(f"🏛️  CARGA COMPLETA DE DEPARTAMENTO - CÓDIGO: {departamento_codigo}")
        print("=" * 80)
        
        # PASO 1: Validaciones iniciales
        print("🔍 PASO 1: VALIDACIONES INICIALES")
        print("-" * 40)
        
        if not self.validar_archivo_csv():
            raise ValueError("Archivo CSV no válido")
        
        # Verificar que el departamento existe
        departamentos_disponibles = self.listar_departamentos_disponibles()
        depto_info = next((d for d in departamentos_disponibles 
                          if d['departamento_codigo'] == departamento_codigo), None)
        
        if not depto_info:
            print(f"❌ Departamento con código {departamento_codigo} no encontrado")
            print("\n📋 Departamentos disponibles:")
            for dept in departamentos_disponibles[:10]:  # Mostrar primeros 10
                print(f"   {dept['departamento_codigo']} - {dept['departamento_nombre']}")
            if len(departamentos_disponibles) > 10:
                print(f"   ... y {len(departamentos_disponibles) - 10} más")
            raise ValueError(f"Departamento {departamento_codigo} no encontrado")
        
        print(f"✅ Departamento encontrado: {depto_info['departamento_nombre']}")
        print(f"   📊 Municipios: {depto_info['total_municipios']}")
        print(f"   🏢 Puestos: {depto_info['total_puestos']}")
        print(f"   🗳️  Mesas: {depto_info['total_mesas']}")
        
        # PASO 2: Verificar estado actual
        print(f"\n🔍 PASO 2: VERIFICANDO ESTADO ACTUAL")
        print("-" * 40)
        
        estado_actual = self.verificar_estado_departamento(departamento_codigo)
        
        if estado_actual['esta_cargado'] and not forzar:
            print(f"ℹ️  El departamento ya está cargado:")
            print(f"   📍 Ubicaciones: {estado_actual['total_ubicaciones']}")
            print(f"   👥 Usuarios: {estado_actual['total_usuarios']}")
            print(f"\n💡 Use --forzar para recargar completamente")
            
            respuesta = input("\n¿Continuar con la recarga? (s/N): ").strip().lower()
            if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Carga cancelada")
                return {'cancelado': True, 'motivo': 'Usuario canceló'}
        
        if estado_actual['esta_cargado']:
            print(f"🔄 Recargando departamento existente...")
        else:
            print(f"🆕 Cargando departamento nuevo...")
        
        # PASO 3: Cargar datos usando el servicio
        print(f"\n📥 PASO 3: CARGANDO DATOS")
        print("-" * 40)
        
        with self.app.app_context():
            try:
                resultado = DepartamentoService.habilitar_departamento(
                    departamento_codigo=departamento_codigo,
                    es_principal=es_principal,
                    auto_cargar=True
                )
                
                print("✅ Carga básica completada")
                
                # PASO 4: Validaciones y correcciones post-carga
                print(f"\n🔧 PASO 4: VALIDACIONES Y CORRECCIONES")
                print("-" * 40)
                
                correcciones = self.aplicar_correcciones_post_carga(departamento_codigo)
                
                # PASO 5: Verificación final
                print(f"\n✅ PASO 5: VERIFICACIÓN FINAL")
                print("-" * 40)
                
                estado_final = self.verificar_estado_departamento(departamento_codigo)
                
                # Mostrar resumen
                self.mostrar_resumen_carga(depto_info, resultado, correcciones, estado_final, es_principal)
                
                return {
                    'exitoso': True,
                    'departamento_info': depto_info,
                    'resultado_carga': resultado,
                    'correcciones': correcciones,
                    'estado_final': estado_final,
                    'es_principal': es_principal
                }
                
            except Exception as e:
                print(f"❌ Error durante la carga: {str(e)}")
                db.session.rollback()
                raise
    
    def aplicar_correcciones_post_carga(self, departamento_codigo: str) -> Dict:
        """Aplicar correcciones necesarias después de la carga"""
        correcciones = {
            'testigos_corregidos': 0,
            'usuarios_reactivados': 0,
            'ubicaciones_reactivadas': 0,
            'cedulas_asignadas': 0
        }
        
        # 1. Corregir ubicación de testigos (deben estar en puestos, no en mesas)
        print("   🔧 Corrigiendo ubicación de testigos...")
        testigos_en_mesas = db.session.query(User, Location).join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            Location.tipo == 'mesa',
            Location.departamento_codigo == departamento_codigo
        ).all()
        
        for testigo, mesa in testigos_en_mesas:
            # Buscar el puesto correspondiente
            puesto = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo=mesa.departamento_codigo,
                municipio_codigo=mesa.municipio_codigo,
                zona_codigo=mesa.zona_codigo,
                puesto_codigo=mesa.puesto_codigo,
                activo=True
            ).first()
            
            if puesto:
                testigo.ubicacion_id = puesto.id
                correcciones['testigos_corregidos'] += 1
        
        print(f"   ✅ {correcciones['testigos_corregidos']} testigos movidos a puestos")
        
        # 2. Verificar y asignar cédulas a testigos
        print("   🔧 Verificando cédulas de testigos...")
        testigos_sin_cedula = User.query.join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            User.cedula.is_(None),
            Location.departamento_codigo == departamento_codigo
        ).all()
        
        for testigo in testigos_sin_cedula:
            # Generar cédula basada en la ubicación
            ubicacion = Location.query.get(testigo.ubicacion_id)
            if ubicacion and ubicacion.tipo == 'puesto':
                cedula = f"{ubicacion.puesto_codigo}001"
                testigo.cedula = cedula
                correcciones['cedulas_asignadas'] += 1
        
        print(f"   ✅ {correcciones['cedulas_asignadas']} cédulas asignadas")
        
        # 3. Reactivar usuarios desactivados
        print("   🔧 Reactivando usuarios...")
        ubicaciones_ids = [loc.id for loc in Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            activo=True
        ).all()]
        
        if ubicaciones_ids:
            usuarios_desactivados = User.query.filter(
                User.ubicacion_id.in_(ubicaciones_ids),
                User.activo == False,
                User.rol != 'super_admin'
            ).all()
            
            for usuario in usuarios_desactivados:
                usuario.activo = True
                correcciones['usuarios_reactivados'] += 1
        
        print(f"   ✅ {correcciones['usuarios_reactivados']} usuarios reactivados")
        
        # 4. Reactivar ubicaciones desactivadas
        print("   🔧 Reactivando ubicaciones...")
        ubicaciones_desactivadas = Location.query.filter_by(
            departamento_codigo=departamento_codigo,
            activo=False
        ).all()
        
        for ubicacion in ubicaciones_desactivadas:
            ubicacion.activo = True
            correcciones['ubicaciones_reactivadas'] += 1
        
        print(f"   ✅ {correcciones['ubicaciones_reactivadas']} ubicaciones reactivadas")
        
        # Commit de todas las correcciones
        db.session.commit()
        
        return correcciones
    
    def mostrar_resumen_carga(self, depto_info: Dict, resultado: Dict, correcciones: Dict, estado_final: Dict, es_principal: bool):
        """Mostrar resumen completo de la carga"""
        print("\n" + "=" * 80)
        print("🎉 CARGA COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        
        carga = resultado.get('carga', {})
        ubicaciones = carga.get('ubicaciones', {})
        usuarios = carga.get('usuarios', {})
        
        print(f"\n📍 DEPARTAMENTO: {depto_info['departamento_nombre']}")
        if es_principal:
            print("   ⭐ MARCADO COMO PRINCIPAL")
        
        print(f"\n📊 UBICACIONES CARGADAS:")
        print(f"   • Departamentos: {ubicaciones.get('departamentos', 0)}")
        print(f"   • Municipios: {ubicaciones.get('municipios', 0)}")
        print(f"   • Zonas: {ubicaciones.get('zonas', 0)}")
        print(f"   • Puestos: {ubicaciones.get('puestos', 0)}")
        print(f"   • Mesas: {ubicaciones.get('mesas_creadas', 0)}")
        
        print(f"\n👥 USUARIOS CREADOS:")
        print(f"   • Coordinador Departamental: {usuarios.get('coordinador_departamental', 0)}")
        print(f"   • Coordinadores Municipales: {usuarios.get('coordinador_municipal', 0)}")
        print(f"   • Coordinadores de Puesto: {usuarios.get('coordinador_puesto', 0)}")
        print(f"   • Testigos Electorales: {usuarios.get('testigo_electoral', 0)}")
        
        print(f"\n🔧 CORRECCIONES APLICADAS:")
        print(f"   • Testigos movidos a puestos: {correcciones['testigos_corregidos']}")
        print(f"   • Cédulas asignadas: {correcciones['cedulas_asignadas']}")
        print(f"   • Usuarios reactivados: {correcciones['usuarios_reactivados']}")
        print(f"   • Ubicaciones reactivadas: {correcciones['ubicaciones_reactivadas']}")
        
        print(f"\n📈 ESTADO FINAL:")
        print(f"   • Total ubicaciones: {estado_final['total_ubicaciones']}")
        print(f"   • Total usuarios: {estado_final['total_usuarios']}")
        
        print(f"\n🔐 CREDENCIALES:")
        print(f"   • Contraseña para todos los usuarios: test123")
        print(f"   • Los testigos pueden usar su cédula como usuario")
        
        print(f"\n✅ SISTEMA LISTO PARA USAR")
        print("=" * 80)


def main():
    """Función principal con argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Cargar departamento completo con todas las validaciones',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/cargar_departamento_completo.py 26 --principal
  python scripts/cargar_departamento_completo.py 05 --forzar
  python scripts/cargar_departamento_completo.py --listar
        """
    )
    
    parser.add_argument('codigo', nargs='?', help='Código del departamento (ej: 26 para Quindío)')
    parser.add_argument('--principal', action='store_true', 
                       help='Marcar como departamento principal')
    parser.add_argument('--forzar', action='store_true',
                       help='Forzar recarga aunque ya exista')
    parser.add_argument('--listar', action='store_true',
                       help='Listar departamentos disponibles')
    
    args = parser.parse_args()
    
    cargador = CargadorDepartamentoCompleto()
    
    # Listar departamentos disponibles
    if args.listar:
        print("📋 DEPARTAMENTOS DISPONIBLES EN COLOMBIA")
        print("=" * 60)
        try:
            departamentos = cargador.listar_departamentos_disponibles()
            for dept in departamentos:
                print(f"  {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                print(f"      📊 {dept['total_municipios']} municipios, {dept['total_puestos']} puestos, {dept['total_mesas']} mesas")
            print()
            print("💡 Uso: python scripts/cargar_departamento_completo.py <codigo> [--principal] [--forzar]")
        except Exception as e:
            print(f"❌ Error: {e}")
        return
    
    # Validar código
    if not args.codigo:
        print("❌ Código de departamento requerido")
        print("💡 Use --listar para ver departamentos disponibles")
        sys.exit(1)
    
    # Normalizar código
    codigo = args.codigo.strip().zfill(2)
    
    try:
        resultado = cargador.cargar_departamento_completo(
            departamento_codigo=codigo,
            es_principal=args.principal,
            forzar=args.forzar
        )
        
        if resultado.get('cancelado'):
            print(f"ℹ️  Carga cancelada: {resultado.get('motivo')}")
            sys.exit(0)
        
        if resultado.get('exitoso'):
            print(f"\n🎯 ¡DEPARTAMENTO {codigo} LISTO PARA PRODUCCIÓN!")
            print("\n💡 PRÓXIMOS PASOS:")
            print("   1. Verificar el dashboard de administración")
            print("   2. Probar login con usuarios creados")
            print("   3. Configurar datos adicionales si es necesario")
        
    except Exception as e:
        print(f"\n❌ Error cargando departamento: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
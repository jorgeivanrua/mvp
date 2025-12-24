#!/usr/bin/env python3
"""
Test testigo login functionality
"""

import requests
import json

def test_testigo_login():
    """Test testigo login with cedula"""
    print("🧪 TESTING TESTIGO LOGIN")
    print("=" * 30)
    
    base_url = "http://localhost:5000"
    
    # Try to login with a testigo cedula
    testigo_cedula = "2601010101001"  # First testigo from the list
    
    # Test 1: Try location-based login (current system)
    print("📍 Test 1: Location-based login (current system)")
    login_data = {
        "rol": "testigo_electoral",
        "password": "test123"  # Default password
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success')}")
            if result.get('success'):
                print("   ✅ Location-based login works")
            else:
                print(f"   ❌ Error: {result.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error')}")
            except:
                print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print()
    
    # Test 2: Try cedula-based login (what we need)
    print("🆔 Test 2: Cedula-based login (what we need)")
    login_data_cedula = {
        "rol": "testigo_electoral",
        "cedula": testigo_cedula,
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data_cedula)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success')}")
            if result.get('success'):
                print("   ✅ Cedula-based login works")
                token = result.get('access_token')
                if token:
                    print(f"   Token: {token[:50]}...")
            else:
                print(f"   ❌ Error: {result.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error')}")
            except:
                print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print()
    
    # Test 3: Check if testigo exists in database
    print("🔍 Test 3: Verify testigo exists in database")
    try:
        # Login as super admin first
        admin_creds = {
            "rol": "super_admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{base_url}/api/auth/login", json=admin_creds)
        if response.status_code == 200:
            admin_data = response.json()
            if admin_data.get('success'):
                token = admin_data.get('access_token')
                headers = {"Authorization": f"Bearer {token}"}
                
                # Get users
                response = requests.get(f"{base_url}/api/admin/users", headers=headers)
                if response.status_code == 200:
                    users_data = response.json()
                    users = users_data.get('data', [])
                    
                    # Find our testigo
                    testigo = None
                    for user in users:
                        if user.get('cedula') == testigo_cedula:
                            testigo = user
                            break
                    
                    if testigo:
                        print(f"   ✅ Testigo found:")
                        print(f"      • ID: {testigo.get('id')}")
                        print(f"      • Nombre: {testigo.get('nombre')}")
                        print(f"      • Cédula: {testigo.get('cedula')}")
                        print(f"      • Rol: {testigo.get('rol')}")
                        print(f"      • Activo: {testigo.get('activo')}")
                        print(f"      • Ubicación ID: {testigo.get('ubicacion_id')}")
                    else:
                        print(f"   ❌ Testigo with cedula {testigo_cedula} not found")
                else:
                    print(f"   ❌ Error getting users: {response.status_code}")
            else:
                print(f"   ❌ Admin login failed: {admin_data.get('error')}")
        else:
            print(f"   ❌ Admin login HTTP error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

def analyze_auth_system():
    """Analyze the current authentication system"""
    print("\n🔧 ANALYZING AUTHENTICATION SYSTEM")
    print("=" * 40)
    
    print("Current system:")
    print("• Location-based authentication for most roles")
    print("• Testigos need cedula-based authentication")
    print("• 212 testigos already exist with cedulas")
    print()
    
    print("Required changes:")
    print("• Modify auth service to handle cedula for testigos")
    print("• Update login endpoint to accept cedula parameter")
    print("• Ensure frontend shows cedula field for testigos")
    print()
    
    print("Next steps:")
    print("1. Check if cedula authentication already exists")
    print("2. If not, implement cedula-based auth for testigos")
    print("3. Test testigo login with cedula")
    print("4. Verify E-14 form registration works")

if __name__ == "__main__":
    test_testigo_login()
    analyze_auth_system()
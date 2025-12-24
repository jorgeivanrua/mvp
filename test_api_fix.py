#!/usr/bin/env python3
"""
Test script to verify the API fixes for incidentes and delitos endpoints
"""

import requests
import json

def test_login():
    """Test login and get JWT token"""
    url = "http://localhost:5000/api/auth/login"
    data = {
        "cedula": "18",  # Coordinador Puesto user
        "password": "test123"
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            return result.get('access_token')
    
    print(f"Login failed: {response.status_code} - {response.text}")
    return None

def test_incidentes_endpoint(token):
    """Test the incidentes endpoint"""
    url = "http://localhost:5000/api/coordinador-puesto/incidentes"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"Incidentes endpoint: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Incidentes endpoint working: {len(result.get('data', []))} incidentes found")
        return True
    else:
        print(f"❌ Incidentes endpoint failed: {response.text}")
        return False

def test_delitos_endpoint(token):
    """Test the delitos endpoint"""
    url = "http://localhost:5000/api/coordinador-puesto/delitos"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"Delitos endpoint: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Delitos endpoint working: {len(result.get('data', []))} delitos found")
        return True
    else:
        print(f"❌ Delitos endpoint failed: {response.text}")
        return False

def main():
    print("🧪 Testing API fixes...")
    
    # Test login
    print("\n1. Testing login...")
    token = test_login()
    if not token:
        print("❌ Cannot proceed without valid token")
        return
    
    print("✅ Login successful")
    
    # Test endpoints
    print("\n2. Testing incidentes endpoint...")
    incidentes_ok = test_incidentes_endpoint(token)
    
    print("\n3. Testing delitos endpoint...")
    delitos_ok = test_delitos_endpoint(token)
    
    # Summary
    print("\n📊 Test Results:")
    print(f"  - Incidentes endpoint: {'✅ PASS' if incidentes_ok else '❌ FAIL'}")
    print(f"  - Delitos endpoint: {'✅ PASS' if delitos_ok else '❌ FAIL'}")
    
    if incidentes_ok and delitos_ok:
        print("\n🎉 All API fixes working correctly!")
    else:
        print("\n⚠️  Some endpoints still have issues")

if __name__ == "__main__":
    main()
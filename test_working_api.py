#!/usr/bin/env python3
import socket
import json
import sys

def make_http_request(host, port, method, path, headers=None, data=None):
    """Make HTTP request using raw sockets"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        
        # Build HTTP request
        request_lines = [f"{method} {path} HTTP/1.1"]
        request_lines.append(f"Host: {host}:{port}")
        
        if headers:
            for key, value in headers.items():
                request_lines.append(f"{key}: {value}")
        
        if data:
            json_data = json.dumps(data)
            request_lines.append("Content-Type: application/json")
            request_lines.append(f"Content-Length: {len(json_data)}")
            request_lines.append("")
            request_lines.append(json_data)
        else:
            request_lines.append("")
            request_lines.append("")
        
        request = "\r\n".join(request_lines)
        sock.send(request.encode())
        
        # Read response
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            # Check if we have complete response
            if b"\r\n\r\n" in response:
                # For JSON responses, check if we have complete content
                if b"Content-Length:" in response:
                    try:
                        headers_part, body_part = response.split(b"\r\n\r\n", 1)
                        content_length_line = [line for line in headers_part.decode().split('\r\n') if 'Content-Length:' in line][0]
                        content_length = int(content_length_line.split(':')[1].strip())
                        if len(body_part) >= content_length:
                            break
                    except:
                        break
                else:
                    break
        
        sock.close()
        return response.decode('utf-8', errors='ignore')
        
    except Exception as e:
        print(f"Error making request: {e}")
        return None

def test_login():
    """Test login endpoint"""
    print("=== TEST LOGIN ===")
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = make_http_request('127.0.0.1', 5000, 'POST', '/api/auth/login', data=login_data)
    
    if response:
        print(f"Response received (first 500 chars):")
        print(response[:500])
        
        # Try to extract token if login successful
        if '"access_token"' in response:
            try:
                json_part = response.split('\r\n\r\n', 1)[1]
                data = json.loads(json_part)
                token = data.get('access_token')
                print(f"\n✓ Login successful! Token: {token[:50]}..." if token else "Login response received but no token")
                return token
            except Exception as e:
                print(f"Could not parse JSON response: {e}")
        else:
            print("Login failed or no token in response")
    else:
        print("No response received")
    
    return None

def test_reporte_simple(token):
    """Test reporte generation endpoint"""
    print("\n=== TEST REPORTE SIMPLE ===")
    
    if not token:
        print("No hay token disponible")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Datos para el reporte
    reporte_data = {
        "tipo_reporte": "participacion",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-12-31",
        "municipio": "Armenia"
    }
    
    response = make_http_request('127.0.0.1', 5000, 'POST', '/api/reportes/generar', 
                               headers=headers, data=reporte_data)
    
    if response:
        print("Response received (first 500 chars):")
        print(response[:500])
        
        if "200 OK" in response:
            print("\n✓ Reporte generado exitosamente!")
        else:
            print("\n✗ Error al generar reporte")
    else:
        print("No response received")

def test_dashboard_stats(token):
    """Test dashboard stats endpoint"""
    print("\n=== TEST DASHBOARD STATS ===")
    
    if not token:
        print("No hay token disponible")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = make_http_request('127.0.0.1', 5000, 'GET', '/api/dashboard/stats', headers=headers)
    
    if response:
        print("Response received (first 500 chars):")
        print(response[:500])
        
        if "200 OK" in response:
            print("\n✓ Dashboard stats obtenidas exitosamente!")
        else:
            print("\n✗ Error al obtener dashboard stats")
    else:
        print("No response received")

if __name__ == "__main__":
    print("Iniciando tests del sistema electoral...")
    
    # Test de login
    token = test_login()
    
    # Test de reporte si el login fue exitoso
    if token:
        test_reporte_simple(token)
        test_dashboard_stats(token)
    
    print("\nTests completados.")
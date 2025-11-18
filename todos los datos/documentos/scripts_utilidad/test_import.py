"""Test imports"""
print("Testing imports...")

try:
    from backend.app import create_app
    print("✓ backend.app imported successfully")
    
    app = create_app('development')
    print("✓ App created successfully")
    print(f"✓ Template folder: {app.template_folder}")
    print(f"✓ Static folder: {app.static_folder}")
    
    print("\n✓ All imports successful!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

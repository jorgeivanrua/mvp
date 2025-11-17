import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User

app = create_app()

with app.app_context():
    print("Reseteando contraseñas...")
    usuarios = User.query.all()
    print(f"Total usuarios: {len(usuarios)}")
    
    for usuario in usuarios:
        usuario.set_password('test123')
        print(f"  - {usuario.nombre}: test123")
    
    db.session.commit()
    print("Listo!")

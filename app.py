"""
Punto de entrada principal para Gunicorn en Render
"""
from backend.app import app

if __name__ == '__main__':
    app.run()

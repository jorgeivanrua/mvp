#!/usr/bin/env python
"""
WSGI application entry point para gunicorn
"""
import os

os.environ['FLASK_ENV'] = 'production'

from backend.app import create_app

app = create_app('production')

if __name__ == '__main__':
    app.run()

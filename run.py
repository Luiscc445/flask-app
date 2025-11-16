"""
Punto de entrada de la aplicación Flask Veterinaria
"""
import os
from app import create_app, db, init_database
from app.models import *

# Obtener configuración del entorno
config_name = os.getenv('FLASK_ENV', 'development')

# Crear la aplicación
app = create_app(config_name)

# Contexto de la aplicación
with app.app_context():
    # Crear todas las tablas
    db.create_all()
    
    # Inicializar datos de ejemplo
    init_database()
    
    print(f"""
    ========================================
    Sistema Veterinario v2.0.0
    ========================================
    Configuración: {config_name}
    Base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}
    
    Credenciales de acceso:
    - Usuario: admin
    - Contraseña: admin123
    
    Servidor iniciado en: http://localhost:5000
    ========================================
    """)

if __name__ == '__main__':
    # Ejecutar la aplicación
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(config_name == 'development')
    )

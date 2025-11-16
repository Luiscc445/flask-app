"""
Inicialización de la aplicación Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
    
    Returns:
        app: Instancia de Flask configurada
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configurar login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    # Importar modelos (necesario para crear las tablas)
    from app.models import user, mascota, cita, medicamento
    
    # Registrar blueprints (controladores)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.tutor_controller import tutor_bp
    from app.controllers.veterinario_controller import veterinario_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(tutor_bp, url_prefix='/tutor')
    app.register_blueprint(veterinario_bp, url_prefix='/veterinario')
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    return app


@login_manager.user_loader
def load_user(user_id):
    """
    Callback para cargar un usuario desde la sesión
    
    Args:
        user_id: ID del usuario
    
    Returns:
        Usuario o None si no existe
    """
    from app.models.user import Usuario
    return Usuario.query.get(int(user_id))

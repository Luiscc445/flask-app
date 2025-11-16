"""
Configuración de la aplicación Flask Veterinaria
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base"""
    # Configuración de la aplicación
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///veterinaria.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de Flask-Login
    LOGIN_VIEW = 'auth.login'
    LOGIN_MESSAGE = 'Por favor, inicia sesión para acceder a esta página.'
    LOGIN_MESSAGE_CATEGORY = 'info'
    
    # Configuración de correo
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@veterinaria.com'
    
    # Configuración de uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # Configuración de paginación
    ITEMS_PER_PAGE = 10
    
    # Configuración de la aplicación
    APP_NAME = 'Sistema Veterinario'
    APP_VERSION = '2.0.0'
    APP_DESCRIPTION = 'Sistema de Gestión Veterinaria Profesional'
    
    # Colores corporativos
    PRIMARY_COLOR = '#2563eb'  # Azul profesional
    SECONDARY_COLOR = '#10b981'  # Verde médico
    DANGER_COLOR = '#ef4444'
    WARNING_COLOR = '#f59e0b'
    INFO_COLOR = '#3b82f6'
    SUCCESS_COLOR = '#22c55e'
    
    # Configuración de notificaciones
    ENABLE_NOTIFICATIONS = True
    NOTIFICATION_TIMEOUT = 5000  # 5 segundos

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    
class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # En producción, asegurarse de que estas variables estén configuradas
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

class TestingConfig(Config):
    """Configuración de pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class SQLServerConfig(Config):
    """
    Configuración para SQL Server

    Variables de entorno necesarias:
    - SQLSERVER_DRIVER: Driver ODBC (default: ODBC Driver 17 for SQL Server)
    - SQLSERVER_SERVER: Servidor (ejemplo: localhost o IP)
    - SQLSERVER_DATABASE: Nombre de la base de datos
    - SQLSERVER_USERNAME: Usuario de SQL Server
    - SQLSERVER_PASSWORD: Contraseña
    - SQLSERVER_PORT: Puerto (default: 1433)
    - SQLSERVER_TRUSTED: true para autenticación Windows (opcional)

    Ejemplo de DATABASE_URL:
    mssql+pyodbc://user:pass@localhost:1433/veterinaria?driver=ODBC+Driver+17+for+SQL+Server
    """

    @staticmethod
    def get_sqlserver_uri():
        """Construye la URI de SQL Server desde variables de entorno"""
        driver = os.environ.get('SQLSERVER_DRIVER', 'ODBC Driver 17 for SQL Server')
        server = os.environ.get('SQLSERVER_SERVER', 'localhost')
        database = os.environ.get('SQLSERVER_DATABASE', 'veterinaria')
        username = os.environ.get('SQLSERVER_USERNAME')
        password = os.environ.get('SQLSERVER_PASSWORD')
        port = os.environ.get('SQLSERVER_PORT', '1433')
        trusted = os.environ.get('SQLSERVER_TRUSTED', 'false').lower() == 'true'

        # Si usa autenticación de Windows
        if trusted:
            return f"mssql+pyodbc://{server}:{port}/{database}?driver={driver}&trusted_connection=yes"

        # Autenticación con usuario y contraseña
        if username and password:
            return f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={driver}"

        # Fallback a SQLite si no hay configuración de SQL Server
        return 'sqlite:///veterinaria.db'

    SQLALCHEMY_DATABASE_URI = get_sqlserver_uri.__func__()
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'echo_pool': True
    }

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'sqlserver': SQLServerConfig,
    'default': DevelopmentConfig
}

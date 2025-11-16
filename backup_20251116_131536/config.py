import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-super-segura-cambiar-en-produccion'
    
    # ============================================
    # CONFIGURACIÓN SQL SERVER CON PYMSSQL
    # ============================================
    
    SQL_SERVER = 'LUIS_CARLOS69\\SQLDEV'
    SQL_DATABASE = 'VetRamboPetFlask'
    
    # pymssql con autenticación Windows (sin trusted_connection)
    SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{SQL_SERVER}/{SQL_DATABASE}?charset=utf8'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = 3600
    
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    ITEMS_PER_PAGE = 10


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
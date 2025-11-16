"""
Aplicación Flask - Sistema Veterinario Mejorado
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import os
from datetime import datetime

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

def create_app(config_name='default'):
    """Factory para crear la aplicación"""
    app = Flask(__name__)
    
    # Cargar configuración
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Configurar login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Callback para cargar usuario
    from app.models.user import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registrar blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.veterinario_controller import veterinario_bp
    from app.controllers.tutor_controller import tutor_bp
    from app.controllers.recepcionista_controller import recepcionista_bp
    from app.controllers.api_controller import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(veterinario_bp, url_prefix='/veterinario')
    app.register_blueprint(tutor_bp, url_prefix='/tutor')
    app.register_blueprint(recepcionista_bp, url_prefix='/recepcion')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Ruta principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Manejadores de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    @app.context_processor
    def inject_config():
        return {
            'app_name': app.config.get('APP_NAME', 'Sistema Veterinario'),
            'app_version': app.config.get('APP_VERSION', '2.0.0'),
            'primary_color': app.config.get('PRIMARY_COLOR', '#2563eb'),
            'secondary_color': app.config.get('SECONDARY_COLOR', '#10b981')
        }
    
    # Filtros personalizados para templates
    @app.template_filter('dateformat')
    def dateformat(value, format='%d/%m/%Y'):
        if value is None:
            return ''
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value.strftime(format)
    
    @app.template_filter('timeformat')
    def timeformat(value, format='%H:%M'):
        if value is None:
            return ''
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value.strftime(format)
    
    @app.template_filter('currency')
    def currency(value):
        """Formato de moneda"""
        if value is None:
            return 'Bs. 0.00'
        return f'Bs. {value:,.2f}'
    
    # Crear directorios necesarios
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'pets'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
    
    return app

# Función para inicializar la base de datos
def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    from app.models import Usuario, Servicio, Medicamento, ConfiguracionSistema
    from werkzeug.security import generate_password_hash
    
    # Crear usuario administrador por defecto
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            email='admin@veterinaria.com',
            password='admin123',
            nombre='Administrador',
            apellido='Sistema',
            rol='admin',
            activo=True,
            verificado=True
        )
        db.session.add(admin)
    
    # Crear servicios básicos
    servicios_base = [
        {'codigo': 'CONS-01', 'nombre': 'Consulta General', 'categoria': 'consulta', 'precio': 50.00, 'duracion_estimada': 30},
        {'codigo': 'CONS-02', 'nombre': 'Consulta de Emergencia', 'categoria': 'consulta', 'precio': 100.00, 'duracion_estimada': 45},
        {'codigo': 'VAC-01', 'nombre': 'Vacunación Básica', 'categoria': 'vacunacion', 'precio': 30.00, 'duracion_estimada': 15},
        {'codigo': 'VAC-02', 'nombre': 'Vacuna Antirrábica', 'categoria': 'vacunacion', 'precio': 35.00, 'duracion_estimada': 15},
        {'codigo': 'CIR-01', 'nombre': 'Castración/Esterilización', 'categoria': 'cirugia', 'precio': 250.00, 'duracion_estimada': 120},
        {'codigo': 'LAB-01', 'nombre': 'Análisis de Sangre', 'categoria': 'laboratorio', 'precio': 80.00, 'duracion_estimada': 30},
        {'codigo': 'LAB-02', 'nombre': 'Radiografía', 'categoria': 'laboratorio', 'precio': 120.00, 'duracion_estimada': 30},
        {'codigo': 'LIMP-01', 'nombre': 'Limpieza Dental', 'categoria': 'higiene', 'precio': 150.00, 'duracion_estimada': 60},
        {'codigo': 'DESP-01', 'nombre': 'Desparasitación', 'categoria': 'tratamiento', 'precio': 25.00, 'duracion_estimada': 15}
    ]
    
    for servicio_data in servicios_base:
        servicio = Servicio.query.filter_by(codigo=servicio_data['codigo']).first()
        if not servicio:
            servicio = Servicio(**servicio_data)
            db.session.add(servicio)
    
    # Configuraciones del sistema
    configuraciones = [
        {'clave': 'horario_apertura', 'valor': '08:00', 'tipo': 'string', 'descripcion': 'Hora de apertura de la clínica'},
        {'clave': 'horario_cierre', 'valor': '20:00', 'tipo': 'string', 'descripcion': 'Hora de cierre de la clínica'},
        {'clave': 'dias_laborables', 'valor': 'lunes,martes,miércoles,jueves,viernes,sábado', 'tipo': 'string', 'descripcion': 'Días laborables'},
        {'clave': 'tiempo_cita_default', 'valor': '30', 'tipo': 'integer', 'descripcion': 'Duración por defecto de una cita (minutos)'},
        {'clave': 'recordatorio_cita_horas', 'valor': '24', 'tipo': 'integer', 'descripcion': 'Horas antes para enviar recordatorio de cita'},
        {'clave': 'email_clinica', 'valor': 'contacto@veterinaria.com', 'tipo': 'string', 'descripcion': 'Email de contacto'},
        {'clave': 'telefono_clinica', 'valor': '+591 70000000', 'tipo': 'string', 'descripcion': 'Teléfono de contacto'},
        {'clave': 'direccion_clinica', 'valor': 'Av. Principal #123, La Paz, Bolivia', 'tipo': 'string', 'descripcion': 'Dirección de la clínica'}
    ]
    
    for config_data in configuraciones:
        config = ConfiguracionSistema.query.filter_by(clave=config_data['clave']).first()
        if not config:
            config = ConfiguracionSistema(**config_data)
            db.session.add(config)
    
    db.session.commit()
    print("Base de datos inicializada con datos de ejemplo")

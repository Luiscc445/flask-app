"""
Modelo de Usuario Mejorado con Estadísticas
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from sqlalchemy import func, and_
from app import db

class Usuario(UserMixin, db.Model):
    """Modelo de Usuario con soporte para múltiples roles y estadísticas"""
    __tablename__ = 'usuarios'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Información personal
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=True)
    telefono = db.Column(db.String(20))
    telefono_emergencia = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    
    # Rol del usuario
    rol = db.Column(db.String(20), nullable=False, default='tutor')
    # Roles: 'admin', 'veterinario', 'tutor', 'recepcionista', 'asistente'
    
    # Estado del usuario
    activo = db.Column(db.Boolean, default=True)
    verificado = db.Column(db.Boolean, default=False)
    
    # Campos de especialidad (solo para veterinarios)
    especialidad = db.Column(db.String(100))
    licencia_profesional = db.Column(db.String(50))
    anos_experiencia = db.Column(db.Integer)
    
    # Foto de perfil
    foto_perfil = db.Column(db.String(200))
    
    # Timestamps
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime)
    
    # Configuración de notificaciones
    notificaciones_email = db.Column(db.Boolean, default=True)
    notificaciones_sms = db.Column(db.Boolean, default=False)
    
    # Relaciones
    mascotas = db.relationship('Mascota', backref='tutor', lazy='dynamic', cascade='all, delete-orphan')
    citas_como_tutor = db.relationship('Cita', foreign_keys='Cita.tutor_id', backref='tutor', lazy='dynamic')
    citas_como_veterinario = db.relationship('Cita', foreign_keys='Cita.veterinario_id', backref='veterinario', lazy='dynamic')
    historiales_creados = db.relationship('HistorialClinico', backref='creado_por', lazy='dynamic')
    notificaciones = db.relationship('Notificacion', backref='usuario', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        # Extraer password antes de llamar a super
        password = kwargs.pop('password', None)
        super(Usuario, self).__init__(**kwargs)
        if password:
            self.set_password(password)
    
    def set_password(self, password):
        """Hashea la contraseña antes de guardarla"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.rol == 'admin'
    
    def is_veterinario(self):
        """Verifica si el usuario es veterinario"""
        return self.rol == 'veterinario'
    
    def is_tutor(self):
        """Verifica si el usuario es tutor"""
        return self.rol == 'tutor'
    
    def is_recepcionista(self):
        """Verifica si el usuario es recepcionista"""
        return self.rol == 'recepcionista'
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    def actualizar_ultimo_acceso(self):
        """Actualiza el último acceso del usuario"""
        self.ultimo_acceso = datetime.utcnow()
        db.session.commit()
    
    # Métodos de estadísticas para veterinarios
    def get_estadisticas_veterinario(self):
        """Obtiene estadísticas del veterinario"""
        if not self.is_veterinario():
            return None
            
        hoy = date.today()
        
        # Citas totales
        total_citas = self.citas_como_veterinario.count()
        
        # Citas pendientes
        citas_pendientes = self.citas_como_veterinario.filter(
            Cita.estado == 'pendiente'
        ).count()
        
        # Citas hoy
        citas_hoy = self.citas_como_veterinario.filter(
            func.date(Cita.fecha) == hoy
        ).count()
        
        # Citas completadas
        citas_completadas = self.citas_como_veterinario.filter(
            Cita.estado == 'completada'
        ).count()
        
        # Pacientes únicos atendidos
        pacientes_unicos = db.session.query(func.count(func.distinct(Cita.mascota_id))).filter(
            Cita.veterinario_id == self.id,
            Cita.estado == 'completada'
        ).scalar()
        
        # Ingresos generados (si se maneja facturación)
        ingresos_mes = db.session.query(func.sum(Cita.costo)).filter(
            Cita.veterinario_id == self.id,
            Cita.estado == 'completada',
            func.extract('month', Cita.fecha) == hoy.month,
            func.extract('year', Cita.fecha) == hoy.year
        ).scalar() or 0
        
        return {
            'total_citas': total_citas,
            'citas_pendientes': citas_pendientes,
            'citas_hoy': citas_hoy,
            'citas_completadas': citas_completadas,
            'pacientes_unicos': pacientes_unicos,
            'ingresos_mes': ingresos_mes,
            'tasa_completacion': (citas_completadas / total_citas * 100) if total_citas > 0 else 0
        }
    
    # Métodos de estadísticas para tutores
    def get_estadisticas_tutor(self):
        """Obtiene estadísticas del tutor"""
        if not self.is_tutor():
            return None
            
        return {
            'total_mascotas': self.mascotas.count(),
            'mascotas_activas': self.mascotas.filter_by(activo=True).count(),
            'total_citas': self.citas_como_tutor.count(),
            'citas_pendientes': self.citas_como_tutor.filter_by(estado='pendiente').count(),
            'proxima_cita': self.citas_como_tutor.filter(
                Cita.fecha >= datetime.now(),
                Cita.estado == 'pendiente'
            ).order_by(Cita.fecha).first()
        }
    
    def get_notificaciones_no_leidas(self):
        """Obtiene el número de notificaciones no leídas"""
        return self.notificaciones.filter_by(leida=False).count()
    
    def puede_editar_usuario(self, usuario):
        """Verifica si puede editar un usuario"""
        if self.is_admin():
            return True
        return self.id == usuario.id
    
    def __repr__(self):
        return f'<Usuario {self.username} - {self.rol}>'

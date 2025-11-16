"""
Modelo de Usuario
Gestiona los usuarios del sistema: Administradores, Veterinarios y Tutores
"""
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Usuario(UserMixin, db.Model):
    """
    Modelo de Usuario con soporte para múltiples roles
    """
    __tablename__ = 'usuarios'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Información personal
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    
    # Rol del usuario
    rol = db.Column(db.String(20), nullable=False, default='tutor')
    # Roles: 'admin', 'veterinario', 'tutor'
    
    # Estado del usuario
    activo = db.Column(db.Boolean, default=True)
    
    # Campos de especialidad (solo para veterinarios)
    especialidad = db.Column(db.String(100))
    licencia_profesional = db.Column(db.String(50))
    
    # Timestamps
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    mascotas = db.relationship('Mascota', backref='tutor', lazy=True, cascade='all, delete-orphan')
    citas_como_tutor = db.relationship('Cita', foreign_keys='Cita.tutor_id', backref='tutor', lazy=True)
    citas_como_veterinario = db.relationship('Cita', foreign_keys='Cita.veterinario_id', backref='veterinario', lazy=True)
    
    def __init__(self, username, email, password, nombre, apellido, rol='tutor', **kwargs):
        """
        Constructor del modelo Usuario
        """
        self.username = username
        self.email = email
        self.set_password(password)
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
        
        # Campos opcionales
        self.telefono = kwargs.get('telefono')
        self.direccion = kwargs.get('direccion')
        self.especialidad = kwargs.get('especialidad')
        self.licencia_profesional = kwargs.get('licencia_profesional')
        self.activo = kwargs.get('activo', True)
    
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
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    def __repr__(self):
        return f'<Usuario {self.username} - {self.rol}>'

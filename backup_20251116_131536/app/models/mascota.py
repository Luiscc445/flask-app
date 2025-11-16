"""
Modelo de Mascota
Gestiona las mascotas de los tutores
"""
from app import db
from datetime import datetime


class Mascota(db.Model):
    """
    Modelo de Mascota
    """
    __tablename__ = 'mascotas'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)  # Perro, Gato, Ave, etc.
    raza = db.Column(db.String(100))
    
    # Información de la mascota
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(10))  # Macho, Hembra
    color = db.Column(db.String(50))
    peso = db.Column(db.Float)  # En kilogramos
    
    # Información médica
    esterilizado = db.Column(db.Boolean, default=False)
    chip_identificacion = db.Column(db.String(50), unique=True)
    observaciones = db.Column(db.Text)
    
    # Estado
    activo = db.Column(db.Boolean, default=True)
    
    # Relación con el tutor
    tutor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Timestamps
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    citas = db.relationship('Cita', backref='mascota', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, nombre, especie, tutor_id, **kwargs):
        """
        Constructor del modelo Mascota
        """
        self.nombre = nombre
        self.especie = especie
        self.tutor_id = tutor_id
        
        # Campos opcionales
        self.raza = kwargs.get('raza')
        self.fecha_nacimiento = kwargs.get('fecha_nacimiento')
        self.sexo = kwargs.get('sexo')
        self.color = kwargs.get('color')
        self.peso = kwargs.get('peso')
        self.esterilizado = kwargs.get('esterilizado', False)
        self.chip_identificacion = kwargs.get('chip_identificacion')
        self.observaciones = kwargs.get('observaciones')
        self.activo = kwargs.get('activo', True)
    
    @property
    def edad(self):
        """Calcula la edad de la mascota en años"""
        if self.fecha_nacimiento:
            today = datetime.now().date()
            edad = today.year - self.fecha_nacimiento.year
            if today.month < self.fecha_nacimiento.month or \
               (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
                edad -= 1
            return edad
        return None
    
    def __repr__(self):
        return f'<Mascota {self.nombre} - {self.especie}>'

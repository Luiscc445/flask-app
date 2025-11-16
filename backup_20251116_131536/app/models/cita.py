"""
Modelo de Cita
Gestiona las citas médicas entre tutores, mascotas y veterinarios
"""
from app import db
from datetime import datetime


class Cita(db.Model):
    """
    Modelo de Cita Médica
    """
    __tablename__ = 'citas'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    
    # Relaciones
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascotas.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    veterinario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # Información de la cita
    fecha_hora = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    # Estados: 'pendiente', 'aceptada', 'pospuesta', 'atendida', 'cancelada'
    
    # Información de la atención
    diagnostico = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    
    # Información de posponer
    motivo_posposicion = db.Column(db.Text)
    nueva_fecha_sugerida = db.Column(db.DateTime)
    
    # Timestamps
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_atencion = db.Column(db.DateTime)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    recetas = db.relationship('Receta', backref='cita', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, mascota_id, tutor_id, fecha_hora, motivo, **kwargs):
        """
        Constructor del modelo Cita
        """
        self.mascota_id = mascota_id
        self.tutor_id = tutor_id
        self.fecha_hora = fecha_hora
        self.motivo = motivo
        
        # Campos opcionales
        self.veterinario_id = kwargs.get('veterinario_id')
        self.estado = kwargs.get('estado', 'pendiente')
        self.diagnostico = kwargs.get('diagnostico')
        self.tratamiento = kwargs.get('tratamiento')
        self.observaciones = kwargs.get('observaciones')
        self.motivo_posposicion = kwargs.get('motivo_posposicion')
        self.nueva_fecha_sugerida = kwargs.get('nueva_fecha_sugerida')
    
    def aceptar(self, veterinario_id):
        """Acepta la cita y asigna un veterinario"""
        self.estado = 'aceptada'
        self.veterinario_id = veterinario_id
        self.fecha_actualizacion = datetime.utcnow()
    
    def posponer(self, motivo, nueva_fecha=None):
        """Pospone la cita"""
        self.estado = 'pospuesta'
        self.motivo_posposicion = motivo
        if nueva_fecha:
            self.nueva_fecha_sugerida = nueva_fecha
        self.fecha_actualizacion = datetime.utcnow()
    
    def atender(self, diagnostico, tratamiento, observaciones=None):
        """Marca la cita como atendida"""
        self.estado = 'atendida'
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.fecha_atencion = datetime.utcnow()
        self.fecha_actualizacion = datetime.utcnow()
    
    def cancelar(self):
        """Cancela la cita"""
        self.estado = 'cancelada'
        self.fecha_actualizacion = datetime.utcnow()
    
    @property
    def esta_pendiente(self):
        """Verifica si la cita está pendiente"""
        return self.estado == 'pendiente'
    
    @property
    def esta_aceptada(self):
        """Verifica si la cita está aceptada"""
        return self.estado == 'aceptada'
    
    @property
    def esta_atendida(self):
        """Verifica si la cita fue atendida"""
        return self.estado == 'atendida'
    
    def __repr__(self):
        return f'<Cita {self.id} - {self.estado} - {self.fecha_hora}>'

"""
Modelo de Servicios veterinarios
"""
from datetime import datetime
from app import db


class Servicio(db.Model):
    """Modelo de Servicios veterinarios"""
    __tablename__ = 'servicios'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))  # consulta, cirugia, vacunacion, laboratorio
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    duracion_estimada = db.Column(db.Integer)  # En minutos
    activo = db.Column(db.Boolean, default=True)

    requiere_ayuno = db.Column(db.Boolean, default=False)
    requiere_cita = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

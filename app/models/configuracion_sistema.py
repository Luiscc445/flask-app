"""
Modelo de Configuración del Sistema
"""
from datetime import datetime
from app import db


class ConfiguracionSistema(db.Model):
    """Configuración general del sistema"""
    __tablename__ = 'configuracion_sistema'

    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    tipo = db.Column(db.String(20))  # string, integer, boolean, json
    descripcion = db.Column(db.Text)

    # Configuraciones comunes:
    # - horario_apertura
    # - horario_cierre
    # - dias_laborables
    # - tiempo_cita_default
    # - recordatorio_cita_horas
    # - email_clinica
    # - telefono_clinica
    # - direccion_clinica

    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

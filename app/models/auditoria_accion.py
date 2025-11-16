"""
Modelo de Auditoría de Acciones
"""
from datetime import datetime
from app import db


class AuditoriaAccion(db.Model):
    """Registro de auditoría de acciones en el sistema"""
    __tablename__ = 'auditoria_acciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    accion = db.Column(db.String(100))  # login, logout, crear_cita, editar_mascota, etc.
    entidad = db.Column(db.String(50))  # usuario, mascota, cita, etc.
    entidad_id = db.Column(db.Integer)

    descripcion = db.Column(db.Text)
    datos_anteriores = db.Column(db.JSON)
    datos_nuevos = db.Column(db.JSON)

    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

"""
Modelo de Notificaciones
"""
from datetime import datetime
from app import db


class Notificacion(db.Model):
    """Modelo de Notificaciones"""
    __tablename__ = 'notificaciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    tipo = db.Column(db.String(50))  # cita_recordatorio, vacuna_pendiente, resultado_disponible
    titulo = db.Column(db.String(200))
    mensaje = db.Column(db.Text)

    # Enlaces relacionados
    url_accion = db.Column(db.String(200))
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascotas.id'))

    # Estado
    leida = db.Column(db.Boolean, default=False)
    enviada_email = db.Column(db.Boolean, default=False)
    enviada_sms = db.Column(db.Boolean, default=False)

    # Prioridad
    prioridad = db.Column(db.String(20), default='normal')  # baja, normal, alta, urgente

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_lectura = db.Column(db.DateTime)
    fecha_expiracion = db.Column(db.DateTime)

    def marcar_como_leida(self):
        """Marca la notificación como leída"""
        self.leida = True
        self.fecha_lectura = datetime.utcnow()
        db.session.commit()

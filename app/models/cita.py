"""
Modelo de Cita Mejorado
"""
from datetime import datetime, timedelta
from app import db

class Cita(db.Model):
    """Modelo de Cita con información detallada"""
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información básica
    fecha = db.Column(db.DateTime, nullable=False)
    duracion = db.Column(db.Integer, default=30)  # Duración en minutos
    
    # Tipo y motivo
    tipo = db.Column(db.String(50), nullable=False)  # Consulta, Emergencia, Cirugía, Vacunación, Control
    motivo = db.Column(db.String(200), nullable=False)
    sintomas = db.Column(db.Text)
    urgencia = db.Column(db.String(20), default='normal')  # baja, normal, alta, emergencia
    
    # Estado
    estado = db.Column(db.String(20), default='pendiente')
    # Estados: pendiente, confirmada, en_progreso, completada, cancelada, no_asistio
    
    # Información de la consulta
    diagnostico = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    receta = db.Column(db.Text)
    indicaciones = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    
    # Signos vitales (registrados durante la consulta)
    temperatura = db.Column(db.Float)
    frecuencia_cardiaca = db.Column(db.Integer)
    frecuencia_respiratoria = db.Column(db.Integer)
    peso_actual = db.Column(db.Float)
    
    # Próximo control
    requiere_seguimiento = db.Column(db.Boolean, default=False)
    fecha_proximo_control = db.Column(db.Date)
    
    # Costos
    costo = db.Column(db.Float, default=0)
    pagado = db.Column(db.Boolean, default=False)
    metodo_pago = db.Column(db.String(50))  # efectivo, tarjeta, transferencia
    
    # Timestamps
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_confirmacion = db.Column(db.DateTime)
    fecha_inicio_atencion = db.Column(db.DateTime)
    fecha_fin_atencion = db.Column(db.DateTime)
    fecha_cancelacion = db.Column(db.DateTime)
    
    # Razón de cancelación
    razon_cancelacion = db.Column(db.Text)
    
    # Calificación
    calificacion = db.Column(db.Integer)  # 1-5 estrellas
    comentario_calificacion = db.Column(db.Text)
    
    # Relaciones
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascotas.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    veterinario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    recepcionista_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # Archivos adjuntos
    archivos = db.relationship('ArchivoCita', backref='cita', lazy='dynamic', cascade='all, delete-orphan')
    servicios = db.relationship('ServicioCita', backref='cita', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def hora_fin_estimada(self):
        """Calcula la hora estimada de finalización"""
        return self.fecha + timedelta(minutes=self.duracion)
    
    @property
    def esta_retrasada(self):
        """Verifica si la cita está retrasada"""
        if self.estado != 'pendiente':
            return False
        return datetime.now() > self.fecha
    
    @property
    def tiempo_espera(self):
        """Calcula el tiempo de espera si está retrasada"""
        if not self.esta_retrasada:
            return None
        diferencia = datetime.now() - self.fecha
        return int(diferencia.total_seconds() / 60)  # En minutos
    
    def confirmar(self):
        """Confirma la cita"""
        self.estado = 'confirmada'
        self.fecha_confirmacion = datetime.utcnow()
        db.session.commit()
    
    def iniciar_atencion(self):
        """Inicia la atención de la cita"""
        self.estado = 'en_progreso'
        self.fecha_inicio_atencion = datetime.utcnow()
        db.session.commit()
    
    def completar(self):
        """Completa la cita"""
        self.estado = 'completada'
        self.fecha_fin_atencion = datetime.utcnow()
        db.session.commit()
    
    def cancelar(self, razon=None):
        """Cancela la cita"""
        self.estado = 'cancelada'
        self.fecha_cancelacion = datetime.utcnow()
        if razon:
            self.razon_cancelacion = razon
        db.session.commit()
    
    def marcar_no_asistio(self):
        """Marca la cita como no asistió"""
        self.estado = 'no_asistio'
        db.session.commit()
    
    def get_duracion_real(self):
        """Obtiene la duración real de la cita"""
        if self.fecha_inicio_atencion and self.fecha_fin_atencion:
            diferencia = self.fecha_fin_atencion - self.fecha_inicio_atencion
            return int(diferencia.total_seconds() / 60)  # En minutos
        return None
    
    def __repr__(self):
        return f'<Cita {self.id} - {self.fecha} - {self.estado}>'

class ArchivoCita(db.Model):
    """Archivos adjuntos a una cita"""
    __tablename__ = 'archivos_cita'
    
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    
    tipo = db.Column(db.String(50))  # imagen, documento, resultado_lab
    nombre_archivo = db.Column(db.String(200))
    url_archivo = db.Column(db.String(500))
    descripcion = db.Column(db.Text)
    
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    subido_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

class ServicioCita(db.Model):
    """Servicios prestados en una cita"""
    __tablename__ = 'servicios_cita'
    
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float)
    descuento = db.Column(db.Float, default=0)
    
    @property
    def subtotal(self):
        """Calcula el subtotal del servicio"""
        return (self.cantidad * self.precio_unitario) - self.descuento

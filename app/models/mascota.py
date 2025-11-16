"""
Modelo de Mascota Mejorado
"""
from datetime import datetime, date
from app import db

class Mascota(db.Model):
    """Modelo de Mascota con información detallada"""
    __tablename__ = 'mascotas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)  # Perro, Gato, Ave, etc.
    raza = db.Column(db.String(100))
    
    # Información básica
    sexo = db.Column(db.String(10))  # Macho, Hembra
    fecha_nacimiento = db.Column(db.Date)
    peso = db.Column(db.Float)  # En kilogramos
    altura = db.Column(db.Float)  # En centímetros
    color = db.Column(db.String(50))
    
    # Identificación
    chip_identificacion = db.Column(db.String(50), unique=True)
    numero_registro = db.Column(db.String(50))
    
    # Estado de salud
    esterilizado = db.Column(db.Boolean, default=False)
    alergias = db.Column(db.Text)
    condiciones_medicas = db.Column(db.Text)
    medicacion_actual = db.Column(db.Text)
    
    # Comportamiento
    temperamento = db.Column(db.String(200))
    notas_comportamiento = db.Column(db.Text)
    
    # Fotos
    foto_principal = db.Column(db.String(200))
    fotos_adicionales = db.Column(db.JSON)  # Array de URLs
    
    # Estado
    activo = db.Column(db.Boolean, default=True)
    fecha_fallecimiento = db.Column(db.Date)
    causa_fallecimiento = db.Column(db.Text)
    
    # Timestamps
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    tutor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    citas = db.relationship('Cita', backref='mascota', lazy='dynamic', cascade='all, delete-orphan')
    historiales = db.relationship('HistorialClinico', backref='mascota', lazy='dynamic', cascade='all, delete-orphan')
    vacunas = db.relationship('Vacuna', backref='mascota', lazy='dynamic', cascade='all, delete-orphan')
    documentos = db.relationship('DocumentoMascota', backref='mascota', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def edad(self):
        """Calcula la edad de la mascota"""
        if not self.fecha_nacimiento:
            return None
        
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        
        # Ajustar si no ha llegado el cumpleaños este año
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
            
        return edad
    
    @property
    def edad_detallada(self):
        """Retorna la edad en formato detallado (años y meses)"""
        if not self.fecha_nacimiento:
            return "Edad desconocida"
        
        hoy = date.today()
        diferencia = hoy - self.fecha_nacimiento
        anos = diferencia.days // 365
        meses = (diferencia.days % 365) // 30
        
        if anos == 0:
            return f"{meses} {'mes' if meses == 1 else 'meses'}"
        elif meses == 0:
            return f"{anos} {'año' if anos == 1 else 'años'}"
        else:
            return f"{anos} {'año' if anos == 1 else 'años'} y {meses} {'mes' if meses == 1 else 'meses'}"
    
    def get_proxima_cita(self):
        """Obtiene la próxima cita de la mascota"""
        return self.citas.filter(
            Cita.fecha >= datetime.now(),
            Cita.estado == 'pendiente'
        ).order_by(Cita.fecha).first()
    
    def get_ultima_visita(self):
        """Obtiene la última visita completada"""
        return self.citas.filter_by(estado='completada').order_by(Cita.fecha.desc()).first()
    
    def get_historial_peso(self):
        """Obtiene el historial de peso de los últimos 6 meses"""
        historial = []
        for h in self.historiales.order_by(HistorialClinico.fecha.desc()).limit(6):
            if h.peso:
                historial.append({
                    'fecha': h.fecha.strftime('%Y-%m-%d'),
                    'peso': h.peso
                })
        return historial
    
    def tiene_vacunas_pendientes(self):
        """Verifica si tiene vacunas pendientes"""
        return self.vacunas.filter(
            Vacuna.fecha_proxima <= date.today(),
            Vacuna.aplicada == False
        ).count() > 0
    
    def get_vacunas_pendientes(self):
        """Obtiene las vacunas pendientes"""
        return self.vacunas.filter(
            Vacuna.fecha_proxima <= date.today(),
            Vacuna.aplicada == False
        ).all()
    
    def __repr__(self):
        return f'<Mascota {self.nombre} - {self.especie}>'

class Vacuna(db.Model):
    """Modelo de Vacunas"""
    __tablename__ = 'vacunas'
    
    id = db.Column(db.Integer, primary_key=True)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascotas.id'), nullable=False)
    
    nombre = db.Column(db.String(100), nullable=False)
    fecha_aplicacion = db.Column(db.Date)
    fecha_proxima = db.Column(db.Date)
    dosis = db.Column(db.String(50))
    lote = db.Column(db.String(50))
    veterinario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    aplicada = db.Column(db.Boolean, default=False)
    notas = db.Column(db.Text)
    
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class DocumentoMascota(db.Model):
    """Modelo para documentos de mascotas"""
    __tablename__ = 'documentos_mascota'
    
    id = db.Column(db.Integer, primary_key=True)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascotas.id'), nullable=False)
    
    tipo = db.Column(db.String(50))  # Certificado, Radiografía, Análisis, etc.
    titulo = db.Column(db.String(200))
    archivo_url = db.Column(db.String(500))
    descripcion = db.Column(db.Text)
    
    fecha_documento = db.Column(db.Date)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    subido_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

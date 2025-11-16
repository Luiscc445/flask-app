"""
Modelo de Historial Clínico
"""
from datetime import datetime
from app import db


class HistorialClinico(db.Model):
    """Modelo de Historial Clínico"""
    __tablename__ = 'historiales_clinicos'

    id = db.Column(db.Integer, primary_key=True)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascotas.id'), nullable=False)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'))

    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo_registro = db.Column(db.String(50))  # consulta, cirugia, vacunacion, etc.

    # Anamnesis
    motivo_consulta = db.Column(db.Text)
    sintomas_presentados = db.Column(db.Text)
    tiempo_evolucion = db.Column(db.String(100))

    # Examen físico
    peso = db.Column(db.Float)
    temperatura = db.Column(db.Float)
    frecuencia_cardiaca = db.Column(db.Integer)
    frecuencia_respiratoria = db.Column(db.Integer)
    mucosas = db.Column(db.String(100))
    tiempo_llenado_capilar = db.Column(db.String(50))
    estado_hidratacion = db.Column(db.String(50))
    condicion_corporal = db.Column(db.String(50))

    # Hallazgos clínicos
    examen_fisico_detallado = db.Column(db.Text)
    diagnostico_presuntivo = db.Column(db.Text)
    diagnostico_definitivo = db.Column(db.Text)
    pronostico = db.Column(db.String(50))  # bueno, reservado, grave

    # Tratamiento
    tratamiento_aplicado = db.Column(db.Text)
    medicamentos_recetados = db.Column(db.Text)
    indicaciones = db.Column(db.Text)

    # Recomendaciones
    recomendaciones = db.Column(db.Text)
    proxima_revision = db.Column(db.Date)

    # Usuario que creó el registro
    creado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

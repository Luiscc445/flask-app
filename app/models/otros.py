"""
Modelos adicionales para el sistema veterinario
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

class Medicamento(db.Model):
    """Modelo de Medicamentos e Inventario"""
    __tablename__ = 'medicamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    principio_activo = db.Column(db.String(100))
    presentacion = db.Column(db.String(100))
    concentracion = db.Column(db.String(50))
    
    # Categoría
    categoria = db.Column(db.String(50))  # antibiotico, analgesico, vacuna, etc.
    via_administracion = db.Column(db.String(50))  # oral, inyectable, topico
    
    # Stock
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    unidad_medida = db.Column(db.String(20))  # unidad, ml, mg, etc.
    
    # Precios
    precio_compra = db.Column(db.Float)
    precio_venta = db.Column(db.Float)
    
    # Información adicional
    laboratorio = db.Column(db.String(100))
    lote = db.Column(db.String(50))
    fecha_vencimiento = db.Column(db.Date)
    
    # Control
    requiere_receta = db.Column(db.Boolean, default=False)
    controlado = db.Column(db.Boolean, default=False)
    
    # Estado
    activo = db.Column(db.Boolean, default=True)
    
    # Ubicación en almacén
    ubicacion_almacen = db.Column(db.String(50))
    
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def esta_por_vencer(self):
        """Verifica si el medicamento está próximo a vencer (30 días)"""
        if not self.fecha_vencimiento:
            return False
        dias_restantes = (self.fecha_vencimiento - datetime.now().date()).days
        return 0 < dias_restantes <= 30
    
    @property
    def esta_vencido(self):
        """Verifica si el medicamento está vencido"""
        if not self.fecha_vencimiento:
            return False
        return self.fecha_vencimiento < datetime.now().date()
    
    @property
    def necesita_restock(self):
        """Verifica si necesita reabastecimiento"""
        return self.stock_actual <= self.stock_minimo

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

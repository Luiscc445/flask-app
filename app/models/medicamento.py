"""
Modelo de Medicamento y Receta
Gestiona el inventario de medicamentos y las recetas médicas
"""
from datetime import datetime
from app import db


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

    def reducir_stock(self, cantidad):
        """
        Reduce el stock del medicamento

        Args:
            cantidad: Cantidad a reducir

        Returns:
            bool: True si se pudo reducir, False si no hay suficiente stock
        """
        if self.stock_actual >= cantidad:
            self.stock_actual -= cantidad
            self.ultima_actualizacion = datetime.utcnow()
            return True
        return False

    def aumentar_stock(self, cantidad):
        """Aumenta el stock del medicamento"""
        self.stock_actual += cantidad
        self.ultima_actualizacion = datetime.utcnow()


class Receta(db.Model):
    """
    Modelo de Receta Médica
    Relaciona medicamentos con citas
    """
    __tablename__ = 'recetas'

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)

    # Relaciones
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)

    # Información de la receta
    cantidad = db.Column(db.Integer, nullable=False)
    dosis = db.Column(db.String(200))  # Ej: "1 tableta cada 8 horas"
    duracion = db.Column(db.String(100))  # Ej: "7 días"
    indicaciones = db.Column(db.Text)

    # Timestamps
    fecha_receta = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, cita_id, medicamento_id, cantidad, **kwargs):
        """
        Constructor del modelo Receta
        """
        self.cita_id = cita_id
        self.medicamento_id = medicamento_id
        self.cantidad = cantidad

        # Campos opcionales
        self.dosis = kwargs.get('dosis')
        self.duracion = kwargs.get('duracion')
        self.indicaciones = kwargs.get('indicaciones')

    def __repr__(self):
        return f'<Receta {self.id} - Cita: {self.cita_id} - Medicamento: {self.medicamento_id}>'

"""
Modelo de Medicamento y Receta
Gestiona el inventario de medicamentos y las recetas médicas
"""
from app import db
from datetime import datetime


class Medicamento(db.Model):
    """
    Modelo de Medicamento para inventario
    """
    __tablename__ = 'medicamentos'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Información del medicamento
    principio_activo = db.Column(db.String(200))
    presentacion = db.Column(db.String(100))  # Tabletas, Jarabe, Inyectable, etc.
    concentracion = db.Column(db.String(50))
    
    # Inventario
    stock = db.Column(db.Integer, default=0, nullable=False)
    stock_minimo = db.Column(db.Integer, default=10)
    unidad_medida = db.Column(db.String(50))  # Unidades, ml, gr, etc.
    
    # Información comercial
    lote = db.Column(db.String(100))
    fecha_vencimiento = db.Column(db.Date)
    proveedor = db.Column(db.String(200))
    precio_unitario = db.Column(db.Float)
    
    # Estado
    activo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    recetas = db.relationship('Receta', backref='medicamento', lazy=True)
    
    def __init__(self, nombre, stock=0, **kwargs):
        """
        Constructor del modelo Medicamento
        """
        self.nombre = nombre
        self.stock = stock
        
        # Campos opcionales
        self.descripcion = kwargs.get('descripcion')
        self.principio_activo = kwargs.get('principio_activo')
        self.presentacion = kwargs.get('presentacion')
        self.concentracion = kwargs.get('concentracion')
        self.stock_minimo = kwargs.get('stock_minimo', 10)
        self.unidad_medida = kwargs.get('unidad_medida', 'unidades')
        self.lote = kwargs.get('lote')
        self.fecha_vencimiento = kwargs.get('fecha_vencimiento')
        self.proveedor = kwargs.get('proveedor')
        self.precio_unitario = kwargs.get('precio_unitario')
        self.activo = kwargs.get('activo', True)
    
    def reducir_stock(self, cantidad):
        """
        Reduce el stock del medicamento
        
        Args:
            cantidad: Cantidad a reducir
        
        Returns:
            bool: True si se pudo reducir, False si no hay suficiente stock
        """
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.ultima_actualizacion = datetime.utcnow()
            return True
        return False
    
    def aumentar_stock(self, cantidad):
        """Aumenta el stock del medicamento"""
        self.stock += cantidad
        self.ultima_actualizacion = datetime.utcnow()
    
    @property
    def necesita_reposicion(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.stock <= self.stock_minimo
    
    @property
    def esta_vencido(self):
        """Verifica si el medicamento está vencido"""
        if self.fecha_vencimiento:
            return self.fecha_vencimiento < datetime.now().date()
        return False
    
    def __repr__(self):
        return f'<Medicamento {self.nombre} - Stock: {self.stock}>'


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

"""
Clase que crea la base de datos
"""

from peewee import AutoField, Model, SqliteDatabase, CharField, DecimalField, IntegerField

# crea la db
db = SqliteDatabase('basededatos.db')

class BaseModel(Model):
    """
    Clase base para los modelos de la
    base de datos, que hereda de peewee
    """
    class Meta:
        database = db

class Producto(BaseModel):
    """
    Modelo de productos
    que modela un material con sus campos
    """

    id = AutoField()
    material = CharField()
    descripcion = CharField()
    precio_venta = DecimalField()
    precio_costo = DecimalField()
    stock = IntegerField()  # Cambiado de AutoField a IntegerField
    proveedor = CharField()

    def __str__(self):
        return f"Producto: {self.material} - Descripción: {self.descripcion} - Precio venta: ${self.precio_venta:.2f}"

class RegistroLog(BaseModel):
    """
    Modelo de registro de log
    que modela un registro de log con sus campos
    """
    id = AutoField()
    fecha = CharField()
    hora = CharField()
    descripcion = CharField()
    usuario = CharField()
    accion = CharField()

    def __str__(self):
        return f"Fecha: {self.fecha} - Descripción: {self.descripcion}"

class CrearBaseDatos():
    """
    Clase  para crear la
    base de datos y las tablas correspondientes
    """
    def crear_base_datos(self):
        """
        Metodo para crear la base de datos
        """
        db.connect()
        db.create_tables([Producto, RegistroLog])
    
    def __str__(self):
        return "realiza la conexion y crea la tabla"

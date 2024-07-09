"""
Modulo para crear el registro de Log.
"""
import datetime
import peewee
from model import RegistroLog

def log_evento(func):
    """
    Funcion para registrar el evento en el log.
    """
    def registro_modificacion(*args, **kwargs):
        resultado = func(*args, **kwargs)
        registro = datetime.datetime.now()

        print(f"{registro}: Se ha realizado la acción de '{func.__name__}' en la base de datos")

        # ingreso el evento en la base de datos en el registro de log
        log = RegistroLog()
        log.fecha = registro.date()
        log.hora = registro.time()
        log.descripcion = "Se ha realizado una accion en la base de datos"
        log.usuario = "anonimo"
        log.accion = func.__name__
        log.save()

    return registro_modificacion
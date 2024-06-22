"""
Inicia la ejecución de la aplicación
"""
from tkinter import Tk
from view import POSApp
from model import CrearBaseDatos

# Función principal que da inicio a la app
#en esta funcion instancio la clase de mi aplicación y paso la ventana principal como argumento
def main():
    """
    Función que crea  e inicializa la ventana principal.
    """
    #instancio la clase de base de datos y luego la creo
    db = CrearBaseDatos()
    db.crear_base_datos()

    root = Tk()
    POSApp(root)
    root.mainloop()

# utilizo una estructura condicional para verificar si este script se está ejecutando directamente
if __name__ == "__main__":
    # Si el archivo es llamado directamente, creo la base de datos y llamo a la función principal
    main()

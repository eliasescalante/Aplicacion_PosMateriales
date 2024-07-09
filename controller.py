"""
Clase Controlador:
Contiene todos los metodos que controlan la aplicación
"""
from tkinter import filedialog, END
import tkinter.messagebox as messagebox
from tkinter.messagebox import showerror
import re
import pandas as pd # me dice que no puede importarlo sin embargo si me toma la libreria
import peewee
from model import Producto, RegistroLog
from decoradores import log_evento


class Controlador:
    """
    Clase Controlador:
    Contiene todos los metodos que controlan la aplicación
    """
    def obtener_registros_log(self):
        """
        Obtiene los registros del log
        :return: Registros del log
        """
        registro = RegistroLog()
        return registro.select()

    def limpiar_tree(self, arbol, entry_list):
        """
        LIMPIA EL TREEVIEWW DE TODA LA INFO QUE ESTE EN EL MOMENTO
        TAMBIEN LIMPIA LOS ENTRY DEL FORMULARIO
        """
        # Limpio el Treeview utilizando un For que recorre todos los hijos del nodo raiz
        for record in arbol.get_children():
            arbol.delete(record)
            print("limpiando treeview...")

        # limpio los campos de entrada
        for entry in entry_list:
            entry.delete(0, END)
            print("limpiando entry")
    @log_evento
    def exportar_base(self):
        """
        EXPORTA TODA LA BASE DE DATOS A UN ARCHIVO DE
        EXCEL Y DEJA ELEGIR DONDE GUARDARLO MEDIANTE UNA VENTANA EMERGENTE.
        IMPRIME EN CONSOLA LA ACCION SI SE EXPORTA CORRECTAMENTE 
        ADEMAS DE MOSTRAR CON UN SHOWINFO UNA VENTANA EMERGENTE 
        CON EL MISMO MENSAJE.
        EN CASO CONTRARIO SE CANCELA Y SE IMPRIME POR CONSOLA
        Y CON UN SHOWERROR PARA MOSTRAR EL MENSAJE DE CANCELACION.
        """

        #imprimo en consola a modo testing para ver si se ejecuta la funcion.
        print("Exportando base...")

        # Pido al usuario que seleccione la ubicación y el nombre del archivo
        #utilizo el metodo filedialog.asksaveasfilename(),para elegir la ruta
        #por parametro paso la extension como defaul .xlsx
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")]
                )

            #uso una estructura condicional para verificar si el usuario selecciono un archivo
            if file_path:
                productos = Producto.select()
            # uso un arrays para ir agregando campo a campo los datos de la base
                info = []
                for producto in productos:
                    info.append([
                    producto.id,
                    producto.material,
                    producto.descripcion,
                    producto.precio_venta,
                    producto.precio_costo,
                    producto.stock,
                    producto.proveedor
                ])
                # utilizo pandas para grabar las columnas del excel a exportar.
                f = pd.DataFrame(
                    info,
                    columns=[
                        'ID', 
                        'Material', 
                        'Descripción', 
                        'Precio Venta', 
                        'Precio Costo', 
                        'Stock', 
                        'Proveedor'
                        ]
                    )
                f.to_excel(file_path, index=False)

                print("base de datos exportada...")
                messagebox.showinfo("Exportación", "La base fue exitosamente exportada a Excel")
            else:
                print("exportación cancelada")
                messagebox.showerror("Exportacion", "Exportacion cancelada")
        except peewee.PeeweeException as e:
            messagebox.showerror("Error", f"Error al acceder a la base de datos: {e}")

    def mostrar_ayuda(self):
        """
        MUESTRA UN MENSAJE EN UNA VENTANA EMERGENTE CON LAS ISNTRUCCIONES Y DESCRIPCION DEL PROGRAMA
        """
        mensaje = """Esta es una aplicación realizada por ELIAS ESCALANTE  que
        muestra una maquetación básica de una interfaz gráfica utilizando Tkinter. 
        Puedes utilizar esta aplicación para gestionar una base de datos de materiales, donde puedes consultar, dar de alta, borrar y modificar registros.
        Realiza un CRUD utilizando el paradigma de programación orientada a objetos utilizando el modelo MVC
        ...
        GIT DEL PROYECTO: https://github.com/eliasescalante/app_pos_POO.git
        """
        messagebox.showinfo("Ayuda", mensaje)
    
    @log_evento
    def alta_registro(
        self, material, descripcion,
        precio_venta, precio_costo,
        stock, proveedor, arbol, entry_list):
        """
        Funcion que realiza un alta de un registro en la base de datos
        recibe por parametros la informacion necesaria
        """
        print("dando de alta al registro")
        if (
            not material or not descripcion or not precio_venta
            or not precio_costo or not stock or not proveedor
        ):
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
        # uso regex para validar los campos los asigno a variables para usar despues
        patron_precio = r"^\d+(\.\d+)?$"
        patron_entero = r"^\d+$"

        if not re.match(patron_entero, material):
            showerror("Error", "El material debe ser un número entero.")
            return
        if not re.match(patron_precio, precio_venta):
            showerror("Error", "El precio de venta debe ser un número flotante.")
            return
        if not re.match(patron_precio, precio_costo):
            showerror("Error", "El precio de costo debe ser un número flotante.")
            return
        if not re.match(patron_entero, stock):
            showerror("Error", "El stock debe ser un número entero.")
            return
        #obtengo los valores de los campos que recibo por parametro
        producto = Producto()
        producto.material = int(material)
        producto.descripcion = descripcion
        producto.precio_venta = float(precio_venta)
        producto.precio_costo = float(precio_costo)
        producto.stock = int(stock)
        producto.proveedor = proveedor
        producto.save()

        nuevo_registro = Producto.select().order_by(Producto.id.desc()).first()
        messagebox.showinfo("Alta de registro", "Registro agregado correctamente.")
        #limpio los campos del treeview
        self.limpiar_tree(arbol, entry_list)
        #imprimo los valores en el treeview
        arbol.insert('', 'end', values=(
            nuevo_registro.material, nuevo_registro.descripcion, 
            nuevo_registro.precio_venta, nuevo_registro.precio_costo, 
            nuevo_registro.stock, nuevo_registro.proveedor)
            )

    @log_evento
    def exportar_consulta(self, arbol):
        """
        EXPORTA LA CONSULTA REALIZADA E IMPRESA EN EL TREEVIEW EN UN ARCHIVO .TXT
        MUESTRA EN UNA VENTANA EMERGENTE SI LA ACCION SI REALIZO CORRECTAMENTE.
        EN CASO QUE NO HAYA UNA CONSULTA REALIZADA PREVIAMENTE MUESTRA 
        UN MENSAJE EN UN SHOWWARNING INDICANDO QUE NO HAY REGISTROS.
        SI SE CANCELA LA OPERACION TAMBIEN SE MUESTRA POR PANTALLA CON UN SHOWWARNING.
        """
        # Verifico si hay registros en el Treeview
        if not arbol.get_children():
            messagebox.showwarning(
                "Exportar consulta", "Debes realizar una consulta primero antes de exportar"
            )
            return
        print("exportando consulta...")
            # Pido al usuario que seleccione la ubicación y el nombre del archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )

        if file_path:
            registros = []
            for item in arbol.get_children():
                registros.append(arbol.item(item)['values'])

            if registros:
                with open(file_path, 'w') as file:
                    for registro in registros:
                        file.write(str(registro) + '\n')
                    messagebox.showinfo("Exportar consulta", "Consulta exportada correctamente.")
            else:
                messagebox.showwarning("Exportar consulta", "No hay registros para exportar.")
        else:
            messagebox.showwarning("Exportar consulta", "Operación cancelada.")

    @log_evento
    def consultar_registro(self, descripcion, arbol, entry_list):
        """
        REALIZA UNA CONSULTA  A LA TABLA DE MATERIALES EN LA BASE 
        DE DATOS PARA OBTENER TODOS LOS REGISTROS Y LOS AGREGA AL TREEVIEW
        SI NO SE COMPLETA LOS CAMPOS REQUERIDOS PARA REALIZAR LA CONSULTA 
        EMITE UN MENSAJE EN UN SHOWWARNING PARA QUE SE COMPLETE ALGUN CRITERIO DE BUSQUEDA.
        EL CRITERIO DE BUSQUEDA VA A SER LA DESCRIPCION.
        """
        print("consultando registro")
        #valido si hay una descipcion antes de iniciar por si toca el boton sin ingresar datos
        if descripcion:
            productos = Producto.select().where(Producto.descripcion.contains(descripcion))
        else:
            messagebox.showwarning(
                    "Consulta", "Debe ingresar un criterio de búsqueda (Descripción)."
                    )
            return

        try:
            # Realizo la consulta filtrando por la descripción
            productos = Producto.select().where(Producto.descripcion.contains(descripcion))

            if not productos.exists():
                messagebox.showerror("Error", "No hay registros con la descripción proporcionada.")
                return
            # Limpio el Treeview antes de insertar nuevos registros
            self.limpiar_tree(arbol, entry_list)
            # inserto los registros en el Treeview
            for producto in productos: # me marca el error pero igual lo itera y funciona
                arbol.insert('', 'end', values=(
                    producto.id, producto.material, 
                    producto.descripcion, producto.precio_venta,
                    producto.precio_costo, producto.stock, producto.proveedor,
                    producto)
                    )
        except peewee.DoesNotExist:
            messagebox.showerror("Error", "No hay registros con la descripción proporcionada.")
        except peewee.PeeweeException as e:
            messagebox.showerror("Error", f"Error al acceder a la base de datos: {e}")
    
    @log_evento
    def borrar_registro(self, arbol, entry_list):
        """
        BORRA UN REGISTRO DE LA BASE DE DATOS.
        SE DEBE SELECCIONAR EL REGISTRO DESDE EL TREEVIEW Y LUEGO PRESIONAR EL BOTON BORRAR.
        ES NECESARIO REALIZAR UNA CONSULTA PRIMERO.
        EN CASO DE NO REALIZARLO EMITE UN MENSAJE DE WARNING 
        """
        print("borrando registro")
        try:
        # Obtengo el material del registro seleccionado en el Treeview
        # Si no se proporciona material, emite un mensaje de error
            selection = arbol.selection()
            if not selection:
                messagebox.showwarning("Borrar registro", "Selecciona un registro para eliminar.")
                return
            # Obtengo el elemento id del registro a borrar que fue seleccionado
            # Luego lo guardo en una variable el campo material del registro a borrar
            item = arbol.item(selection[0])
            material_a_borrar = item['values'][0]
            descripcion_del_material_borrado = item['values'][2]

            # Intento borrar el registro de la base de datos
            registro_borrado = Producto.get_by_id(material_a_borrar)
            registro_borrado.delete_instance()
            # Borro el registro del Treeview
            self.limpiar_tree(arbol, entry_list)

            messagebox.showinfo(
                "Borrar registro",
                f"""Registro con número de material {descripcion_del_material_borrado} 
                con ID '{material_a_borrar}'
                eliminado correctamente."""
            )
        except peewee.DoesNotExist:
            messagebox.showerror("Error", "No se encontró el registro en la base de datos.")
        except peewee.PeeweeException as e:
            messagebox.showerror("Error", f"Error al acceder a la base de datos: {e}")

    @log_evento
    def modificar_registro(
        self,
        arbol,
        material,
        descripcion,
        precio_venta,
        precio_costo,
        stock,
        proveedor,
        entry_list
    ):
        """
        MODIFICA UNO O VARIOS CAMPOS DE UN REGISTRO BASANDOSE EN EL NUMERO DE ID
        SE DEBE COMPLETAR LOS CAMPOS QUE SE QUIERAN MODIFICAR
        EMITE UN MENSAJE  SI NO SE HA SELECCIONADO NINGUN REGISTRO Y PARA MODIFICAR
        EMITE UN MENSAJE SI SE MODIFICO EL REGISTRO
        EMITE MENSAJE SI OCURRE UN ERROR DEL TIPO NO 
        EXISTE EL REGISTRO O NO SE COMPLETO NINGUN CAMPO
        """
        print("modificando registro")
        try:
        # Obtengo el material del registro seleccionado en el Treeview
        # Si no se proporciona material, emite un mensaje de error
            id_seleccionado = arbol.selection()
            if not id_seleccionado:
                messagebox.showerror("Modificar", "Debes seleccionar un registro")
                return

            id_seleccionado = arbol.item(id_seleccionado[0])['values'][0]
            print("ID", id_seleccionado)
            # Verifico si el registro con el ID proporcionado existe
            registro = Producto.get_or_none(Producto.id == id_seleccionado)
            # Si se validó el registro, se realiza la modificación
            if registro:
                # Actualizar los campos del registro
                if material:
                    registro.material = material
                if descripcion:
                    registro.descripcion = descripcion
                if precio_venta:
                    registro.precio_venta = float(precio_venta)
                if precio_costo:
                    registro.precio_costo = float(precio_costo)
                if stock:
                    registro.stock = int(stock)
                if proveedor:
                    registro.proveedor = proveedor
                # Guardar los cambios en la base de datos
                registro.save()
                # Mensaje de éxito
                messagebox.showinfo(
                    "Modificar",f"Registro con ID '{id_seleccionado}'modificado correctamente."
                    )
                # Limpiar el Treeview antes de insertar el registro modificado
                self.limpiar_tree(arbol, entry_list)
                # Insertar el registro modificado en el Treeview
                arbol.insert('', 'end', values=(
                    registro.id,
                    registro.material,
                    registro.descripcion,
                    registro.precio_venta,
                    registro.precio_costo,
                    registro.stock,
                    registro.proveedor)
                    )
            else:
                messagebox.showerror(
                    "Error", f"No se encontró ningún registro para el ID '{id_seleccionado}'."
                    )
        except peewee.DoesNotExist:
            messagebox.showerror(
                "Error", f"No se encontró ningún registro para el ID '{id_seleccionado}'."
                )
        except peewee.PeeweeException as e:
            messagebox.showerror("Error", f"Error al acceder a la base de datos: {e}")
        except ValueError as e:
            messagebox.showerror("Error", f"Error al convertir datos: {e}")

    def modo_oscuro(self, aplicacion):
        """
        CAMBIA EL FONDO DE LA APLICACION A GRIS
        """

        aplicacion.configure(background="grey")
        print("cambio a modo oscuro...")

    def modo_clasico(self, aplicacion):
        """
        CAMBIA EL FONDO DE LA APLICACION A BLANCO QUE ES EL MODO ORIGINAL
        """
        aplicacion.configure(background="white")
        print("cambio a modo clasico")

    def __str__(self):
        return "Ventana Principal, modulo que se encarga de controlar la aplicacion"
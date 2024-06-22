"""
Clase que se encarga de la parte grafica de la aplicacion
desarrollada con TKinter
"""

#from tkinter import *
from tkinter import ttk, StringVar, Menu, Label, Entry, Button, W, S
from PIL import Image, ImageTk
from controller import Controlador

# Clase principal de la vista de mi app
class POSApp:
    """
    Esta clase crea la interfaz gráfica de usuario para la aplicación
    Contiene los métodos y atributos que permiten interactuar con ella.
    """
    def __init__(self, raiz):
        self.raiz = raiz
        self.funciones = Controlador()

        # Las VARIABLES
        self.material_var = StringVar(value="0")
        self.descripcion_var = StringVar(value="descripcion")
        self.precio_venta_var = StringVar(value="0")
        self.precio_costo_var = StringVar(value="0")
        self.stock_var = StringVar(value="0")
        self.proveedor_var = StringVar(value="proveedor")

        # Titulo de la ventana
        self.raiz.title("POS base de materiales")
        # seteo del tamaño de la ventana
        self.raiz.geometry("1100x400")

        # MAQUETACION DEL MENU
        self.create_menu()

        # MAQUETACION DE LOS WIDGET
        self.create_widgets()

    def create_menu(self):
        """
        Método para crear el menu de la app.
        """
        menubar = Menu(self.raiz)
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(
            label="Exportar base",
            command=self.funciones.exportar_base
            )
        filemenu.add_command(
            label="Exportar consulta",
            command=lambda: self.funciones.exportar_consulta(self.tree)
            )
        tema_menu = Menu(filemenu, tearoff=False)
        tema_menu.add_command(
            label="Modo Oscuro",
            command=lambda: self.funciones.modo_oscuro(self.raiz)
            )
        tema_menu.add_command(
            label="Modo Clásico",
            command=lambda: self.funciones.modo_clasico(self.raiz)
            )
        filemenu.add_cascade(label="Tema", menu=tema_menu)
        filemenu.add_command(label="Salir", command=self.raiz.quit)
        menubar.add_cascade(label="Archivo", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=False)
        helpmenu.add_command(label="Guia", command=self.funciones.mostrar_ayuda)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)

        self.raiz.config(menu=menubar)

    def create_widgets(self):
        """
        Método para crear los entry y los label  que se mostrara en pantalla.
        """

        # MATERIAL
        label1 = Label(self.raiz, text="NUMERO DE MATERIAL", background="white")
        label1.place(x=260, y=20)
        self.entry1 = Entry(self.raiz, textvariable=self.material_var)
        self.entry1.place(x=400, y=20)

        # DESCRIPCION
        label2 = Label(self.raiz, text="DESCRIPCION", background="white")
        label2.place(x=260, y=50)
        self.entry2 = Entry(self.raiz, textvariable=self.descripcion_var)
        self.entry2.place(x=400, y=50)

        # PRECIO DE VENTA
        label3 = Label(self.raiz, text="PRECIO DE VENTA", background="white")
        label3.place(x=260, y=80)
        self.entry3 = Entry(self.raiz, width=10, textvariable=self.precio_venta_var)
        self.entry3.place(x=400, y=80)

        # PRECIOS DE COSTO
        label4 = Label(self.raiz, text="PRECIO DE COSTO", background="white")
        label4.place(x=260, y=110)
        self.entry4 = Entry(self.raiz, width=10, textvariable=self.precio_costo_var)
        self.entry4.place(x=400, y=110)

        # STOCK
        label5 = Label(self.raiz, text="STOCK", background="white")
        label5.place(x=260, y=140)
        self.entry5 = Entry(self.raiz, width=10, textvariable=self.stock_var)
        self.entry5.place(x=400, y=140)

        # PROVEEDOR
        label6 = Label(self.raiz, text="PROVEEDOR", background="white")
        label6.place(x=260, y=170)
        self.entry6 = Entry(self.raiz, textvariable=self.proveedor_var)
        self.entry6.place(x=400, y=170)

        # BOTONES
        button_width = 10
        button_height = 1

        # boton Consultar
        button1 = Button(
            self.raiz,
            text="Consultar",
            width=button_width,
            height=button_height,
            background="white",
            command=self.consultar_registro
            )
        button1.place(x=200, y=200)

        # boton alta
        button2 = Button(
            self.raiz,
            text="Alta",
            width=button_width,
            height=button_height,
            background="white",
            command=self.alta_registro
            )
        button2.place(x=300, y=200)

        # boton borrar
        button3 = Button(
            self.raiz,
            text="Borrar",
            width=button_width,
            height=button_height,
            background="white",
            command=self.borrar_registro
            )
        button3.place(x=400, y=200)

        # boton modificar
        button4 = Button(
            self.raiz,
            text="Modificar",
            width=button_width,
            height=button_height,
            background="white",
            command=self.modificar_registro
            )
        button4.place(x=500, y=200)

        # boton limpiar
        button5 = Button(
            self.raiz, text="Limpiar",
            width=button_width,
            height=button_height,
            background="white",
            command=self.limpiar_tree
            )
        button5.place(x=600, y=200)

        # TREEVIEW
        self.tree = ttk.Treeview(self.raiz)
        self.tree['show'] = 'headings'
        self.tree["columns"] = ("0", "1", "2", "3", "4", "5", "6")

        # Columnas del Treeview
        self.tree.column("0", width=50, anchor=W)
        self.tree.column("1", width=150, minwidth=150)
        self.tree.column("2", width=150, minwidth=150)
        self.tree.column("3", width=150, minwidth=150)
        self.tree.column("4", width=150, minwidth=150)
        self.tree.column("5", width=150, minwidth=150)
        self.tree.column("6", width=150, minwidth=150)

        # Encabezados de las columnas del Treeview
        self.tree.heading("0", text="ID")
        self.tree.heading("1", text="MATERIAL", anchor=W)
        self.tree.heading("2", text="DESCRIPCION", anchor=W)
        self.tree.heading("3", text="PRECIO DE VENTA", anchor=W)
        self.tree.heading("4", text="PRECIO DE COSTO", anchor=W)
        self.tree.heading("5", text="STOCK", anchor=W)
        self.tree.heading("6", text="PROVEEDOR", anchor=W)
        self.tree.place(relx=0.5, y=480, anchor=S, relwidth=1)

        # Cargar imágenes
        self.load_images()

    def load_images(self):
        """
        Método para cargary ubicar las imagenes en las etiquetas para mostrarlas en la app.
        """

        # Carga y coloca las imágenes en las etiquetas
        images = ["img/1.JPG"] * 6
        image_labels = []

        # imagenes chicas para las viñetas
        for i, img_path in enumerate(images, start=1):
            image = Image.open(img_path)
            image = image.resize((20, 20))
            photo = ImageTk.PhotoImage(image)
            image_label = Label(self.raiz, image=photo)
            image_label.image = photo
            image_label.place(x=220, y=-8 + 30 * i)
            image_labels.append(image_label)

        # Imagen grande, principal
        large_image = Image.open("img/1.JPG")
        large_image = large_image.resize((200, 150))
        large_photo = ImageTk.PhotoImage(large_image)
        large_image_label = Label(self.raiz, image=large_photo)
        large_image_label.image = large_photo
        large_image_label.place(x=580, y=25)
        # Guardo la referencia a la etiqueta en una variable global
        self.image_labels = image_labels
        self.large_image_label = large_image_label
    # funciones para llamar los metodos pasandoles argumentos para evitar usar mucho codigo.
    def consultar_registro(self):
        """
        Método que se encarga de buscar el registro del producto
        en base a los datos ingresados por el usuario.
        Obtengo los argumentos de los entry y los paso por parametros
        al método 'consultar_registro' de la clase 'Controlador'
        """
        self.funciones.consultar_registro(
            self.descripcion_var.get(),
            self.tree,
            [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6]
            )
    def alta_registro(self):
        """
        Método para agregar un registro a la base de datos.
        Utilizo el metodo 'alta_registro' de la clase 'Controlador' le paso
        los argumentos obtenidos de lo entry
        """
        self.funciones.alta_registro(
            self.material_var.get(),
            self.descripcion_var.get(),
            self.precio_venta_var.get(),
            self.precio_costo_var.get(),
            self.stock_var.get(),
            self.proveedor_var.get(),
            self.tree,
            [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6]
            )
    def borrar_registro(self):
        """
        Método para eleminar un registro de la base de datos. 
        Utilizo el metodo 'borrar_registro' de la clase 'Controlador'. 
        Paso por argumentos los valores obtenidos para borrar el registro
        que se selecciona del treeview.
        """
        self.funciones.borrar_registro(
            self.tree,
            [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6]
            )
    def modificar_registro(self):
        """
        Método para modificar un registro de la base de datos.
        utilizo el metodo 'modificar_registro' de la clase 'Controlador'
        paso por argumento los datos obtenidos de los entry.
        """
        self.funciones.modificar_registro(
            self.tree,
            self.material_var.get(),
            self.descripcion_var.get(),
            self.precio_venta_var.get(),
            self.precio_costo_var.get(),
            self.stock_var.get(),
            self.proveedor_var.get(),
            [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6]
            )
    def limpiar_tree(self):
        """
        Método para limpiar los entry.
        Paso por argumento al metodo 'limpiar_tree' de la clase 'Controlador'
        """
        self.funciones.limpiar_tree(
            self.tree,
            [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6]
            )

    def __str__(self):
        pass
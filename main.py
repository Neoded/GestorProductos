from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:
    db = "database/productos.db"
    objetos_carrito = []
    cantidad_objetos_carrito= []
    costos_carrito = []
    total_carrito= 0


    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")  # Titulo de la ventana
        self.ventana.resizable(1, 1)  # Redimension de ventana, este es el valor por defecto
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico")

        # Creacion del contenedor Frame Principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame)  # Caja para input de texto
        self.nombre.focus()  # Ubicar el foco del raton al inicio del programa
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Boton Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command = self.add_producto)
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W + E)

        self.mensaje = Label(text= "", fg= "red")
        self.mensaje.grid(row= 3, column= 0, columnspan=2, sticky= W + E)

        # Tabla de productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 11))
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 13, "bold"))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)  # Encabezado 0
        self.tabla.heading("#1", text="Precio", anchor=CENTER)  # Encabezado 1

        #Botones de Eliminar y Editar
        s_boton_eliminar= ttk.Style()
        s_boton_eliminar.configure("boton_eliminar.TButton", background= "red", foreground= "red")
        boton_eliminar = ttk.Button(text= "ELIMINAR", style= "boton_eliminar.TButton", command= self.del_producto)
        boton_eliminar.grid(row= 5, column= 0, sticky= W+ E)
        boton_editar = ttk.Button(text= "EDITAR", command= self.edit_producto)
        boton_editar.grid(row= 5, column= 1, sticky= W+ E)

        #Botones de Agregar a Carrito y Total
        s_boton_agc = ttk.Style()
        s_boton_agc.configure("boton_agc.TButton", background="blue", foreground="blue") #Aplicar estilo al boton
        boton_agc= ttk.Button(text= "AGREGAR A CARRITO", style= "boton_agc.TButton", command= self.agregar_carrito) #Boton AGregar a Carrito
        boton_agc.grid(row=6, column= 0, sticky= W + E)

        s_boton_total = ttk.Style()
        s_boton_total.configure("boton_total.TButton", background="green", foreground="green")  # Aplicar estilo al boton
        boton_total= ttk.Button(text= "TOTAL", style= "boton_total.TButton", command=self.total)
        boton_total.grid(row=6, column=1, sticky= W+ E)

        # Llamar al metodo get_productos para mostar los datos de la base de datos al inicio del programa
        self.get_productos()

    # Consulta a base de datos
    def una_db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            cursor.execute(consulta, parametros)  # Preparar la consulta SQL (con parametros si los hay)
            resultado = cursor.fetchone()
            con.commit()  # Ejecutar los cambios en la base de datos
        return resultado  # retornar el resultado de la consulta SQL

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)  # Preparar la consulta SQL (con parametros si los hay)
            con.commit()  # Ejecutar los cambios en la base de datos
        return resultado  # retornar el resultado de la consulta SQL

    def get_productos(self):
        # Limpiar la tabla
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        # Consulta SQL
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros = self.db_consulta(query)  # Se llama al metodo db_consultas

        #Mostrar los datos en la ventana de la app
        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text= fila[1], values = fila[2])

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio():
            query = "INSERT INTO producto VALUES (NULL, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"] = "Producto {} añadido con exito".format(self.nombre.get())
            self.nombre.delete(0, END) #Borrar ambos campos del formulario
            self.precio.delete(0, END)

            # Para debug
            #print(self.nombre.get())
            #print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        else:
            print("El nombre y el precio son oblitatorios")
            self.mensaje["text"] = "El nombre y el precio son obligatorios"

        self.get_productos() #Actualizar el contenido y ver los cambios

    def del_producto(self):
        # Debug
        #print(self.tabla.item(self.tabla.selection()))
        #print(self.tabla.item(self.tabla.selection())["text"])
        #print(self.tabla.item(self.tabla.selection())["values"])
        #print(self.tabla.item(self.tabla.selection())["values"][0])

        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return

        self.mensaje["text"] = ""
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?" #Consulta SQL
        self.db_consulta(query, (nombre,)) #Ejecutar la consulta
        self.mensaje["text"]= "Producto {} eliminado con exito".format(nombre)
        self.get_productos() #Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje["text"]= ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return

        nombre= self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]

        self.ventana_editar = Toplevel() #Crear una nueva ventana delante de la principal
        self.ventana_editar.title = "Editar Producto" #Titulo de la ventana
        self.ventana_editar.resizable(1,1) #Redimension de ventana
        self.ventana_editar.wm_iconbitmap("recursos/M6_P2_icon.ico") #Icono de la ventana

        titulo = Label(self.ventana_editar, text="Edicion de Productos", font=("Calibri", 50, "bold"))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text= "Editar el siguiente producto")
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text= "Nombre antiguo: ") #Etiqueta nombre antiguo
        self.etiqueta_nombre_antiguo.grid(row=2, column= 0) #Posicionamiento etiqueta
        #Entry nombre antiguo(texto no modificable)
        self.input_nombre_antiguo= Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value= nombre),
                                         state="readonly")
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text= "Nombre nuevo: ") #Etiqueta nombre nuevo
        self.etiqueta_nombre_nuevo.grid(row=3, column=0) #Posicionamiento etiqueta
        # Entry Nombre nuevo modificable
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus() #Foco del raton de la ventana Editar Producto

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text= "Precio antiguo: ") #Etiqueta precio antiguo
        self.etiqueta_precio_antiguo.grid(row=4, column= 0)
        # Entry precio antiguo no modificable
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state="readonly")
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio Nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text= "Precio nuevo")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        #Entry precio nuevo modificable
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)

        # Boton actualizar producto
        self.boton_actualizar = ttk.Button(frame_ep, text= "Actualizar Producto", command= lambda:
                                           self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                     self.input_nombre_antiguo.get(),
                                                                     self.input_precio_nuevo.get(),
                                                                     self.input_precio_antiguo.get()))
        self.boton_actualizar.grid(row=6, columnspan=2, sticky= W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio):
        producto_modificado= False
        query= "UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?"

        # Cambiar ambos si es usuario introduce nuevo nombre y nuevo precio
        if nuevo_nombre != "" and nuevo_precio != "":

            parametros= (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True

        # Mantener el precio anterior si no se introduce nuevo precio
        elif nuevo_nombre != "" and nuevo_precio == "":
            parametros= (nuevo_nombre, antiguo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado= True

        #Mantener el nombre anterior si no se introduce nuevo nombre
        elif nuevo_nombre == "" and nuevo_precio != "":
            parametros= (antiguo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado= True

        if(producto_modificado):
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje["text"] = "El producto {} ha sido actualizado con exito".format(antiguo_nombre) # Mensaje para el usuario
            self.get_productos()
        else:
            self.ventana_editar.destroy() #Cerrar la ventana de edicion de productos
            self.mensaje["text"] = "El producto {} NO ha sido actualizado".format(antiguo_nombre) # Mensaje para el usuario

    def agregar_carrito(self):
        self.mensaje["text"]= ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return

        producto= self.tabla.item(self.tabla.selection())["text"]
        precio= float(self.tabla.item(self.tabla.selection())["values"][0])

        def agc():  # agregar a carrito
            self.objetos_carrito.append(producto)
            self.cantidad_objetos_carrito.append(int(self.input_cantidad.get()))
            self.costos_carrito.append(int(self.input_cantidad.get()) * precio)
            self.total_carrito += (int(self.input_cantidad.get()) * precio)

            self.mensaje["text"] = "Se agregaron {} unidades de '{}' al carrito de compras.".format(self.input_cantidad.get(),
                                                                                                  producto)

            cancelar()

        def cancelar():
            self.ventana_carrito.destroy()


        self.ventana_carrito = Toplevel()  # Crear una nueva ventana delante de la principal
        self.ventana_carrito.title("Agregar al Carrito de Compras")  # Titulo de la ventana
        self.ventana_carrito.resizable(1, 1)  # Redimension de ventana
        self.ventana_carrito.wm_iconbitmap("recursos/shoppingcart.ico")  # Icono de la ventana



        titulo = Label(self.ventana_carrito, text="Agregar '{}' al carrito de compras".format(producto), font=("Calibri", 20, "bold"))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de agregar al carrito de compras
        frame_agc = LabelFrame(self.ventana_carrito, text="Cantidad")
        frame_agc.grid(row=1, column=0, columnspan=10, pady=20)

        # Label Cantidad
        self.etiqueta_cantidad = Label(frame_agc, text="Cantidad: ")  # Etiqueta nombre antiguo
        self.etiqueta_cantidad.grid(row=2, column=0)  # Posicionamiento etiqueta
        # Entry nombre antiguo(texto no modificable)
        self.input_cantidad = Entry(frame_agc)
        self.input_cantidad.grid(row=2, column=1)
        self.input_cantidad.focus()

        # Boton agregar al carrito ---> ac
        boton_ac = ttk.Button(frame_agc, text="AGREGAR AL CARRITO", style="boton_agc.TButton", command= agc)
        boton_ac.grid(row=3, columnspan=2, sticky= W + E)

        # Boton cancelar
        boton_cancelar = ttk.Button(frame_agc, text= "CANCELAR", style= "boton_eliminar.TButton", command=cancelar)
        boton_cancelar.grid(row=4, columnspan=2, sticky= W + E)

    def total(self):
        #Devolver un mensaje si el carrito de compras esta vacio
        if self.total_carrito== 0:
            self.mensaje["text"] = "El carrito de compras esta vacio"
            return
        else:
            self.ventana_total = Toplevel()  # Crear una nueva ventana delante de la principal
            self.ventana_total.title("Su Carrito de Compras")  # Titulo de la ventana
            self.ventana_total.resizable(1, 1)  # Redimension de ventana
            self.ventana_total.wm_iconbitmap("recursos/shoppingcart.ico")  # Icono de la ventana

            titulo = Label(self.ventana_total, text="CARRITO DE COMPRAS", font=("Calibri", 20, "bold"))
            titulo.grid(column=0, row=0)

            #Estructura de la tabla carrito de compras
            columnas = ["Cantidad","Producto", "Precio por Unidad", "Precio Total"]
            self.tabla_total = ttk.Treeview(self.ventana_total, height=20, columns=columnas[0:3])
            self.tabla_total.grid(column=0, row=1, columnspan=4, sticky= W + E)
            self.tabla_total.heading("#0", text= "Cantidad", anchor=CENTER)  # Encabezado 0
            self.tabla_total.heading("#1", text="Producto", anchor=CENTER)  # Encabezado 1
            self.tabla_total.heading("#2", text= "Precio por Unidad", anchor=CENTER) # Encabezado 2
            self.tabla_total.heading("#3", text= "Precio total", anchor=CENTER) # Encabezado 3

            # Limpiar la tabla
            registros_tabla_total = self.tabla_total.get_children()
            for fila in registros_tabla_total:
                self.tabla.delete(fila)



            # Mostrar los datos en la ventana de la app
            for i, dato in enumerate(self.objetos_carrito):
                producto =  self.objetos_carrito[i]
                # Consulta SQL
                query = 'SELECT precio FROM producto WHERE nombre = ?'
                registro = self.una_db_consulta(query, (producto,))  # Se llama al metodo db_consultas
                print(self.objetos_carrito[i],self.cantidad_objetos_carrito[i],self.costos_carrito[i])
                self.tabla_total.insert("", 0, text=self.objetos_carrito[i],
                                        values=(self.cantidad_objetos_carrito[i],
                                                registro,
                                                self.costos_carrito[i]))

            total = Label(self.ventana_total, text="Total", font=("Calibri", 15, "bold"))
            total.grid(column=1, row=2, sticky= E)

            total_carrito = Label(self.ventana_total, text= self.total_carrito, font=("Calibri", 15))
            total_carrito.grid(column= 2, row=2, sticky= E)


# Programa principal
if __name__ == "__main__":
    root = Tk()  # Instancia de la ventana principal
    app = Producto(root)
    root.mainloop()  # Bucle para mantener la ventana abierta hasta que finalice el usuario

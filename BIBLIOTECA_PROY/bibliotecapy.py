from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from navegacion import VentanaBase
from src.Consulta import buscar_libros
from src.Usuario import registrar_usuario


class MainConsulta(VentanaBase):
    def buscar_y_mostrar(self, **criterios):
        encontrados = buscar_libros(**criterios)

        if not encontrados:
            QMessageBox.information(
                self,
                "Sin resultados",
                "No se encontraron libros con esos datos.",
            )
            return

        partes = []
        for campo, valor in criterios.items():
            valor = str(valor or "").strip()
            if not valor:
                continue
            if campo == "estado" and valor.upper() == "TODOS":
                continue
            partes.append(valor)

        self.ir_a(ListaConsulta, libros=encontrados, criterios=" · ".join(partes))


class MainConsultaUsuario(MainConsulta):
    archivo_ui = "main_consulta_us.ui"

    def preparar(self):
        self.btnBuscar.clicked.connect(self.buscar)
        for caja in (self.txtProducto, self.txtNombre, self.txtAutor):
            caja.returnPressed.connect(self.buscar)

    def buscar(self):
        self.buscar_y_mostrar(
            producto=self.txtProducto.text().strip(),
            nombre=self.txtNombre.text().strip(),
            autor=self.txtAutor.text().strip(),
        )


class MainConsultaAdmin(MainConsulta):
    archivo_ui = "main_consulta_adm.ui"

    def preparar(self):
        self.btnBuscar.clicked.connect(self.buscar)
        for caja in (self.txtProducto, self.txtNombre, self.txtAutor):
            caja.returnPressed.connect(self.buscar)

    def buscar(self):
        self.buscar_y_mostrar(
            producto=self.txtProducto.text().strip(),
            nombre=self.txtNombre.text().strip(),
            autor=self.txtAutor.text().strip(),
            estado=self.cmbEstado.currentText().strip(),
        )


class ListaConsulta(VentanaBase):
    archivo_ui = "list_consulta.ui"

    def __init__(self, anterior=None, libros=None, criterios=""):
        self.libros = libros or []
        self.criterios = criterios
        super().__init__(anterior=anterior)

    def preparar(self):
        self.pushButton.clicked.connect(self.volver)

        if self.criterios:
            self.setWindowTitle(f"Resultados: {len(self.libros)} · {self.criterios}")
        else:
            self.setWindowTitle(f"Resultados: {len(self.libros)}")

        self.llenar_tabla()

    def llenar_tabla(self):
        tabla = self.tableWidget
        tabla.setRowCount(len(self.libros))

        for fila, libro in enumerate(self.libros):
            stock = libro.get("stock", 0)
            valores = (
                str(fila + 1),
                libro.get("tipo", ""),
                libro.get("nombre", ""),
                libro.get("autor", ""),
                str(stock),
                "SÍ" if stock > 0 else "NO",
            )
            for columna, valor in enumerate(valores):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

        tabla.resizeColumnsToContents()


class loginUsuario(VentanaBase):
    archivo_ui = "login_usuario.ui"

    def preparar(self):
        self.btnIniciar.clicked.connect(self.ini_sesion)
        self.txtNombre.returnPressed.connect(self.ini_sesion)
        self.txtDni.returnPressed.connect(self.ini_sesion)

    def ini_sesion(self):
        nombre = self.txtNombre.text().strip()
        dni = self.txtDni.text().strip()

        if not nombre or not dni:
            QMessageBox.warning(self, "Errorrrrrrrr", "Complete nombre y DNI")
            return

        if not registrar_usuario(nombre, dni):
            QMessageBox.warning(
                self,
                "Errorrrrrrrr",
                "Ese DNI no coincide con el usuario registrado",
            )
            return

        self.ir_a(MainConsultaUsuario)


class loginAdmin(VentanaBase):
    archivo_ui = "login_admin.ui"

    def preparar(self):
        self.btnIniciar.clicked.connect(self.ini_sesion)

    def ini_sesion(self):
        nombre = self.txtNombre.text().strip()
        contrasena = self.txtContrasena.text().strip()

        if not nombre or not contrasena:
            QMessageBox.warning(self, "Errorrrrrrrr", "Complete todo los campos")
            return

        else:
            self.ir_a(MainConsultaAdmin)


class login(VentanaBase):
    archivo_ui = "login.ui"

    def preparar(self):
        # Configurar el título de la ventana.
        self.setWindowTitle("Sistema de Biblioteca - Inicio de Sesión")

        # Conectar los botones a sus respectivas ventanas
        self.btnUsuario.clicked.connect(self.abrir_login_usuario)
        self.btnAdmin.clicked.connect(self.abrir_login_admin)

    def abrir_login_usuario(self):
        self.ir_a(loginUsuario)

    def abrir_login_admin(self):
        self.ir_a(loginAdmin)

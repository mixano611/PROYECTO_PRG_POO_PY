from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from navegacion import VentanaBase
from src.Admin import validar_admin
from src.Almacen import cargar_datos, guardar_datos
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

    # Columna de la tabla -> campo correspondiente en Almacen.json
    COLUMNAS_EDITABLES = {1: "tipo", 2: "nombre", 3: "autor", 4: "stock"}

    def __init__(self, anterior=None, libros=None, criterios=""):
        self.libros = libros or []
        self.criterios = criterios
        super().__init__(anterior=anterior)

    def preparar(self):
        # En este diseño el botón BACK se llama pushButton.
        self.pushButton.clicked.connect(self.volver)
        self.btnGuardar.clicked.connect(self.guardar_cambios)

        if self.criterios:
            self.setWindowTitle(f"Resultados: {len(self.libros)} · {self.criterios}")
        else:
            self.setWindowTitle(f"Resultados: {len(self.libros)}")

        self.llenar_tabla()

    def llenar_tabla(self):
        tabla = self.tableWidget
        tabla.setRowCount(len(self.libros))
        self.original = []

        for fila, libro in enumerate(self.libros):
            stock = int(libro.get("stock", 0) or 0)
            valores = (
                str(fila + 1),
                libro.get("tipo", ""),
                libro.get("nombre", ""),
                libro.get("autor", ""),
                str(stock),
                "SÍ" if stock > 0 else "NO",
            )

            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                # N° y DISPONIBLE se calculan solos: no se editan.
                if columna not in self.COLUMNAS_EDITABLES:
                    item.setFlags(
                        Qt.ItemFlags()
                        | Qt.ItemFlag.ItemIsEnabled
                        | Qt.ItemFlag.ItemIsSelectable
                    )
                tabla.setItem(fila, columna, item)

            # Foto de cómo estaban los datos al abrir la ventana.
            self.original.append(
                {
                    "id": libro.get("id"),
                    "tipo": str(libro.get("tipo", "")),
                    "nombre": str(libro.get("nombre", "")),
                    "autor": str(libro.get("autor", "")),
                    "stock": stock,
                }
            )

        tabla.resizeColumnsToContents()

    def _texto(self, fila, columna):
        item = self.tableWidget.item(fila, columna)
        return item.text().strip() if item else ""

    def guardar_cambios(self):
        """Escribe en Almacen.json lo que se editó en la tabla."""
        cambios = []

        for fila, antes in enumerate(self.original):
            texto_stock = self._texto(fila, 4)

            try:
                stock = int(texto_stock)
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Stock inválido",
                    f"El stock de la fila {fila + 1} debe ser un número entero.",
                )
                return

            if stock < 0:
                QMessageBox.warning(
                    self,
                    "Stock inválido",
                    f"El stock de la fila {fila + 1} no puede ser negativo.",
                )
                return

            despues = {
                "tipo": self._texto(fila, 1),
                "nombre": self._texto(fila, 2),
                "autor": self._texto(fila, 3),
                "stock": stock,
            }

            if despues != {campo: antes[campo] for campo in despues}:
                cambios.append((fila, antes["id"], despues))

        if not cambios:
            QMessageBox.information(
                self,
                "Sin cambios",
                "No se pudo guardar porque no hay ningún cambio.",
            )
            return

        datos = cargar_datos()
        libros = datos["libros"]

        for fila, id_libro, despues in cambios:
            libro = next(
                (libro for libro in libros if libro.get("id") == id_libro),
                None,
            )
            if libro is None:
                continue

            libro.update(despues)
            self.actualizar_fila(fila, despues)

        guardar_datos(datos)

        # Lo guardado pasa a ser el nuevo punto de comparación, así un
        # segundo GUARDAR sin editar nada dirá que no hay cambios.
        for fila, _, despues in cambios:
            self.original[fila].update(despues)

        QMessageBox.information(self, "Guardado", "Se guardó exitosamente.")

    def actualizar_fila(self, fila, valores):
        """Refresca el stock normalizado y la columna DISPONIBLE."""
        self.tableWidget.item(fila, 4).setText(str(valores["stock"]))
        self.tableWidget.item(fila, 5).setText("SÍ" if valores["stock"] > 0 else "NO")


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

        self.ir_a(libros)

class libros(VentanaBase):
    archivo_ui = "aver.ui"
    
    def preparar(self):
        self.BntVolver.clicked.connect(self.volver)




class loginAdmin(VentanaBase):
    archivo_ui = "login_admin.ui"

    def preparar(self):
        self.btnIniciar.clicked.connect(self.ini_sesion)
        self.txtNombre.returnPressed.connect(self.ini_sesion)
        self.txtContrasena.returnPressed.connect(self.ini_sesion)

    def ini_sesion(self):
        nombre = self.txtNombre.text().strip()
        contrasena = self.txtContrasena.text().strip()

        # Solo entran las cuentas escritas en data/admin_data.json.
        if not validar_admin(nombre, contrasena):
            QMessageBox.warning(
                self,
                "Acceso denegado",
                "Nombre o contraseña incorrectos.",
            )
            return

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

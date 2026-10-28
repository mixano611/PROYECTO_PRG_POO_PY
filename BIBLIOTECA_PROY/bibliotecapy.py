from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import QEasingCurve, QEvent, QPropertyAnimation, Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
    QMessageBox,
    QPushButton,
    QTableWidgetItem,
)

from navegacion import VentanaBase
from src.Admin import validar_admin
from src.Almacen import cargar_datos, guardar_datos
from src.Consulta import buscar_libros
from src.Usuario import registrar_usuario

# Carpeta donde están las portadas de los libros.
RUTA_IMAGENES = Path(__file__).resolve().parent / "assets" / "images"


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


class MainConsultaAdmin(MainConsulta):
    archivo_ui = "main_consulta_admin.ui"

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

        self.ir_a(libros, usuario=nombre)


class libros(VentanaBase):
    """Catálogo: cada portada es el botón que abre el detalle del libro."""

    archivo_ui = "aver.ui"

    # Píxeles que crece la portada al pasar el mouse por encima.
    ZOOM_PORTADA = 6

    def __init__(self, anterior=None, usuario=None):
        # Se guarda el nombre del usuario para registrarlo en cada pedido.
        self.usuario = usuario
        self.animaciones = {}
        self.geometrias = {}
        self.libros_por_portada = {}
        super().__init__(anterior=anterior)

    def preparar(self):
        self.setWindowTitle("Biblioteca - Catálogo")

        # Se lee el JSON una sola vez para todas las portadas.
        libros = cargar_datos()["libros"]

        # Cada portada abre el detalle del libro que muestra.
        for numero in range(1, 17):
            portada = getattr(self, f"Cover{numero}", None)
            if isinstance(portada, QPushButton):
                self.preparar_portada(portada, libros)
                portada.clicked.connect(self.abrir_detalle)

    def preparar_portada(self, portada, libros):
        """Pone la imagen del libro y activa la animación al pasar el mouse."""
        portada.setCursor(Qt.CursorShape.PointingHandCursor)
        portada.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.geometrias[portada] = portada.geometry()
        portada.installEventFilter(self)

        # El campo "portada" del JSON dice qué portada muestra cada libro.
        libro = next(
            (
                libro
                for libro in libros
                if libro.get("portada") == portada.objectName()
            ),
            None,
        )
        if libro is None:
            return

        self.libros_por_portada[portada] = libro.get("id")

        if libro.get("imagen"):
            ruta = (RUTA_IMAGENES / str(libro["imagen"])).as_posix()
            portada.setStyleSheet(
                "QPushButton { border: none; background: transparent;"
                f' border-image: url("{ruta}") 0 0 0 0 stretch stretch; }}'
            )

    def abrir_detalle(self, checked=False):
        """Abre el detalle del libro de la portada presionada."""
        portada = self.sender()
        if not isinstance(portada, QPushButton):
            return

        id_libro = self.libros_por_portada.get(portada)
        if id_libro is None:
            return

        self.ir_a(catalogo, id_libro=id_libro, usuario=self.usuario)

    def eventFilter(self, objeto, evento):
        if objeto in self.geometrias:
            if evento.type() == QEvent.Type.Enter:
                self.animar_portada(objeto, entrar=True)
            elif evento.type() == QEvent.Type.Leave:
                self.animar_portada(objeto, entrar=False)

        return super().eventFilter(objeto, evento)

    def animar_portada(self, portada, entrar):
        """Crece la portada y le pone un brillo morado, estilo catálogo."""
        base = self.geometrias[portada]
        zoom = self.ZOOM_PORTADA

        # Se reutiliza una sola animación por portada: así nunca queda una
        # referencia a un objeto ya eliminado por Qt.
        animacion = self.animaciones.get(portada)
        if animacion is None:
            animacion = QPropertyAnimation(portada, b"geometry", self)
            animacion.setDuration(170)
            animacion.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.animaciones[portada] = animacion

        animacion.stop()

        if entrar:
            destino = base.adjusted(-zoom, -zoom, zoom, zoom)
            portada.raise_()
            self.aplicar_brillo(portada)
        else:
            destino = base
            self.quitar_brillo(portada)

        animacion.setStartValue(portada.geometry())
        animacion.setEndValue(destino)
        animacion.start()

    def aplicar_brillo(self, portada):
        brillo = QGraphicsDropShadowEffect(portada)
        brillo.setBlurRadius(34)
        brillo.setOffset(0, 0)
        brillo.setColor(QColor(124, 77, 255, 235))
        portada.setGraphicsEffect(brillo)

    def quitar_brillo(self, portada):
        portada.setGraphicsEffect(None)


class catalogo(VentanaBase):
    """Detalle de un libro: portada, autor, precio, descripción y cantidad."""

    archivo_ui = "menu_com-res.ui"

    def __init__(self, anterior=None, id_libro=None, usuario=None):
        self.id_libro = id_libro
        self.usuario = usuario
        self.libro = None
        self.precio_unitario = 0.0
        super().__init__(anterior=anterior)

    def preparar(self):
        self.setWindowTitle("Biblioteca - Detalle del libro")

        self.pushButton.clicked.connect(lambda: self.registrar_pedido("COMPRA"))
        self.pushButton_2.clicked.connect(lambda: self.registrar_pedido("RESERVA"))
        self.spinBox.valueChanged.connect(self.actualizar_total)

        self.configurar_contenido(self.id_libro)

    def configurar_contenido(self, id_libro):
        """Busca en Almacen.json el libro por su id."""
        self.id_libro = id_libro

        self.libro = next(
            (
                libro
                for libro in cargar_datos()["libros"]
                if libro.get("id") == id_libro
            ),
            None,
        )

        if self.libro is None:
            self.LblTitulo.setText("No disponible")
            self.LblAutor.setText("")
            self.LblPrecio.setText("S/ 0.00")
            self.LblTotal.setText("Total: S/ 0.00")
            self.LblDescripcion.setText(
                "No se encontraron detalles para este libro."
            )
            self.LblFoto.clear()
            self.spinBox.setMinimum(0)
            self.spinBox.setMaximum(0)
            self.spinBox.setValue(0)
            self.spinBox.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            return

        self.precio_unitario = float(self.libro.get("precio", 0) or 0)
        stock = int(self.libro.get("stock", 0) or 0)

        self.LblTitulo.setText(str(self.libro.get("nombre", "")))
        self.LblAutor.setText(str(self.libro.get("autor", "")))
        self.LblDescripcion.setText(
            str(self.libro.get("descripcion", "Sin descripción."))
        )
        self.cargar_imagen(self.libro.get("imagen"))

        # La cantidad nunca baja de 1 ni supera el stock disponible.
        self.spinBox.setMinimum(1 if stock > 0 else 0)
        self.spinBox.setMaximum(max(stock, 0))
        self.spinBox.setValue(1 if stock > 0 else 0)
        self.spinBox.setEnabled(stock > 0)

        self.pushButton.setEnabled(stock > 0)
        self.pushButton_2.setEnabled(stock > 0)

        # El precio siempre se muestra; si no hay stock se avisa aparte.
        self.LblPrecio.setText(f"S/ {self.precio_unitario:.2f}")

        if stock > 0:
            self.actualizar_total()
        else:
            self.LblTotal.setText("AGOTADO: sin ejemplares disponibles.")

    def cargar_imagen(self, nombre_imagen):
        """Muestra la portada; si falta el archivo, deja el espacio vacío."""
        imagen = QPixmap(str(RUTA_IMAGENES / str(nombre_imagen or "")))
        if imagen.isNull():
            self.LblFoto.clear()
            return
        self.LblFoto.setPixmap(imagen)

    def actualizar_total(self, *args):
        if self.libro is None or self.spinBox.value() <= 0:
            self.LblTotal.setText("Total: S/ 0.00")
            return

        total = self.precio_unitario * self.spinBox.value()
        self.LblTotal.setText(f"Total: S/ {total:.2f}")

    def registrar_pedido(self, tipo):
        """Agrega el pedido a la lista "pedidos" sin tocar el inventario."""
        if self.libro is None:
            QMessageBox.warning(
                self,
                "Sin libro",
                "No se encontró la información de este libro.",
            )
            return

        cantidad = self.spinBox.value()
        if cantidad <= 0:
            QMessageBox.warning(
                self,
                "Cantidad inválida",
                "Selecciona al menos un ejemplar.",
            )
            return

        datos = cargar_datos()
        libro_actual = next(
            (
                libro
                for libro in datos["libros"]
                if libro.get("id") == self.libro.get("id")
            ),
            None,
        )

        if libro_actual is None:
            QMessageBox.warning(
                self,
                "Sin libro",
                "El libro ya no está disponible en el almacén.",
            )
            return

        stock = int(libro_actual.get("stock", 0) or 0)
        if cantidad > stock:
            QMessageBox.warning(
                self,
                "Stock insuficiente",
                f"Solo quedan {stock} ejemplar(es) disponibles.",
            )
            return

        precio = float(libro_actual.get("precio", 0) or 0)
        total = precio * cantidad

        pedido = {
            "id_libro": libro_actual.get("id"),
            "nombre": libro_actual.get("nombre", ""),
            "autor": libro_actual.get("autor", ""),
            "precio": precio,
            "cantidad": cantidad,
            "total": total,
            "tipo": tipo,
            "usuario": self.usuario or "invitado",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # "pedidos" es una lista aparte de "libros": el administrador no la ve.
        datos.setdefault("pedidos", []).append(pedido)
        guardar_datos(datos)

        QMessageBox.information(
            self,
            "Pedido registrado",
            f"Se registró tu {tipo.lower()} de {cantidad} ejemplar(es) de "
            f"\"{libro_actual.get('nombre', '')}\".\nTotal: S/ {total:.2f}",
        )


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

from pathlib import Path

from PyQt5.QtCore import QEasingCurve, QEvent, QPropertyAnimation, Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import (
    QComboBox,
    QGraphicsDropShadowEffect,
    QMessageBox,
    QPushButton,
    QTableWidgetItem,
)

from navegacion import VentanaBase
from src.Admin import validar_admin
from src.Almacen import cargar_datos, guardar_datos
from src.Busqueda import construir_libros
from src.Carrito import cargar_carrito, guardar_carrito
from src.Consulta import buscar_libros
from src.Excepciones import BibliotecaError, DatosInvalidosError
from src.Membresia import (
    TELEFONO_ATENCION,
    aprobar_solicitud,
    aviso_vencimiento,
    construir_usuario,
    crear_solicitud,
    listar_miembros,
    listar_solicitudes,
    marcar_notificado,
    notificacion_pendiente,
    quitar_miembro,
    rechazar_solicitud,
    renovar_miembro,
    texto_notificacion,
)
from src.Modelos import (
    COMPRA,
    PRESTAMO,
    Libro,
    MapaBiblioteca,
)
from src.Operaciones import (
    cargar_cajas,
    finalizar_compra,
    guardar_cajas,
    listar_movimientos,
    registrar_devolucion,
    resumen,
)
from src.Usuario import registrar_usuario

# Carpeta donde están las portadas de los libros.
RUTA_IMAGENES = Path(__file__).resolve().parent / "assets" / "images"

# Estilos que se aplican en tiempo de ejecución.
ESTILO_BOTON = (
    "QPushButton{border:1px solid #000000;border-radius:8px;"
    "background-color:#BBAFDB;color:black;font-size:11px;cursor:pointer;}"
    "QPushButton:hover{background-color:#8E7CC3;}"
)

ESTILO_CAJA_ABIERTA = (
    "QPushButton{border:2px solid #000000;border-radius:10px;"
    "background-color:#8FD19E;color:black;font-size:13px;}"
)
ESTILO_CAJA_CERRADA = (
    "QPushButton{border:2px solid #000000;border-radius:10px;"
    "background-color:#E39A9A;color:black;font-size:13px;}"
)


def _item_solo_lectura(texto) -> QTableWidgetItem:
    """Crea una celda que se puede seleccionar pero no editar."""
    item = QTableWidgetItem(str(texto))
    item.setFlags(
        Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
    )
    return item


def _celda_editable(texto) -> QTableWidgetItem:
    return QTableWidgetItem(str(texto))


class MainConsulta(VentanaBase):
    """Parte común de las consultas del administrador."""

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
        self.setWindowTitle("Panel del administrador")
        self.btnBuscar.clicked.connect(self.buscar)
        for caja in (self.txtProducto, self.txtNombre, self.txtAutor):
            caja.returnPressed.connect(self.buscar)

        self.btnNuevoLibro.clicked.connect(self.abrir_nuevo_libro)
        self.btnMembresias.clicked.connect(self.abrir_membresias)
        self.btnCajas.clicked.connect(self.abrir_cajas)
        self.btnReportes.clicked.connect(self.abrir_reportes)

        # Menús que ya existían en el diseño.
        if hasattr(self, "actionCOMPRAS"):
            self.actionCOMPRAS.triggered.connect(
                lambda _checked=False: self.abrir_reportes("COMPRA")
            )
        if hasattr(self, "actionRENTADAS"):
            self.actionRENTADAS.triggered.connect(
                lambda _checked=False: self.abrir_reportes("PRESTAMO")
            )

    def buscar(self):
        self.buscar_y_mostrar(
            producto=self.txtProducto.text().strip(),
            nombre=self.txtNombre.text().strip(),
            autor=self.txtAutor.text().strip(),
            estado=self.cmbEstado.currentText().strip(),
        )

    def abrir_nuevo_libro(self):
        self.ir_a(RegistrarLibro)

    def abrir_membresias(self):
        self.ir_a(SolicitudesAdmin)

    def abrir_cajas(self):
        self.ir_a(CajasAdmin)

    def abrir_reportes(self, filtro=None):
        self.ir_a(ReportesAdmin, filtro=filtro)


class ListaConsulta(VentanaBase):
    archivo_ui = "list_consulta.ui"

    def __init__(self, anterior=None, libros=None, criterios=""):
        self.libros = libros or []
        self.criterios = criterios
        self.original = []
        super().__init__(anterior=anterior)

    def preparar(self):
        # En este diseño el botón BACK se llama pushButton.
        self.pushButton.clicked.connect(self.volver)
        self.btnGuardar.clicked.connect(self.guardar_cambios)
        self.btnEliminar.clicked.connect(self.eliminar_libro)

        if self.criterios:
            self.setWindowTitle(f"Resultados: {len(self.libros)} · {self.criterios}")
        else:
            self.setWindowTitle(f"Resultados: {len(self.libros)}")

        if hasattr(self, "actionCOMPRADAS"):
            self.actionCOMPRADAS.triggered.connect(
                lambda _checked=False: self.ir_a(ReportesAdmin, filtro="COMPRA")
            )
        if hasattr(self, "actionALQUILADAS"):
            self.actionALQUILADAS.triggered.connect(
                lambda _checked=False: self.ir_a(ReportesAdmin, filtro="PRESTAMO")
            )

        self.llenar_tabla()

    def llenar_tabla(self):
        tabla = self.tableWidget
        tabla.setRowCount(0)
        tabla.setRowCount(len(self.libros))
        self.original = []

        for fila, libro in enumerate(self.libros):
            stock = int(libro.get("stock", 0) or 0)
            precio = float(libro.get("precio", 0) or 0)
            descripcion = str(libro.get("descripcion", ""))

            tabla.setItem(fila, 0, _item_solo_lectura(fila + 1))
            tabla.setItem(fila, 1, _celda_editable(libro.get("tipo", "")))
            tabla.setItem(fila, 2, _celda_editable(libro.get("nombre", "")))
            tabla.setItem(fila, 3, _celda_editable(libro.get("autor", "")))
            tabla.setItem(fila, 4, _celda_editable(stock))
            tabla.setItem(fila, 5, _celda_editable(f"{precio:.2f}"))
            tabla.setItem(fila, 6, _celda_editable(descripcion))
            tabla.setItem(
                fila, 7, _item_solo_lectura("SÍ" if stock > 0 else "NO")
            )

            # Foto de cómo estaban los datos al abrir la ventana.
            self.original.append(
                {
                    "id": libro.get("id"),
                    "tipo": str(libro.get("tipo", "")),
                    "nombre": str(libro.get("nombre", "")),
                    "autor": str(libro.get("autor", "")),
                    "stock": stock,
                    "precio": round(precio, 2),
                    "descripcion": descripcion,
                }
            )

        tabla.verticalHeader().setVisible(False)
        # Anchos fijos para que la descripción no empuje la columna DISPONIBLE.
        for columna, ancho in enumerate((40, 80, 180, 170, 60, 80, 260, 90)):
            tabla.setColumnWidth(columna, ancho)

    def _texto(self, fila, columna):
        item = self.tableWidget.item(fila, columna)
        return item.text().strip() if item else ""

    def guardar_cambios(self):
        """Escribe en Almacen.json lo que se editó en la tabla."""
        cambios = []

        for fila, antes in enumerate(self.original):
            try:
                stock = int(self._texto(fila, 4))
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

            try:
                precio = float(self._texto(fila, 5).replace(",", "."))
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Precio inválido",
                    f"El precio de la fila {fila + 1} debe ser un número.",
                )
                return

            if precio < 0:
                QMessageBox.warning(
                    self,
                    "Precio inválido",
                    f"El precio de la fila {fila + 1} no puede ser negativo.",
                )
                return

            despues = {
                "tipo": self._texto(fila, 1),
                "nombre": self._texto(fila, 2),
                "autor": self._texto(fila, 3),
                "stock": stock,
                "precio": round(precio, 2),
                "descripcion": self._texto(fila, 6),
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
        self.tableWidget.item(fila, 5).setText(f"{valores['precio']:.2f}")
        self.tableWidget.item(fila, 7).setText(
            "SÍ" if valores["stock"] > 0 else "NO"
        )

    def eliminar_libro(self):
        """Elimina del almacén el libro seleccionado."""
        fila = self.tableWidget.currentRow()
        if fila < 0 or fila >= len(self.original):
            QMessageBox.warning(
                self,
                "Sin selección",
                "Selecciona el libro que quieres eliminar.",
            )
            return

        nombre = self.original[fila].get("nombre", "")
        respuesta = QMessageBox.question(
            self,
            "Eliminar libro",
            f"¿Eliminar \"{nombre}\" del almacén?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if respuesta != QMessageBox.Yes:
            return

        datos = cargar_datos()
        id_libro = self.original[fila]["id"]
        datos["libros"] = [
            libro for libro in datos["libros"] if libro.get("id") != id_libro
        ]
        guardar_datos(datos)

        self.tableWidget.removeRow(fila)
        self.original.pop(fila)
        if fila < len(self.libros):
            self.libros.pop(fila)

        # Se renumeran las filas que quedaron.
        for indice in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(indice, 0)
            if item is not None:
                item.setText(str(indice + 1))

        QMessageBox.information(
            self, "Eliminado", f"Se eliminó \"{nombre}\" del almacén."
        )


class loginUsuario(VentanaBase):
    archivo_ui = "login_usuario.ui"

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Usuario")
        self.btnIniciar.clicked.connect(self.ini_sesion)
        self.txtNombre.returnPressed.connect(self.ini_sesion)
        self.txtDni.returnPressed.connect(self.ini_sesion)
        if hasattr(self, "btnMembresia"):
            self.btnMembresia.clicked.connect(self.abrir_membresia)

    def ini_sesion(self):
        nombre = self.txtNombre.text().strip()
        dni = self.txtDni.text().strip()

        if not nombre or not dni:
            QMessageBox.warning(
                self, "Datos incompletos", "Complete nombre y DNI."
            )
            return

        if not registrar_usuario(nombre, dni):
            QMessageBox.warning(
                self,
                "Acceso denegado",
                "Ese DNI no coincide con el usuario registrado.",
            )
            return

        usuario_obj = construir_usuario(nombre)

        # Aviso de membresía aprobada o denegada (solo la primera vez).
        solicitud = notificacion_pendiente(usuario_obj.nombre)
        if solicitud is not None:
            mensaje = texto_notificacion(solicitud)
            if solicitud.estado == "APROBADA":
                QMessageBox.information(self, "¡Ya eres miembro!", mensaje)
            else:
                QMessageBox.warning(self, "Solicitud denegada", mensaje)
            marcar_notificado(solicitud.id)

        # Aviso si la membresía está por vencer o ya venció.
        if usuario_obj.es_miembro():
            aviso = aviso_vencimiento(usuario_obj)
            if aviso:
                QMessageBox.information(self, "Tu membresía", aviso)

        self.ir_a(libros, usuario=usuario_obj.nombre)

    def abrir_membresia(self):
        self.ir_a(
            RegistroMembresia,
            usuario=self.txtNombre.text().strip() or None,
        )


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
        self.setWindowTitle("LETRAS Y MUNDOS - Catálogo")

        # Se lee el JSON una sola vez para todas las portadas.
        libros_json = cargar_datos()["libros"]

        # Cada portada abre el detalle del libro que muestra.
        for numero in range(1, 17):
            portada = getattr(self, f"Cover{numero}", None)
            if isinstance(portada, QPushButton):
                self.preparar_portada(portada, libros_json)
                portada.clicked.connect(self.abrir_detalle)

    def preparar_portada(self, portada, libros_json):
        """Pone la imagen del libro y activa la animación al pasar el mouse."""
        portada.setCursor(Qt.CursorShape.PointingHandCursor)
        portada.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.geometrias[portada] = portada.geometry()
        portada.installEventFilter(self)

        # El campo "portada" del JSON dice qué portada muestra cada libro.
        libro = next(
            (
                libro
                for libro in libros_json
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
        self.libro_json = None
        self.libro_obj = None
        self.usuario_obj = None
        self.precio_unitario = 0.0
        super().__init__(anterior=anterior)

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Detalle del libro")
        self.btnAgregar.clicked.connect(self.agregar_al_carrito)
        self.spinBox.valueChanged.connect(self.actualizar_total)
        self.configurar_contenido(self.id_libro)

    def configurar_contenido(self, id_libro):
        """Busca en Almacen.json el libro por su id."""
        self.id_libro = id_libro
        self.usuario_obj = construir_usuario(self.usuario or "invitado")

        self.libro_json = next(
            (
                libro
                for libro in cargar_datos()["libros"]
                if libro.get("id") == id_libro
            ),
            None,
        )

        if self.libro_json is None:
            self.LblTitulo.setText("No disponible")
            self.LblAutor.setText("")
            self.LblPrecio.setText("S/ 0.00")
            self.LblTotal.setText("Total: S/ 0.00")
            self.LblDescripcion.setText(
                "No se encontraron detalles para este libro."
            )
            self.LblFoto.clear()
            self.LblOferta.setText("")
            self.spinBox.setMinimum(0)
            self.spinBox.setMaximum(0)
            self.spinBox.setValue(0)
            self.spinBox.setEnabled(False)
            self.btnAgregar.setEnabled(False)
            return

        self.libro_obj = Libro.desde_dict(self.libro_json)
        self.precio_unitario = self.libro_obj.precio_para(self.usuario_obj)
        stock = self.libro_obj.stock

        self.LblTitulo.setText(self.libro_obj.nombre)
        self.LblAutor.setText(self.libro_obj.autor)
        self.LblDescripcion.setText(
            self.libro_obj.descripcion or "Sin descripción."
        )
        self.cargar_imagen(self.libro_obj.imagen)

        # La cantidad nunca baja de 1 ni supera el stock disponible.
        self.spinBox.setMinimum(1 if stock > 0 else 0)
        self.spinBox.setMaximum(max(stock, 0))
        self.spinBox.setValue(1 if stock > 0 else 0)
        self.spinBox.setEnabled(stock > 0)
        self.btnAgregar.setEnabled(stock > 0)

        self.LblPrecio.setText(f"S/ {self.precio_unitario:.2f}")
        self.mostrar_oferta(stock)

        if stock > 0:
            self.actualizar_total()
        else:
            self.LblTotal.setText("AGOTADO: sin ejemplares disponibles.")

    def mostrar_oferta(self, stock):
        """Texto de oferta exclusiva para miembros."""
        if not self.libro_obj.oferta or self.libro_obj.precio_oferta is None:
            self.LblOferta.setText("")
            return

        if self.usuario_obj.es_miembro():
            self.LblOferta.setText(
                f"★ OFERTA MIEMBRO: S/ {self.libro_obj.precio_oferta:.2f} "
                f"(antes S/ {self.libro_obj.precio:.2f})"
            )
        else:
            self.LblOferta.setText(
                f"★ Hazte miembro y llévalo a "
                f"S/ {self.libro_obj.precio_oferta:.2f}"
            )

        if stock <= 0:
            self.LblOferta.setText("AGOTADO")

    def cargar_imagen(self, nombre_imagen):
        """Muestra la portada; si falta el archivo, deja el espacio vacío."""
        imagen = QPixmap(str(RUTA_IMAGENES / str(nombre_imagen or "")))
        if imagen.isNull():
            self.LblFoto.clear()
            return
        self.LblFoto.setPixmap(imagen)

    def actualizar_total(self, *args):
        if self.libro_obj is None or self.spinBox.value() <= 0:
            self.LblTotal.setText("Total: S/ 0.00")
            return

        total = self.precio_unitario * self.spinBox.value()
        self.LblTotal.setText(f"Total: S/ {total:.2f}")

    def agregar_al_carrito(self):
        """Agrega el libro al carrito del usuario (siempre como compra)."""
        if self.libro_obj is None:
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

        carrito = cargar_carrito(self.usuario_obj)
        try:
            carrito.agregar(self.libro_obj, cantidad, COMPRA)
            guardar_carrito(carrito)
        except BibliotecaError as error:
            QMessageBox.warning(self, "No se pudo agregar", str(error))
            return

        self.actualizar_boton_carrito()
        QMessageBox.information(
            self,
            "Agregado al carrito",
            f"Se agregaron {cantidad} ejemplar(es) de "
            f"\"{self.libro_obj.nombre}\" al carrito.",
        )


class ventana_carrito(VentanaBase):
    archivo_ui = "venta-carrito.ui"

    def __init__(self, anterior=None, usuario=None):
        self.usuario = usuario
        self.usuario_obj = construir_usuario(usuario or "invitado")
        self.carrito = None
        super().__init__(anterior=anterior)

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Mi carrito")
        self.carrito = cargar_carrito(self.usuario_obj)
        self.btnPagar.clicked.connect(self.pagar)
        self.btnSeguir.clicked.connect(self.seguir_comprando)
        self.btnVaciar.clicked.connect(self.vaciar)
        self.llenar_tabla()

    def llenar_tabla(self):
        items = self.carrito.items
        tabla = self.tableCarrito
        tabla.setRowCount(0)
        tabla.setRowCount(len(items))

        for fila, item in enumerate(items):
            tabla.setItem(fila, 0, _item_solo_lectura(item.libro.nombre))
            tabla.setItem(fila, 1, _item_solo_lectura(item.cantidad))
            tabla.setItem(
                fila,
                2,
                _item_solo_lectura(
                    f"S/ {item.precio_unitario(self.usuario_obj):.2f}"
                ),
            )
            tabla.setItem(
                fila,
                3,
                _item_solo_lectura(
                    f"S/ {item.subtotal(self.usuario_obj):.2f}"
                ),
            )

            combo = QComboBox()
            combo.addItem(COMPRA)
            if self.usuario_obj.puede_prestar():
                combo.addItem(PRESTAMO)
            combo.setCurrentText(item.tipo)
            combo.currentTextChanged.connect(
                lambda texto, id_libro=item.libro.id: self.cambiar_tipo(
                    id_libro, texto
                )
            )
            tabla.setCellWidget(fila, 4, combo)

            boton = QPushButton("QUITAR")
            boton.setStyleSheet(ESTILO_BOTON)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.clicked.connect(
                lambda _checked=False, id_libro=item.libro.id: self.quitar_item(
                    id_libro
                )
            )
            tabla.setCellWidget(fila, 5, boton)

        tabla.resizeColumnsToContents()
        tabla.verticalHeader().setVisible(False)
        self.actualizar_totales()

    def actualizar_totales(self):
        self.LblTotal.setText(f"TOTAL: S/ {self.carrito.total():.2f}")
        descuento = self.carrito.descuento_total()
        if descuento > 0:
            self.LblDescuento.setText(
                f"Descuento miembro: -S/ {descuento:.2f}"
            )
        else:
            self.LblDescuento.setText("Descuento miembro: S/ 0.00")

        if self.usuario_obj.es_miembro():
            self.LblAviso.setText(
                "Elige COMPRA o PRÉSTAMO en cada libro. "
                "Los préstamos se devuelven en 7 días."
            )
        else:
            self.LblAviso.setText(
                "Solo los miembros pueden pedir libros prestados. "
                "Pasa a Membresía para acceder a ese beneficio."
            )

        self.btnPagar.setEnabled(bool(self.carrito.items))

    def cambiar_tipo(self, id_libro, tipo):
        try:
            self.carrito.cambiar_tipo(id_libro, tipo)
        except BibliotecaError as error:
            QMessageBox.warning(self, "No permitido", str(error))
            self.llenar_tabla()
            return

        guardar_carrito(self.carrito)

        for fila, item in enumerate(self.carrito.items):
            if item.libro.id == id_libro:
                self.tableCarrito.item(fila, 3).setText(
                    f"S/ {item.subtotal(self.usuario_obj):.2f}"
                )
                break
        self.actualizar_totales()

    def quitar_item(self, id_libro):
        if self.carrito.quitar(id_libro):
            guardar_carrito(self.carrito)
            self.llenar_tabla()

    def vaciar(self):
        if not self.carrito.items:
            return

        respuesta = QMessageBox.question(
            self,
            "Vaciar carrito",
            "¿Quitar todos los libros del carrito?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if respuesta != QMessageBox.Yes:
            return

        self.carrito.vaciar()
        guardar_carrito(self.carrito)
        self.llenar_tabla()

    def seguir_comprando(self):
        self.ir_a(libros, usuario=self.usuario)

    def pagar(self):
        if not self.carrito.items:
            QMessageBox.information(
                self,
                "Carrito vacío",
                "Agrega libros antes de pagar.",
            )
            return

        mapa = cargar_cajas()
        caja = mapa.caja_abierta()
        if caja is None:
            QMessageBox.warning(
                self,
                "Cajas cerradas",
                "No hay ninguna caja abierta. Pide al administrador que "
                "abra una caja para poder pagar.",
            )
            return

        try:
            resultado = finalizar_compra(self.carrito, caja)
        except BibliotecaError as error:
            QMessageBox.warning(self, "No se pudo finalizar", str(error))
            return

        self.ir_a(
            BoletaVentana,
            usuario=self.usuario,
            texto=resultado["texto"],
            movimiento=resultado["movimiento"],
        )


class BoletaVentana(VentanaBase):
    archivo_ui = "boleta.ui"

    def __init__(self, anterior=None, usuario=None, texto="", movimiento=None):
        self.usuario = usuario
        self.texto = texto
        self.movimiento = movimiento or {}
        super().__init__(anterior=anterior)

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Boleta")
        self.textBoleta.setPlainText(self.texto)

        caja = self.movimiento.get("caja")
        if caja is not None:
            self.LblCaja.setText(
                f"PASA A PAGAR Y RECOGER EN LA CAJA {caja}"
            )
        else:
            self.LblCaja.setText("PASA A PAGAR EN CAJA")

        self.btnCatalogo.clicked.connect(self.ir_catalogo)
        self.btnSalir.clicked.connect(self.salir)

    def ir_catalogo(self):
        self.ir_a(libros, usuario=self.usuario)

    def volver(self):
        """Desde la boleta, VOLVER lleva al catálogo (el carrito ya está vacío)."""
        self.ir_a(libros, usuario=self.usuario)

    def salir(self):
        self.ir_a(login)


class RegistroMembresia(VentanaBase):
    archivo_ui = "membresia.ui"

    def __init__(self, anterior=None, usuario=None):
        self.usuario = usuario
        super().__init__(anterior=anterior)

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Membresía")
        if self.usuario:
            self.txtNombre.setText(str(self.usuario))
        elif hasattr(self, "btnCarrito"):
            # Si se llega desde el login, todavía no hay carrito que ver.
            self.btnCarrito.hide()
        self.btnSolicitar.clicked.connect(self.enviar_solicitud)

    def enviar_solicitud(self):
        nombre = self.txtNombre.text().strip()
        dni = self.txtDni.text().strip()
        monto = self.spinMonto.value()

        try:
            solicitud = crear_solicitud(nombre, dni, monto)
        except BibliotecaError as error:
            QMessageBox.warning(self, "Solicitud no enviada", str(error))
            return

        QMessageBox.information(
            self,
            "Solicitud enviada",
            "Tu solicitud de membresía fue enviada al administrador.\n\n"
            f"Usuario: {solicitud.usuario}\n"
            f"Cuota mensual: S/ {solicitud.monto:.2f}\n\n"
            "Cuando sea revisada recibirás un aviso al iniciar sesión.\n"
            f"Atención al cliente: {TELEFONO_ATENCION}",
        )
        self.ir_a(loginUsuario)


class SolicitudesAdmin(VentanaBase):
    archivo_ui = "solicitudes.ui"

    def __init__(self, anterior=None):
        self.ids_solicitudes = []
        self.nombres_miembros = []
        super().__init__(anterior=anterior)

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Membresías")
        self.btnAceptar.clicked.connect(self.aceptar)
        self.btnDenegar.clicked.connect(self.denegar)
        self.btnRenovar.clicked.connect(self.renovar)
        self.btnQuitar.clicked.connect(self.quitar)
        self.cargar_tablas()

    def caja_abierta(self):
        caja = cargar_cajas().caja_abierta()
        if caja is None:
            QMessageBox.warning(
                self,
                "Sin cajas abiertas",
                "Abre una caja en el apartado CAJAS antes de continuar.",
            )
        return caja

    def cargar_tablas(self):
        solicitudes = listar_solicitudes("PENDIENTE")
        tabla = self.tableSolicitudes
        tabla.setRowCount(0)
        tabla.setRowCount(len(solicitudes))
        self.ids_solicitudes = []

        for fila, solicitud in enumerate(solicitudes):
            tabla.setItem(fila, 0, _item_solo_lectura(solicitud.id))
            tabla.setItem(fila, 1, _item_solo_lectura(solicitud.usuario))
            tabla.setItem(fila, 2, _item_solo_lectura(solicitud.dni))
            tabla.setItem(
                fila, 3, _item_solo_lectura(f"S/ {solicitud.monto:.2f}")
            )
            tabla.setItem(fila, 4, _item_solo_lectura(solicitud.fecha))
            tabla.setItem(fila, 5, _item_solo_lectura(solicitud.estado))
            self.ids_solicitudes.append(solicitud.id)

        tabla.resizeColumnsToContents()
        tabla.verticalHeader().setVisible(False)

        miembros = listar_miembros()
        tabla = self.tableMiembros
        tabla.setRowCount(0)
        tabla.setRowCount(len(miembros))
        self.nombres_miembros = []

        for fila, miembro in enumerate(miembros):
            estado = "VENCIDO" if miembro.esta_vencido() else "ACTIVO"
            tabla.setItem(fila, 0, _item_solo_lectura(miembro.nombre))
            tabla.setItem(fila, 1, _item_solo_lectura(miembro.dni))
            tabla.setItem(
                fila, 2, _item_solo_lectura(f"S/ {miembro.monto:.2f}")
            )
            tabla.setItem(fila, 3, _item_solo_lectura(miembro.desde))
            tabla.setItem(fila, 4, _item_solo_lectura(miembro.hasta))
            tabla.setItem(fila, 5, _item_solo_lectura(estado))
            self.nombres_miembros.append(miembro.nombre)

        tabla.resizeColumnsToContents()
        tabla.verticalHeader().setVisible(False)

    def _solicitud_seleccionada(self):
        fila = self.tableSolicitudes.currentRow()
        if fila < 0 or fila >= len(self.ids_solicitudes):
            QMessageBox.warning(
                self,
                "Sin selección",
                "Selecciona una solicitud de la tabla.",
            )
            return None
        return self.ids_solicitudes[fila]

    def _miembro_seleccionado(self):
        fila = self.tableMiembros.currentRow()
        if fila < 0 or fila >= len(self.nombres_miembros):
            QMessageBox.warning(
                self,
                "Sin selección",
                "Selecciona un miembro de la tabla.",
            )
            return None
        return self.nombres_miembros[fila]

    def aceptar(self):
        id_solicitud = self._solicitud_seleccionada()
        if id_solicitud is None:
            return

        caja = self.caja_abierta()
        if caja is None:
            return

        try:
            solicitud = aprobar_solicitud(id_solicitud, caja.numero)
        except BibliotecaError as error:
            QMessageBox.warning(self, "No se pudo aceptar", str(error))
            return

        QMessageBox.information(
            self,
            "Solicitud aceptada",
            f"{solicitud.usuario} ahora es miembro.\n"
            f"Debe pasar a pagar su membresía en la CAJA {caja.numero}.",
        )
        self.cargar_tablas()

    def denegar(self):
        id_solicitud = self._solicitud_seleccionada()
        if id_solicitud is None:
            return

        caja = self.caja_abierta()
        if caja is None:
            return

        try:
            solicitud = rechazar_solicitud(id_solicitud, caja.numero)
        except BibliotecaError as error:
            QMessageBox.warning(self, "No se pudo denegar", str(error))
            return

        QMessageBox.information(
            self,
            "Solicitud denegada",
            f"Se denegó la solicitud de {solicitud.usuario}.\n"
            f"Código de reembolso: {solicitud.codigo}\n"
            f"Debe acercarse a la CAJA {caja.numero}.",
        )
        self.cargar_tablas()

    def renovar(self):
        nombre = self._miembro_seleccionado()
        if nombre is None:
            return

        if renovar_miembro(nombre, 30):
            QMessageBox.information(
                self,
                "Membresía renovada",
                f"Se renovó la membresía de {nombre} por 30 días.",
            )
            self.cargar_tablas()
        else:
            QMessageBox.warning(
                self, "No se pudo renovar", "No se encontró el miembro."
            )

    def quitar(self):
        nombre = self._miembro_seleccionado()
        if nombre is None:
            return

        respuesta = QMessageBox.question(
            self,
            "Quitar miembro",
            f"¿Quitar a {nombre} de los miembros?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if respuesta != QMessageBox.Yes:
            return

        if quitar_miembro(nombre):
            QMessageBox.information(
                self, "Miembro eliminado", f"{nombre} ya no es miembro."
            )
            self.cargar_tablas()
        else:
            QMessageBox.warning(
                self, "No se pudo quitar", "No se encontró el miembro."
            )


class CajasAdmin(VentanaBase):
    archivo_ui = "cajas.ui"

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Cajas y mapa")
        self.mapa = cargar_cajas()
        self.botones = [
            self.btnCaja1,
            self.btnCaja2,
            self.btnCaja3,
            self.btnCaja4,
            self.btnCaja5,
            self.btnCaja6,
        ]

        for indice, boton in enumerate(self.botones):
            boton.clicked.connect(
                lambda _checked=False, numero=indice + 1: self.alternar(numero)
            )

        self.btnGuardar.clicked.connect(self.guardar)
        self.actualizar()

    def actualizar(self):
        for indice, boton in enumerate(self.botones):
            caja = self.mapa.caja(indice + 1)
            if caja is None:
                continue
            estado = "ABIERTA" if caja.abierta else "CERRADA"
            boton.setText(f"CAJA {indice + 1}\n{estado}")
            boton.setStyleSheet(
                ESTILO_CAJA_ABIERTA if caja.abierta else ESTILO_CAJA_CERRADA
            )

        self.llenar_mapa()

    def alternar(self, numero):
        self.mapa.alternar(numero)
        self.actualizar()

    def llenar_mapa(self):
        libros_obj = construir_libros(cargar_datos()["libros"])
        matriz = MapaBiblioteca(libros_obj).disponibilidad(libros_obj)

        tabla = self.tableMapa
        tabla.setRowCount(MapaBiblioteca.FILAS)
        tabla.setColumnCount(MapaBiblioteca.COLUMNAS)

        for fila in range(MapaBiblioteca.FILAS):
            for columna in range(MapaBiblioteca.COLUMNAS):
                tabla.setItem(
                    fila,
                    columna,
                    _item_solo_lectura(matriz[fila][columna]),
                )

        tabla.resizeColumnsToContents()

    def guardar(self):
        guardar_cajas(self.mapa)
        QMessageBox.information(
            self,
            "Cajas guardadas",
            "El mapa de cajas se guardó correctamente.",
        )


class ReportesAdmin(VentanaBase):
    archivo_ui = "reportes.ui"

    def __init__(self, anterior=None, filtro=None):
        self.filtro = filtro
        self.ids_movimientos = []
        super().__init__(anterior=anterior)

    def preparar(self):
        titulo = "LETRAS Y MUNDOS - Reportes"
        if self.filtro:
            titulo += f" ({self.filtro})"
        self.setWindowTitle(titulo)

        self.btnDevolver.clicked.connect(self.devolver)
        self.btnActualizar.clicked.connect(self.cargar)
        self.cargar()

    def movimientos(self):
        movimientos = listar_movimientos()
        if self.filtro == "COMPRA":
            return [
                movimiento
                for movimiento in movimientos
                if movimiento.get("tipo") in ("COMPRA", "MIXTO")
            ]
        if self.filtro == "PRESTAMO":
            return [
                movimiento
                for movimiento in movimientos
                if movimiento.get("tipo") in ("PRESTAMO", "MIXTO")
            ]
        return movimientos

    def cargar(self):
        movimientos = self.movimientos()
        tabla = self.tableMovimientos
        tabla.setRowCount(0)
        tabla.setRowCount(len(movimientos))
        self.ids_movimientos = []

        for fila, movimiento in enumerate(movimientos):
            libros_texto = ", ".join(
                f"{item.get('nombre', '')} x{item.get('cantidad', 0)}"
                for item in movimiento.get("items", [])
            )
            tabla.setItem(fila, 0, _item_solo_lectura(movimiento.get("id")))
            tabla.setItem(fila, 1, _item_solo_lectura(movimiento.get("fecha")))
            tabla.setItem(fila, 2, _item_solo_lectura(movimiento.get("usuario")))
            tabla.setItem(fila, 3, _item_solo_lectura(movimiento.get("tipo")))
            tabla.setItem(fila, 4, _item_solo_lectura(libros_texto))
            tabla.setItem(
                fila,
                5,
                _item_solo_lectura(
                    f"S/ {float(movimiento.get('total', 0) or 0):.2f}"
                ),
            )
            tabla.setItem(fila, 6, _item_solo_lectura(movimiento.get("caja")))
            tabla.setItem(fila, 7, _item_solo_lectura(movimiento.get("estado")))
            self.ids_movimientos.append(int(movimiento.get("id", 0) or 0))

        tabla.resizeColumnsToContents()
        tabla.verticalHeader().setVisible(False)

        datos = resumen()
        self.LblResumen.setText(
            f"Recaudado: S/ {datos['recaudado']:.2f} · "
            f"Préstamos activos: {datos['prestamos_activos']} · "
            f"Libros disponibles: {datos['libros_disponibles']} · "
            f"Miembros: {datos['miembros']} · "
            f"Movimientos: {datos['movimientos']}"
        )

    def devolver(self):
        fila = self.tableMovimientos.currentRow()
        if fila < 0 or fila >= len(self.ids_movimientos):
            QMessageBox.warning(
                self,
                "Sin selección",
                "Selecciona un préstamo ACTIVO de la tabla.",
            )
            return

        id_movimiento = self.ids_movimientos[fila]
        if registrar_devolucion(id_movimiento):
            QMessageBox.information(
                self,
                "Devolución registrada",
                "Los libros volvieron al almacén y ya están disponibles.",
            )
            self.cargar()
        else:
            QMessageBox.warning(
                self,
                "No se puede devolver",
                "Selecciona un préstamo con estado ACTIVO.",
            )


class RegistrarLibro(VentanaBase):
    archivo_ui = "registrar_libro.ui"

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Registrar libro")
        self.spinPrecioOferta.setEnabled(False)
        self.chkOferta.toggled.connect(self.spinPrecioOferta.setEnabled)
        self.btnGuardar.clicked.connect(self.guardar)

    def guardar(self):
        nombre = self.txtNombre.text().strip()
        autor = self.txtAutor.text().strip()

        if not nombre or not autor:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "El nombre y el autor son obligatorios.",
            )
            return

        datos = cargar_datos()
        siguiente = max(
            [int(libro.get("id", 0) or 0) for libro in datos["libros"]] or [0]
        ) + 1
        oferta = self.chkOferta.isChecked()

        try:
            libro = Libro(
                id_libro=siguiente,
                nombre=nombre,
                autor=autor,
                tipo=self.cmbTipo.currentText(),
                estado=self.cmbEstado.currentText(),
                stock=self.spinStock.value(),
                precio=self.spinPrecio.value(),
                descripcion=self.txtDescripcion.toPlainText().strip(),
                imagen=self.txtImagen.text().strip(),
                oferta=oferta,
                precio_oferta=(
                    self.spinPrecioOferta.value() if oferta else None
                ),
            )
        except DatosInvalidosError as error:
            QMessageBox.warning(self, "Datos inválidos", str(error))
            return

        if oferta and (libro.precio_oferta is None or libro.precio_oferta <= 0):
            QMessageBox.warning(
                self,
                "Oferta inválida",
                "Indica un precio de oferta mayor que cero.",
            )
            return

        datos["libros"].append(libro.a_dict())
        guardar_datos(datos)

        QMessageBox.information(
            self,
            "Libro registrado",
            f"Se registró \"{nombre}\" con el id {siguiente}.",
        )
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.txtNombre.clear()
        self.txtAutor.clear()
        self.txtDescripcion.clear()
        self.txtImagen.clear()
        self.spinStock.setValue(1)
        self.spinPrecio.setValue(25.0)
        self.chkOferta.setChecked(False)
        self.spinPrecioOferta.setValue(0.0)


class loginAdmin(VentanaBase):
    archivo_ui = "login_admin.ui"

    def preparar(self):
        self.setWindowTitle("LETRAS Y MUNDOS - Administrador")
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

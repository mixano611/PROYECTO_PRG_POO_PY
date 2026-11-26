"""
Para agregar una ventana nueva solo hay que:

1. Crear su diseno en Qt Designer y guardarlo en assets/.
2. Heredar de VentanaBase e indicar el archivo:

class PantallaPrestamos(VentanaBase):
archivo_ui = "prestamos.ui"

3. Para avanzar a otra ventana:  self.ir_a(OtraVentana)

Todas las ventanas se abren en pantalla completa. Las que usan layouts se
adaptan solas al tamaño; las que conservan un diseno de posiciones fijas se
escalan de forma uniforme para aprovechar toda la pantalla.
"""

from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QWidget,
)

from tema_admin import animar_entrada, aplicar_tema_admin
from tema_usuario import aplicar_tema_usuario


class VistaEscalada(QGraphicsView):
    """Muestra un diseno de tamaño fijo escalado al tamaño de la ventana.

    Asi las ventanas de usuario conservan exactamente su diseño original,
    pero las letras, imagenes y botones crecen para aprovechar la pantalla.
    """

    def __init__(self, escena, padre=None):
        super().__init__(escena, padre)
        self.setObjectName("vistaEscalada")
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.SmoothPixmapTransform
            | QPainter.TextAntialiasing
        )
        self.setStyleSheet(
            "QGraphicsView { background: transparent; border: none; }"
        )
        self.viewport().setAutoFillBackground(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, evento):
        super().resizeEvent(evento)
        self.ajustar()

    def showEvent(self, evento):
        super().showEvent(evento)
        self.ajustar()

    def ajustar(self):
        escena = self.scene()
        if escena is None:
            return

        rect = escena.itemsBoundingRect()
        if rect.isEmpty():
            return

        margen = 10
        self.fitInView(
            rect.adjusted(-margen, -margen, margen, margen),
            Qt.AspectRatioMode.KeepAspectRatio,
        )


class VentanaBase(QMainWindow):
    """Ventana que recuerda de donde vino y sabe regresar."""

    # Nombre del archivo .ui dentro de assets/. Cada subclase lo define.
    archivo_ui = None

    # Tema visual: "admin" aplica la paleta beige del panel.
    tema = None

    # Las ventanas con diseno de posiciones fijas se escalan para llenar
    # la pantalla; las que usan layouts (como el login principal) no.
    escala_fija = True

    def __init__(self, anterior=None):
        super().__init__()
        self.anterior = anterior

        if not self.archivo_ui:
            raise ValueError(
                f"{type(self).__name__} debe definir el atributo archivo_ui"
            )

        ruta_ui = Path(__file__).resolve().parent / "assets" / self.archivo_ui
        uic.loadUi(str(ruta_ui), self)

        # Los estilos viejos de cada .ui se descartan para que el tema comun
        # controle botones, campos, tablas y estados de hover.
        if self.tema == "usuario":
            self.setStyleSheet("")
            for hijo in self.findChildren(QWidget):
                hijo.setStyleSheet("")
            for boton in self.findChildren(QPushButton):
                boton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Se prepara antes de mover el lienzo a la escena de escalado.
        if self.tema != "admin" and self.escala_fija:
            self._preparar_tablas_usuario()

        # Las ventanas con diseno de posiciones fijas se escalan para llenar
        # la pantalla; las que ya usan layouts no se tocan.
        self._preparar_responsivo()

        # Si la ventana tiene un boton llamado btnBack (o btnVolver), se conecta solo.
        if hasattr(self, "btnBack"):
            self.btnBack.clicked.connect(self.volver)
        elif hasattr(self, "btnVolver"):
            self.btnVolver.clicked.connect(self.volver)

        # El boton VER CARRITO se conecta solo en todas las ventanas de usuario.
        if hasattr(self, "btnCarrito"):
            self.btnCarrito.clicked.connect(self.abrir_carrito)

        self.preparar()

        if self.tema == "admin":
            aplicar_tema_admin(self)
        elif self.tema == "usuario":
            aplicar_tema_usuario(self)

    def _preparar_tablas_usuario(self):
        """Deja las tablas listas para el tema comun."""
        for tabla in self.findChildren(QTableWidget):
            tabla.setAlternatingRowColors(True)
            tabla.setShowGrid(False)
            tabla.verticalHeader().setVisible(False)
            tabla.verticalHeader().setDefaultSectionSize(30)
            cabecera = tabla.horizontalHeader()
            cabecera.setHighlightSections(False)
            cabecera.setDefaultAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )

    # ------------------------------------------------------------------
    # Adaptacion a pantalla completa y a distintos tamaños
    # ------------------------------------------------------------------
    def _preparar_responsivo(self):
        central = self.centralWidget()
        if central is None or not self.escala_fija or self.tema == "admin":
            return

        menu = self.findChild(QMenuBar)
        estado = self.findChild(QStatusBar)
        alto_menu = menu.sizeHint().height() if menu else 0
        alto_estado = estado.sizeHint().height() if estado else 0

        ancho = max(1, self.width())
        alto = max(1, self.height() - alto_menu - alto_estado)

        # Se retira sin borrarlo para poder insertarlo en la escena.
        central = self.takeCentralWidget()
        central.setFixedSize(ancho, alto)
        # El fondo lo pinta la ventana; el lienzo debe ser transparente.
        central.setStyleSheet(
            (central.styleSheet() or "")
            + "\nQWidget#centralwidget { background: transparent; }"
        )

        escena = QGraphicsScene(self)
        self._proxy = escena.addWidget(central)

        vista = VistaEscalada(escena, self)
        self.setCentralWidget(vista)

        self._lienzo = central
        self._vista = vista

    def show(self):
        """La primera vez que aparece, la ventana ocupa toda la pantalla."""
        primera_vez = not getattr(self, "_ya_mostrada", False)
        if primera_vez:
            self._ya_mostrada = True
            self.showFullScreen()
            if self.tema == "admin":
                animar_entrada(self)
        else:
            super().show()

    def keyPressEvent(self, evento):
        """F11 alterna pantalla completa y ESC sale de ella."""
        if evento.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showMaximized()
            else:
                self.showFullScreen()
            return
        if evento.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showMaximized()
            return
        super().keyPressEvent(evento)

    def preparar(self):
        """Se ejecuta al final del __init__. Aqui van las conexiones propias.

        Las subclases lo sobrescriben cuando necesitan conectar sus botones.
        """

    def ir_a(self, ventana, **datos):
        """Abre `ventana` recordando esta como anterior y oculta la actual."""
        self.siguiente = ventana(anterior=self, **datos)
        self.siguiente.show()
        self.hide()
        return self.siguiente

    def volver(self):
        """Regresa a la ventana anterior, tal como estaba."""
        if self.anterior is None:
            return

        self.anterior.show()
        self.hide()

    # ------------------------------------------------------------------
    # Carrito compartido por todas las pantallas de usuario
    # ------------------------------------------------------------------
    def usuario_actual(self):
        """Busca el nombre de usuario recorriendo la cadena de ventanas."""
        ventana = self
        while ventana is not None:
            nombre = getattr(ventana, "usuario", None)
            if isinstance(nombre, str) and nombre.strip():
                return nombre.strip().lower()
            ventana = getattr(ventana, "anterior", None)
        return None

    def actualizar_boton_carrito(self):
        """Muestra cuantos ejemplares tiene el usuario en el carrito."""
        if not hasattr(self, "btnCarrito"):
            return

        from src.Carrito import cantidad_en_carrito

        nombre = self.usuario_actual()
        cantidad = cantidad_en_carrito(nombre) if nombre else 0
        self.btnCarrito.setText(f"VER CARRITO ({cantidad})")

    def abrir_carrito(self):
        """Abre la ventana del carrito del usuario actual."""
        nombre = self.usuario_actual()
        if not nombre:
            QMessageBox.information(
                self,
                "Carrito",
                "Inicia sesion para usar el carrito.",
            )
            return

        # Importacion diferida: bibliotecapy importa este modulo.
        from bibliotecapy import ventana_carrito

        self.ir_a(ventana_carrito, usuario=nombre)

    def showEvent(self, evento):
        """Cada vez que se muestra la ventana se actualiza el contador."""
        super().showEvent(evento)
        self.actualizar_boton_carrito()

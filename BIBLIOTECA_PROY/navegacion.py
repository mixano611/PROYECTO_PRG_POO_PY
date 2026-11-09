"""
Para agregar una ventana nueva solo hay que:

1. Crear su diseno en Qt Designer y guardarlo en assets/.
2. Heredar de VentanaBase e indicar el archivo:

class PantallaPrestamos(VentanaBase):
archivo_ui = "prestamos.ui"

3. Para avanzar a otra ventana:  self.ir_a(OtraVentana)
"""

from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class VentanaBase(QMainWindow):
    """Ventana que recuerda de donde vino y sabe regresar."""

    # Nombre del archivo .ui dentro de assets/. Cada subclase lo define.
    archivo_ui = None

    def __init__(self, anterior=None):
        super().__init__()
        self.anterior = anterior

        if not self.archivo_ui:
            raise ValueError(
                f"{type(self).__name__} debe definir el atributo archivo_ui"
            )

        ruta_ui = Path(__file__).resolve().parent / "assets" / self.archivo_ui
        uic.loadUi(str(ruta_ui), self)

        # Si la ventana tiene un boton llamado btnBack (o btnVolver), se conecta solo.
        if hasattr(self, "btnBack"):
            self.btnBack.clicked.connect(self.volver)
        elif hasattr(self, "btnVolver"):
            self.btnVolver.clicked.connect(self.volver)

        # El boton VER CARRITO se conecta solo en todas las ventanas de usuario.
        if hasattr(self, "btnCarrito"):
            self.btnCarrito.clicked.connect(self.abrir_carrito)

        self.preparar()

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

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
from PyQt5.QtWidgets import QMainWindow


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

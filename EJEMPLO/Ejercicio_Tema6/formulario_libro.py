
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class FormularioLibro(QMainWindow):

    def __init__(self):
        super().__init__()

        # Cargar el diseño creado en Qt Designer.
        ruta_ui = Path(__file__).resolve().parent / "aver.ui"
        uic.loadUi(str(ruta_ui), self)


from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMainWindow


class loginAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent / "assets" / "login_admin.ui"
        uic.loadUi(str(ruta_ui), self)


class loginUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent / "assets" / "login_usuario.ui"
        uic.loadUi(str(ruta_ui), self)


class login(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar el diseño creado en Qt Designer.
        ruta_ui = Path(__file__).resolve().parent / "assets" / "login.ui"
        uic.loadUi(str(ruta_ui), self)

        # Configurar el título de la ventana.
        self.setWindowTitle("Sistema de Biblioteca - Inicio de Sesión")

        # Conectar los botones a sus respectivas ventanas
        self.btnUsuario.clicked.connect(self.abrir_login_usuario)
        self.btnAdmin.clicked.connect(self.abrir_login_admin)

    def abrir_login_usuario(self):
        self.login_usuario_window = loginUsuario()
        self.login_usuario_window.show()
        self.close()

    def abrir_login_admin(self):
        self.login_admin_window = loginAdmin()
        self.login_admin_window.show()
        self.close()


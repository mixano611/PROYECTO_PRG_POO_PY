
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow


class loginAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent / "assets" / "login_admin.ui"
        uic.loadUi(str(ruta_ui), self)

class MainConsulta(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent / "assets" / "main_consulta.ui"
        uic.loadUi(str(ruta_ui), self)

class loginUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent / "assets" / "login_usuario.ui"
        uic.loadUi(str(ruta_ui), self)

        self.btnIniciar.clicked.connect(self.ini_sesion)

    def ini_sesion(self):
        nombre = self.txtNombre.text().strip()

        if not nombre:
            QMessageBox.warning(
                self,
                "Errorrrrrrrr",
                "Ingrese nombre de usuario"
            )
            return

        else:
            self.main_consulta_window = MainConsulta()
            self.main_consulta_window.show()
            self.close()

class loginAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = Path(__file__).resolve().parent / "assets" / "login_admin.ui"
        uic.loadUi(str(ruta_ui),self)

        self.btnIniciar.clicked.connect(self.ini_sesion)
        
    def ini_sesion(self):
        nombre = self.txtNombre.text().strip()
        contrasena = self.txtContrasena.text().strip()
            
        if not nombre or not contrasena:
            QMessageBox.warning(
                self,
                "Errorrrrrrrr",
                "Complete todo los campos"
            )
            return
            
        else:
            self.main_consulta_window = MainConsulta()
            self.main_consulta_window.show()
            self.close()



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

    


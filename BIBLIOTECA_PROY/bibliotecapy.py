
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class login(QMainWindow):

    def __init__(self):
        super().__init__()

        # Cargar el diseño creado en Qt Designer.
        ruta_ui = Path(__file__).resolve().parent / "formulario_libro.ui"
        uic.loadUi(str(ruta_ui), self)

        # Configurar el título de la ventana.
        self.setWindowTitle("Sistema de Biblioteca - Registro de Libros")

        # Lista para almacenar los libros durante la ejecución.
        self.libros = []

        # Configurar el formulario.
        self._configurar_formulario()

        # Conectar el botón Grabar con el método registrar_libro.
        self.btnGrabar.clicked.connect(self.registrar_libro)

    def _configurar_formulario(self):
        """Prepara los componentes del formulario."""

        # Agregar las opciones de categoría.
        self.cmbCategoria.clear()
        self.cmbCategoria.addItems([
            "Novela",
            "Ciencia",
            "Historia",
            "Tecnología",
            "Educación",
            "Otro"
        ])

        # Utilizar el área de texto para mostrar los libros.
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText(
            "Aquí aparecerán los libros registrados."
        )

    def registrar_libro(self):
        """Valida y registra un libro."""

        # Obtener los datos ingresados.
        codigo = self.txtCodigo.text().strip()
        titulo = self.txtTitulo.text().strip()
        autor = self.txtAutor.text().strip()
        categoria = self.cmbCategoria.currentText()

        # Validar los campos obligatorios.
        if not codigo or not titulo or not autor:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingresa el código, el título y el autor."
            )
            return

        # Verificar que el código no esté registrado.
        for libro in self.libros:
            if libro["codigo"].casefold() == codigo.casefold():
                QMessageBox.warning(
                    self,
                    "Código duplicado",
                    "Ya existe un libro con ese código."
                )
                return

        # Crear el registro del libro.
        libro = {
            "codigo": codigo,
            "titulo": titulo,
            "autor": autor,
            "categoria": categoria
        }

        # Guardar el libro en la lista.
        self.libros.append(libro)

        # Actualizar el área de texto.
        self._mostrar_libros()

        # Confirmar el registro.
        QMessageBox.information(
            self,
            "Registro exitoso",
            "El libro se registró correctamente."
        )

        # Limpiar los campos para el siguiente registro.
        self.txtCodigo.clear()
        self.txtTitulo.clear()
        self.txtAutor.clear()
        self.txtCodigo.setFocus()

    def _mostrar_libros(self):
        """Muestra todos los libros registrados."""

        texto = ""

        for libro in self.libros:
            texto += (
                f"Código: {libro['codigo']}\n"
                f"Título: {libro['titulo']}\n"
                f"Autor: {libro['autor']}\n"
                f"Categoría: {libro['categoria']}\n"
                f"{'-' * 40}\n"
            )

        self.textEdit.setPlainText(texto)
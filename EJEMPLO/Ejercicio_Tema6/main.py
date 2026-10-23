import sys

from PyQt5.QtWidgets import QApplication

from formulario_libro import FormularioLibro


def main():
    app = QApplication(sys.argv)

    ventana = FormularioLibro()
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
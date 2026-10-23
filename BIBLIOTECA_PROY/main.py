import sys

from PyQt5.QtWidgets import QApplication

from BIBLIOTECA_PY import bibliotecapy


def main():
    app = QApplication(sys.argv)

    ventana = bibliotecapy()
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

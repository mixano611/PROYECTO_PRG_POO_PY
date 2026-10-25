import sys

from bibliotecapy import login
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    ventana = login()
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

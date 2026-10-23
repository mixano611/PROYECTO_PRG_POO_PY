import sys

from PyQt5.QtWidgets import QApplication

from bibliotecapy import login


def main():
    app = QApplication(sys.argv)

    ventana = login()
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


    
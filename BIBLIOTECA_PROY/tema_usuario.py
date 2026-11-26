"""Tema visual de las pantallas del usuario.

Mantiene la identidad calida del catalogo (fondo crema) y usa el morado del
login como color de accion. Todas las ventanas de usuario comparten los
mismos botones, campos, tablas y estados de hover.
"""

from pathlib import Path

from PyQt5.QtWidgets import QWidget

# Paleta del area de usuario.
CREMA = "#FFEBA8"
CREMA_CLARA = "#FFF8E1"
CREMA_TARJETA = "#FFF3D2"
CREMA_BANDA = "#F3DBA9"
BORDE = "#E2C98F"
BORDE_FUERTE = "#D3B36B"
MORADO = "#6E5AA8"
MORADO_CLARO = "#7D68B8"
MORADO_OSCURO = "#5B4A8F"
MORADO_BORDE = "#4E3E85"
LAVANDA = "#E7DFF9"
TEXTO = "#3D2E66"
TEXTO_SUAVE = "#6A5D8A"
ROJO = "#A33F3C"
ROJO_BORDE = "#DDB0AA"

_ASSETS = Path(__file__).resolve().parent / "assets"
FLECHA_ABAJO = (_ASSETS / "chevron_down_usuario.png").as_posix()
FLECHA_ARRIBA = (_ASSETS / "chevron_up_usuario.png").as_posix()

QSS_USUARIO = f"""
QMainWindow, QWidget#centralwidget {{
    background-color: {CREMA};
}}
QScrollArea, QWidget#scrollAreaWidgetContents, QFrame#frame {{
    background-color: {CREMA};
    border: none;
}}
QWidget {{
    color: {TEXTO};
    font-family: "Segoe UI";
}}
QLabel {{
    background: transparent;
}}
QWidget#widget {{
    background-color: {CREMA_BANDA};
}}

/* ---------------------------------------------------------------- titulos */
QLabel#LblTitulo, QLabel#label, QLabel#label_41 {{
    color: {TEXTO};
}}
QLabel#LblAutor, QLabel#LblDescripcion, QLabel#LblInfo,
QLabel#LblTelefono, QLabel#LblDescuento, QLabel#label_7,
QLabel#label_8, QLabel#label_10, QLabel#label_2, QLabel#label_3,
QLabel#label_4 {{
    color: {TEXTO_SUAVE};
}}
QLabel#LblTotal, QLabel#LblPrecio, QLabel#LblCaja {{
    color: {MORADO_OSCURO};
}}
QLabel#LblOferta {{
    color: {MORADO};
    font-weight: 800;
}}
QLabel#LblAviso {{
    color: {TEXTO_SUAVE};
}}
QLabel#LblFoto {{
    background-color: {CREMA_CLARA};
    border: 2px solid {BORDE};
    border-radius: 14px;
}}
QLabel#lblAgotado {{
    background-color: rgba(61, 46, 102, 175);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1px;
}}

/* ---------------------------------------------------------------- botones */
QPushButton {{
    background-color: {MORADO};
    color: #FFFFFF;
    border: 2px solid {MORADO_BORDE};
    border-radius: 10px;
    padding: 3px 12px;
    font-size: 13px;
    font-weight: 700;
}}
QPushButton:hover {{
    background-color: {MORADO_CLARO};
    border-color: {MORADO_OSCURO};
}}
QPushButton:pressed {{
    background-color: {MORADO_OSCURO};
    border-color: {MORADO_BORDE};
}}
QPushButton:disabled {{
    background-color: #DCD3EE;
    color: #9A8FB5;
    border-color: #CDC2E4;
}}

QPushButton#btnVolver, QPushButton#btnCarrito,
QPushButton#btnSeguir, QPushButton#btnMembresia,
QPushButton#btnCatalogo, QPushButton#btnSalir {{
    background-color: rgba(255, 255, 255, 0.55);
    color: {MORADO_OSCURO};
    border: 2px solid #C9B6E6;
}}
QPushButton#btnVolver:hover, QPushButton#btnCarrito:hover,
QPushButton#btnSeguir:hover, QPushButton#btnMembresia:hover,
QPushButton#btnCatalogo:hover, QPushButton#btnSalir:hover {{
    background-color: #F1EBFC;
    border-color: {MORADO};
    color: {TEXTO};
}}
QPushButton#btnVolver:pressed, QPushButton#btnCarrito:pressed,
QPushButton#btnSeguir:pressed, QPushButton#btnMembresia:pressed,
QPushButton#btnCatalogo:pressed, QPushButton#btnSalir:pressed {{
    background-color: {LAVANDA};
}}

QPushButton#btnVaciar, QPushButton#btnQuitarFila {{
    background-color: rgba(255, 255, 255, 0.62);
    color: {ROJO};
    border: 2px solid {ROJO_BORDE};
}}
QPushButton#btnVaciar:hover, QPushButton#btnQuitarFila:hover {{
    background-color: #F8E4E1;
    border-color: #C0504D;
    color: {ROJO};
}}
QPushButton#btnVaciar:pressed, QPushButton#btnQuitarFila:pressed {{
    background-color: #F0D3CE;
}}
QPushButton#btnQuitarFila {{
    font-size: 11px;
    padding: 2px 8px;
}}

/* --------------------------------------------------------------- portadas */
QPushButton#Cover1, QPushButton#Cover2, QPushButton#Cover3,
QPushButton#Cover4, QPushButton#Cover5, QPushButton#Cover6,
QPushButton#Cover7, QPushButton#Cover8, QPushButton#Cover9,
QPushButton#Cover10, QPushButton#Cover11, QPushButton#Cover12,
QPushButton#Cover13, QPushButton#Cover14, QPushButton#Cover15,
QPushButton#Cover16 {{
    background: transparent;
    border: none;
    padding: 0px;
}}
QFrame#haloPortada {{
    background-color: rgba(124, 77, 255, 35);
    border: 2px solid {MORADO};
    border-radius: 12px;
}}

/* ---------------------------------------------------------------- campos */
QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QComboBox {{
    background-color: #FFFFFF;
    border: 2px solid {BORDE_FUERTE};
    border-radius: 8px;
    padding: 3px 8px;
    color: {TEXTO};
    font-size: 12px;
    selection-background-color: {MORADO_CLARO};
    selection-color: #FFFFFF;
}}
QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover,
QTextEdit:hover, QComboBox:hover {{
    border-color: {MORADO_CLARO};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QTextEdit:focus, QComboBox:focus {{
    border-color: {MORADO};
}}
QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled,
QTextEdit:disabled, QComboBox:disabled {{
    background-color: #F2ECD9;
    border-color: #E4D8B8;
    color: #A79A88;
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: url("{FLECHA_ABAJO}");
    width: 12px;
    height: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {CREMA_CLARA};
    border: 1px solid {BORDE_FUERTE};
    selection-background-color: {LAVANDA};
    selection-color: {TEXTO};
    outline: none;
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border: none;
    border-left: 1px solid {BORDE};
    border-top-right-radius: 6px;
    background: transparent;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border: none;
    border-left: 1px solid {BORDE};
    border-bottom-right-radius: 6px;
    background: transparent;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {LAVANDA};
}}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed,
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
    background-color: #DCD3EE;
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: url("{FLECHA_ARRIBA}");
    width: 10px;
    height: 7px;
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: url("{FLECHA_ABAJO}");
    width: 10px;
    height: 7px;
}}
QTextEdit#textBoleta {{
    background-color: #FFFDF7;
    border: 2px solid {BORDE};
    border-radius: 12px;
    padding: 10px;
    font-size: 12px;
}}

/* ---------------------------------------------------------------- tablas */
QTableWidget {{
    background-color: {CREMA_CLARA};
    alternate-background-color: #FDF3D2;
    border: 2px solid {BORDE};
    border-radius: 12px;
    gridline-color: #F0E4C6;
    color: {TEXTO};
    font-size: 12px;
    selection-background-color: {LAVANDA};
    selection-color: {TEXTO};
}}
QTableWidget::item {{
    padding: 5px 8px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: {LAVANDA};
    color: {TEXTO};
}}
QHeaderView {{
    background-color: {CREMA_BANDA};
    border: none;
}}
QHeaderView::section {{
    background-color: {CREMA_BANDA};
    color: {MORADO_OSCURO};
    border: none;
    border-right: 1px solid {BORDE};
    border-bottom: 1px solid {BORDE};
    padding: 6px 8px;
    font-size: 12px;
    font-weight: 700;
}}
QTableCornerButton::section {{
    background-color: {CREMA_BANDA};
    border: none;
}}
QTableWidget QComboBox {{
    font-size: 11px;
    padding: 1px 6px;
}}

/* -------------------------------------------------------------- scrollbar */
QScrollBar:vertical {{
    background: {CREMA_BANDA};
    width: 12px;
    margin: 0px;
    border-radius: 6px;
}}
QScrollBar::handle:vertical {{
    background: #C9B6E6;
    min-height: 30px;
    border-radius: 6px;
}}
QScrollBar::handle:vertical:hover {{
    background: {MORADO_CLARO};
}}
QScrollBar::handle:vertical:pressed {{
    background: {MORADO_OSCURO};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
QScrollBar:horizontal {{
    background: {CREMA_BANDA};
    height: 12px;
    margin: 0px;
    border-radius: 6px;
}}
QScrollBar::handle:horizontal {{
    background: #C9B6E6;
    min-width: 30px;
    border-radius: 6px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {MORADO_CLARO};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: transparent;
}}

QMenuBar, QStatusBar {{
    background-color: {CREMA};
    color: {TEXTO_SUAVE};
}}
QToolTip {{
    background-color: {TEXTO};
    color: {CREMA_CLARA};
    border: none;
    padding: 6px;
}}
"""


def aplicar_tema_usuario(ventana):
    """Aplica el tema a la ventana y al lienzo que se escala a pantalla."""
    ventana.setStyleSheet(QSS_USUARIO)

    central = getattr(ventana, "_lienzo", None)
    if central is None:
        central = ventana.centralWidget()
    if isinstance(central, QWidget):
        # El lienzo se mueve a una escena grafica; tener el QSS aqui asegura
        # que todos sus hijos lo hereden aunque cambie de padre.
        central.setStyleSheet(QSS_USUARIO)

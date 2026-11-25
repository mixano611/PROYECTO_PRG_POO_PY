"""Tema visual beige para las ventanas del administrador.

Centralizar los estilos aqui permite que todas las pantallas del panel
de administracion se vean igual de elegantes sin repetir el mismo bloque
de QSS en cada archivo .ui.
"""

from pathlib import Path

from PyQt5.QtCore import QAbstractAnimation, QEasingCurve, QPropertyAnimation, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QWidget,
)

# Paleta beige usada en todo el panel de administracion.
BEIGE_FONDO = "#F4EEE3"
BEIGE_TARJETA = "#FFFCF6"
BEIGE_BORDE = "#E6DAC9"
BEIGE_ACENTO = "#B98A4E"
BEIGE_TEXTO = "#3F382F"
BEIGE_TEXTO_SUAVE = "#8A7B69"

# Iconos pequenos del tema (rutas absolutas para que el QSS los encuentre).
_ASSETS = Path(__file__).resolve().parent / "assets"
FLECHA_ABAJO = (_ASSETS / "chevron_down.png").as_posix()
FLECHA_ARRIBA = (_ASSETS / "chevron_up.png").as_posix()
ICONO_CHECK = (_ASSETS / "check.png").as_posix()

QSS_ADMIN = f"""
QMainWindow, QWidget#centralwidget, QWidget#lienzo {{
    background-color: {BEIGE_FONDO};
}}
QWidget {{
    color: {BEIGE_TEXTO};
    font-family: "Segoe UI";
    font-size: 14px;
}}
QLabel {{
    background: transparent;
    color: #4A4036;
}}
QLabel#LblTitulo, QLabel#LblMarca {{
    color: #352E26;
    font-size: 31px;
    font-weight: 700;
}}
QLabel#LblSubtitulo, QLabel#LblAyudaLogin, QLabel#LblCajas,
QLabel#LblAviso, QLabel#LblAvisoBusqueda {{
    color: {BEIGE_TEXTO_SUAVE};
    font-size: 14px;
}}
QLabel#LblRol, QLabel#LblRolAdmin {{
    color: #A8865B;
    font-size: 13px;
    font-weight: 700;
}}
QLabel#LblSeccion, QLabel#LblSeccionAcciones,
QLabel#LblSolicitudes, QLabel#LblMiembros {{
    color: #6B5A45;
    font-size: 14px;
    font-weight: 700;
}}
QLabel#LblResumen {{
    color: #5A4A38;
    font-size: 14px;
    font-weight: 600;
}}
QFrame#statLibros, QFrame#statPrestamos, QFrame#statMiembros,
QFrame#tipAcciones {{
    background-color: #F8F2E7;
    border: 1px solid #EDE2D2;
    border-radius: 12px;
}}
QLabel#LblStatLibros, QLabel#LblStatPrestamos, QLabel#LblStatMiembros {{
    color: {BEIGE_ACENTO};
    font-size: 24px;
    font-weight: 700;
}}
QLabel#LblStatLibrosCap, QLabel#LblStatPrestamosCap,
QLabel#LblStatMiembrosCap {{
    color: {BEIGE_TEXTO_SUAVE};
    font-size: 12px;
}}
QLabel#LblTipTitulo {{
    color: #A8865B;
    font-size: 12px;
    font-weight: 700;
}}
QLabel#LblTip {{
    color: {BEIGE_TEXTO_SUAVE};
    font-size: 13px;
}}
QLabel#LblResumenCajas {{
    background-color: #EFE6D8;
    border-radius: 10px;
    padding: 6px 14px;
    color: #6B5A45;
    font-size: 14px;
    font-weight: 700;
}}
QFrame#cardLogin, QFrame#cardBusqueda, QFrame#cardAcciones,
QFrame#cardSolicitudes, QFrame#cardMiembros, QFrame#cardCajas,
QFrame#cardResumen, QFrame#cardFormulario {{
    background-color: {BEIGE_TARJETA};
    border: 1px solid {BEIGE_BORDE};
    border-radius: 18px;
}}
QFrame#lineaSeparador {{
    background-color: {BEIGE_BORDE};
    border: none;
}}
QPushButton {{
    background-color: {BEIGE_ACENTO};
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 9px 18px;
    font-size: 14px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #A87A41;
}}
QPushButton:pressed {{
    background-color: #946A37;
}}
QPushButton:disabled {{
    background-color: #E6DAC9;
    color: #A79A88;
}}
QPushButton#btnVolver, QPushButton#pushButton {{
    background-color: transparent;
    color: #7C6C58;
    border: 1px solid #D9CBB6;
    border-radius: 9px;
    padding: 8px 16px;
    font-weight: 600;
}}
QPushButton#btnVolver:hover, QPushButton#pushButton:hover {{
    background-color: #EFE6D8;
    color: {BEIGE_TEXTO};
    border-color: #C9B69C;
}}
QPushButton#btnAceptar {{
    background-color: #6F8F63;
}}
QPushButton#btnAceptar:hover {{
    background-color: #5F7C55;
}}
QPushButton#btnDenegar, QPushButton#btnEliminar, QPushButton#btnQuitar {{
    background-color: #B36B62;
}}
QPushButton#btnDenegar:hover, QPushButton#btnEliminar:hover,
QPushButton#btnQuitar:hover {{
    background-color: #9E5B53;
}}
QPushButton#btnNuevoLibro, QPushButton#btnMembresias,
QPushButton#btnCajas, QPushButton#btnReportes {{
    background-color: {BEIGE_TARJETA};
    color: {BEIGE_TEXTO};
    border: 1px solid {BEIGE_BORDE};
    border-radius: 14px;
    padding: 11px 18px;
    font-size: 15px;
    font-weight: 600;
    text-align: left;
}}
QPushButton#btnNuevoLibro:hover, QPushButton#btnMembresias:hover,
QPushButton#btnCajas:hover, QPushButton#btnReportes:hover {{
    background-color: #F8F0E2;
    border-color: #C9A87C;
    color: #352E26;
}}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{
    background-color: #FFFFFF;
    border: 1px solid #DDCFBB;
    border-radius: 8px;
    padding: 8px 10px;
    color: {BEIGE_TEXTO};
    selection-background-color: #C9A87C;
    selection-color: #FFFFFF;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
QDoubleSpinBox:focus, QTextEdit:focus {{
    border: 1px solid #C9A87C;
}}
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled,
QDoubleSpinBox:disabled, QTextEdit:disabled {{
    background-color: #F1EAE0;
    color: #A79A88;
}}
QComboBox::drop-down {{
    border: none;
    width: 26px;
}}
QComboBox::down-arrow {{
    image: url("{FLECHA_ABAJO}");
    width: 12px;
    height: 8px;
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border: none;
    border-left: 1px solid #DDCFBB;
    border-top-right-radius: 8px;
    background: transparent;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border: none;
    border-left: 1px solid #DDCFBB;
    border-bottom-right-radius: 8px;
    background: transparent;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: #F1E6D5;
}}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed,
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
    background-color: #E7D9C4;
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
QComboBox QAbstractItemView {{
    background-color: {BEIGE_TARJETA};
    border: 1px solid #DDCFBB;
    selection-background-color: #EFE6D8;
    selection-color: {BEIGE_TEXTO};
    outline: none;
}}
QTableWidget {{
    background-color: {BEIGE_TARJETA};
    alternate-background-color: #FBF6ED;
    border: 1px solid {BEIGE_BORDE};
    border-radius: 12px;
    gridline-color: #F1E9DC;
    selection-background-color: #EFE1CB;
    selection-color: {BEIGE_TEXTO};
}}
QTableWidget::item {{
    padding: 7px 8px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: #EFE1CB;
    color: {BEIGE_TEXTO};
}}
QHeaderView::section {{
    background-color: #F0E7DA;
    color: #6B5A45;
    border: none;
    border-right: 1px solid {BEIGE_BORDE};
    border-bottom: 1px solid {BEIGE_BORDE};
    padding: 9px 8px;
    font-size: 13px;
    font-weight: 700;
}}
QHeaderView {{
    background-color: #F0E7DA;
    border: none;
}}
QTableCornerButton::section {{
    background-color: #F0E7DA;
    border: none;
}}
QCheckBox {{
    color: #4A4036;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #C9B69C;
    border-radius: 4px;
    background-color: #FFFFFF;
}}
QCheckBox::indicator:checked {{
    background-color: {BEIGE_ACENTO};
    border-color: {BEIGE_ACENTO};
    image: url("{ICONO_CHECK}");
}}
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: #D9CBB6;
    border-radius: 5px;
    min-height: 28px;
}}
QScrollBar::handle:vertical:hover {{
    background: #C9A87C;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: #D9CBB6;
    border-radius: 5px;
    min-width: 28px;
}}
QScrollBar::handle:horizontal:hover {{
    background: #C9A87C;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: transparent;
}}
QMenuBar {{
    background-color: transparent;
    color: #6B5A45;
}}
QMenuBar::item {{
    background: transparent;
    padding: 6px 14px;
    border-radius: 6px;
}}
QMenuBar::item:selected {{
    background-color: #EFE6D8;
}}
QMenu {{
    background-color: {BEIGE_TARJETA};
    border: 1px solid {BEIGE_BORDE};
    padding: 6px;
}}
QMenu::item {{
    padding: 7px 24px;
    border-radius: 6px;
}}
QMenu::item:selected {{
    background-color: #EFE6D8;
}}
QStatusBar {{
    background: transparent;
    color: {BEIGE_TEXTO_SUAVE};
}}
QToolTip {{
    background-color: {BEIGE_TEXTO};
    color: {BEIGE_TARJETA};
    border: none;
    padding: 6px;
}}
"""


def _aplicar_sombras(ventana):
    """Da profundidad a las tarjetas marcadas con la propiedad sombra."""
    for widget in ventana.findChildren(QWidget):
        if not widget.property("sombra"):
            continue
        efecto = QGraphicsDropShadowEffect(widget)
        efecto.setBlurRadius(34)
        efecto.setOffset(0, 9)
        efecto.setColor(QColor(120, 96, 64, 40))
        widget.setGraphicsEffect(efecto)


def _preparar_tablas(ventana):
    """Deja las tablas con filas alternas y seleccion completa."""
    for tabla in ventana.findChildren(QTableWidget):
        tabla.setAlternatingRowColors(True)
        tabla.setShowGrid(False)
        tabla.setWordWrap(False)
        tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        tabla.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.EditKeyPressed
            | QAbstractItemView.AnyKeyPressed
        )
        tabla.verticalHeader().setVisible(False)
        tabla.verticalHeader().setDefaultSectionSize(36)
        cabecera = tabla.horizontalHeader()
        cabecera.setHighlightSections(False)
        cabecera.setMinimumSectionSize(70)
        cabecera.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        if tabla.objectName() == "tableWidget":
            # La tabla del almacén conserva los anchos que define el codigo
            # y la ultima columna ocupa el espacio restante.
            cabecera.setSectionResizeMode(QHeaderView.Interactive)
            cabecera.setStretchLastSection(True)
        else:
            cabecera.setSectionResizeMode(QHeaderView.Stretch)
            cabecera.setStretchLastSection(False)


def aplicar_tema_admin(ventana):
    """Aplica el tema beige, sombras y detalles a una ventana admin."""
    ventana.setStyleSheet(QSS_ADMIN)

    for boton in ventana.findChildren(QPushButton):
        boton.setCursor(Qt.CursorShape.PointingHandCursor)

    _preparar_tablas(ventana)
    _aplicar_sombras(ventana)


def animar_entrada(ventana):
    """Aparicion suave del contenido al abrir una ventana del panel."""
    central = ventana.centralWidget()
    if central is None:
        return

    efecto = QGraphicsOpacityEffect(central)
    efecto.setOpacity(0.0)
    central.setGraphicsEffect(efecto)

    animacion = QPropertyAnimation(efecto, b"opacity", central)
    animacion.setDuration(260)
    animacion.setStartValue(0.0)
    animacion.setEndValue(1.0)
    animacion.setEasingCurve(QEasingCurve.Type.OutCubic)
    animacion.finished.connect(lambda: central.setGraphicsEffect(None))
    animacion.start(QAbstractAnimation.DeleteWhenStopped)

    # Se guarda la referencia para que Python no la elimine antes de tiempo.
    ventana._animacion_entrada = animacion

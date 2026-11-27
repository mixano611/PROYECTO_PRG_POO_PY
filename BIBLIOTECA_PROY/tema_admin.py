"""Tema visual del panel de administracion.

Comparte la paleta del area de usuario: fondo crema, tarjetas claras y
morado como color de accion. Asi el login, las pantallas del usuario y el
panel del administrador forman un solo lenguaje visual.
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

from tema_usuario import (
    BORDE,
    BORDE_FUERTE,
    CREMA,
    CREMA_BANDA,
    CREMA_CLARA,
    CREMA_TARJETA,
    FLECHA_ABAJO,
    FLECHA_ARRIBA,
    LAVANDA,
    MORADO,
    MORADO_BORDE,
    MORADO_CLARO,
    MORADO_OSCURO,
    ROJO,
    TEXTO,
    TEXTO_SUAVE,
)

_ASSETS = Path(__file__).resolve().parent / "assets"
ICONO_CHECK = (_ASSETS / "check_blanco.png").as_posix()

QSS_ADMIN = f"""
QMainWindow, QWidget#centralwidget, QWidget#lienzo {{
    background-color: {CREMA};
}}
QWidget {{
    color: {TEXTO};
    font-family: "Segoe UI";
    font-size: 14px;
}}
QLabel {{
    background: transparent;
    color: {TEXTO};
}}
QLabel#LblTitulo, QLabel#LblMarca {{
    color: {TEXTO};
    font-size: 31px;
    font-weight: 700;
}}
QLabel#LblSubtitulo, QLabel#LblAyudaLogin, QLabel#LblCajas,
QLabel#LblAviso, QLabel#LblAvisoBusqueda {{
    color: {TEXTO_SUAVE};
    font-size: 14px;
}}
QLabel#LblRol, QLabel#LblRolAdmin {{
    color: {MORADO_CLARO};
    font-size: 13px;
    font-weight: 700;
}}
QLabel#LblSeccion, QLabel#LblSeccionAcciones,
QLabel#LblSolicitudes, QLabel#LblMiembros {{
    color: {MORADO_OSCURO};
    font-size: 14px;
    font-weight: 700;
}}
QLabel#LblResumen {{
    color: {TEXTO};
    font-size: 14px;
    font-weight: 600;
}}
QFrame#statLibros, QFrame#statPrestamos, QFrame#statMiembros,
QFrame#tipAcciones {{
    background-color: {CREMA_TARJETA};
    border: 1px solid {BORDE};
    border-radius: 12px;
}}
QLabel#LblStatLibros, QLabel#LblStatPrestamos, QLabel#LblStatMiembros {{
    color: {MORADO};
    font-size: 24px;
    font-weight: 700;
}}
QLabel#LblStatLibrosCap, QLabel#LblStatPrestamosCap,
QLabel#LblStatMiembrosCap {{
    color: {TEXTO_SUAVE};
    font-size: 12px;
}}
QLabel#LblTipTitulo {{
    color: {MORADO_CLARO};
    font-size: 12px;
    font-weight: 700;
}}
QLabel#LblTip {{
    color: {TEXTO_SUAVE};
    font-size: 13px;
}}
QLabel#LblResumenCajas {{
    background-color: {LAVANDA};
    border-radius: 10px;
    padding: 6px 14px;
    color: {MORADO_OSCURO};
    font-size: 14px;
    font-weight: 700;
}}
QFrame#cardLogin, QFrame#cardBusqueda, QFrame#cardAcciones,
QFrame#cardSolicitudes, QFrame#cardMiembros, QFrame#cardCajas,
QFrame#cardResumen, QFrame#cardFormulario {{
    background-color: {CREMA_CLARA};
    border: 1px solid {BORDE};
    border-radius: 18px;
}}
QFrame#lineaSeparador {{
    background-color: {BORDE};
    border: none;
}}
QPushButton {{
    background-color: {MORADO};
    color: #FFFFFF;
    border: 2px solid {MORADO_BORDE};
    border-radius: 10px;
    padding: 9px 18px;
    font-size: 14px;
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
QPushButton#btnVolver, QPushButton#pushButton {{
    background-color: {CREMA_CLARA};
    color: {MORADO_OSCURO};
    border: 2px solid #C9B6E6;
    border-radius: 9px;
    padding: 8px 16px;
    font-weight: 700;
}}
QPushButton#btnVolver:hover, QPushButton#pushButton:hover {{
    background-color: #F1EBFC;
    color: {TEXTO};
    border-color: {MORADO};
}}
QPushButton#btnAceptar {{
    background-color: {MORADO};
    border-color: {MORADO_BORDE};
}}
QPushButton#btnAceptar:hover {{
    background-color: {MORADO_CLARO};
}}
QPushButton#btnDenegar, QPushButton#btnEliminar, QPushButton#btnQuitar {{
    background-color: {ROJO};
    border-color: #8E3532;
}}
QPushButton#btnDenegar:hover, QPushButton#btnEliminar:hover,
QPushButton#btnQuitar:hover {{
    background-color: #8E3532;
    border-color: #792B29;
}}
QPushButton#btnNuevoLibro, QPushButton#btnMembresias,
QPushButton#btnCajas, QPushButton#btnReportes {{
    background-color: {CREMA_CLARA};
    color: {TEXTO};
    border: 2px solid {BORDE};
    border-radius: 14px;
    padding: 11px 18px;
    font-size: 15px;
    font-weight: 600;
    text-align: left;
}}
QPushButton#btnNuevoLibro:hover, QPushButton#btnMembresias:hover,
QPushButton#btnCajas:hover, QPushButton#btnReportes:hover {{
    background-color: {LAVANDA};
    border-color: {MORADO_CLARO};
    color: {TEXTO};
}}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{
    background-color: #FFFFFF;
    border: 2px solid {BORDE_FUERTE};
    border-radius: 8px;
    padding: 7px 10px;
    color: {TEXTO};
    selection-background-color: {MORADO_CLARO};
    selection-color: #FFFFFF;
}}
QLineEdit:hover, QComboBox:hover, QSpinBox:hover,
QDoubleSpinBox:hover, QTextEdit:hover {{
    border-color: {MORADO_CLARO};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
QDoubleSpinBox:focus, QTextEdit:focus {{
    border-color: {MORADO};
}}
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled,
QDoubleSpinBox:disabled, QTextEdit:disabled {{
    background-color: #F2ECD9;
    border-color: #E4D8B8;
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
QComboBox QAbstractItemView {{
    background-color: {CREMA_CLARA};
    border: 1px solid {BORDE_FUERTE};
    selection-background-color: {LAVANDA};
    selection-color: {TEXTO};
    outline: none;
}}
QTableWidget {{
    background-color: {CREMA_CLARA};
    alternate-background-color: #FDF3D2;
    border: 2px solid {BORDE};
    border-radius: 12px;
    gridline-color: #F0E4C6;
    color: {TEXTO};
    selection-background-color: {LAVANDA};
    selection-color: {TEXTO};
}}
QTableWidget::item {{
    padding: 7px 8px;
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
    padding: 9px 8px;
    font-size: 13px;
    font-weight: 700;
}}
QTableCornerButton::section {{
    background-color: {CREMA_BANDA};
    border: none;
}}
QCheckBox {{
    color: {TEXTO};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {BORDE_FUERTE};
    border-radius: 4px;
    background-color: #FFFFFF;
}}
QCheckBox::indicator:checked {{
    background-color: {MORADO};
    border-color: {MORADO_BORDE};
    image: url("{ICONO_CHECK}");
}}
QScrollBar:vertical {{
    background: {CREMA_BANDA};
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical {{
    background: #C9B6E6;
    border-radius: 5px;
    min-height: 28px;
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
    height: 10px;
    margin: 0px;
    border-radius: 5px;
}}
QScrollBar::handle:horizontal {{
    background: #C9B6E6;
    border-radius: 5px;
    min-width: 28px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {MORADO_CLARO};
}}
QScrollBar::handle:horizontal:pressed {{
    background: {MORADO_OSCURO};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: transparent;
}}
QMenuBar {{
    background-color: {CREMA};
    color: {MORADO_OSCURO};
}}
QMenuBar::item {{
    background: transparent;
    padding: 6px 14px;
    border-radius: 6px;
}}
QMenuBar::item:selected {{
    background-color: {LAVANDA};
}}
QMenu {{
    background-color: {CREMA_CLARA};
    border: 1px solid {BORDE};
    padding: 6px;
}}
QMenu::item {{
    padding: 7px 24px;
    border-radius: 6px;
}}
QMenu::item:selected {{
    background-color: {LAVANDA};
    color: {TEXTO};
}}
QStatusBar {{
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


def _aplicar_sombras(ventana):
    """Da profundidad a las tarjetas marcadas con la propiedad sombra."""
    for widget in ventana.findChildren(QWidget):
        if not widget.property("sombra"):
            continue
        efecto = QGraphicsDropShadowEffect(widget)
        efecto.setBlurRadius(32)
        efecto.setOffset(0, 8)
        efecto.setColor(QColor(90, 70, 150, 40))
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
    """Aplica el tema crema/morado, sombras y detalles a una ventana admin."""
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

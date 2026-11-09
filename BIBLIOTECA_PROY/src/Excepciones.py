"""Excepciones propias del sistema de biblioteca.

Se usan para que la logica de negocio no dependa de la interfaz. las
ventanas capturan estos errores y muestran el mensaje al usuario. Waaa
"""


class BibliotecaError(Exception):
    """Error base de todo el sistema."""


class DatosInvalidosError(BibliotecaError):
    """Un dato ingresado no cumple las reglas del sistema."""


class LibroNoDisponibleError(BibliotecaError):
    """El libro no existe o ya no tiene ejemplares."""


class StockInsuficienteError(BibliotecaError):
    """No hay suficientes ejemplares para la cantidad pedida."""

    def __init__(self, nombre_libro: str, disponibles: int):
        self.nombre_libro = nombre_libro
        self.disponibles = disponibles
        super().__init__(f'Solo quedan {disponibles} ejemplar(es) de "{nombre_libro}".')


class SinCajaDisponibleError(BibliotecaError):
    """Todas las cajas están cerradas."""


class CarritoVacioError(BibliotecaError):
    """Se intentó pagar un carrito sin productos."""


class MembresiaError(BibliotecaError):
    """Problema al registrar o usar una membresía."""

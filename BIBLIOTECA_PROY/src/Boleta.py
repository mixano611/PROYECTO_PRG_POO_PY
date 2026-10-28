import json
from json import JSONDecodeError
from pathlib import Path


class boleta:
    def __init__(self, nombre, dni, producto, monto, cant, tiempo):
        self.nombre = nombre
        self.dni = dni
        self.producto = producto
        self.monto = monto
        self.cant = cant
        self.tiempo = tiempo

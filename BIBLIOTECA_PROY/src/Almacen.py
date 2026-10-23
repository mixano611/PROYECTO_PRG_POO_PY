import time
import json
from json import JSONDecodeError
from pathlib import Path

ruta = Path(__file__).parent / 'data' / 'Almacen.json'

def cargar_datos():
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print("El archivo 'Almacen.json' no se encontró. Se creará uno nuevo.")
        return {}
    except JSONDecodeError:
        print("Error al decodificar el archivo JSON. Se creará un archivo nuevo.")
        return {}

def guardar_datos(datos):
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)



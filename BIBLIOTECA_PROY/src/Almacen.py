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

#---------------------------------------------------------------------------------------------

def ver_almacen():
    datos = cargar_datos()
    if not datos:
        print("El almacén está vacío.")
        return
    
    print("Cargando datos del almacén...")
    time.sleep(1)
    print('\n-------------------------------')
    print("Contenido del almacén:")
    print("-------------------------------")
    for clave, valor in datos.items():
        print(f"# {clave}:\t{valor}")

def agregar_producto_g(nombre, stock):
    datos = cargar_datos()
    if nombre in datos:
        print(f"El producto '{nombre}' ya existe en el almacén. Se actualizará la cantidad.")
        datos[nombre] += stock
    else:
        datos[nombre] = stock
    guardar_datos(datos)
    print(f"Producto '{nombre}' agregado/actualizado con cantidad {stock}.")

def eliminar_producto_g(nombre):
    datos = cargar_datos()
    if nombre in datos:
        del datos[nombre]
        guardar_datos(datos)
        print(f"Producto '{nombre}' eliminado del almacén.")
    else:
        print(f"El producto '{nombre}' no se encuentra en el almacén.")
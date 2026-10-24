import json
from json import JSONDecodeError
from pathlib import Path

RUTA_ALMACEN = Path(__file__).resolve().parent.parent / "data" / "Almacen.json"


def cargar_datos():
    try:
        with open(RUTA_ALMACEN, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        print(f"No se encontró {RUTA_ALMACEN.name}. Se empieza con un almacén vacío.")
        return {"libros": []}
    except JSONDecodeError:
        print(
            f"{RUTA_ALMACEN.name} tiene un error de formato. Se empieza con un almacén vacío."
        )
        return {"libros": []}

    # También acepta un archivo que sea directamente una lista de libros.
    if isinstance(datos, list):
        return {"libros": datos}

    if not isinstance(datos, dict):
        return {"libros": []}

    datos.setdefault("libros", [])
    return datos


def guardar_datos(datos):
    with open(RUTA_ALMACEN, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def cargar_libros():
    return cargar_datos()["libros"]

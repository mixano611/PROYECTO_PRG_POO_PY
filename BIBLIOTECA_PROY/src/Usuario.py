import json
from json import JSONDecodeError
from pathlib import Path


RUTA_USUARIOS = Path(__file__).resolve().parent.parent / "data" / "usuarios_data.json"


def cargar_usuarios():
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        guardar_usuarios({})
        return {}
    except JSONDecodeError:
        print(f"{RUTA_USUARIOS.name} tiene un error de formato. Se crea de nuevo.")
        guardar_usuarios({})
        return {}

    if not isinstance(datos, dict):
        guardar_usuarios({})
        return {}

    return datos


def guardar_usuarios(usuarios):
    RUTA_USUARIOS.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)


def registrar_usuario(nombre, dni):
    nombre = str(nombre or "").strip().lower()
    dni = str(dni or "").strip()

    if not nombre or not dni:
        return False

    usuarios = cargar_usuarios()

    if nombre in usuarios and usuarios[nombre] != dni:
        return False

    usuarios[nombre] = dni
    guardar_usuarios(usuarios)
    return True


def existe_usuario(nombre):
    return str(nombre or "").strip().lower() in cargar_usuarios()

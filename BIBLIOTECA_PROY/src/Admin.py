import json
from json import JSONDecodeError
from pathlib import Path

# data/ está un nivel arriba de src/
RUTA_ADM = Path(__file__).resolve().parent.parent / "data" / "admin_data.json"

# Cuenta que se crea si admin_data.json no existe o está dañado.
ADMIN_POR_DEFECTO = {"admin": "admin123"}


def cargar_adm():
    try:
        with open(RUTA_ADM, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        guardar_adm(ADMIN_POR_DEFECTO)
        return dict(ADMIN_POR_DEFECTO)
    except JSONDecodeError:
        print(f"{RUTA_ADM.name} tiene un error de formato. Se crea de nuevo.")
        guardar_adm(ADMIN_POR_DEFECTO)
        return dict(ADMIN_POR_DEFECTO)

    if not isinstance(datos, dict):
        guardar_adm(ADMIN_POR_DEFECTO)
        return dict(ADMIN_POR_DEFECTO)

    return datos


def guardar_adm(cuentas):
    RUTA_ADM.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_ADM, "w", encoding="utf-8") as archivo:
        json.dump(cuentas, archivo, indent=4, ensure_ascii=False)


def validar_admin(nombre, contrasena):
    nombre = str(nombre or "").strip().lower()
    contrasena = str(contrasena or "")

    if not nombre or not contrasena:
        return False

    # Se normalizan las claves del archivo para que "Admin" y "admin"
    # sean la misma cuenta, igual que se explica en el formato de arriba.
    cuentas = {
        str(clave).strip().lower(): str(valor) for clave, valor in cargar_adm().items()
    }
    return cuentas.get(nombre) == contrasena

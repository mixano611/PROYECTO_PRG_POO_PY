"""Guardado y carga del carrito en data/carrito_data.json."""

import json
from json import JSONDecodeError
from pathlib import Path

from src.Almacen import cargar_datos
from src.Busqueda import buscar_por_id
from src.Excepciones import DatosInvalidosError
from src.Modelos import Carrito, ItemCarrito, Libro, Usuario

RUTA_CARRITOS = Path(__file__).resolve().parent.parent / "data" / "carrito_data.json"


def cargar_carritos() -> dict:
    """Devuelve {usuario: [items]} y crea el archivo si falta o está dañado."""
    try:
        with open(RUTA_CARRITOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        guardar_carritos({})
        return {}
    except JSONDecodeError:
        print(f"{RUTA_CARRITOS.name} tiene un error de formato. Se crea de nuevo.")
        guardar_carritos({})
        return {}

    if not isinstance(datos, dict):
        guardar_carritos({})
        return {}

    return datos


def guardar_carritos(carritos: dict) -> None:
    RUTA_CARRITOS.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_CARRITOS, "w", encoding="utf-8") as archivo:
        json.dump(carritos, archivo, indent=4, ensure_ascii=False)


def cargar_carrito(usuario: Usuario) -> Carrito:
    """Arma el carrito del usuario con los libros actuales del almacén."""
    carritos = cargar_carritos()
    filas = carritos.get(usuario.nombre, [])
    libros_json = cargar_datos()["libros"]
    items: list[ItemCarrito] = []

    for fila in filas:
        if not isinstance(fila, dict):
            continue
        libro_json = buscar_por_id(libros_json, int(fila.get("id_libro", 0) or 0))
        if libro_json is None:
            continue
        libro = Libro.desde_dict(libro_json)
        try:
            items.append(
                ItemCarrito(
                    libro,
                    cantidad=int(fila.get("cantidad", 1) or 1),
                    tipo=fila.get("tipo", "COMPRA"),
                )
            )
        except DatosInvalidosError:
            continue

    return Carrito(usuario, items)


def guardar_carrito(carrito: Carrito) -> None:
    carritos = cargar_carritos()
    carritos[carrito.usuario.nombre] = carrito.a_lista()
    guardar_carritos(carritos)


def cantidad_en_carrito(nombre: str) -> int:
    """Cantidad total de ejemplares que el usuario tiene en el carrito."""
    carritos = cargar_carritos()
    filas = carritos.get(str(nombre or "").strip().lower(), [])
    total = 0
    for fila in filas:
        if isinstance(fila, dict):
            try:
                total += int(fila.get("cantidad", 0) or 0)
            except (TypeError, ValueError):
                continue
    return total

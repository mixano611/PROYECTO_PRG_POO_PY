from src.Modelos import Libro


def buscar_por_id(
    libros: list[dict],
    id_libro: int,
    indice: int = 0,
) -> dict | None:

    if indice >= len(libros):
        return None
    if libros[indice].get("id") == id_libro:
        return libros[indice]
    return buscar_por_id(libros, id_libro, indice + 1)


def contar_disponibles(libros: list[dict], indice: int = 0) -> int:
    if indice >= len(libros):
        return 0
    disponible = 1 if int(libros[indice].get("stock", 0) or 0) > 0 else 0
    return disponible + contar_disponibles(libros, indice + 1)


def buscar_por_nombre(
    libros: list[dict],
    nombre: str,
    inicio: int = 0,
    fin: int | None = None,
) -> dict | None:

    nombre = str(nombre or "").strip().lower()
    if not nombre:
        return None

    if fin is None:
        fin = len(libros) - 1
        ordenados = [str(libro.get("nombre", "")).lower() for libro in libros]
        if ordenados != sorted(ordenados):
            return _buscar_lineal(libros, nombre)

    if inicio > fin:
        return None

    medio = (inicio + fin) // 2
    actual = str(libros[medio].get("nombre", "")).strip().lower()
    if actual == nombre:
        return libros[medio]
    if actual < nombre:
        return buscar_por_nombre(libros, nombre, medio + 1, fin)
    return buscar_por_nombre(libros, nombre, inicio, medio - 1)


def _buscar_lineal(libros: list[dict], nombre: str, indice: int = 0) -> dict | None:
    if indice >= len(libros):
        return None
    if str(libros[indice].get("nombre", "")).strip().lower() == nombre:
        return libros[indice]
    return _buscar_lineal(libros, nombre, indice + 1)


def construir_libros(libros: list[dict]) -> list[Libro]:
    return [Libro.desde_dict(libro) for libro in libros]

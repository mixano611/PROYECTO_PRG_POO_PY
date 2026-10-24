import unicodedata

from src.Almacen import cargar_libros


def normalizar(texto):
    texto = str(texto or "").strip().casefold()
    return "".join(
        letra
        for letra in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(letra)
    )


def coincide(valor, busqueda):
    return normalizar(busqueda) in normalizar(valor)


def buscar_libros(producto="", nombre="", autor="", estado="TODOS", libros=None):
    if libros is None:
        libros = cargar_libros()

    producto = normalizar(producto)
    nombre = normalizar(nombre)
    autor = normalizar(autor)
    estado = normalizar(estado)
    sin_filtro_estado = estado in ("", "todos", "todos los estados")

    encontrados = []
    for libro in libros:
        if producto and not coincide(libro.get("tipo", ""), producto):
            continue

        if nombre and not coincide(libro.get("nombre", ""), nombre):
            continue

        if autor and not coincide(libro.get("autor", ""), autor):
            continue

        if not sin_filtro_estado and not coincide(libro.get("estado", ""), estado):
            continue

        encontrados.append(libro)

    return encontrados

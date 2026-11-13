"""Operaciones de la biblioteca: pagar el carrito y registrar devoluciones."""

from datetime import date, datetime, timedelta

from src.Almacen import cargar_datos, guardar_datos
from src.Busqueda import buscar_por_id, contar_disponibles
from src.Carrito import guardar_carrito
from src.Excepciones import (
    CarritoVacioError,
    LibroNoDisponibleError,
    StockInsuficienteError,
)
from src.Membresia import listar_miembros
from src.Modelos import COMPRA, PRESTAMO, Caja, Carrito, MapaCajas, crear_boleta

DIAS_PRESTAMO = 7


def cargar_cajas() -> MapaCajas:
    """Lee la matriz de cajas guardada en Almacen.json."""
    datos = cargar_datos()
    return MapaCajas(datos.get("cajas"))


def guardar_cajas(mapa: MapaCajas) -> None:
    datos = cargar_datos()
    datos["cajas"] = mapa.a_matriz()
    guardar_datos(datos)


def finalizar_compra(carrito: Carrito, caja: Caja) -> dict:
    """Valida el stock, descuenta los ejemplares y genera la boleta."""
    items = carrito.items
    if not items:
        raise CarritoVacioError("Tu carrito está vacío.")

    datos = cargar_datos()
    libros = datos["libros"]

    # 1) Validar todo antes de tocar el inventario.
    for item in items:
        libro_json = buscar_por_id(libros, item.libro.id)
        if libro_json is None:
            raise LibroNoDisponibleError(
                f"El libro \"{item.libro.nombre}\" ya no está en el almacén."
            )
        disponibles = int(libro_json.get("stock", 0) or 0)
        if disponibles < item.cantidad:
            raise StockInsuficienteError(item.libro.nombre, disponibles)

    # 2) Descontar los ejemplares (la disponibilidad se actualiza sola).
    for item in items:
        libro_json = buscar_por_id(libros, item.libro.id)
        libro_json["stock"] = int(libro_json.get("stock", 0) or 0) - item.cantidad

    # 3) Registrar el movimiento.
    movimientos = datos.setdefault("movimientos", [])
    id_movimiento = max(
        [int(movimiento.get("id", 0)) for movimiento in movimientos] or [0]
    ) + 1
    codigo = f"B-{id_movimiento:04d}"

    tipos = {item.tipo for item in items}
    if tipos == {COMPRA}:
        tipo_movimiento = COMPRA
    elif tipos == {PRESTAMO}:
        tipo_movimiento = PRESTAMO
    else:
        tipo_movimiento = "MIXTO"

    estado = "ACTIVO" if PRESTAMO in tipos else "PAGADO"

    items_json = []
    for item in items:
        precio = item.precio_unitario(carrito.usuario)
        items_json.append(
            {
                "id_libro": item.libro.id,
                "nombre": item.libro.nombre,
                "cantidad": item.cantidad,
                "tipo": item.tipo,
                "precio": round(precio, 2),
                "subtotal": item.subtotal(carrito.usuario),
            }
        )

    movimiento = {
        "id": id_movimiento,
        "codigo": codigo,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": carrito.usuario.nombre,
        "dni": carrito.usuario.dni,
        "tipo": tipo_movimiento,
        "items": items_json,
        "descuento": carrito.descuento_total(),
        "total": carrito.total(),
        "caja": caja.numero,
        "estado": estado,
    }
    if estado == "ACTIVO":
        movimiento["fecha_devolucion"] = (
            date.today() + timedelta(days=DIAS_PRESTAMO)
        ).strftime("%Y-%m-%d")

    movimientos.append(movimiento)
    guardar_datos(datos)

    # 4) La boleta se arma antes de vaciar el carrito.
    boleta = crear_boleta(codigo, carrito.usuario, items, caja)
    texto = boleta.generar_texto()

    carrito.vaciar()
    guardar_carrito(carrito)

    return {"movimiento": movimiento, "texto": texto}


def registrar_devolucion(id_movimiento: int) -> bool:
    """Devuelve al almacén los libros prestados de un movimiento."""
    datos = cargar_datos()
    for movimiento in datos.get("movimientos", []):
        if int(movimiento.get("id", 0)) != int(id_movimiento):
            continue
        if movimiento.get("estado") != "ACTIVO":
            return False

        for item in movimiento.get("items", []):
            if item.get("tipo") != PRESTAMO:
                continue
            libro_json = buscar_por_id(
                datos["libros"], int(item.get("id_libro", 0))
            )
            if libro_json is None:
                continue
            libro_json["stock"] = (
                int(libro_json.get("stock", 0) or 0)
                + int(item.get("cantidad", 0) or 0)
            )

        movimiento["estado"] = "DEVUELTO"
        movimiento["fecha_devolucion_real"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        guardar_datos(datos)
        return True

    return False


def listar_movimientos() -> list[dict]:
    """Historial de compras y préstamos, del más nuevo al más antiguo."""
    movimientos = cargar_datos().get("movimientos", [])
    return list(reversed(movimientos))


def resumen() -> dict:
    """Datos para el panel de reportes."""
    datos = cargar_datos()
    movimientos = datos.get("movimientos", [])
    prestamos_activos = sum(
        1 for movimiento in movimientos if movimiento.get("estado") == "ACTIVO"
    )
    return {
        "recaudado": round(
            sum(float(movimiento.get("total", 0) or 0) for movimiento in movimientos),
            2,
        ),
        "prestamos_activos": prestamos_activos,
        "libros_disponibles": contar_disponibles(datos["libros"]),
        "miembros": len(listar_miembros()),
        "movimientos": len(movimientos),
    }

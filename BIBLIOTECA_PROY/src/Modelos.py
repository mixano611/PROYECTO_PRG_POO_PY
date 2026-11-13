"""Clases del sistema de biblioteca.

Aquí está la parte de Programación Orientada a Objetos del proyecto:

* Encapsulación: todos los atributos son privados (``_atributo``) y se
  acceden con propiedades y métodos públicos.
* Herencia y polimorfismo: ``Miembro`` hereda de ``Usuario`` y cambia
  sus descuentos y permisos; ``LibroEnOferta`` hereda de ``Libro``;
  ``BoletaCompra``, ``BoletaPrestamo`` y ``BoletaMixta`` heredan de
  ``Boleta``.
* Matrices: ``MapaCajas`` (2x3) y ``MapaBiblioteca`` (4x4).
* Recursividad: búsqueda de cajas abiertas, ubicación de un libro y
  suma de subtotales.
"""

from datetime import date, datetime, timedelta

from src.Excepciones import DatosInvalidosError, MembresiaError

# Tipos de operación que puede tener un producto del carrito.
COMPRA = "COMPRA"
PRESTAMO = "PRESTAMO"


class Libro:
    """Un libro del almacén con sus datos protegidos."""

    def __init__(
        self,
        id_libro: int,
        nombre: str,
        autor: str,
        tipo: str,
        estado: str,
        stock: int,
        precio: float,
        descripcion: str = "",
        imagen: str = "",
        portada: str | None = None,
        oferta: bool = False,
        precio_oferta: float | None = None,
    ):
        self._id = int(id_libro)
        self._nombre = ""
        self._autor = ""
        self._tipo = ""
        self._estado = ""
        self._stock = 0
        self._precio = 0.0
        self._descripcion = ""
        self._imagen = ""
        self._portada = portada
        self._oferta = bool(oferta)
        self._precio_oferta = precio_oferta

        self.nombre = nombre
        self.autor = autor
        self.tipo = tipo
        self.estado = estado
        self.stock = stock
        self.precio = precio
        self.descripcion = descripcion
        self.imagen = imagen
        if precio_oferta is not None:
            self.precio_oferta = precio_oferta

    # ------------------------- propiedades -------------------------
    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = str(valor or "").strip()
        if not valor:
            raise DatosInvalidosError("El nombre del libro no puede estar vacío.")
        self._nombre = valor

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        valor = str(valor or "").strip()
        if not valor:
            raise DatosInvalidosError("El autor del libro no puede estar vacío.")
        self._autor = valor

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: str) -> None:
        self._tipo = str(valor or "").strip() or "Novela"

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        self._estado = str(valor or "").strip().upper() or "ALMACEN"

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            numero = int(valor)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError("El stock debe ser un número entero.") from error
        if numero < 0:
            raise DatosInvalidosError("El stock no puede ser negativo.")
        self._stock = numero

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            numero = float(valor)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError("El precio debe ser un número.") from error
        if numero < 0:
            raise DatosInvalidosError("El precio no puede ser negativo.")
        self._precio = round(numero, 2)

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self._descripcion = str(valor or "").strip()

    @property
    def imagen(self) -> str:
        return self._imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self._imagen = str(valor or "").strip()

    @property
    def portada(self) -> str | None:
        return self._portada

    @property
    def oferta(self) -> bool:
        return self._oferta

    @property
    def precio_oferta(self) -> float | None:
        return self._precio_oferta

    @precio_oferta.setter
    def precio_oferta(self, valor: float | None) -> None:
        if valor is None:
            self._precio_oferta = None
            return
        numero = float(valor)
        if numero < 0:
            raise DatosInvalidosError("El precio de oferta no puede ser negativo.")
        self._precio_oferta = round(numero, 2)

    # --------------------------- lógica ----------------------------
    def disponible(self) -> bool:
        """Devuelve True si queda al menos un ejemplar."""
        return self._stock > 0

    def precio_para(self, usuario: "Usuario") -> float:
        """Precio base del libro para cualquier usuario."""
        return self._precio

    def a_dict(self) -> dict:
        """Convierte el libro al formato que se guarda en Almacen.json."""
        return {
            "id": self._id,
            "nombre": self._nombre,
            "autor": self._autor,
            "tipo": self._tipo,
            "estado": self._estado,
            "stock": self._stock,
            "precio": self._precio,
            "descripcion": self._descripcion,
            "imagen": self._imagen,
            "portada": self._portada,
            "oferta": self._oferta,
            "precio_oferta": self._precio_oferta,
        }

    @classmethod
    def desde_dict(cls, datos: dict) -> "Libro":
        """Crea el libro (u oferta) a partir de un diccionario del JSON."""
        oferta = bool(datos.get("oferta", False))
        precio_oferta = datos.get("precio_oferta")
        clase = LibroEnOferta if oferta and precio_oferta is not None else Libro
        return clase(
            id_libro=int(datos.get("id", 0)),
            nombre=datos.get("nombre", ""),
            autor=datos.get("autor", ""),
            tipo=datos.get("tipo", ""),
            estado=datos.get("estado", "ALMACEN"),
            stock=int(datos.get("stock", 0) or 0),
            precio=float(datos.get("precio", 0) or 0),
            descripcion=datos.get("descripcion", ""),
            imagen=datos.get("imagen", ""),
            portada=datos.get("portada"),
            oferta=oferta,
            precio_oferta=precio_oferta,
        )


class LibroEnOferta(Libro):
    """Libro con precio especial solo para miembros (polimorfismo)."""

    def precio_para(self, usuario: "Usuario") -> float:
        if usuario.es_miembro() and self._precio_oferta is not None:
            return self._precio_oferta
        return super().precio_para(usuario)


class Usuario:
    """Usuario común: puede comprar, pero no pedir prestado."""

    def __init__(self, nombre: str, dni: int):
        self._nombre = str(nombre or "").strip().lower()
        if not self._nombre:
            raise DatosInvalidosError("El nombre del usuario no puede estar vacío.")
        try:
            self._dni = int(dni)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError("El DNI debe ser un número entero.") from error
        if self._dni <= 0:
            raise DatosInvalidosError("El DNI debe ser mayor que cero.")

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def dni(self) -> int:
        return self._dni

    def es_miembro(self) -> bool:
        return False

    def puede_prestar(self) -> bool:
        return False

    def descuento_compra(self) -> float:
        return 0.0

    def descuento_prestamo(self) -> float:
        return 0.0

    def tipo(self) -> str:
        return "USUARIO"

    def a_dict(self) -> dict:
        return {"usuario": self._nombre, "dni": self._dni, "tipo": self.tipo()}


class Miembro(Usuario):
    """Miembro de la biblioteca: presta libros y tiene descuentos."""

    DESCUENTO_COMPRA = 0.10
    DESCUENTO_PRESTAMO = 0.15

    def __init__(
        self,
        nombre: str,
        dni: int,
        monto: float = 20.0,
        desde: str | None = None,
        hasta: str | None = None,
        caja: int | None = None,
    ):
        super().__init__(nombre, dni)
        self._monto = round(float(monto), 2)
        self._desde = desde or date.today().strftime("%Y-%m-%d")
        self._hasta = hasta or self._sumar_dias(self._desde, 30)
        self._caja = caja

    @staticmethod
    def _sumar_dias(fecha: str, dias: int) -> str:
        base = datetime.strptime(fecha, "%Y-%m-%d").date()
        return (base + timedelta(days=dias)).strftime("%Y-%m-%d")

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def desde(self) -> str:
        return self._desde

    @property
    def hasta(self) -> str:
        return self._hasta

    @property
    def caja(self) -> int | None:
        return self._caja

    def esta_vencido(self) -> bool:
        """True cuando ya pasó la fecha de vencimiento."""
        vence = datetime.strptime(self._hasta, "%Y-%m-%d").date()
        return vence < date.today()

    def renovar(self, dias: int = 30) -> None:
        """Extiende la membresía desde hoy."""
        self._desde = date.today().strftime("%Y-%m-%d")
        self._hasta = self._sumar_dias(self._desde, dias)

    # -------- polimorfismo: cambia el comportamiento del padre --------
    def es_miembro(self) -> bool:
        return True

    def puede_prestar(self) -> bool:
        return not self.esta_vencido()

    def descuento_compra(self) -> float:
        return self.DESCUENTO_COMPRA if not self.esta_vencido() else 0.0

    def descuento_prestamo(self) -> float:
        return self.DESCUENTO_PRESTAMO if not self.esta_vencido() else 0.0

    def tipo(self) -> str:
        return "MIEMBRO"

    def a_dict(self) -> dict:
        return {
            "usuario": self._nombre,
            "dni": self._dni,
            "monto": self._monto,
            "desde": self._desde,
            "hasta": self._hasta,
            "caja": self._caja,
            "estado": "VENCIDO" if self.esta_vencido() else "ACTIVO",
        }


class SolicitudMembresia:
    """Pedido de una persona para convertirse en miembro."""

    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"

    def __init__(
        self,
        id_solicitud: int,
        usuario: str,
        dni: int,
        monto: float,
        fecha: str,
        estado: str = PENDIENTE,
        caja: int | None = None,
        codigo: str | None = None,
        notificado: bool = False,
    ):
        self._id = int(id_solicitud)
        self._usuario = str(usuario or "").strip().lower()
        self._dni = int(dni)
        self._monto = round(float(monto), 2)
        self._fecha = fecha
        self._estado = estado
        self._caja = caja
        self._codigo = codigo
        self._notificado = bool(notificado)

    @property
    def id(self) -> int:
        return self._id

    @property
    def usuario(self) -> str:
        return self._usuario

    @property
    def dni(self) -> int:
        return self._dni

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def fecha(self) -> str:
        return self._fecha

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def caja(self) -> int | None:
        return self._caja

    @property
    def codigo(self) -> str | None:
        return self._codigo

    @property
    def notificado(self) -> bool:
        return self._notificado

    def aprobar(self, numero_caja: int) -> None:
        if self._estado != self.PENDIENTE:
            raise MembresiaError("Esta solicitud ya fue revisada.")
        self._estado = self.APROBADA
        self._caja = numero_caja
        self._notificado = False

    def rechazar(self, numero_caja: int, codigo: str) -> None:
        if self._estado != self.PENDIENTE:
            raise MembresiaError("Esta solicitud ya fue revisada.")
        self._estado = self.RECHAZADA
        self._caja = numero_caja
        self._codigo = codigo
        self._notificado = False

    def marcar_notificado(self) -> None:
        self._notificado = True

    def a_dict(self) -> dict:
        return {
            "id": self._id,
            "usuario": self._usuario,
            "dni": self._dni,
            "monto": self._monto,
            "fecha": self._fecha,
            "estado": self._estado,
            "caja": self._caja,
            "codigo": self._codigo,
            "notificado": self._notificado,
        }

    @classmethod
    def desde_dict(cls, datos: dict) -> "SolicitudMembresia":
        return cls(
            id_solicitud=int(datos.get("id", 0)),
            usuario=datos.get("usuario", ""),
            dni=int(datos.get("dni", 0) or 0),
            monto=float(datos.get("monto", 0) or 0),
            fecha=datos.get("fecha", ""),
            estado=datos.get("estado", cls.PENDIENTE),
            caja=datos.get("caja"),
            codigo=datos.get("codigo"),
            notificado=bool(datos.get("notificado", False)),
        )


class ItemCarrito:
    """Un libro dentro del carrito, con su cantidad y su tipo."""

    def __init__(self, libro: Libro, cantidad: int = 1, tipo: str = COMPRA):
        self._libro = libro
        self._cantidad = 0
        self._tipo = COMPRA
        self.cantidad = cantidad
        self.tipo = tipo

    @property
    def libro(self) -> Libro:
        return self._libro

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            numero = int(valor)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError("La cantidad debe ser un número entero.") from error
        if numero <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero.")
        self._cantidad = numero

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: str) -> None:
        valor = str(valor or COMPRA).upper()
        if valor not in (COMPRA, PRESTAMO):
            raise DatosInvalidosError("El tipo debe ser COMPRA o PRESTAMO.")
        self._tipo = valor

    def precio_unitario(self, usuario: Usuario) -> float:
        return self._libro.precio_para(usuario)

    def descuento(self, usuario: Usuario) -> float:
        if self._tipo == PRESTAMO:
            return usuario.descuento_prestamo()
        return usuario.descuento_compra()

    def subtotal(self, usuario: Usuario) -> float:
        """Precio final de esta línea, ya con el descuento del usuario."""
        base = self.precio_unitario(usuario) * self._cantidad
        return round(base * (1 - self.descuento(usuario)), 2)

    def a_dict(self) -> dict:
        return {
            "id_libro": self._libro.id,
            "cantidad": self._cantidad,
            "tipo": self._tipo,
        }


class Carrito:
    """Carrito de un usuario. Suma sus subtotales de forma recursiva."""

    def __init__(self, usuario: Usuario, items: list[ItemCarrito] | None = None):
        self._usuario = usuario
        self._items: list[ItemCarrito] = list(items or [])

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def items(self) -> list[ItemCarrito]:
        return list(self._items)

    def buscar_item(self, id_libro: int) -> ItemCarrito | None:
        return next(
            (item for item in self._items if item.libro.id == id_libro),
            None,
        )

    def agregar(
        self,
        libro: Libro,
        cantidad: int = 1,
        tipo: str = COMPRA,
    ) -> ItemCarrito:
        """Agrega un libro o suma la cantidad si ya estaba en el carrito."""
        if tipo == PRESTAMO and not self._usuario.puede_prestar():
            raise MembresiaError(
                "Solo los miembros pueden pedir libros prestados. "
                "Regístrate como miembro para acceder a este beneficio."
            )

        item = self.buscar_item(libro.id)
        actual = item.cantidad if item is not None else 0

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(
                "La cantidad debe ser un número entero."
            ) from error
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero.")

        if actual + cantidad > libro.stock:
            raise DatosInvalidosError(
                f"No puedes agregar más de {libro.stock} ejemplar(es) de "
                f"\"{libro.nombre}\"."
            )

        if item is None:
            item = ItemCarrito(libro, cantidad, tipo)
            self._items.append(item)
        else:
            item.cantidad = actual + cantidad
            item.tipo = tipo
        return item

    def quitar(self, id_libro: int) -> bool:
        item = self.buscar_item(id_libro)
        if item is None:
            return False
        self._items.remove(item)
        return True

    def cambiar_tipo(self, id_libro: int, tipo: str) -> None:
        item = self.buscar_item(id_libro)
        if item is None:
            raise DatosInvalidosError("Ese libro ya no está en el carrito.")
        if tipo == PRESTAMO and not self._usuario.puede_prestar():
            raise MembresiaError(
                "Solo los miembros pueden pedir libros prestados."
            )
        item.tipo = tipo

    def vaciar(self) -> None:
        self._items.clear()

    def cantidad_total(self) -> int:
        return sum(item.cantidad for item in self._items)

    def subtotal(self, indice: int = 0) -> float:
        """Suma recursiva de los subtotales (sin descuento)."""
        if indice >= len(self._items):
            return 0.0
        item = self._items[indice]
        base = item.precio_unitario(self._usuario) * item.cantidad
        return round(base + self.subtotal(indice + 1), 2)

    def total(self, indice: int = 0) -> float:
        """Suma recursiva de los subtotales con descuento."""
        if indice >= len(self._items):
            return 0.0
        return round(
            self._items[indice].subtotal(self._usuario) + self.total(indice + 1),
            2,
        )

    def descuento_total(self) -> float:
        return round(self.subtotal() - self.total(), 2)

    def a_lista(self) -> list[dict]:
        return [item.a_dict() for item in self._items]


class Caja:
    """Una caja de atención: abierta (1) o cerrada (0)."""

    def __init__(self, numero: int, abierta: bool = True):
        self._numero = int(numero)
        self._abierta = bool(abierta)

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def abierta(self) -> bool:
        return self._abierta

    def alternar(self) -> bool:
        self._abierta = not self._abierta
        return self._abierta

    def a_valor(self) -> int:
        return 1 if self._abierta else 0


class MapaCajas:
    """Matriz 2x3 con el estado 0/1 de las cajas de atención."""

    FILAS = 2
    COLUMNAS = 3

    def __init__(self, matriz: list[list[int]] | None = None):
        if matriz is None:
            matriz = [[1] * self.COLUMNAS for _ in range(self.FILAS)]

        self._cajas: list[list[Caja]] = []
        numero = 1
        for fila in range(self.FILAS):
            fila_cajas = []
            for columna in range(self.COLUMNAS):
                try:
                    valor = int(matriz[fila][columna])
                except (IndexError, TypeError, ValueError):
                    valor = 1
                fila_cajas.append(Caja(numero, valor == 1))
                numero += 1
            self._cajas.append(fila_cajas)

    def caja(self, numero: int) -> Caja | None:
        for fila in self._cajas:
            for caja in fila:
                if caja.numero == numero:
                    return caja
        return None

    def alternar(self, numero: int) -> Caja | None:
        caja = self.caja(numero)
        if caja is not None:
            caja.alternar()
        return caja

    def caja_abierta(self, fila: int = 0, columna: int = 0) -> Caja | None:
        """Busca la primera caja abierta recorriendo la matriz (recursivo)."""
        if fila >= len(self._cajas):
            return None
        if columna >= len(self._cajas[fila]):
            return self.caja_abierta(fila + 1, 0)
        if self._cajas[fila][columna].abierta:
            return self._cajas[fila][columna]
        return self.caja_abierta(fila, columna + 1)

    def total_abiertas(self) -> int:
        return sum(1 for fila in self._cajas for caja in fila if caja.abierta)

    def a_matriz(self) -> list[list[int]]:
        return [[caja.a_valor() for caja in fila] for fila in self._cajas]


class MapaBiblioteca:
    """Matriz 4x4 con la ubicación de los libros en la biblioteca."""

    FILAS = 4
    COLUMNAS = 4

    def __init__(self, libros: list[Libro] | None = None):
        self._matriz = [[0] * self.COLUMNAS for _ in range(self.FILAS)]
        for indice, libro in enumerate(libros or []):
            if indice >= self.FILAS * self.COLUMNAS:
                break
            self._matriz[indice // self.COLUMNAS][indice % self.COLUMNAS] = libro.id

    def a_matriz(self) -> list[list[int]]:
        return [list(fila) for fila in self._matriz]

    def ubicacion(
        self,
        id_libro: int,
        fila: int = 0,
        columna: int = 0,
    ) -> tuple[int, int] | None:
        """Posición (fila, columna) del libro dentro de la matriz (recursivo)."""
        if fila >= self.FILAS:
            return None
        if columna >= self.COLUMNAS:
            return self.ubicacion(id_libro, fila + 1, 0)
        if self._matriz[fila][columna] == id_libro:
            return fila, columna
        return self.ubicacion(id_libro, fila, columna + 1)

    def disponibilidad(self, libros: list[Libro]) -> list[list[int]]:
        """Matriz 4x4 con 1 si el libro tiene stock y 0 si no."""
        stock = {libro.id: libro.stock for libro in libros}
        return [
            [
                1 if stock.get(id_libro, 0) > 0 else 0
                for id_libro in fila
            ]
            for fila in self._matriz
        ]


class Boleta:
    """Boleta base. Las subclases cambian el título y las condiciones."""

    def __init__(
        self,
        codigo: str,
        usuario: Usuario,
        items: list[ItemCarrito],
        caja: Caja,
        fecha: str | None = None,
    ):
        self._codigo = codigo
        self._usuario = usuario
        self._items = list(items)
        self._caja = caja
        self._fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def items(self) -> list[ItemCarrito]:
        return list(self._items)

    @property
    def caja(self) -> Caja:
        return self._caja

    @property
    def fecha(self) -> str:
        return self._fecha

    def titulo(self) -> str:
        return "BOLETA"

    def condiciones(self) -> str:
        return "Gracias por tu preferencia."

    def total(self) -> float:
        return round(sum(item.subtotal(self._usuario) for item in self._items), 2)

    def descuento(self) -> float:
        base = sum(
            item.precio_unitario(self._usuario) * item.cantidad
            for item in self._items
        )
        return round(base - self.total(), 2)

    def generar_texto(self) -> str:
        lineas = [
            "=" * 46,
            "LETRAS Y MUNDOS",
            self.titulo(),
            "=" * 46,
            f"Código: {self._codigo}",
            f"Fecha: {self._fecha}",
            f"Cliente: {self._usuario.nombre} ({self._usuario.tipo()})",
            f"DNI: {self._usuario.dni}",
            "-" * 46,
            f"{'LIBRO':<24}{'CANT':>5}{'P.UNIT':>9}{'SUBTOTAL':>10}",
        ]
        for item in self._items:
            nombre = item.libro.nombre
            if len(nombre) > 23:
                nombre = nombre[:20] + "..."
            lineas.append(
                f"{nombre:<24}{item.cantidad:>5}"
                f"{item.precio_unitario(self._usuario):>9.2f}"
                f"{item.subtotal(self._usuario):>10.2f}"
            )
            if item.tipo == PRESTAMO:
                lineas.append("   (PRÉSTAMO: devolver en 7 días)")
        lineas.extend(
            [
                "-" * 46,
                f"Descuento: -S/ {self.descuento():.2f}",
                f"TOTAL A PAGAR: S/ {self.total():.2f}",
                "=" * 46,
                f"PASA A PAGAR Y RECOGER EN LA CAJA {self._caja.numero}",
                self.condiciones(),
                "=" * 46,
            ]
        )
        return "\n".join(lineas)


class BoletaCompra(Boleta):
    def titulo(self) -> str:
        return "BOLETA DE COMPRA"

    def condiciones(self) -> str:
        return "Gracias por tu compra. Conserva tu boleta."


class BoletaPrestamo(Boleta):
    def titulo(self) -> str:
        return "BOLETA DE PRÉSTAMO"

    def condiciones(self) -> str:
        return "Recuerda devolver los libros dentro de 7 días."


class BoletaMixta(Boleta):
    def titulo(self) -> str:
        return "BOLETA DE COMPRA Y PRÉSTAMO"

    def condiciones(self) -> str:
        return "Los libros comprados son tuyos; los prestados se devuelven en 7 días."


def crear_boleta(
    codigo: str,
    usuario: Usuario,
    items: list[ItemCarrito],
    caja: Caja,
) -> Boleta:
    """Elige la subclase de boleta según lo que lleva el carrito."""
    tipos = {item.tipo for item in items}
    if tipos == {COMPRA}:
        return BoletaCompra(codigo, usuario, items, caja)
    if tipos == {PRESTAMO}:
        return BoletaPrestamo(codigo, usuario, items, caja)
    return BoletaMixta(codigo, usuario, items, caja)

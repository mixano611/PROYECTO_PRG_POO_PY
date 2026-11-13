"""Gestión de membresías: solicitudes, aprobación, rechazo y avisos."""

import json
import random
from datetime import date, datetime
from json import JSONDecodeError
from pathlib import Path

from src.Excepciones import DatosInvalidosError, MembresiaError
from src.Modelos import Miembro, SolicitudMembresia, Usuario
from src.Usuario import cargar_usuarios, registrar_usuario

RUTA_MEMBRESIAS = (
    Path(__file__).resolve().parent.parent / "data" / "membresias_data.json"
)

CUOTA_MINIMA = 20.0
TELEFONO_ATENCION = "+51 987 654 321"


def _datos_vacios() -> dict:
    return {"solicitudes": [], "miembros": []}


def cargar_membresias() -> dict:
    """Lee el JSON de membresías y lo repara si falta o está dañado."""
    try:
        with open(RUTA_MEMBRESIAS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        guardar_membresias(_datos_vacios())
        return _datos_vacios()
    except JSONDecodeError:
        print(f"{RUTA_MEMBRESIAS.name} tiene un error de formato. Se crea de nuevo.")
        guardar_membresias(_datos_vacios())
        return _datos_vacios()

    if not isinstance(datos, dict):
        guardar_membresias(_datos_vacios())
        return _datos_vacios()

    datos.setdefault("solicitudes", [])
    datos.setdefault("miembros", [])
    if not isinstance(datos["solicitudes"], list):
        datos["solicitudes"] = []
    if not isinstance(datos["miembros"], list):
        datos["miembros"] = []
    return datos


def guardar_membresias(datos: dict) -> None:
    RUTA_MEMBRESIAS.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_MEMBRESIAS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def listar_solicitudes(estado: str | None = "PENDIENTE") -> list[SolicitudMembresia]:
    datos = cargar_membresias()
    solicitudes = [
        SolicitudMembresia.desde_dict(fila)
        for fila in datos["solicitudes"]
        if isinstance(fila, dict)
    ]
    if estado is None:
        return solicitudes
    return [solicitud for solicitud in solicitudes if solicitud.estado == estado]


def obtener_solicitud(id_solicitud: int) -> SolicitudMembresia | None:
    return next(
        (
            solicitud
            for solicitud in listar_solicitudes(None)
            if solicitud.id == id_solicitud
        ),
        None,
    )


def listar_miembros() -> list[Miembro]:
    datos = cargar_membresias()
    miembros = []
    for fila in datos["miembros"]:
        if not isinstance(fila, dict):
            continue
        try:
            miembros.append(
                Miembro(
                    nombre=fila.get("usuario", ""),
                    dni=int(fila.get("dni", 0) or 0),
                    monto=float(fila.get("monto", CUOTA_MINIMA) or CUOTA_MINIMA),
                    desde=fila.get("desde"),
                    hasta=fila.get("hasta"),
                    caja=fila.get("caja"),
                )
            )
        except DatosInvalidosError:
            continue
    return miembros


def obtener_miembro(nombre: str) -> Miembro | None:
    nombre = str(nombre or "").strip().lower()
    return next(
        (miembro for miembro in listar_miembros() if miembro.nombre == nombre),
        None,
    )


def es_miembro(nombre: str) -> bool:
    return obtener_miembro(nombre) is not None


def construir_usuario(nombre: str) -> Usuario:
    """Devuelve un Miembro si corresponde o un Usuario común."""
    miembro = obtener_miembro(nombre)
    if miembro is not None:
        return miembro

    nombre = str(nombre or "").strip().lower()
    dni = cargar_usuarios().get(nombre, 0)
    try:
        return Usuario(nombre, dni or 1)
    except DatosInvalidosError:
        return Usuario(nombre or "invitado", 1)


def crear_solicitud(nombre: str, dni: str | int, monto: float) -> SolicitudMembresia:
    """Registra una solicitud de membresía pendiente."""
    nombre = str(nombre or "").strip().lower()
    if not nombre:
        raise DatosInvalidosError("Escribe tu nombre.")

    try:
        dni_numero = int(dni)
    except (TypeError, ValueError) as error:
        raise DatosInvalidosError("El DNI debe ser un número entero.") from error
    if dni_numero <= 0:
        raise DatosInvalidosError("El DNI debe ser mayor que cero.")

    try:
        monto_numero = float(monto)
    except (TypeError, ValueError) as error:
        raise DatosInvalidosError("El monto debe ser un número.") from error
    if monto_numero < CUOTA_MINIMA:
        raise DatosInvalidosError(f"La cuota mínima mensual es S/ {CUOTA_MINIMA:.2f}.")

    if obtener_miembro(nombre) is not None:
        raise MembresiaError("Ya eres miembro de la biblioteca.")

    if any(
        solicitud.usuario == nombre
        for solicitud in listar_solicitudes(SolicitudMembresia.PENDIENTE)
    ):
        raise MembresiaError(
            "Ya tienes una solicitud pendiente. Espera la respuesta del administrador."
        )

    usuarios = cargar_usuarios()
    if nombre in usuarios and int(usuarios[nombre]) != dni_numero:
        raise MembresiaError("El DNI no coincide con el usuario registrado.")
    if nombre not in usuarios:
        registrar_usuario(nombre, dni_numero)

    datos = cargar_membresias()
    siguiente = (
        max([int(fila.get("id", 0)) for fila in datos["solicitudes"]] or [0]) + 1
    )
    solicitud = SolicitudMembresia(
        id_solicitud=siguiente,
        usuario=nombre,
        dni=dni_numero,
        monto=monto_numero,
        fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    datos["solicitudes"].append(solicitud.a_dict())
    guardar_membresias(datos)
    return solicitud


def aprobar_solicitud(id_solicitud: int, numero_caja: int) -> SolicitudMembresia:
    """Convierte la solicitud en miembro y la mueve al apartado de miembros."""
    datos = cargar_membresias()
    for indice, fila in enumerate(datos["solicitudes"]):
        if not isinstance(fila, dict) or int(fila.get("id", 0)) != id_solicitud:
            continue

        solicitud = SolicitudMembresia.desde_dict(fila)
        solicitud.aprobar(numero_caja)
        datos["solicitudes"][indice] = solicitud.a_dict()

        miembro = Miembro(
            nombre=solicitud.usuario,
            dni=solicitud.dni,
            monto=solicitud.monto,
            caja=numero_caja,
        )
        datos["miembros"] = [
            fila_miembro
            for fila_miembro in datos["miembros"]
            if str(fila_miembro.get("usuario", "")).strip().lower() != miembro.nombre
        ]
        datos["miembros"].append(miembro.a_dict())
        guardar_membresias(datos)
        return solicitud

    raise MembresiaError("No se encontró la solicitud.")


def rechazar_solicitud(id_solicitud: int, numero_caja: int) -> SolicitudMembresia:
    """Rechaza la solicitud y genera un código de reembolso."""
    datos = cargar_membresias()
    for indice, fila in enumerate(datos["solicitudes"]):
        if not isinstance(fila, dict) or int(fila.get("id", 0)) != id_solicitud:
            continue

        solicitud = SolicitudMembresia.desde_dict(fila)
        codigo = f"REF-{random.randint(100000, 999999)}"
        solicitud.rechazar(numero_caja, codigo)
        datos["solicitudes"][indice] = solicitud.a_dict()
        guardar_membresias(datos)
        return solicitud

    raise MembresiaError("No se encontró la solicitud.")


def renovar_miembro(nombre: str, dias: int = 30) -> bool:
    nombre = str(nombre or "").strip().lower()
    datos = cargar_membresias()
    for fila in datos["miembros"]:
        if str(fila.get("usuario", "")).strip().lower() != nombre:
            continue
        miembro = Miembro(
            nombre=fila.get("usuario", ""),
            dni=int(fila.get("dni", 0) or 0),
            monto=float(fila.get("monto", CUOTA_MINIMA) or CUOTA_MINIMA),
            desde=fila.get("desde"),
            hasta=fila.get("hasta"),
            caja=fila.get("caja"),
        )
        miembro.renovar(dias)
        fila.update(miembro.a_dict())
        guardar_membresias(datos)
        return True
    return False


def quitar_miembro(nombre: str) -> bool:
    nombre = str(nombre or "").strip().lower()
    datos = cargar_membresias()
    antes = len(datos["miembros"])
    datos["miembros"] = [
        fila
        for fila in datos["miembros"]
        if str(fila.get("usuario", "")).strip().lower() != nombre
    ]
    if len(datos["miembros"]) == antes:
        return False
    guardar_membresias(datos)
    return True


def notificacion_pendiente(nombre: str) -> SolicitudMembresia | None:
    """Solicitud aprobada o rechazada que el usuario todavía no vio."""
    nombre = str(nombre or "").strip().lower()
    for solicitud in listar_solicitudes(None):
        if solicitud.usuario != nombre or solicitud.notificado:
            continue
        if solicitud.estado in (
            SolicitudMembresia.APROBADA,
            SolicitudMembresia.RECHAZADA,
        ):
            return solicitud
    return None


def marcar_notificado(id_solicitud: int) -> None:
    datos = cargar_membresias()
    for fila in datos["solicitudes"]:
        if isinstance(fila, dict) and int(fila.get("id", 0)) == id_solicitud:
            fila["notificado"] = True
            guardar_membresias(datos)
            return


def texto_notificacion(solicitud: SolicitudMembresia) -> str:
    """Mensaje emergente que ve el usuario al entrar a su cuenta."""
    caja = solicitud.caja if solicitud.caja is not None else "abierta"
    if solicitud.estado == SolicitudMembresia.APROBADA:
        return (
            f"¡Felicidades! Ahora eres miembro de LETRAS Y MUNDOS.\n\n"
            f"Pasa a pagar tu membresía de S/ {solicitud.monto:.2f} "
            f"en la CAJA {caja}.\n\n"
            "Como miembro tienes descuentos exclusivos y puedes pedir "
            "libros prestados."
        )

    return (
        "Tu solicitud para ser miembro de LETRAS Y MUNDOS fue DENEGADA.\n\n"
        f"Pasa por la CAJA {caja} para recibir tu reembolso de "
        f"S/ {solicitud.monto:.2f}.\n"
        f"Presenta este código: {solicitud.codigo}\n\n"
        f"Cualquier duda o consulta llama al {TELEFONO_ATENCION}."
    )


def aviso_vencimiento(miembro: Miembro) -> str | None:
    """Mensaje si la membresía está vencida o vence en menos de 5 días."""
    if not miembro.esta_vencido():
        vence = datetime.strptime(miembro.hasta, "%Y-%m-%d").date()
        if (vence - date.today()).days > 5:
            return None
        return (
            f"Tu membresía vence el {miembro.hasta}.\n"
            f"Pasa a renovarla en la CAJA {miembro.caja or 'abierta'}."
        )
    return (
        f"Tu membresía venció el {miembro.hasta}.\n"
        f"Pasa a renovarla en la CAJA {miembro.caja or 'abierta'}."
    )

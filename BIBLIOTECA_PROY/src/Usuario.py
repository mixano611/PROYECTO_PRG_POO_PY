# Simulación de una "base de datos" simple en diccionarios y listas
usuarios_registrados = {
    "hugo": "12345678",
    "miguel": "87654321",
    "li": "11223344"
}

libros = [
    {"id": 1, "titulo": "Python para Principiantes", "stock": 3, "precio": 15.0},
    {"id": 2, "titulo": "Cien Años de Soledad", "stock": 2, "precio": 20.0},
    {"id": 3, "titulo": "El Principito", "stock": 5, "precio": 10.0}
]

def iniciar_sesion():
    print("--------------------------------")
    print("   SISTEMA DE BIBLIOTECA - U/A   ")
    print("--------------------------------")
    
    usuario = input("Ingrese su nombre de usuario: ").strip().lower()
    dni = input("Ingrese su DNI: ").strip()
    
    # Validar si el usuario existe y coincide con el DNI
    if usuario in usuarios_registrados and usuarios_registrados[usuario] == dni:
        print(f"\n¡Acceso concedido! Bienvenido, {usuario.capitalize()}.")
        return True
    else:
        print("\n[Error] Usuario o DNI incorrectos. Inténtelo de nuevo.")
        return False

def consultar_libros():
    print("\n--- LIBROS DISPONIBLES ---")
    for libro in libros:
        print(f"ID: {libro['id']} | Título: {libro['titulo']} | Stock: {libro['stock']} | Precio: ${libro['precio']}")

def reservar_libros():
    consultar_libros()
    try:
        id_libro = int(input("\nIngrese el ID del libro que desea reservar: "))
        for libro in libros:
            if libro['id'] == id_libro:
                if libro['stock'] > 0:
                    print(f"¡Éxito! Ha reservado el libro: '{libro['titulo']}'.")
                else:
                    print("Lo sentimos, este libro no tiene stock disponible para reservar.")
                return
        print("No se encontró un libro con ese ID.")
    except ValueError:
        print("Por favor, ingrese un número válido.")

def comprar_libros():
    consultar_libros()
    try:
        id_libro = int(input("\nIngrese el ID del libro que desea comprar: "))
        for libro in libros:
            if libro['id'] == id_libro:
                if libro['stock'] > 0:
                    libro['stock'] -= 1  # Restamos uno al stock
                    print(f"¡Compra exitosa! Ha comprado '{libro['titulo']}'. Total a pagar: ${libro['precio']}")
                else:
                    print("Lo sentimos, el libro está agotado.")
                return
        print("No se encontró un libro con ese ID.")
    except ValueError:
        print("Por favor, ingrese un número válido.")

def mostrar_menu():
    while True:
        print("\n================================")
        print("        MENÚ PRINCIPAL          ")
        print("================================")
        print("1. Consultar libros")
        print("2. Reservar libros")
        print("3. Comprar libros")
        print("4. Salir")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            consultar_libros()
        elif opcion == "2":
            reservar_libros()
        elif opcion == "3":
            comprar_libros()
        elif opcion == "4":
            print("\n¡Gracias por usar el sistema de la biblioteca! Hasta luego.")
            break
        else:
            print("\n[Error] Opción no válida. Elija un número entre 1 y 4.")

# Programa Principal
if __name__ == "__main__":
    # Intentar iniciar sesión antes de mostrar el menú
    if iniciar_sesion():
        mostrar_menu()
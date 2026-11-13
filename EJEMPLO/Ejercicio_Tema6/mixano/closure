def crear_calculadora_descuento(porcentaje_descuento):
    # Variable en el ámbito de la función externa
    descuento = porcentaje_descuento

    # Función anidada (el closure)
    def calcular(precio_libro):
        # Utiliza la variable 'descuento' de la función externa
        return precio_libro - (precio_libro * (descuento / 100))

    return calcular

# --- Cómo se usa ---
# Creamos una función especializada para un descuento de socio del 20%
descuento_socio = crear_calculadora_descuento(20)

# Aunque 'crear_calculadora_descuento' ya terminó, 'descuento_socio' recuerda que el descuento es 20
precio_final = descuento_socio(100.00) 
print(f"Precio con descuento de socio: {precio_final}") # Imprime: 80.0
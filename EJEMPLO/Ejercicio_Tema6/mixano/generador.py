def leer_inventario_txt(ruta_archivo):
    """Lee un archivo de texto línea por línea y genera objetos Libro sobre la marcha."""
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            # Suponiendo que en el txt cada línea es: Novela,Cien años de soledad,Gabriel García Márquez,10,35.00
            datos = linea.strip().split(',')
            
            if len(datos) == 5:
                tipo, nombre, autor, stock, precio = datos
                # Crea y "cede" el objeto Libro en el momento exacto
                yield Libro(tipo, nombre, autor, int(stock), float(precio))

# --- Cómo lo integras en tu programa para pasarlo a la tabla de PyQt5 ---
# for libro in leer_inventario_txt("inventario.txt"):
#     print(f"Cargado al sistema: {libro.NOMBRE}")

"""
LEE ARCHIVOS COMO ESTE:
Novela,Cien años de soledad,Gabriel García Márquez,10,35.00
Cuento,El Aleph,Jorge Luis Borges,8,20.00
Poesía,Veinte poemas de amor,Pablo Neruda,6,18.00

"""
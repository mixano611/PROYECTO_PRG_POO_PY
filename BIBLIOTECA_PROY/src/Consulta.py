
"""
oy a revisar `Consulta.py` y la estructura del proyecto para explicarte cómo encajaría un buscador en tu programa.

Read 
Completed with input: {
  "path": "C:\\Users\\IDAT\\Desktop\\MC\\PROYECTO PROGRAMACION\\_PROYECTO\\PROYECTO_PRG_POO_PY\\BIBLIOTECA_PROY\\src\\Consulta.py"
}

Find files matching `BIBLIOTECA_PROY/**/*`

Read 
Completed with input: {
  "path": "C:\\Users\\IDAT\\Desktop\\MC\\PROYECTO PROGRAMACION\\_PROYECTO\\PROYECTO_PRG_POO_PY\\BIBLIOTECA_PROY\\src\\Consulta.py"
}

Read 
Completed with input: {
  "path": "C:\\Users\\IDAT\\Desktop\\MC\\PROYECTO PROGRAMACION\\_PROYECTO\\PROYECTO_PRG_POO_PY\\BIBLIOTECA_PROY\\src\\Almacen.py"
}

Read 
Completed with input: {
  "path": "C:\\Users\\IDAT\\Desktop\\MC\\PROYECTO PROGRAMACION\\_PROYECTO\\PROYECTO_PRG_POO_PY\\BIBLIOTECA_PROY\\main.py"
}

Read 
Completed with input: {
  "path": "C:\\Users\\IDAT\\Desktop\\MC\\PROYECTO PROGRAMACION\\_PROYECTO\\PROYECTO_PRG_POO_PY\\BIBLIOTECA_PROY\\data\\Almacen.json"
}

Read 
Completed with input: {
  "path": "C:\\Users\\IDAT\\Desktop\\MC\\PROYECTO PROGRAMACION\\_PROYECTO\\PROYECTO_PRG_POO_PY\\BIBLIOTECA_PROY\\assets\\main_consulta.ui"
}

Read 
Completed with input: {
  "path": "C:\\Users\\IDAT\\Desktop\\MC\\PROYECTO PROGRAMACION\\_PROYECTO\\PROYECTO_PRG_POO_PY\\BIBLIOTECA_PROY\\bibliotecapy.py"
}

Para tu buscador de libros **no necesitas instalar una librería de búsqueda**. Puedes usar:

- **PyQt5**, que ya utiliza el proyecto, para los campos y el botón de la ventana.
- **`json`**, que viene incluido en Python, para leer los datos guardados.
- Las funciones normales de Python, como `in` y `casefold()`, para comparar textos sin distinguir mayúsculas y minúsculas.

En la interfaz `main_consulta.ui` ya tienes campos para libro y autor, un selector de estado y un botón **BUSCAR**. La idea es conectar ese botón a una función en `Consulta.py`, leer lo escrito y filtrar la lista de libros.

Por ejemplo, si tus libros están organizados así:

```python
libros = [
    {"titulo": "Don Quijote", "autor": "Cervantes", "estado": "ALMACEN"},
    {"titulo": "La ciudad y los perros", "autor": "Vargas Llosa", "estado": "VENDIDOS"},
]
```

puedes hacer una función de búsqueda:

```python
def buscar_libros(libros, titulo="", autor="", estado="ALMACEN"):
    titulo = titulo.strip().casefold()
    autor = autor.strip().casefold()

    return [
        libro for libro in libros
        if titulo in libro["titulo"].casefold()
        and autor in libro["autor"].casefold()
        and (estado == "Todos" or libro["estado"].casefold() == estado.casefold())
    ]
```

La búsqueda acepta coincidencias parciales: por ejemplo, escribir `"quij"` encuentra `"Don Quijote"`. En tu ventana, conectarías el botón con el método que llama a esa función:

```python
self.pushButton.clicked.connect(self.buscar)
```

Y dentro de `buscar`, tomarías los valores de la interfaz:

```python
titulo = self.lineEdit.text()
autor = self.lineEdit_2.text()
estado = self.comboBox.currentText()
```

Un detalle importante: ahora mismo `Almacen.py` guarda datos como producto y cantidad, no como libro, autor y estado. Para buscar por esos tres campos, primero debes guardar los libros con una estructura que incluya esos datos. Y la ventana también necesita un lugar donde mostrar resultados, como un `QListWidget` o un `QTextEdit`.
"""
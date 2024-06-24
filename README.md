# Filtrar Keywords

Este proyecto contiene un script en Python para filtrar palabras clave de archivos CSV o Excel. El script elimina las comas de las palabras clave y filtra aquellas que tienen menos de 80 caracteres y menos de 10 palabras. Esto es para poderlas analizar con la herramienta keywordtool.io y poder sacar el CPC y la competencia. También se ha añadido una interfaz gráfica usando `tkinter` y la posibilidad de trabajar con archivos de `Ubersuggest`. Además, ahora se pueden importar palabras clave desde Google y Bing.

## Requisitos

- Python 3.x
- Librerías: `csv`, `codecs`, `tkinter`, `pandas`, `openpyxl`

## Uso

1. Clona este repositorio.
2. Crea un entorno virtual:

    ```bash
    python -m venv venv
    ```

3. Activa el entorno virtual:
    - En Windows:

        ```bash
        venv\Scripts\activate
        ```

    - En macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Instala las dependencias necesarias con el comando:

    ```bash
    pip install -r requirements.txt
    ```

5. Ejecuta el script:

    ```bash
    python filter.py
    ```

6. Usa la interfaz gráfica para seleccionar el archivo que deseas filtrar.
7. El archivo filtrado se guardará como `keywords-filter.csv` o `keywords-filter.xlsx`, dependiendo del formato de entrada.

## Estructura del Proyecto

- `filter.py`: Contiene el script principal para filtrar las palabras clave.
- `requirements.txt`: Contiene las dependencias necesarias para ejecutar el script.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.


# Filtrar Keywords

Este proyecto contiene un script en Python para filtrar palabras clave Bing de un archivo CSV. El script elimina las comas de las palabras clave y filtra aquellas que tienen menos de 80 caracteres y menos de 10 palabras. Esto es para poderlas analizar con la herramienta keywordtool.io y poder sacar el CPC y la competencia.

## Requisitos

- Python 3.x
- Librerías: `csv`, `codecs`

## Uso

1. Clona este repositorio.
2. Crea un entorno virtual:

    python -m venv venv

3. Activa el entorno virtual:
    - En Windows:

    
        venv\Scripts\activate

    - En macOS/Linux:


    
        source venv/bin/activate


4. Instala las dependencias necesarias con el comando 'pip install -r requirements.txt'
5. Coloca tu archivo `keywords.csv` en el directorio raíz del proyecto.
6. Ejecuta el script:

7. El archivo filtrado se guardará como `keywords-filter.csv`.

## Estructura del Proyecto

- `filter.py`: Contiene el script principal para filtrar las palabras clave.
- `keywords.csv`: Archivo de entrada con las palabras clave.
- `keywords-filter.csv`: Archivo de salida con las palabras clave filtradas.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
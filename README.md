# PIA – Analizador de productos alimenticios

Aplicación desarrollada en Python que consulta la API pública de [OpenFoodFacts](https://world.openfoodfacts.org/) para obtener información de productos alimenticios comercializados en México, específicamente de la categoría de snacks.

El programa procesa los datos obtenidos mediante técnicas de limpieza y validación, elimina registros duplicados, realiza análisis estadísticos y exporta los resultados a un archivo de Excel.

## Requisitos

- Python 3.14.7 o superior.
- Conexión a internet para consultar la API de OpenFoodFacts.
- Dependencias de Python:
  - `requests`: solicitudes HTTP a la API.
  - `openpyxl`: creación y formato de archivos Excel.

## Instalación

1. Accede a la carpeta del proyecto:

   cd PIA

2. Crea un entorno virtual:

   python -m venv .venv

3. Activa el entorno virtual:

   - **Windows (CMD):**
     .venv\Scripts\activate.bat
   - **Windows (PowerShell):**
     .venv\Scripts\Activate.ps1
   - **Mac/Linux:**
     source .venv/bin/activate

4. Instala las dependencias:

   pip install -r requirements.txt

## Ejecución

Para ejecutar el programa completo, utiliza:

python main.py

El archivo principal coordina la ejecución de los cuatro módulos en el siguiente orden:

1. **api_cliente.py:** consulta la API de OpenFoodFacts, obtiene información de productos de snacks en México y guarda la respuesta en formato JSON.
2. **limpiador_datos.py:** limpia y valida los registros mediante expresiones regulares, normaliza los campos y elimina productos duplicados.
3. **analizador.py:** ordena los productos mediante el algoritmo Quicksort y calcula estadísticas descriptivas sobre sus cantidades.
4. **exportador.py:** genera un archivo Excel con el inventario de productos y los resultados del análisis estadístico.
5. **graficas.py:** genera gráficas a partir de los datos analizados.

## Estructura del proyecto

```text
PIA/
├── main.py
│
├── modulos/
│   ├── api_cliente.py
│   ├── limpiador_datos.py
│   ├── analizador.py
│   └── exportador.py
│
├── datos/
│   ├── datos_crudos.json
│   ├── datos_limpios.json
│   └── resultados.xlsx
│
├── requirements.txt
└── README.md
```

### Descripción de los módulos

| Archivo | Descripción |
|---|---|
| `main.py` | Coordina el flujo completo de ejecución. |
| `api_cliente.py` | Realiza las solicitudes HTTP y obtiene los datos de OpenFoodFacts. |
| `limpiador_datos.py` | Valida, normaliza y depura los registros utilizando expresiones regulares. |
| `analizador.py` | Ordena los productos mediante Quicksort y calcula estadísticas descriptivas. |
| `exportador.py` | Genera el libro de Excel con el inventario y las estadísticas. |

## Procesamiento de datos

### Obtención de datos

Se utiliza la API de OpenFoodFacts para consultar productos que cumplan con los siguientes filtros:

- País: México.
- Categoría: Snacks.
- Campos obtenidos: código de barras, nombre, marcas, cantidad y categorías.

Se consultan hasta tres páginas de resultados, con un máximo de 100 productos por página. También se implementan mecanismos de reintento para gestionar errores de conexión y respuestas HTTP temporales.

### Limpieza y validación

Los registros obtenidos pasan por un proceso de depuración que incluye:

- Validación del código de barras.
- Eliminación de productos sin nombre.
- Detección y eliminación de registros duplicados.
- Normalización de nombres y marcas.
- Estandarización de cantidades a gramos (g) o mililitros (ml).
- Limpieza y normalización de categorías.

### Análisis estadístico

Se aplica el algoritmo de ordenamiento Quicksort para organizar los productos según su cantidad.

Se calculan las siguientes estadísticas:

- Total de productos únicos.
- Cantidad de marcas diferentes.
- Productos sin cantidad especificada.
- Promedio.
- Mediana.
- Mínimo y máximo.
- Rango.
- Desviación estándar.

Las estadísticas de cantidades se calculan utilizando únicamente los productos cuya unidad de medida está expresada en gramos.

## Salidas generadas

Los archivos resultantes se almacenan dentro de la carpeta `datos/`:

| Archivo | Contenido |
|---|---|
| `datos_crudos.json` | Registros originales obtenidos de la API. |
| `datos_limpios.json` | Productos después del proceso de limpieza y validación. |
| `resultados.xlsx` | Libro de Excel con el inventario y las estadísticas. |

El archivo Excel contiene dos hojas:

- **Inventario_Supermercado:** presenta los productos con su código de barras, nombre, marca, cantidad, unidad de medida y categorías.
- **Estadisticas:** contiene los indicadores generales y las estadísticas descriptivas calculadas durante el análisis.

## Autor

Desarrollado por: 
Kenia Janett Arcivar Vazquez 1753251
Yesenia Stephania Chavez Montiel 1941628
Angel Emmanuel Barbosa Silos 1905405
Proyecto Integrador de Aprendizaje (PIA).
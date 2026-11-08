"""
Módulo: api_cliente.py
Descripción: Cliente para consultar la API de Open Food Facts.

Autor: Angel Emmanuel Barbosa Silos
Matrícula: 1905405
Rol: Programador
Materia: Programación Básica
Fecha: 24/10/2026
"""
import json
import time
try:
    import requests  # type: ignore[import-not-found]
except ModuleNotFoundError as exc:
    raise SystemExit(
        "La librería 'requests' no está instalada. Instálala con: pip install requests"
    ) from exc
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATOS = RUTA_PROYECTO / "datos"

URL = "https://world.openfoodfacts.org/api/v2/search"
HEADERS = {"User-Agent": "PIA Programacion Basica UANL (angel.barbosasl@uanl.edu.mx)"}
PARAMS = {
    "countries_tags": "en:mexico",
    "categories_tags": "en:snacks",
    "page_size": 100,
    "fields": "code,product_name,brands,quantity,categories",
}
PAGINAS = 3


def consultar_pagina(pagina):
    params = {**PARAMS, "page": pagina}
    intentos = 3

    for intento in range(1, intentos + 1):
        try:
            r = requests.get(
                URL,
                params=params,
                headers=HEADERS,
                timeout=30
            )
            r.raise_for_status()
            return r.json()

        except requests.exceptions.Timeout:
            print(f"Página {pagina}: tiempo de espera agotado")

        except requests.exceptions.ConnectionError:
            print(f"Página {pagina}: error de conexión")

        except requests.exceptions.HTTPError as e:
            codigo = e.response.status_code
            print(f"Página {pagina}: error HTTP {codigo}")

            # No reintentar errores que probablemente sean permanentes.
            if codigo not in (429, 500, 502, 503, 504):
                break

        except ValueError:
            print(f"Página {pagina}: la respuesta no es JSON válido")
            break

        if intento < intentos:
            espera = 2 ** intento
            print(f"Reintentando en {espera} segundos...")
            time.sleep(espera)

    return None


def main():
    productos = []

    # Consultar primero la página 1
    datos = consultar_pagina(1)

    if datos is None:
        print("No se pudieron obtener los datos.")
        return

    # Obtener el total de resultados
    total_productos = datos.get("count", 0)
    total_paginas = (
        total_productos + PARAMS["page_size"] - 1
    ) // PARAMS["page_size"]

    paginas_consultar = min(total_paginas, PAGINAS)

    print(f"Productos disponibles: {total_productos}")
    print(f"Páginas disponibles: {total_paginas}")
    print(f"Páginas que se consultarán: {paginas_consultar}")

    productos.extend(datos.get("products", []))

    # Consultar las páginas restantes
    for pagina in range(2, paginas_consultar + 1):
        datos = consultar_pagina(pagina)

        if datos is None:
            break

        productos.extend(datos.get("products", []))
        time.sleep(6)

    if not productos:
        print("No se obtuvieron datos.")
        return

    with open(RUTA_DATOS / "datos_crudos.json", "w", encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)

    print(f"Guardados {len(productos)} productos en datos_crudos.json")


if __name__ == "__main__":
    main()
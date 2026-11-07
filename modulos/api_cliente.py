import json
import time
import requests

URL = "https://world.openfoodfacts.org/api/v2/search"
HEADERS = {"User-Agent": "E2026_PB_E7 (barbosamane@gmail.com)"}
PARAMS = {
    "countries_tags": "en:mexico",
    "categories_tags": "en:snacks",
    "page_size": 100,
    "fields": "code,product_name,brands,quantity,categories",
}
PAGINAS = 3


def consultar_pagina(pagina):
    params = {**PARAMS, "page": pagina}
    try:
        r = requests.get(URL, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        print(f"Página {pagina}: tiempo de espera agotado")
    except requests.exceptions.ConnectionError:
        print(f"Página {pagina}: error de conexión")
    except requests.exceptions.HTTPError as e:
        print(f"Página {pagina}: error HTTP {e.response.status_code}")
    except ValueError:
        print(f"Página {pagina}: la respuesta no es JSON válido")
    return None


def main():
    productos = []
    for pagina in range(1, PAGINAS + 1):
        datos = consultar_pagina(pagina)
        if datos is None:
            break
        productos.extend(datos.get("products", []))
        time.sleep(1)  # no saturar la API

    if not productos:
        print("No se obtuvieron datos.")
        return

    with open("datos/datos_crudos.json", "w", encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)
    print(f"Guardados {len(productos)} productos en datos_crudos.json")


if __name__ == "__main__":
    main()
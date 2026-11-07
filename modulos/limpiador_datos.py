import json
import re

RE_CODIGO = re.compile(r"\d{8,13}")
RE_ESPACIOS = re.compile(r"\s+")
RE_PREFIJO_IDIOMA = re.compile(r"^[a-z]{2}:", re.I)
RE_MULTIPACK = re.compile(r"^\s*(\d+)\s*x\s*(\d+(?:[.,]\d+)?)\s*(kg|gr|g|ml|l)\b", re.I)
RE_CANTIDAD = re.compile(r"(\d+(?:[.,]\d+)?)\s*(kg|gr|g|ml|l|oz)\b", re.I)
RE_SUFIJO_LEGAL = re.compile(r"\s*\b(?:s\.?\s?a\.?(?:\s+de\s+c\.?\s?v\.?)?|de\s+c\.?\s?v\.?)\s*$", re.I)


def limpiar_texto(texto):
    return RE_ESPACIOS.sub(" ", texto or "").strip().title()


def convertir(valor, unidad):
    unidad = unidad.lower()
    if unidad == "kg":
        return round(valor * 1000, 1), "g"
    if unidad in ("g", "gr"):
        return round(valor, 1), "g"
    if unidad == "l":
        return round(valor * 1000, 1), "ml"
    return round(valor, 1), "ml"


def normalizar_cantidad(texto):
    if not texto:
        return None, None

    m = RE_MULTIPACK.match(texto)
    if m:
        valor = int(m.group(1)) * float(m.group(2).replace(",", "."))
        return convertir(valor, m.group(3))

    for valor, unidad in RE_CANTIDAD.findall(texto):
        if unidad.lower() != "oz":
            return convertir(float(valor.replace(",", ".")), unidad)

    return None, None


def limpiar_categorias(texto):
    categorias = []
    for c in (texto or "").split(","):
        c = RE_PREFIJO_IDIOMA.sub("", c.strip())
        c = RE_ESPACIOS.sub(" ", c.replace("-", " ")).strip()
        if c and c.lower() not in [x.lower() for x in categorias]:
            categorias.append(c)
    return categorias


def limpiar_marcas(texto):
    marcas = []
    for m in (texto or "").split(","):
        m = limpiar_texto(RE_SUFIJO_LEGAL.sub("", m))
        if m and m not in marcas:
            marcas.append(m)
    return marcas or ["Desconocida"]


def main():
    with open("datos/datos_crudos.json", encoding="utf-8") as f:
        crudos = json.load(f)

    limpios = []
    vistos_codigo = set()
    vistos_clave = set()
    descartados = {"sin nombre": 0, "código inválido": 0, "duplicado": 0}

    for p in crudos:
        codigo = str(p.get("code", "")).strip()
        nombre = limpiar_texto(p.get("product_name"))

        if not RE_CODIGO.fullmatch(codigo):
            descartados["código inválido"] += 1
            continue
        if not nombre:
            descartados["sin nombre"] += 1
            continue

        marcas = limpiar_marcas(p.get("brands"))
        marca = marcas[0]
        cantidad, unidad = normalizar_cantidad(p.get("quantity"))

        clave = (marca.lower(), nombre.lower(), cantidad, unidad)
        if codigo in vistos_codigo or clave in vistos_clave:
            descartados["duplicado"] += 1
            continue
        vistos_codigo.add(codigo)
        vistos_clave.add(clave)

        limpios.append({
            "codigo": codigo,
            "nombre": nombre,
            "marca": marca,
            "marcas": marcas,
            "cantidad": cantidad,
            "unidad": unidad,
            "categorias": limpiar_categorias(p.get("categories")),
        })

    with open("datos/datos_limpios.json", "w", encoding="utf-8") as f:
        json.dump(limpios, f, ensure_ascii=False, indent=2)
    indice = {p["codigo"]: p for p in limpios}

    print("Guardado en datos/datos_limpios.json")
    print(f"Registros originales: {len(crudos)}")
    print(f"Registros limpios:    {len(limpios)}")
    print(f"Descartados: {descartados}")
    print("\nEjemplo:")
    print(json.dumps(limpios[0], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
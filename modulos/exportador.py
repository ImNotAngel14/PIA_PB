import json
from pathlib import Path

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter
except ModuleNotFoundError as exc:
    raise SystemExit(
        "La librería 'openpyxl' no está instalada. Instálala con: pip install openpyxl"
    ) from exc

from modulos import analizador

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATOS = RUTA_PROYECTO / "datos"

ENCABEZADOS = [
    "Código de Barras", "Nombre del Producto", "Marca Principal",
    "Cantidad Numérica", "Unidad de Medida", "Categorías",
]


def dar_formato_encabezado(hoja):
    for celda in hoja[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill("solid", fgColor="305496")


def ajustar_anchos(hoja, maximo=60):
    for columna in hoja.columns:
        ancho = max(len(str(c.value)) if c.value is not None else 0 for c in columna)
        hoja.column_dimensions[get_column_letter(columna[0].column)].width = min(ancho + 2, maximo)


def exportar_a_excel(productos, stats):
    wb = openpyxl.Workbook()

    # --- Hoja 1: inventario ---
    hoja = wb.active
    hoja.title = "Inventario_Supermercado"
    hoja.append(ENCABEZADOS)

    peso_solidos_g = 0.0
    volumen_liquidos_ml = 0.0

    for prod in productos:
        cantidad = prod.get("cantidad")
        unidad = prod.get("unidad")

        if cantidad is None:
            cantidad_celda, unidad_celda = "No especifica", "N/A"
        else:
            cantidad_celda, unidad_celda = cantidad, unidad
            if unidad == "g":
                peso_solidos_g += cantidad
            elif unidad == "ml":
                volumen_liquidos_ml += cantidad

        categorias = prod.get("categorias", [])
        hoja.append([
            prod.get("codigo", "N/A"),
            prod.get("nombre", "N/A"),
            prod.get("marca", "Desconocida"),
            cantidad_celda,
            unidad_celda,
            " > ".join(categorias) if categorias else "Sin categorías",
        ])

    dar_formato_encabezado(hoja)
    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions
    ajustar_anchos(hoja)

    # --- Hoja 2: estadísticas ---
    est = wb.create_sheet("Estadisticas")
    est.append(["Estadística", "Valor"])
    est.append(["Total de productos únicos", len(productos)])
    est.append(["Peso total en sólidos (g)", round(peso_solidos_g, 1)])
    est.append(["Volumen total en líquidos (ml)", round(volumen_liquidos_ml, 1)])

    if stats:
        est.append(["Marcas diferentes", stats["marcas_diferentes"]])
        est.append(["Productos sin cantidad", stats["sin_cantidad"]])
        est.append(["Productos con cantidad en gramos", stats["con_gramos"]])
        est.append(["Promedio (g)", round(stats["promedio"], 2)])
        est.append(["Mediana (g)", round(stats["mediana"], 2)])
        est.append(["Mínimo (g)", stats["minimo"]])
        est.append(["Máximo (g)", stats["maximo"]])
        est.append(["Rango (g)", round(stats["rango"], 2)])
        est.append(["Desviación estándar (g)", round(stats["desviacion"], 2)])

    dar_formato_encabezado(est)
    ajustar_anchos(est)

    RUTA_DATOS.mkdir(exist_ok=True)
    ruta_excel = RUTA_DATOS / "resultados.xlsx"
    wb.save(ruta_excel)
    print(f"Excel generado con {len(productos)} productos: {ruta_excel}")


def main():
    productos = analizador.cargar_productos()
    stats = analizador.calcular_estadisticas(productos)
    exportar_a_excel(productos, stats)


if __name__ == "__main__":
    main()